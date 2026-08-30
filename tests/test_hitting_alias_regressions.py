from mlbstatsapi.models.stats.hitting import AdvancedHittingSplit, SimpleHittingSplit


def test_simple_hitting_split_populates_out_stats_from_mlb_aliases():
    stat = SimpleHittingSplit(
        flyOuts=101,
        groundOuts=202,
        airOuts=303,
        strikeOuts=404,
        groundOutsToAirouts="0.667",
    )

    assert stat.flyouts == 101
    assert stat.groundouts == 202
    assert stat.airouts == 303
    assert stat.strikeouts == 404
    assert stat.groundouts_to_airouts == "0.667"


def test_advanced_hitting_split_populates_out_stats_from_mlb_aliases():
    stat = AdvancedHittingSplit(
        walkOffs=2,
        flyOuts=111,
        popOuts=22,
        lineOuts=33,
        groundOuts=144,
    )

    assert stat.walkoffs == 2
    assert stat.flyouts == 111
    assert stat.popouts == 22
    assert stat.lineouts == 33
    assert stat.groundouts == 144
