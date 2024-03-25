from typing import Union, List, Optional, Dict
from pydantic import BaseModel
from mlbstatsapi.models.people import Person, Position
from mlbstatsapi.models.teams import Team
from mlbstatsapi.models.data import CodeDesc


class BoxScoreVL(BaseModel):
    """Represents a label and its associated value in a team's boxscore information, providing a structured way to display specific pieces of data.

    Attributes:
        label (str): The label for this piece of information, describing what the data represents.
        value (str): The information associated with the label, detailing specific stats or facts.
    """
    label: str
    value: Optional[str] = None


class BoxScoreTeamInfo(BaseModel):
    """Represents a team's information within the boxscore, detailing specific types of information and associated data.

    Attributes:
        title (str): The type of information (e.g., "Pitching", "Batting").
        fieldList (List[BoxScoreVL]): A list holding detailed information for this info type, typically including statistics or relevant data points.
    """
    title: str
    fieldList: List[BoxScoreVL]



class GameStatus(BaseModel):
    """Represents the game status of a player, indicating their current role or position in the game.

    Attributes:
        isCurrentBatter (bool): Indicates whether the player is the current batter.
        isCurrentPitcher (bool): Indicates whether the player is the current pitcher.
        isOnBench (bool): Indicates whether the player is on the bench.
        isSubstitute (bool): Indicates whether the player is a substitute.
    """
    isCurrentBatter: bool
    isCurrentPitcher: bool
    isOnBench: bool
    isSubstitute: bool

class PlayersDictPerson(BaseModel):
    """Represents a person within a dictionary of players, detailing their roles, stats, and statuses within the game context.

    Attributes:
        person (Person): The person object encapsulating basic personal details.
        jerseyNumber (str, optional): The person's jersey number. Default is None.
        position (Position, optional): The person's playing position. Default is None.
        status (CodeDesc): The current status of the person, including code and description.
        parentTeamId (int, optional): The ID of the person's parent team. Default is None.
        stats (dict): A dictionary containing the person's statistical data.
        seasonStats (dict): A dictionary containing the person's statistical data for the current season.
        gameStatus (GameStatus): The person's status for the current game.
        battingOrder (int, optional): The person's place in the batting order, if available. Default is None.
        allPositions (List[Position], optional): A list of all positions the person has, if available. Default is None.
    """
    person: Person
    status: CodeDesc
    stats: dict
    seasonStats: dict
    gameStatus: GameStatus
    position: Optional[Position] = None
    battingOrder: Optional[int] = None
    jerseyNumber: Optional[str] = None
    parentTeamId: Optional[int] = None
    allPositions: Optional[List[Position]] = None



class BoxScoreTeam(BaseModel):
    """Represents the boxscore information for a specific team, detailing players, team statistics, and additional notes.

    Attributes:
        team (Team): The team object containing basic information about the team.
        teamStats (Dict): A dictionary containing team statistics.
        players (Dict): A dictionary of players on the team, keyed by player ID.
        batters (List[int]): A list of player IDs representing the batters for this team.
        pitchers (List[int]): A list of player IDs representing the pitchers for this team.
        bench (List[int]): A list of player IDs representing the players on the bench for this team.
        bullpen (List[int]): A list of player IDs representing the bullpen for this team.
        battingOrder (List[int]): A list of player IDs representing the batting order for this team.
        info (List[BoxScoreTeamInfo]): A list of `BoxScoreTeamInfo` objects providing batting and fielding information for the team.
        note (List[str]): A list of notes related to the team.
    """
    team: Team
    teamStats: Dict
    players: Dict[str, PlayersDictPerson]  # Assuming keys are strings, values are PlayersDictPerson
    batters: List[int]
    pitchers: List[int]
    bench: List[int]
    bullpen: List[int]
    battingOrder: List[int]
    info: List[BoxScoreTeamInfo]
    note: List[str]

class BoxScoreTeams(BaseModel):
    """Represents the boxscore information for both the home and away teams, providing a structured view of each team's performance and statistics.

    Attributes:
        home (BoxScoreTeam): The boxscore information for the home team, including players, stats, and additional notes.
        away (BoxScoreTeam): The boxscore information for the away team, including players, stats, and additional notes.
    """
    home: BoxScoreTeam
    away: BoxScoreTeam


class BoxScoreOffical(BaseModel):
    """Represents an official in the game, detailing their role and identity.

    Attributes:
        official (Person): The official person, including their name and any relevant personal details.
        officialType (str): The type of official this person is (e.g., "Referee", "Umpire").
    """
    official: Person
    officialType: str

