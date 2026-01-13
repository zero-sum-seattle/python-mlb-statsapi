from typing import List
from pydantic import Field
from mlbstatsapi.models.base import MLBBaseModel
from .attributes import ScheduleDates


class Schedule(MLBBaseModel):
    """
    A class to represent a Schedule.

    Attributes
    ----------
    total_items : int
        Total items in schedule.
    total_events : int
        Total events in schedule.
    total_games : int
        Total games in schedule.
    total_games_in_progress : int
        Total games in progress in schedule.
    dates : List[ScheduleDates]
        List of dates with games in schedule.
    """
    total_items: int = Field(alias="totalitems")
    total_events: int = Field(alias="totalevents")
    total_games: int = Field(alias="totalgames")
    total_games_in_progress: int = Field(alias="totalgamesinprogress")
    dates: List[ScheduleDates] = []
