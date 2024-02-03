from typing import List
from pydantic import BaseModel

from .attributes import ScheduleDates


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
    totalItems: int
    totalEvents: int
    totalGames: int
    totalGamesInProgress: int
    dates: List[ScheduleDates]
