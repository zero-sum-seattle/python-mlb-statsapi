from typing import Union, List
from dataclasses import dataclass
from mlbstatsapi.models.people import Person
from mlbstatsapi.models.teams import Team

@dataclass
class BoxScoreVL:
    """
    A class to represent a boxscore team's infos label and value

    Attributes
    ----------
    label : str
        The label for this peice of info
    value : str = None
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

@dataclass
class BoxScoreTeams:
    """
    A class to represent the boxscore home and away teams

    Attributes
    ----------
    home: BoxScoreTeam
        Home team boxscore information
    away: BoxScoreTeam
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
