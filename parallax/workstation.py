"""Read-only local workstation adapter. No inference or financial calculations.

Run: python -m parallax.workstation [--port 8001]
"""

import argparse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import mimetypes
from pathlib import Path
from urllib.parse import urlsplit

from . import benchmark

ROOT = Path(__file__).resolve().parent.parent
REFERENCE_PATH = ROOT / "protocols/scientific-validation-v1/references.json"
DIST = ROOT / "frontend/dist"
TICKERS = {
    "nvidia-ports": "NVDA", "meta-capacity": "META",
    "coreweave-deposit": "CRWV", "apple-manufacturing": "AAPL",
    "microsoft-leases": "MSFT",
}
# Display selections only: exact strings in the named source paraphrase/quote.
# No conversion, aggregation, expected-loss estimate or balance reconstruction.
AMOUNTS = {
    "nvidia-ports": [
        ("Initial shared contractual cap", "$105 billion", "SEC_8K", "Initial commitment; contingent ceiling, not a payable balance"),
    ],
    "meta-capacity": [
        ("Contingent capacity purchases", "$14.72 billion", "META_10Q", "Up to this amount over five years; third-party sales may reduce it"),
    ],
    "coreweave-deposit": [
        ("Original refundable deposit", "$230 million", "CRWV_10K", "Financing received in August 2024; not a cap"),
        ("Recognized carrying obligation", "$189 million", "CRWV_10Q", "June 30, 2026; includes unused deposit and accrued premiums"),
        ("Earlier carrying obligation", "$273 million", "CRWV_10K", "December 31, 2025; includes $43 million redemption premiums"),
        ("Partial settlement", "$100 million", "CRWV_10Q", "June 2026; not an additional obligation"),
    ],
    "apple-manufacturing": [
        ("Manufacturing purchase obligations", "$56.2 billion", "AAPL_10K", "September 27, 2025; commitment, not additional funded debt"),
        ("Payable within 12 months", "$55.4 billion", "AAPL_10K", "Part of the disclosed manufacturing purchase obligations"),
    ],
    "microsoft-leases": [
        ("Recognized operating lease liabilities", "$22,861 million", "MSFT_10K", "June 30, 2025; present-value measurement"),
        ("Current operating lease liabilities", "$5,424 million", "MSFT_10K", "Component of recognized operating lease liabilities"),
        ("Noncurrent operating lease liabilities", "$17,437 million", "MSFT_10K", "Component of recognized operating lease liabilities"),
        ("Undiscounted operating lease payments", "$25,481 million", "MSFT_10K", "Before $2,620 million imputed interest; not additional debt"),
        ("Fiscal 2026 operating lease payments", "$6,111 million", "MSFT_10K", "Cash payment schedule; distinct from current carrying liability"),
    ],
}


def records():
    return benchmark.read_json(REFERENCE_PATH)["cases"]


def load_workstation_case(key):
    if key not in TICKERS:
        raise KeyError(key)
    reference = next(record for record in records() if record["case_key"] == key)
    if key in benchmark.registry():
        _, evidence = benchmark.load_case(key)
    else:
        evidence = benchmark.read_json(ROOT / reference["evidence_file"])
    documents = evidence.get("documents", [])
    by_id = {doc["id"]: doc for doc in documents}
    amounts = []
    for label, value, document_id, context in AMOUNTS[key]:
        doc = by_id.get(document_id, {})
        # Fail closed on source drift/missing evidence; never substitute zero.
        supported = value in (doc.get("factual_paraphrase", "") + doc.get("short_quote", ""))
        amounts.append({"label": label, "value": value if supported else None,
                        "document_id": document_id if doc else None, "context": context,
                        "status": "source_pack" if supported else "unavailable"})
    accounting = reference.get("recognized_accounting_liabilities") or {}
    return {
        "key": key, "ticker": TICKERS[key], "company": reference["company"],
        "arrangement": evidence.get("arrangement"), "analysis_as_of": evidence.get("analysis_as_of"),
        "preparation": evidence.get("preparation"), "documents": documents, "amounts": amounts,
        "evidence_file": reference["evidence_file"],
        "evidence_sha256": benchmark.digest(ROOT / reference["evidence_file"]),
        "reference_file": str(REFERENCE_PATH.relative_to(ROOT)),
        "reference_sha256": benchmark.digest(REFERENCE_PATH),
        "reference_status": reference.get("status", "unavailable"),
        "independent_verification": reference.get("independent_verification"),
        "accounting": {"status": accounting.get("status", "unavailable"),
                       "statement": accounting.get("statement")},
        "interpretations": reference.get("financial_interpretations") or {},
        "limitations": reference.get("material_uncertainties_and_unsupported_conclusions") or [],
    }


def case_catalog():
    return [{field: case[field] for field in
             ("key", "ticker", "company", "arrangement", "analysis_as_of")}
            for key in TICKERS for case in [load_workstation_case(key)]]


class Handler(BaseHTTPRequestHandler):
    def send_body(self, status, body, content_type):
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()
        self.wfile.write(body)

    def send_json(self, status, value):
        self.send_body(status, json.dumps(value, allow_nan=False).encode(), "application/json; charset=utf-8")

    def do_GET(self):
        path = urlsplit(self.path).path
        try:
            if path == "/api/cases":
                self.send_json(200, {"cases": case_catalog()})
            elif path.startswith("/api/cases/"):
                key = path.removeprefix("/api/cases/")
                if key not in TICKERS:
                    self.send_json(404, {"error": "Unknown case"})
                else:
                    self.send_json(200, load_workstation_case(key))
            elif path.startswith("/api/"):
                self.send_json(404, {"error": "Unknown endpoint"})
            else:
                target = (DIST / ("index.html" if path == "/" else path.lstrip("/"))).resolve()
                if not target.is_relative_to(DIST.resolve()) or not target.is_file():
                    self.send_json(404, {"error": "Not found. Build frontend first with npm run build."})
                    return
                self.send_body(200, target.read_bytes(), mimetypes.guess_type(target.name)[0] or "application/octet-stream")
        except (OSError, ValueError, KeyError, TypeError, StopIteration):
            self.send_json(500, {"error": "Case evidence unavailable; inspect local source files."})


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", type=int, default=8001)
    args = parser.parse_args()
    server = ThreadingHTTPServer(("127.0.0.1", args.port), Handler)
    print(f"Parallax workstation: http://127.0.0.1:{args.port}", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
