from typing import Union, List, Optional
from dataclasses import dataclass, field
from mlbstatsapi.models.people import Person, Position
from mlbstatsapi.models.teams import Team
from mlbstatsapi.models.data import CodeDesc


@dataclass
class BoxScoreVL:
    """
    A class to represent a boxscore team's infos label and value

    Attributes
    ----------
    label : str
        The label for this peice of info
    value : str
        The info associated with this label
    """
    label: str
    value: str = None


@dataclass
class BoxScoreTeamInfo:
    """
    A class to represent a boxscore team's info

    Attributes
    ----------
    title : str
        Type of information
    fieldlist : List[BoxScoreVL]
        List holding the info for this info type
    """
    title: str
    fieldlist: Union[List[BoxScoreVL], List[dict]]

    def __post_init__(self):
        self.fieldlist = [BoxScoreVL(**fieldlists) for fieldlists in self.fieldlist]


@dataclass
class GameStatus:
    """
    A class representing the game status of a player.

    Attributes
    ----------
    iscurrentbatter : bool
        Whether the player is the current batter.
    iscurrentpitcher : bool
        Whether the player is the current pitcher.
    isonbench : bool
        Whether the player is on the bench.
    issubstitute : bool
        Whether the player is a substitute.
    """
    iscurrentbatter: bool
    iscurrentpitcher: bool
    isonbench: bool
    issubstitute: bool

@dataclass
class PlayersDictPerson:
    """
    A class representing a person in a dictionary of players.

    Attributes
    ----------
    person : Person
        The person object.
    jerseynumber : str
        The person's jersey number.
    position : Position
        The person's position.
    status : CodeDesc
        The person's status.
    parentteamid : int
        The ID of the person's parent team.
    stats : dict
        A dictionary of the person's stats.
    seasonstats : dict
        A dictionary of the person's season stats.
    gameStatus : GameStatus
        The person's game status.
    battingorder : int
        The persons place in the batting order if avaliable.
    allpositions : Position
        All of the person's positions if avaliable.
    """
    person: Union[Person, dict]
    jerseynumber: str
    position: Union[Position, dict]
    status: Union[CodeDesc, dict]
    parentteamid: int
    stats: dict
    seasonstats: dict
    gamestatus: Union[GameStatus, dict]
    battingorder: Optional[int] = None
    allpositions: Optional[Union[List[Position], List[dict]]] = None

    def __post_init__(self):
        self.person = Person(**self.person)
        self.position = Position(**self.position)
        self.status = CodeDesc(**self.status)
        self.gamestatus = GameStatus(**self.gamestatus)
        self.allpositions = [Position(**allposition) for allposition in self.allpositions] if self.allpositions else self.allpositions

@dataclass
class BoxScoreTeam:
    """
    A class to represent the boxscore team

    Attributes
    ----------
    team : Team
        This team
    teamstats : Dict
        Team stats
    players : Dict
        Players on team
    batters : List[int]
        List of batters playerid for this team
    pitchers : List[int]
        List of pitcher playerid for this team
    bench : List[int]
        List of bench playerid for this team
    bullpen : List[int]
        Bullpen list of playerid
    battingorder : List[int]
        Batting order for this team as a list of playerid
    info : List[BoxScoreTeamInfo]
        Batting and fielding info for team
    note : List[str]
        Team notes
    """
    team: Union[Team, dict]
    teamstats: dict
    players: dict
    batters: List[int]
    pitchers: List[int]
    bench: List[int]
    bullpen: List[int]
    battingorder: List[int]
    info: Union[List[BoxScoreTeamInfo], List[dict]]
    note: List[str]

    def __post_init__(self):
        self.team = Team(**self.team)
        self.info = [BoxScoreTeamInfo(**infos) for infos in self.info]

        for player in self.players:
            self.players[player] = PlayersDictPerson(**self.players[player])

@dataclass
class BoxScoreTeams:
    """
    A class to represent the boxscore home and away teams

    Attributes
    ----------
    home : BoxScoreTeam
        Home team boxscore information
    away : BoxScoreTeam
        Away team boxscore information
    """
    home: Union[BoxScoreTeam, dict]
    away: Union[BoxScoreTeam, dict]

    def __post_init__(self):
        self.home = BoxScoreTeam(**self.home)
        self.away = BoxScoreTeam(**self.away)

@dataclass
class BoxScoreOffical:
    """
    A class to represent an official for this game

    Attributes
    ----------
    official : Person
        The official person
    officialtype : str
        What type of official this person is
    """
    official: Union[Person, dict]
    officialtype: str

    def __post_init__(self):
        self.official = Person(**self.official)
