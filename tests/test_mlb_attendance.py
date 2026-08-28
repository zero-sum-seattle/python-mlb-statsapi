"""Offline coverage for Mlb.get_attendance, including a regression test for a
guard bug found while porting this endpoint to AsyncMlb (issue #305):
``any(required_args)`` iterates dict keys (always truthy) instead of values,
so the documented "at least one of team_id/league_id/league_list_id" guard
never actually fired. Fixed to ``any(required_args.values())``.

These tests must not contact the live MLB API.
"""

from __future__ import annotations

from unittest.mock import MagicMock

from mlbstatsapi import Mlb
from mlbstatsapi.mlb_dataadapter import MlbResult
from mlbstatsapi.models.attendances import Attendance


ATTENDANCE_PAYLOAD = {
    "records": [
        {
            "openingsTotal": 160,
            "openingsTotalAway": 81,
            "openingsTotalHome": 79,
            "openingsTotalLost": 2,
            "gamesTotal": 162,
            "gamesAwayTotal": 82,
            "gamesHomeTotal": 80,
            "year": "2022",
            "attendanceAverageYtd": 18103,
            "attendanceHigh": 40065,
            "attendanceHighDate": "2022-08-06T00:00:00",
            "attendanceTotal": 2896460,
            "attendanceTotalAway": 2108558,
            "attendanceTotalHome": 787902,
            "gameType": {"id": "R", "description": "Regular Season"},
            "team": {"id": 133, "name": "Oakland Athletics", "link": "/api/v1/teams/133"},
        }
    ],
    "aggregateTotals": {
        "openingsTotalAway": 81,
        "openingsTotalHome": 79,
        "openingsTotalLost": 2,
        "openingsTotalYtd": 0,
        "attendanceAverageYtd": 18103,
        "attendanceHigh": 40065,
        "attendanceHighDate": "2022-08-06T00:00:00",
        "attendanceTotal": 2896460,
        "attendanceTotalAway": 2108558,
        "attendanceTotalHome": 787902,
    },
}


def test_get_attendance_with_no_identifier_does_not_request_and_returns_none():
    """Regression test: no team/league/league-list id must short-circuit."""
    with Mlb() as mlb:
        mock = MagicMock()
        mlb._mlb_adapter_v1.get = mock

        result = mlb.get_attendance()

        assert result is None
        mock.assert_not_called()


def test_get_attendance_with_team_id_requests_and_parses_the_result():
    with Mlb() as mlb:
        mlb._mlb_adapter_v1.get = MagicMock(
            return_value=MlbResult(status_code=200, message=None, data=ATTENDANCE_PAYLOAD)
        )

        result = mlb.get_attendance(team_id=133)

        assert isinstance(result, Attendance)
        assert result.aggregate_totals.attendance_total == 2896460
        mlb._mlb_adapter_v1.get.assert_called_once_with(
            "attendance", ep_params={"teamId": 133}
        )


def test_get_attendance_returns_none_on_client_error():
    with Mlb() as mlb:
        mlb._mlb_adapter_v1.get = MagicMock(
            return_value=MlbResult(status_code=404, message=None, data={})
        )

        assert mlb.get_attendance(team_id=133) is None
