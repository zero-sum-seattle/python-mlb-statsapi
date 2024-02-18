from typing import Union, Optional
from pydantic import BaseModel
from mlbstatsapi.models.people import Person


class GameDecisions(BaseModel):
    """Represents the winning and losing pitcher for a game, used post-game.

    Attributes:
        winner (Person): The winning person/pitcher.
        loser (Person): The losing person/pitcher.
        save (Optional[Person]): The person credited with the save, if applicable. Defaults to None.
    """
    winner: Person
    loser: Person
    save: Optional[Person] = None



class GameLeaders(BaseModel):
    """Represents live data leaders for a game, though often unused with empty data.

    Attributes:
        hitdistance (dict): Hit distance data, though typically empty.
        hitspeed (dict): Hit speed data, though typically empty.
        pitchspeed (dict): Pitch speed data, though typically empty.
    """
    # Dont know what this populated looks like. Every game ive seen its three empty dicts?
    hitdistance: dict
    hitspeed: dict
    pitchspeed: dict