from typing import Union, Optional
from dataclasses import dataclass
from pydantic import BaseModel

from mlbstatsapi.models.people import Person, Position


class RunnerCredits(BaseModel):
    """
    A class to represent a runner's credit.

    Attributes:
        player (Person): The player involved in the runner's credit.
        position (Position): The position related to the runner's credit.
        credit (str): A description or type of credit awarded to the runner.
    """

    player: Person
    position: Position
    credit: str



class RunnerMovement(BaseModel):
    """
    A class to represent a runner's movement during a play.

    Attributes:
        isOut (bool): Indicates if the running movement resulted in an out.
        outNumber (int): The sequence number of the out during the play.
        originBase (Optional[str]): The original base of the runner before the play started, defaults to None.
        start (Optional[str]): The base from which the runner started, defaults to None.
        end (Optional[str]): The base at which the runner ended after the play, defaults to None.
        outBase (Optional[str]): The base at which the runner was made out, defaults to None.
    """

    isOut: bool
    outNumber: int
    originBase: Optional[str] = None
    start: Optional[str] = None
    end: Optional[str] = None
    outBase: Optional[str] = None

class RunnerDetails(BaseModel):
    """
    A class to represent the details of a play runner's action.

    Attributes:
        event (str): Description of the runner event.
        eventType (str): Type of the runner event.
        runner (Person): The player who is the runner.
        isScoringEvent (bool): Indicates whether the event was a scoring event.
        rbi (bool): Indicates whether the event resulted in a run batted in (RBI).
        earned (bool): Specifies if the run was earned.
        teamUnearned (bool): Specifies if the run was unearned by the team.
        playIndex (int): Index of the play in the game.
        movementReason (Optional[str]): Reason for the runner's movement, defaults to None.
        responsiblePitcher (Optional[Person]): The pitcher responsible for the runner, defaults to None.
    """

    event: str
    eventType: str
    runner: Person
    isScoringEvent: bool
    rbi: bool
    earned: bool
    teamUnearned: bool
    playIndex: int
    movementReason: Optional[str] = None
    responsiblePitcher: Optional[Person] = None