from dataclasses import dataclass, field
from typing import Optional, Union

from mlbstatsapi.models.people import Person, Position
from mlbstatsapi.models.teams import Team
from mlbstatsapi.models.leagues import League
from mlbstatsapi.models.sports import Sport
from mlbstatsapi.models.game import Game

from .stats import Stats

@dataclass
class SimplePitching:
    """
    A class to represent a advanced pitching statistics
    """
    gamesplayed: Optional[int] = None
    gamesstarted: Optional[int] = None
    groundouts: Optional[int] = None
    airouts: Optional[int] = None
    runs: Optional[int] = None
    doubles: Optional[int] = None
    triples: Optional[int] = None
    homeruns: Optional[int] = None
    strikeouts: Optional[int] = None
    baseonballs: Optional[int] = None
    intentionalwalks: Optional[int] = None
    hits: Optional[int] = None
    hitbypitch: Optional[int] = None
    avg: Optional[str] = None
    atbats: Optional[int] = None
    obp: Optional[str] = None
    slg: Optional[str] = None
    ops: Optional[str] = None
    caughtstealing: Optional[int] = None
    stolenbases: Optional[int] = None
    stolenbasepercentage: Optional[str] = None
    groundintodoubleplay: Optional[int] = None
    numberofpitches: Optional[int] = None
    era: Optional[str] = None
    inningspitched: Optional[str] = None
    wins: Optional[int] = None
    losses: Optional[int] = None
    saves: Optional[int] = None
    saveopportunities: Optional[int] = None
    holds: Optional[int] = None
    blownsaves: Optional[int] = None
    earnedruns: Optional[int] = None
    whip: Optional[str] = None
    outs: Optional[int] = None
    gamespitched: Optional[int] = None
    completegames: Optional[int] = None
    shutouts: Optional[int] = None
    strikes: Optional[int] = None
    strikepercentage: Optional[str] = None
    hitbatsmen: Optional[int] = None
    balks: Optional[int] = None
    wildpitches: Optional[int] = None
    pickoffs: Optional[int] = None
    totalbases: Optional[int] = None
    groundoutstoairouts: Optional[str] = None
    winpercentage: Optional[str] = None
    pitchesperinning: Optional[str] = None
    gamesfinished: Optional[int] = None
    strikeoutwalkratio: Optional[str] = None
    strikeoutsper9inn: Optional[str] = None
    walksper9inn: Optional[str] = None
    hitsper9inn: Optional[str] = None
    runsscoredper9: Optional[str] = None
    homerunsper9: Optional[str] = None
    catchersinterference: Optional[int] = None
    sacbunts: Optional[int] = None
    sacflies: Optional[int] = None
    battersfaced: Optional[int] = None
    inheritedrunners: Optional[int] = None
    inheritedrunnersscored: Optional[int] = None

@dataclass
class AdvancedPitching:
    """
    A class to represent a advanced pitching statistics

    Used for the following stat types:
    seasonAdvanced, careerAdvanced
    """
    winningpercentage: Optional[str] = None
    runsscoredper9: Optional[str] = None
    battersfaced: Optional[int] = None
    babip: Optional[str] = None
    obp: Optional[str] = None
    slg: Optional[str] = None
    ops: Optional[str] = None
    strikeoutsper9: Optional[str] = None
    baseonballsper9: Optional[str] = None
    homerunsper9: Optional[str] = None
    hitsper9: Optional[str] = None
    strikesoutstowalks: Optional[str] = None
    stolenbases: Optional[int] = None
    caughtstealing: Optional[int] = None
    qualitystarts: Optional[int] = None
    gamesfinished: Optional[int] = None
    doubles: Optional[int] = None
    triples: Optional[int] = None
    gidp: Optional[int] = None
    gidpopp: Optional[int] = None
    wildpitches: Optional[int] = None
    balks: Optional[int] = None
    pickoffs: Optional[int] = None
    totalswings: Optional[int] = None
    swingandmisses: Optional[int] = None
    ballsinplay: Optional[int] = None
    runsupport: Optional[int] = None
    strikepercentage: Optional[str] = None
    pitchesperinning: Optional[str] = None
    pitchesperplateappearance: Optional[str] = None
    walksperplateappearance: Optional[str] = None
    strikeoutsperplateappearance: Optional[str] = None
    homerunsperplateappearance: Optional[str] = None
    walksperstrikeout: Optional[str] = None
    iso: Optional[str] = None
    flyouts: Optional[int] = None
    popouts: Optional[int] = None
    lineouts: Optional[int] = None
    groundouts: Optional[int] = None
    flyhits: Optional[int] = None
    pophits: Optional[int] = None
    linehits: Optional[int] = None
    groundhits: Optional[int] = None
    inheritedrunners: Optional[int] = None
    inheritedrunnersscored: Optional[int] = None
    bequeathedrunners: Optional[int] = None
    bequeathedrunnersscored: Optional[int] = None

@dataclass
class PitchingSabermetrics(Stats):
    """
    A class to represent a pitching sabermetric statistics

    Attributes
    ----------
    season : str
        the batter of the pitching season
    gametype : Team
        the gametype code of the pitching season 
    player : Person
        the player of the pitching season
    sport : Sport
        the sport of the pitching season 
    league : League
        the league of the pitching season
    team : Team
        the team of the pitching season
    numteams : str
        the number of teams for the pitching season
    """
    type_ = ['sabermetrics']
    season: str
    gametype: str
    player: Union[Person, dict]
    sport: Union[Sport, dict]
    fip: float
    fipminus: float
    ra9war: float
    rar: float
    war: float
    league: Optional[Union[League, dict]] = None
    team: Optional[Union[Team, dict]] = None
    numteams: Optional[str] = None

@dataclass(kw_only=True)
class PitchingSeason(Stats, SimplePitching):
    """
    A class to represent a pitching season statistic

    Attributes
    ----------
    season : str
        the batter of the pitching season
    gametype : Team
        the gametype code of the pitching season 
    player : Person
        the player of the pitching season
    sport : Sport
        the sport of the pitching season 
    league : League
        the league of the pitching season
    team : Team
        the team of the pitching season
    numteams : str
        the number of teams for the pitching season
    """
    type_ = [ 'season', 'statsSingleSeason' ]
    season: str
    gametype: Optional[str] = None
    player: Optional[Union[Person, dict]] = None
    sport: Optional[Union[Sport, dict]] = None
    league: Optional[Union[League, dict]] = None
    team: Optional[Union[Team, dict]] = None
    numteams: Optional[str] = None

@dataclass(kw_only=True)
class PitchingYBY(Stats, SimplePitching):
    """
    A class to represent a yearByYear season statistic

    Attributes
    ----------
    season : str
        the batter of the pitching yearByYear
    gametype : Team
        the gametype code of the pitching yearByYear 
    player : Person
        the player of the pitching yearByYear
    sport : Sport
        the sport of the pitching yearByYear 
    league : League
        the league of the pitching yearByYear
    team : Team
        the team of the pitching yearByYear
    numteams : str
        the number of teams for the pitching yearByYear
    """
    type_ = [ 'yearByYear', 'yearByYearPlayoffs' ]
    season: str
    gametype: str
    player: Union[Person, dict]
    sport: Union[Sport, dict]
    league: Optional[Union[League, dict]] = None
    team: Optional[Union[Team, dict]] = None
    numteams: Optional[str] = None

@dataclass(kw_only=True)
class PitchingDBD(Stats, SimplePitching):
    """
    A class to represent a yearByYear season statistic

    Attributes
    ----------
    season : str
        the batter of the pitching byDayOfWeek
    gametype : Team
        the gametype code of the pitching byDayOfWeek 
    player : Person
        the player of the pitching byDayOfWeek
    sport : Sport
        the sport of the pitching byDayOfWeek 
    league : League
        the league of the pitching byDayOfWeek
    team : Team
        the team of the pitching byDayOfWeek
    numteams : str
        the number of teams for the pitching byDayOfWeek
    dayofweek : int
        the day of the week
    """
    type_ = [ 'byDayOfWeek' ]
    season: str
    gametype: str
    dayofweek: int
    player: Union[Person, dict]
    sport: Union[Sport, dict]
    league: Optional[Union[League, dict]] = None
    team: Optional[Union[Team, dict]] = None
    numteams: Optional[str] = None

@dataclass(kw_only=True)
class PitchingAdvanced(Stats, AdvancedPitching):
    """
    A class to represent a pitching seasonAdvanced statistic

    Attributes
    ----------
    season : str
        the batter of the pitching season
    gametype : Team
        the gametype code of the pitching season 
    player : Person
        the player of the pitching season
    sport : Sport
        the sport of the pitching season 
    league : League
        the league of the pitching season
    team : Team
        the team of the pitching season
    numteams : str
        the number of teams for the pitching season
    """
    type_ = [ "seasonAdvanced", "careerAdvanced", 'yearByYearAdvanced']
    season: str
    gametype: str
    player: Union[Person, dict]
    sport: Union[Sport, dict]
    league: Optional[Union[League, dict]] = None
    team: Optional[Union[Team, dict]] = None
    numteams: Optional[str] = None
