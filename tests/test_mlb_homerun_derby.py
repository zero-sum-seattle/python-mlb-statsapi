"""Offline coverage for Mlb.get_homerun_derby, including a regression test for
a bug found while porting this endpoint to AsyncMlb (issue #305): the 400-499
branch executed a bare ``None`` expression instead of ``return None``, so
execution fell through to the parsing logic below. In the common case that
logic still landed on None (an error response rarely has a truthy "status"
key), but a 404 or compatibility-mode 4xx response that happened to include
one would have raised a ValidationError instead of cleanly returning None.
Fixed to ``return None``.

These tests must not contact the live MLB API.
"""

from __future__ import annotations

from unittest.mock import MagicMock

from mlbstatsapi import Mlb
from mlbstatsapi.mlb_dataadapter import MlbResult
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


def test_get_homerun_derby_requests_and_parses_the_result():
    with Mlb() as mlb:
        mlb._mlb_adapter_v1.get = MagicMock(
            return_value=MlbResult(status_code=200, message=None, data=HOMERUN_DERBY_PAYLOAD)
        )

        result = mlb.get_homerun_derby(511101)

        assert isinstance(result, HomeRunDerby)
        assert result.status.state == "Final"


def test_get_homerun_derby_returns_none_on_client_error():
    with Mlb() as mlb:
        mlb._mlb_adapter_v1.get = MagicMock(
            return_value=MlbResult(status_code=404, message=None, data={})
        )

        assert mlb.get_homerun_derby(1) is None


def test_get_homerun_derby_returns_none_without_raising_on_a_malformed_error_body():
    """Regression test: a 4xx body with a truthy "status" key must not reach
    HomeRunDerby(**data) and raise, now that the guard actually returns."""
    with Mlb() as mlb:
        mlb._mlb_adapter_v1.get = MagicMock(
            return_value=MlbResult(
                status_code=404, message=None, data={"status": "error"}
            )
        )

        assert mlb.get_homerun_derby(1) is None
