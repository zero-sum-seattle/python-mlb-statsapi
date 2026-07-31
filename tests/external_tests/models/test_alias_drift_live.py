"""Live counterpart to tests/test_model_alias_coverage.py.

The offline tests compare models against recorded fixtures, which only catch drift the
library introduces. This module runs the same checks against the API as it responds
today, so a rename on MLB's side surfaces even when nobody has re-recorded fixtures.
"""

import json
import urllib.error
import urllib.request

import pytest

from tests import alias_audit

TIMEOUT = 60


def fetch(url):
    try:
        with urllib.request.urlopen(url, timeout=TIMEOUT) as response:
            return json.load(response)
    except (urllib.error.URLError, TimeoutError) as exc:
        pytest.skip(f"MLB API unreachable ({exc})")


@pytest.fixture(scope="module")
def live_api_keys():
    keys = set()
    for url in alias_audit.SNAPSHOT_ENDPOINTS:
        alias_audit.collect_keys(fetch(url), keys)
    return keys


def test_live_api_field_aliases_match(live_api_keys):
    mismatches = alias_audit.alias_mismatches(live_api_keys)
    report = [
        f"  {model.__name__}.{field} reads {expects!r}, API now sends {', '.join(observed)}"
        for model, field, expects, observed in mismatches
    ]
    assert not mismatches, "\n".join(
        [f"{len(mismatches)} field(s) no longer match the live MLB API:", *report]
    )


def test_recorded_fixtures_are_not_stale(live_api_keys):
    """Keys the live API added since the last recording are invisible to the offline tests."""
    new_keys = live_api_keys - alias_audit.load_api_keys()
    modelled = {alias_audit.normalize(key) for key in new_keys}
    relevant = {
        alias_audit.effective_alias(model, name)
        for model in alias_audit.iter_models()
        for name in model.model_fields
        if alias_audit.normalize(alias_audit.effective_alias(model, name)) in modelled
    }
    assert not relevant, (
        "the live API returns keys matching these fields that are missing from "
        f"tests/fixtures/api_keys.json: {sorted(relevant)}. "
        "Re-run python tests/tools/record_api_fixtures.py"
    )


@pytest.mark.parametrize("spec", alias_audit.PAYLOAD_SPECS, ids=lambda spec: spec.label)
def test_live_payload_populates_every_matching_field(spec):
    payload = alias_audit.extract(fetch(spec.url), spec)
    model = alias_audit.resolve(spec.model)
    missed = alias_audit.dropped_keys(model, payload)
    assert not missed, alias_audit.describe_dropped(model, payload, missed)
