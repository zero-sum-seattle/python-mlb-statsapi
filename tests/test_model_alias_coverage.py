"""Guards against models silently dropping values the MLB API returns.

Because ``MLBBaseModel`` ignores unknown keys, a field whose alias does not match the
API exactly fails quietly: no exception, just a permanent ``None``. That is how issue
#246 shipped in v0.7.1 and went unnoticed through a full green test run -- the existing
stats tests assert on the response envelope (``group``, ``type``, ``total_splits``) but
never on a stat value.

These tests run offline against fixtures recorded from the real API. Regenerate them
with ``python tests/tools/record_api_fixtures.py``.
"""

import pytest

from tests import alias_audit
from tests.alias_audit import PAYLOAD_SPECS

RECORDED_PAYLOADS = alias_audit.load_payloads()
OBSERVED_API_KEYS = alias_audit.load_api_keys()

# The specific fields reported in issue #246 and found alongside it. Listing them by
# name keeps the original bug reports executable, and covers the one case the generic
# check above cannot see: MLB spells AdvancedPitchingSplit's field "strikesoutsToWalks",
# a typo on their side that no casing rule derives from "strikeouts_to_walks".
REPORTED_REGRESSIONS = [
    ("hitting_season", "strikeouts"),
    ("hitting_season", "groundouts"),
    ("hitting_season", "airouts"),
    ("hitting_season", "groundouts_to_airouts"),
    ("hitting_season_advanced", "flyouts"),
    ("hitting_season_advanced", "groundouts"),
    ("hitting_season_advanced", "lineouts"),
    ("hitting_season_advanced", "popouts"),
    ("hitting_season_advanced", "walkoffs"),
    ("pitching_season", "strikeouts"),
    ("pitching_season", "groundouts"),
    ("pitching_season", "airouts"),
    ("pitching_season", "groundouts_to_airouts"),
    ("pitching_season_advanced", "flyouts"),
    ("pitching_season_advanced", "groundouts"),
    ("pitching_season_advanced", "lineouts"),
    ("pitching_season_advanced", "popouts"),
    ("pitching_season_advanced", "flyball_percentage"),
    ("pitching_season_advanced", "strikeouts_to_walks"),
    ("fielding_season", "putouts"),
    ("catching_season", "strikeouts"),
    ("hitting_sabermetrics", "wraa"),
    ("hitting_sabermetrics", "wrc"),
    ("hitting_sabermetrics", "wrc_plus"),
    ("person", "nickname"),
    ("season", "preseason_start_date"),
    ("season", "postseason_end_date"),
    ("venue", "timezone"),
    ("team_records", "wildcard_games_back"),
    ("schedule_game", "calendar_event_id"),
    ("game_status", "start_time_tbd"),
    ("game_data_game", "calendar_event_id"),
    ("pitch_coordinates", "ax"),
]


def test_every_payload_spec_was_recorded():
    """A spec that failed to record would quietly shrink coverage of the tests below."""
    missing = sorted({spec.label for spec in PAYLOAD_SPECS} - set(RECORDED_PAYLOADS))
    assert not missing, (
        f"no recorded payload for {missing}; re-run tests/tools/record_api_fixtures.py"
    )


@pytest.mark.parametrize("spec", PAYLOAD_SPECS, ids=lambda spec: spec.label)
def test_recorded_payload_populates_every_matching_field(spec):
    """Every recorded key that names a declared field must reach that field."""
    payload = RECORDED_PAYLOADS.get(spec.label)
    if payload is None:
        pytest.skip(f"{spec.label} was not recorded")

    model = alias_audit.resolve(spec.model)
    missed = alias_audit.dropped_keys(model, payload)
    assert not missed, alias_audit.describe_dropped(model, payload, missed)


@pytest.mark.parametrize("spec", PAYLOAD_SPECS, ids=lambda spec: spec.label)
def test_recorded_payload_parses_without_error(spec):
    payload = RECORDED_PAYLOADS.get(spec.label)
    if payload is None:
        pytest.skip(f"{spec.label} was not recorded")

    alias_audit.resolve(spec.model)(**payload)


def test_field_aliases_match_observed_api_casing():
    """Check every model in the package, not just the ones with a recorded payload.

    A field is only reported when the crawled endpoints prove MLB uses that key, so
    fields the API no longer returns do not produce noise.
    """
    mismatches = alias_audit.alias_mismatches(OBSERVED_API_KEYS)
    if not mismatches:
        return

    report = [
        f"{len(mismatches)} field(s) expect a key the MLB API does not send, so they "
        "always parse as None:",
        "",
        f"  {'MODEL':<26} {'FIELD':<28} {'EXPECTS':<26} API SENDS",
    ]
    for model, field, expects, observed in mismatches:
        report.append(f"  {model.__name__:<26} {field:<28} {expects:<26} {', '.join(observed)}")
    pytest.fail("\n".join(report))


@pytest.mark.parametrize(
    ("label", "field"), REPORTED_REGRESSIONS, ids=lambda value: str(value)
)
def test_reported_regression_fields_populate(label, field):
    payload = RECORDED_PAYLOADS.get(label)
    if payload is None:
        pytest.skip(f"{label} was not recorded")

    spec = next(spec for spec in PAYLOAD_SPECS if spec.label == label)
    model = alias_audit.resolve(spec.model)
    alias = alias_audit.effective_alias(model, field)

    parsed = model(**payload)
    assert getattr(parsed, field) is not None, (
        f"{model.__name__}.{field} is None. It reads {alias!r}; the recorded payload "
        f"has {sorted(k for k in payload if alias.lower() in k.lower())}."
    )
