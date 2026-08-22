from mlbstatsapi._parsers.attendance import parse_attendance
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


def test_parse_attendance():
    """parse_attendance builds an Attendance when records is non-empty."""
    assert parse_attendance({}) is None
    assert parse_attendance({"records": []}) is None

    attendance = parse_attendance(ATTENDANCE_PAYLOAD)

    assert isinstance(attendance, Attendance)
    assert attendance.aggregate_totals.attendance_total == 2896460
    assert attendance.records[0].team.name == "Oakland Athletics"
