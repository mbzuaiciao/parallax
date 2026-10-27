import os
from decimal import Decimal
from pathlib import Path
import unittest
from unittest.mock import patch

from streamlit.testing.v1 import AppTest

from parallax import benchmark
from parallax.ablation import request_for
from parallax.demo import (REAL_CASES, INVESTOR_LABELS, capital_comparison,
                           load_selection, recorded_assessment)
from parallax.model_api import MODEL, ModelAPIError
from parallax.real_world import build_disclosure_request, load_disclosure

APP = Path(__file__).resolve().parent.parent / "streamlit_app.py"


def text(app):
    return "\n".join(x.value for group in (app.markdown, app.caption, app.info, app.warning) for x in group)


def open_page(page):
    app = AppTest.from_file(str(APP), default_timeout=15).run()
    app.radio(key="page").set_value(page).run()
    return app


class DemoTests(unittest.TestCase):
    @patch.dict(os.environ, {"MODEL_API_KEY": ""})
    @patch("parallax.demo.chat_completion")
    def test_overview_is_keyless_and_leads_with_verified_recovery_without_model_panels(self, chat):
        app = AppTest.from_file(str(APP), default_timeout=15).run()
        self.assertFalse(app.exception)
        self.assertEqual(app.radio(key="page").options, ["Overview", "Capital Structure", "AI Reasoning Lab"])
        self.assertIn('100% <span>→</span> 68.75%', text(app))
        for amount in ('$100m', '$60m', '$110m'):
            self.assertIn(amount, text(app))
        self.assertNotIn("Show original saved response", [x.label for x in app.toggle])
        for name in REAL_CASES:
            self.assertIn(name, [x.value for x in app.subheader])
            _, evidence = benchmark.load_case(REAL_CASES[name])
            for doc in evidence['documents']:
                self.assertIn(doc['url'], text(app))
        self.assertIn("neither outstanding debt nor an expected loss", text(app))
        chat.assert_not_called()

    def test_cash_conservation_and_controlled_calculation_comparisons(self):
        a, b = capital_comparison("Cedar")
        self.assertEqual((Decimal(a['Bond recovery %']), Decimal(b['Bond recovery %'])), (Decimal(100), Decimal('68.75')))
        self.assertEqual(Decimal(b['Triggered claim']), Decimal(60))
        self.assertEqual(Decimal(b['Guarantee cap']), Decimal(80))
        self.assertEqual(Decimal(b['Guarantee payment']), Decimal('41.25'))
        for company, scenario in (("Cedar", "stress"), ("Harbor", "base"), ("Harbor", "stress")):
            rows = capital_comparison(company, scenario)
            self.assertEqual(rows[0]['Cash pool'], rows[1]['Cash pool'])
            self.assertEqual(rows[0]['Reported principal'], rows[1]['Reported principal'])
            for row in rows:
                allocated = sum(Decimal(row[k]) for k in ('Bond payment', 'Guarantee payment', 'Equity distribution'))
                self.assertLessEqual(abs(allocated - Decimal(row['Cash pool'])), Decimal('.000001'))
        with self.assertRaises(ValueError):
            capital_comparison('NVIDIA PORTS')

    @patch.dict(os.environ, {"MODEL_API_KEY": ""})
    @patch("parallax.demo.chat_completion")
    def test_capital_navigation_investor_switch_and_harbor_scenarios(self, chat):
        app = open_page('Capital Structure')
        self.assertFalse(app.exception)
        self.assertIn('No parent liability', text(app))
        self.assertEqual([x.value for x in app.metric][-2:], ['$10m', '$0m'])
        app.selectbox(key='capital_investor').set_value('senior_unsecured_creditor').run()
        self.assertEqual([x.value for x in app.metric][-2:], ['100%', '68.75%'])
        app.selectbox(key='cedar_structure').set_value('A').run()
        self.assertEqual([x.value for x in app.metric][:4], ['$100m', '$100m', '$0m', '$0m'])
        app.selectbox(key='capital_company').set_value('Harbor').run()
        self.assertEqual(app.metric[1].value, '$105m')  # principal plus coupon, not $100m
        self.assertEqual([x.value for x in app.metric][-2:], ['100%', '75.86%'])
        app.selectbox(key='harbor_scenario').set_value('base').run()
        self.assertEqual([x.value for x in app.metric][-2:], ['100%', '100%'])
        self.assertEqual(app.metric[3].value, '$0m')  # untriggered cap isn't a claim
        self.assertTrue(app.button(key='run_fresh').disabled)
        self.assertIn('cannot be determined', text(app))
        chat.assert_not_called()

    def test_legacy_saved_selections_and_exact_request_backwards_compatibility(self):
        for company, variants in (('Harbor', ('base', 'stress')), ('Cedar', ('A', 'B'))):
            for p in INVESTOR_LABELS:
                for variant in variants:
                    selection = load_selection(company, p, variant)
                    self.assertTrue(selection['synthetic'])
                    self.assertNotIn('deterministic_reference', selection['request'])
                    self.assertTrue(selection['historical']['choices'][0]['message']['content'])
        for p in INVESTOR_LABELS:
            self.assertEqual(load_selection('NVIDIA PORTS', p)['request'], build_disclosure_request(load_disclosure(), p))
            for company, key in REAL_CASES.items():
                original = load_selection(company, p)
                self.assertEqual(original['request'], benchmark.request_for(key, p))
                self.assertIsNone(original['references'])
                self.assertEqual(original['status'], 'completed')

    @patch.dict(os.environ, {"MODEL_API_KEY": ""})
    @patch("parallax.demo.chat_completion")
    def test_lab_all_cases_investors_conditions_are_keyless_and_show_recorded_assessments(self, chat):
        app = open_page('AI Reasoning Lab')
        with patch('parallax.demo.reference_calculations') as harbor, patch('parallax.demo.reference_values') as cedar:
            for company, key in REAL_CASES.items():
                app.selectbox(key='lab_company').set_value(company).run()
                for p in INVESTOR_LABELS:
                    app.selectbox(key='lab_investor').set_value(p).run()
                    for condition in ('guided', 'neutral'):
                        app.radio(key='lab_condition').set_value(condition).run()
                        self.assertFalse(app.exception)
                        self.assertEqual(len(app.metric), 0)
                        self.assertEqual(len(app.table), 0)
                        selection = load_selection(company, p, condition=condition)
                        self.assertEqual(selection['request'], request_for(key, p, condition))
                        self.assertIsNone(selection['references'])
                        self.assertIn(recorded_assessment(company,p,condition)['judgment']['unsupported_assumptions']['notes'].replace('$','\\$'), text(app))
                        self.assertTrue(app.button(key='run_fresh').disabled)
                    for doc in selection['evidence']['documents']:
                        self.assertIn(doc['url'], text(app))
                harbor.assert_not_called()
                cedar.assert_not_called()
        self.assertIn('preliminary assistant-authored', text(app))
        self.assertIn('one sample per cell', text(app))
        chat.assert_not_called()

    @patch.dict(os.environ, {"MODEL_API_KEY": ""})
    @patch("parallax.demo.chat_completion")
    def test_original_response_is_secondary_and_switches_without_modification(self, chat):
        app = open_page('AI Reasoning Lab')
        guided = load_selection('NVIDIA PORTS', 'equity_holder', condition='guided')['historical']['choices'][0]['message']['content']
        self.assertNotIn(guided.strip(), text(app))
        app.toggle(key='show_saved').set_value(True).run()
        self.assertIn(guided.strip().replace('$','\\$'), text(app))
        app.radio(key='lab_condition').set_value('neutral').run()
        neutral = load_selection('NVIDIA PORTS','equity_holder',condition='neutral')['historical']['choices'][0]['message']['content']
        self.assertIn(neutral.strip().replace('$','\\$'), text(app))
        self.assertNotIn(guided.strip().replace('$','\\$'), text(app))
        app.radio(key='lab_study').set_value('Earlier guided evaluation').run()
        historical=load_selection('NVIDIA PORTS','equity_holder')['historical']['choices'][0]['message']['content']
        self.assertIn(historical.strip().replace('$','\\$'),text(app))
        chat.assert_not_called()

    @patch.dict(os.environ, {"MODEL_API_KEY": "test-secret"})
    @patch('parallax.demo.chat_completion')
    def test_optional_live_submits_only_selected_neutral_investor_and_keeps_binding(self, chat):
        chat.return_value={'model':MODEL,'choices':[{'message':{'content':'Fresh unverified test output'},'finish_reason':'stop'}]}
        app=open_page('AI Reasoning Lab')
        app.selectbox(key='lab_company').set_value('Meta capacity purchases').run()
        app.selectbox(key='lab_investor').set_value('senior_unsecured_creditor').run()
        app.radio(key='lab_condition').set_value('neutral').run()
        chat.assert_not_called()
        app.button(key='run_fresh').click().run()
        self.assertFalse(app.exception)
        chat.assert_called_once_with(request_for('meta-capacity','senior_unsecured_creditor','neutral'),'test-secret')
        self.assertIn('Fresh unverified test output',text(app))
        app.radio(key='lab_condition').set_value('guided').run()
        self.assertNotIn('Fresh unverified test output',text(app))
        self.assertEqual(chat.call_count,1)

    @patch.dict(os.environ, {"MODEL_API_KEY": "test-secret"})
    @patch('parallax.demo.chat_completion',side_effect=ModelAPIError('Meta Model API returned HTTP 429'))
    def test_live_failure_preserves_saved_response_and_does_not_retry(self,chat):
        app=open_page('Capital Structure')
        app.toggle(key='show_saved').set_value(True).run()
        app.button(key='run_fresh').click().run()
        self.assertFalse(app.exception)
        self.assertEqual(app.error[0].value,'Meta Model API returned HTTP 429')
        self.assertIn(load_selection('Cedar','equity_holder','B')['historical']['choices'][0]['message']['content'].strip().replace('$','\\$'),text(app))
        chat.assert_called_once_with(load_selection('Cedar','equity_holder','B')['request'],'test-secret')
