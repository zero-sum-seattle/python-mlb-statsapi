from mlbstatsapi.models.attendances import Attendance


def parse_attendance(data: dict) -> Attendance | None:
    """Parse an Attendance from an MLB /attendance response body."""
    if not data or not data.get("records"):
        return None
    return Attendance(**data)
