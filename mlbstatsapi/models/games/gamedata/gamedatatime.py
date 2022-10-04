from dataclasses import dataclass

@dataclass
class GameDatetime:
    dateTime: str
    originalDate: str
    officialDate: str
    dayNight: str
    time: str
    ampm: str
