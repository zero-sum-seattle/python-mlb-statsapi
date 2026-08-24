from mlbstatsapi._parsers.homerunderby import parse_homerun_derby
from mlbstatsapi.models.homerunderby import HomeRunDerby


HOMERUN_DERBY_PAYLOAD = {
    "info": {
        "id": 511101,
        "nonGameGuid": "test-guid",
        "name": "Home Run Derby",
        "eventType": {"code": "O", "name": "Other"},
        "eventDate": "2017-07-11T00:00:00Z",
        "venue": {"id": 4169, "link": "/api/v1/venues/4169", "name": "Marlins Park"},
        "isMultiDay": False,
        "isPrimaryCalendar": True,
        "fileCode": "2017/07/10/mlb-112",
        "eventNumber": 103,
        "publicFacing": True,
    },
    "status": {
        "state": "Final",
        "currentRound": 3,
        "currentRoundTimeLeft": "0:00",
        "inTieBreaker": False,
        "tieBreakerNum": 0,
        "clockStopped": True,
        "bonusTime": False,
    },
}


def test_parse_homerun_derby():
    """parse_homerun_derby builds a HomeRunDerby when status is present."""
    assert parse_homerun_derby({}) is None
    assert parse_homerun_derby({"status": {}}) is None

    derby = parse_homerun_derby(HOMERUN_DERBY_PAYLOAD)

    assert isinstance(derby, HomeRunDerby)
    assert derby.status.state == "Final"
    assert derby.info.name == "Home Run Derby"
