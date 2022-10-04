from dataclasses import dataclass

@dataclass
class PlaysPlayResult:
    type:           str
    event:          str
    eventType:      str
    description:    str
    rbi:            int
    awayScore:      int
    homeScore:      int
