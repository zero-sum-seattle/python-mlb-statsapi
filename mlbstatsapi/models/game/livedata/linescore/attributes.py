from typing import Union, Optional
from pydantic import BaseModel
from mlbstatsapi.models.people import Person
from mlbstatsapi.models.teams import Team

class LinescoreTeamScoreing(BaseModel):
    """Represents a team's scoring details in a game's Linescore.

    This class includes details on the hits, errors, players left on base, and runs for a particular inning. It also indicates if the team is the winner.

    Attributes:
        hits (int): The number of hits by the team in this inning.
        errors (int): The number of errors committed by the team in this inning.
        leftOnBase (int): The number of players left on base by the team in this inning.
        runs (int): The number of runs scored by the team in this inning. Default is None.
        isWinner (bool): Indicates whether the team is the winner. Default is None.
    """
    hits: int
    errors: int
    leftOnBase: int
    runs: Optional[int] = None
    isWinner: Optional[bool] = None

class LinescoreInning(BaseModel):
    """Represents an inning within a game's Linescore.

    Attributes:
        num (int): The inning number.
        ordinalNum (str): The ordinal representation of the inning number (e.g., "1st", "2nd").
        home (LinescoreTeamScoreing): Scoring details for the home team during this inning.
        away (LinescoreTeamScoreing): Scoring details for the away team during this inning.
    """
    num: int
    ordinalNum: str
    home: LinescoreTeamScoreing
    away: LinescoreTeamScoreing



class LinescoreTeams(BaseModel):
    """Represents the scoring details for both home and away teams in a game's Linescore.

    Attributes:
        home (LinescoreTeamScoreing): Scoring and performance details for the home team.
        away (LinescoreTeamScoreing): Scoring and performance details for the away team.
    """
    home: LinescoreTeamScoreing
    away: LinescoreTeamScoreing



class LinescoreOffense(BaseModel):
    """Represents the current offense in a game.

    Details the composition of the offensive team at a given moment, including the current batter, players on deck and in the hole, the pitcher from the offensive team's perspective, and their position in the batting order.

    Attributes:
        team (Team): The team currently on offense.
        batter (Person): The current batter.
        ondeck (Person): The player on deck, ready to bat next.
        inhole (Person): The player in the hole, batting after the on deck player.
        pitcher (Person): The pitcher for the offensive team.
        battingOrder (int, optional): The position in the batting order for the current offense. Default is None.
        first (str, optional): Identifier for the first base runner. Default is None.
        second (str, optional): Identifier for the second base runner. Default is None.
        third (str, optional): Identifier for the third base runner. Default is None.
    """
    team: Team
    batter: Person
    onDeck: Person
    inHole: Person
    pitcher: Person
    battingOrder: Optional[int] = None
    first: Optional[str] = None
    second: Optional[str] = None
    third: Optional[str] = None

class LinescoreDefense(BaseModel):
    """Represents the current defense in a game.

    Attributes:
        team (Team, optional): The team that is currently playing defense. Default is None.
        pitcher (Person, optional): The current pitcher. Default is None.
        catcher (Person, optional): The current catcher. Default is None.
        first (Person, optional): The player at first base. Default is None.
        second (Person, optional): The player at second base. Default is None.
        third (Person, optional): The player at third base. Default is None.
        shortStop (Person, optional): The current shortstop. Default is None.
        left (Person, optional): The player in left field. Default is None.
        center (Person, optional): The player in center field. Default is None.
        right (Person, optional): The player in right field. Default is None.
        batter (Person, optional): The next batter when this team switches to offense. Default is None.
        onDeck (Person, optional): The next on deck batter when this team switches to offense. Default is None.
        inHole (Person, optional): The next in hole batter when this team switches to offense. Default is None.
        battingOrder (int, optional): The position of this team in the batting order. Default is None.
    """
    team: Optional[Team] = None
    pitcher: Optional[Person] = None
    catcher: Optional[Person] = None
    first: Optional[Person] = None
    second: Optional[Person] = None
    third: Optional[Person] = None
    shortStop: Optional[Person] = None
    left: Optional[Person] = None
    center: Optional[Person] = None
    right: Optional[Person] = None
    batter: Optional[Person] = None
    onDeck: Optional[Person] = None
    inHole: Optional[Person] = None
    battingOrder: Optional[int] = None

