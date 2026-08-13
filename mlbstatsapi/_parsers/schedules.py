from mlbstatsapi.models.schedules import Schedule

def parse_schedules(data: dict) -> list[Schedule]:
    """Parse a list of schedules from the data"""
    return [Schedule(**schedule) for schedule in data['schedules']] if data['schedules'] else []

def parse_schedule(data: dict) -> Schedule:
    """Parse a schedule from the data"""
    return Schedule(**data) if data else None