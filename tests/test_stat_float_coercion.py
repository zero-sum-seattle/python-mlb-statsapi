"""Regression tests for issue #340: Pydantic's native float coercion replaces
the string-typed stat fields that PR #241 proposed handling with a custom
``BeforeValidator``. These tests confirm ``Optional[float]`` alone converts
numeric strings, passes floats through, and treats ``None`` as ``None`` --
with no custom validator involved.
"""

import pytest
from pydantic import ValidationError

from mlbstatsapi.models.stats.catching import SimpleCatchingSplit
from mlbstatsapi.models.stats.fielding import SimpleFieldingSplit
from mlbstatsapi.models.stats.hitting import AdvancedHittingSplit, SimpleHittingSplit
from mlbstatsapi.models.stats.pitching import AdvancedPitchingSplit, SimplePitchingSplit
from mlbstatsapi.models.stats.stats import ExpectedStatistics


def test_numeric_string_avg_converts_to_float():
    split = SimpleHittingSplit(avg=".287")
    assert split.avg == pytest.approx(0.287)
    assert isinstance(split.avg, float)


def test_numeric_string_era_converts_to_float():
    split = SimplePitchingSplit(era="3.42")
    assert split.era == pytest.approx(3.42)
    assert isinstance(split.era, float)


def test_float_input_stays_float():
    split = SimpleHittingSplit(avg=0.287)
    assert split.avg == pytest.approx(0.287)
    assert isinstance(split.avg, float)


def test_none_stays_none():
    split = SimpleHittingSplit(avg=None)
    assert split.avg is None


def test_field_omitted_defaults_to_none():
    split = SimpleHittingSplit()
    assert split.avg is None


def test_model_dump_serializes_as_float_not_string():
    split = SimpleHittingSplit(avg=".287")
    dumped = split.model_dump(include={"avg"})
    assert dumped == {"avg": 0.287}
    assert not isinstance(dumped["avg"], str)


@pytest.mark.parametrize(
    "field, value",
    [
        ("obp", ".366"),
        ("slg", ".411"),
        ("ops", ".777"),
        ("caught_stealing_percentage", "45.5"),
        ("stolen_base_percentage", "80.0"),
        ("babip", ".310"),
        ("groundouts_to_airouts", "1.24"),
        ("at_bats_per_home_run", "18.5"),
    ],
)
def test_simple_hitting_split_numeric_fields_convert(field, value):
    split = SimpleHittingSplit(**{field: value})
    assert getattr(split, field) == pytest.approx(float(value))


@pytest.mark.parametrize(
    "field, value",
    [
        ("whip", "1.09"),
        ("strike_percentage", "64.9"),
        ("win_percentage", "0.625"),
        ("pitches_per_inning", "15.3"),
        ("strikeout_walk_ratio", "5.9"),
        ("strikeouts_per_9_inn", "11.9"),
        ("walks_per_9_inn", "2.1"),
        ("hits_per_9_inn", "6.7"),
        ("runs_scored_per_9", "2.4"),
        ("home_runs_per_9", "0.9"),
    ],
)
def test_simple_pitching_split_numeric_fields_convert(field, value):
    split = SimplePitchingSplit(**{field: value})
    assert getattr(split, field) == pytest.approx(float(value))


def test_advanced_hitting_split_iso_converts():
    split = AdvancedHittingSplit(iso=".212")
    assert split.iso == pytest.approx(0.212)


def test_advanced_pitching_split_babip_converts():
    split = AdvancedPitchingSplit(babip=".290")
    assert split.babip == pytest.approx(0.290)


def test_simple_catching_split_stolen_base_percentage_converts():
    split = SimpleCatchingSplit(stolen_base_percentage="72.0")
    assert split.stolen_base_percentage == pytest.approx(72.0)


def test_simple_fielding_split_fielding_percentage_converts():
    split = SimpleFieldingSplit(fielding="1.000")
    assert split.fielding == pytest.approx(1.0)


def test_expected_statistics_converts_all_fields():
    stat = ExpectedStatistics(avg=".301", slg=".512", woba=".360", wobaCon=".400")
    assert stat.avg == pytest.approx(0.301)
    assert stat.slg == pytest.approx(0.512)
    assert stat.woba == pytest.approx(0.360)
    assert stat.wobacon == pytest.approx(0.400)


def test_expected_statistics_accepts_none():
    stat = ExpectedStatistics(avg=None, slg=None, woba=None, wobaCon=None)
    assert stat.avg is None
    assert stat.slg is None
    assert stat.woba is None
    assert stat.wobacon is None


@pytest.mark.parametrize("garbage", ["garbage", "N/A", "1.2.3"])
def test_malformed_non_numeric_values_raise_validation_error(garbage):
    """We deliberately do not swallow arbitrary malformed values into None.

    No MLB fixture in this repository demonstrates a sentinel string for these
    fields, so unexpected malformed input should surface as a validation
    error rather than being silently discarded.
    """
    with pytest.raises(ValidationError):
        SimpleHittingSplit(avg=garbage)


class TestInningsNotationFieldsRemainStrings:
    """MLB innings notation (e.g. "6.2" == 6 2/3 innings) is not a decimal
    value, so these fields are intentionally excluded from float conversion.
    """

    def test_simple_fielding_split_innings_stays_string(self):
        split = SimpleFieldingSplit(innings="6.2")
        assert split.innings == "6.2"
        assert isinstance(split.innings, str)

    def test_simple_pitching_split_innings_pitched_stays_string(self):
        split = SimplePitchingSplit(innings_pitched="6.2")
        assert split.innings_pitched == "6.2"
        assert isinstance(split.innings_pitched, str)

    def test_advanced_pitching_split_innings_pitched_per_game_stays_string(self):
        split = AdvancedPitchingSplit(innings_pitched_per_game="6.2")
        assert split.innings_pitched_per_game == "6.2"
        assert isinstance(split.innings_pitched_per_game, str)

    def test_innings_notation_serializes_as_string_in_model_dump(self):
        split = SimplePitchingSplit(innings_pitched="6.2")
        dumped = split.model_dump(include={"innings_pitched"})
        assert dumped == {"innings_pitched": "6.2"}
        assert isinstance(dumped["innings_pitched"], str)
