"""Regression tests for issue #340: numeric stat fields are typed as plain
``Optional[float]``. Pydantic's native coercion handles ordinary numeric
strings (e.g. ".287") with no custom validator, but the live MLB Stats API
also returns non-numeric sentinel strings (".---", "-.--") for rate stats
that are not applicable (e.g. a caught-stealing percentage when nobody has
attempted a steal). ``field_validator(mode="before")`` validators on the
affected models normalize those two known sentinels to ``None`` before
Pydantic's float coercion runs, while leaving any other malformed string
alone so it still raises a ``ValidationError``.
"""

import pytest
from pydantic import ValidationError

from mlbstatsapi.models.stats.catching import SimpleCatchingSplit
from mlbstatsapi.models.stats.fielding import SimpleFieldingSplit
from mlbstatsapi.models.stats.hitting import AdvancedHittingSplit, SimpleHittingSplit
from mlbstatsapi.models.stats.pitching import AdvancedPitchingSplit, SimplePitchingSplit
from mlbstatsapi.models.stats.sentinels import normalize_mlb_float_sentinel
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
    """Unexpected malformed values are not swallowed into None.

    Only the two confirmed MLB sentinel strings (".---", "-.--") are
    normalized to None. Any other malformed string should surface as a
    validation error rather than being silently discarded.
    """
    with pytest.raises(ValidationError):
        SimpleHittingSplit(avg=garbage)


class TestMlbFloatSentinelNormalization:
    """Regression coverage for the two confirmed MLB sentinel strings."""

    @pytest.mark.parametrize("sentinel", [".---", "-.--"])
    def test_normalize_mlb_float_sentinel_returns_none(self, sentinel):
        assert normalize_mlb_float_sentinel(sentinel) is None

    def test_normalize_mlb_float_sentinel_leaves_other_values_unchanged(self):
        assert normalize_mlb_float_sentinel(".287") == ".287"
        assert normalize_mlb_float_sentinel(3.42) == 3.42
        assert normalize_mlb_float_sentinel(None) is None
        assert normalize_mlb_float_sentinel("banana") == "banana"

    @pytest.mark.parametrize("unhashable", [{"unexpected": "value"}, ["unexpected"]])
    def test_normalize_mlb_float_sentinel_does_not_raise_on_unhashable_input(self, unhashable):
        """dicts/lists can't be checked with `in` against a set of strings.

        The helper must not raise TypeError itself -- unexpected shapes
        should pass through unchanged so Pydantic's own validation raises
        the ValidationError, rather than the helper crashing first.
        """
        assert normalize_mlb_float_sentinel(unhashable) is unhashable

    @pytest.mark.parametrize("unhashable", [{"unexpected": "value"}, ["unexpected"]])
    def test_simple_hitting_split_unhashable_avg_raises_validation_error(self, unhashable):
        with pytest.raises(ValidationError):
            SimpleHittingSplit(avg=unhashable)

    @pytest.mark.parametrize("sentinel", [".---", "-.--"])
    def test_simple_hitting_split_sentinel_fields_become_none(self, sentinel):
        split = SimpleHittingSplit(
            avg=sentinel,
            obp=sentinel,
            slg=sentinel,
            ops=sentinel,
            caughtStealingPercentage=sentinel,
            stolenBasePercentage=sentinel,
            babip=sentinel,
            groundOutsToAirouts=sentinel,
            atBatsPerHomeRun=sentinel,
        )
        assert split.avg is None
        assert split.obp is None
        assert split.slg is None
        assert split.ops is None
        assert split.caught_stealing_percentage is None
        assert split.stolen_base_percentage is None
        assert split.babip is None
        assert split.groundouts_to_airouts is None
        assert split.at_bats_per_home_run is None

    @pytest.mark.parametrize("sentinel", [".---", "-.--"])
    def test_simple_pitching_split_sentinel_fields_become_none(self, sentinel):
        split = SimplePitchingSplit(
            era=sentinel,
            whip=sentinel,
            winPercentage=sentinel,
            strikeoutWalkRatio=sentinel,
            groundoutsToAirouts=sentinel,
        )
        assert split.era is None
        assert split.whip is None
        assert split.win_percentage is None
        assert split.strikeout_walk_ratio is None
        assert split.groundouts_to_airouts is None

    def test_simple_pitching_split_sentinel_model_dump_is_none(self):
        split = SimplePitchingSplit(era=".---")
        dumped = split.model_dump(include={"era"})
        assert dumped == {"era": None}

    def test_advanced_pitching_split_sentinel_fields_become_none(self):
        split = AdvancedPitchingSplit(babip=".---", winningPercentage="-.--")
        assert split.babip is None
        assert split.winning_percentage is None

    def test_advanced_hitting_split_sentinel_fields_become_none(self):
        split = AdvancedHittingSplit(babip=".---", iso="-.--")
        assert split.babip is None
        assert split.iso is None

    def test_simple_catching_split_sentinel_fields_become_none(self):
        split = SimpleCatchingSplit(
            caughtStealingPercentage=".---",
            stolenBasePercentage="-.--",
        )
        assert split.caught_stealing_percentage is None
        assert split.stolen_base_percentage is None

    def test_simple_fielding_split_sentinel_fields_become_none(self):
        split = SimpleFieldingSplit(
            rangeFactorPer9Inn="-.--",
            caughtStealingPercentage=".---",
        )
        assert split.range_factor_per_9_inn is None
        assert split.caught_stealing_percentage is None

    def test_expected_statistics_sentinel_fields_become_none(self):
        stat = ExpectedStatistics(avg=".---", slg="-.--", woba=None, wobaCon=None)
        assert stat.avg is None
        assert stat.slg is None

    def test_unrelated_string_field_is_not_normalized(self):
        """Sanity check that sentinel normalization is scoped to float
        fields, not applied broadly to every string field on the model."""
        split = SimplePitchingSplit(summary=".---")
        assert split.summary == ".---"


class TestInningsNotationFieldsRemainStrings:
    """MLB innings notation (e.g. "6.2" == 6 2/3 innings) is not a decimal
    value, so these fields are intentionally excluded from float conversion
    and from sentinel normalization.
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
