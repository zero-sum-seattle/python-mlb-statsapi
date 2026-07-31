"""Re-record the API fixtures used by tests/test_model_alias_coverage.py.

Run from the repository root when MLB adds or renames response fields:

    python tests/tools/record_api_fixtures.py

This is the only part of the alias-drift checks that touches the network. It writes
tests/fixtures/api_keys.json (every key the crawled endpoints return) and
tests/fixtures/model_payloads.json (real payloads for the models under check), both of
which are committed so the tests themselves run offline.
"""

from __future__ import annotations

import datetime
import json
import sys
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from tests import alias_audit  # noqa: E402

TIMEOUT = 60


def fetch(url: str):
    with urllib.request.urlopen(url, timeout=TIMEOUT) as response:
        return json.load(response)


def record_api_keys() -> int:
    keys: set[str] = set()
    for url in alias_audit.SNAPSHOT_ENDPOINTS:
        try:
            alias_audit.collect_keys(fetch(url), keys)
        except Exception as exc:  # noqa: BLE001 - report and keep crawling
            print(f"  ! {url.split('?')[0]}: {exc}", file=sys.stderr)

    alias_audit.API_KEYS_FIXTURE.write_text(
        json.dumps(
            {
                "recorded_at": datetime.date.today().isoformat(),
                "endpoints": list(alias_audit.SNAPSHOT_ENDPOINTS),
                "keys": sorted(keys),
            },
            indent=2,
        )
        + "\n"
    )
    return len(keys)


def record_payloads() -> int:
    payloads = {}
    responses: dict[str, object] = {}
    for spec in alias_audit.PAYLOAD_SPECS:
        try:
            if spec.url not in responses:
                responses[spec.url] = fetch(spec.url)
            payloads[spec.label] = alias_audit.extract(responses[spec.url], spec)
        except Exception as exc:  # noqa: BLE001 - report and keep going
            print(f"  ! {spec.label}: {exc}", file=sys.stderr)

    alias_audit.PAYLOADS_FIXTURE.write_text(
        json.dumps(
            {
                "recorded_at": datetime.date.today().isoformat(),
                "specs": {
                    spec.label: {"model": spec.model, "url": spec.url}
                    for spec in alias_audit.PAYLOAD_SPECS
                },
                "payloads": payloads,
            },
            indent=2,
            sort_keys=False,
        )
        + "\n"
    )
    return len(payloads)


if __name__ == "__main__":
    alias_audit.FIXTURE_DIR.mkdir(parents=True, exist_ok=True)
    print(f"recorded {record_api_keys()} distinct API keys")
    print(f"recorded {record_payloads()} model payloads")
