"""Offline data fidelity and real HTTP contract tests for the read-only adapter."""
from copy import deepcopy
from http.server import ThreadingHTTPServer
import json
from pathlib import Path
import tempfile
from threading import Thread
import unittest
from unittest.mock import patch
from urllib.error import HTTPError
from urllib.request import urlopen

from parallax import benchmark, workstation


class WorkstationDataTests(unittest.TestCase):
    def test_backend_default_port_avoids_metis(self):
        with patch('sys.argv', ['parallax.workstation']), patch.object(
                workstation, 'ThreadingHTTPServer') as server:
            server.return_value.serve_forever.side_effect = KeyboardInterrupt
            workstation.main()
        server.assert_called_once_with(('127.0.0.1', 8001), workstation.Handler)
        server.return_value.server_close.assert_called_once()

    def test_all_five_cases_and_evidence_bytes_are_reused(self):
        catalog = workstation.case_catalog()
        self.assertEqual([item['company'] for item in catalog],
                         ['NVIDIA', 'Meta Platforms', 'CoreWeave', 'Apple', 'Microsoft'])
        for summary in catalog:
            with self.subTest(case=summary['key']):
                case = workstation.load_workstation_case(summary['key'])
                source = benchmark.read_json(workstation.ROOT / case['evidence_file'])
                self.assertEqual(case['documents'], source['documents'])
                self.assertEqual(case['evidence_sha256'], benchmark.digest(workstation.ROOT / case['evidence_file']))
                self.assertEqual(case['analysis_as_of'], source['analysis_as_of'])
                self.assertEqual(case['reference_status'], 'provisional')
                self.assertEqual(case['independent_verification']['decision'], 'pending')
                for doc in case['documents']:
                    self.assertTrue(doc['url'].startswith('https://www.sec.gov/Archives/edgar/'))
                    self.assertLessEqual(doc['filed_on'], case['analysis_as_of'])

    def test_every_highlight_is_exactly_in_cited_evidence(self):
        expected = {
            'nvidia-ports': ['$105 billion'],
            'meta-capacity': ['$14.72 billion'],
            'coreweave-deposit': ['$230 million', '$189 million', '$273 million', '$100 million'],
            'apple-manufacturing': ['$56.2 billion', '$55.4 billion'],
            'microsoft-leases': ['$22,861 million', '$5,424 million', '$17,437 million', '$25,481 million', '$6,111 million'],
        }
        for key, values in expected.items():
            case = workstation.load_workstation_case(key)
            self.assertEqual([item['value'] for item in case['amounts']], values)
            docs = {doc['id']: doc for doc in case['documents']}
            for amount in case['amounts']:
                doc = docs[amount['document_id']]
                self.assertEqual(amount['status'], 'source_pack')
                self.assertIn(amount['value'], doc['factual_paraphrase'] + doc['short_quote'])
                self.assertEqual(doc['url'], next(source['url'] for source in benchmark.read_json(
                    workstation.ROOT / case['evidence_file'])['documents'] if source['id'] == doc['id']))

    def test_unknown_accounting_is_preserved_and_interpretation_is_verbatim(self):
        for record in workstation.records():
            case = workstation.load_workstation_case(record['case_key'])
            self.assertEqual(case['interpretations'], record['financial_interpretations'])
            self.assertEqual(case['accounting']['statement'], record['recognized_accounting_liabilities']['statement'])
            if record['case_key'] in ('nvidia-ports', 'meta-capacity', 'apple-manufacturing'):
                self.assertEqual(case['accounting']['status'], 'not_established')
                self.assertNotIn('$0', case['accounting']['statement'])

    def test_missing_fields_and_source_drift_are_unavailable_never_zero(self):
        entry, evidence = benchmark.load_case('meta-capacity')
        changed = deepcopy(evidence)
        changed['documents'][0].pop('factual_paraphrase')
        changed['documents'][0].pop('short_quote')
        reference = next(deepcopy(record) for record in workstation.records() if record['case_key'] == 'meta-capacity')
        for field in ('recognized_accounting_liabilities', 'financial_interpretations',
                      'material_uncertainties_and_unsupported_conclusions'):
            reference.pop(field)
        with patch.object(workstation, 'records', return_value=[reference]), patch.object(
                benchmark, 'load_case', return_value=(entry, changed)):
            case = workstation.load_workstation_case('meta-capacity')
        self.assertIsNone(case['amounts'][0]['value'])
        self.assertEqual(case['amounts'][0]['status'], 'unavailable')
        self.assertEqual(case['accounting'], {'status': 'unavailable', 'statement': None})
        self.assertEqual(case['interpretations'], {})
        self.assertEqual(case['limitations'], [])
        changed['documents'] = []
        with patch.object(benchmark, 'load_case', return_value=(entry, changed)):
            case = workstation.load_workstation_case('meta-capacity')
        self.assertIsNone(case['amounts'][0]['document_id'])
        self.assertIsNone(case['amounts'][0]['value'])


class WorkstationHTTPTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = ThreadingHTTPServer(('127.0.0.1', 0), workstation.Handler)
        cls.thread = Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        cls.url = f'http://127.0.0.1:{cls.server.server_port}'

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join()

    def test_catalog_and_all_case_routes(self):
        with urlopen(self.url + '/api/cases') as response:
            self.assertEqual(response.headers['Content-Type'], 'application/json; charset=utf-8')
            catalog = json.load(response)['cases']
        self.assertEqual(len(catalog), 5)
        for case in catalog:
            with urlopen(self.url + '/api/cases/' + case['key']) as response:
                self.assertEqual(json.load(response), workstation.load_workstation_case(case['key']))

    def test_unknown_routes_traversal_and_private_files_not_served(self):
        for path in ('/api/cases/unknown', '/api/cases/../../.env', '/api/unknown', '/.env', '/../../pyproject.toml'):
            with self.subTest(path=path), self.assertRaises(HTTPError) as caught:
                urlopen(self.url + path)
            self.assertEqual(caught.exception.code, 404)

    def test_built_assets_only_and_no_write_endpoint(self):
        with tempfile.TemporaryDirectory() as directory:
            Path(directory, 'index.html').write_text('<title>Parallax</title>')
            with patch.object(workstation, 'DIST', Path(directory)):
                with urlopen(self.url + '/') as response:
                    self.assertIn('text/html', response.headers['Content-Type'])
                    self.assertIn(b'Parallax', response.read())
        from urllib.request import Request
        with self.assertRaises(HTTPError) as caught:
            urlopen(Request(self.url + '/api/cases', data=b'{}', method='POST'))
        self.assertEqual(caught.exception.code, 501)
