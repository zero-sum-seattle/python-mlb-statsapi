from typing import List
from dataclasses import dataclass, field

from .attributes import ScheduleDates


@dataclass
class Schedule:
    """
    A class to represent a Schedule.

    Attributes
    ----------
    copyright : str
        Copyright
    totalitems : int 
        Total items in schedule
    totalevents : int
        Total events in schedule
    totalgames : int
        Total games in schedule
    totalgamesinprogress : int
        Total games in progress in schedule
    dates : ScheduleDates
        List of dates with games in schedule
    """
    totalitems: int
    totalevents: int
    totalgames: int
    totalgamesinprogress: int
    dates: List[ScheduleDates] = field(default_factory=list)

    def __post_init__(self):
        self.dates = [ScheduleDates(**date) for date in self.dates if self.dates]

