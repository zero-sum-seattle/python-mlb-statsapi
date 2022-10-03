from dataclasses import dataclass, field
from typing import List, Dict, Union, Optional
import mlbstatsapi.mlb_models as mlb




# @dataclass
# class HittingStat:
#     """
#     A class to represent a hitting season split. 
#     It is an example for hard coding a stat split

#     Attributes
#     ----------
#     gamesPlayed : int
#     groundOuts : int 
#     airOuts : int
#     runs : int
#     doubles : int 
#     triples : int 
#     homeRuns : int 
#     strikeOuts : int 
#     baseOnBalls : int 
#     intentionalWalks : int 
#     hits : int 
#     hitByPitch : int
#     avg : str
#     atBats : int 
#     obp : str
#     slg : str
#     ops : str
#     caughtStealing : int 
#     stolenBases : int
#     stolenBasePercentage : int 
#     groundIntoDoublePlay : int 
#     numberOfPitches : int 
#     plateAppearances : int 
#     totalBases : int
#     rbi : int 
#     leftOnBase : int 
#     sacBunts : int 
#     sacFlies : int 
#     babip : str 
#     groundOutsToAirouts : int
#     catchersInterference : int 
#     atBatsPerHomeRun : int
#     """
#     gamesPlayed : int
#     groundOuts : int 
#     airOuts : int
#     runs : int
#     doubles : int 
#     triples : int 
#     homeRuns : int 
#     strikeOuts : int 
#     baseOnBalls : int 
#     intentionalWalks : int 
#     hits : int 
#     hitByPitch : int
#     avg : str
#     atBats : int 
#     obp : str
#     slg : str
#     ops : str
#     caughtStealing : int 
#     stolenBases : int
#     stolenBasePercentage : int 
#     groundIntoDoublePlay : int 
#     numberOfPitches : int 
#     plateAppearances : int 
#     totalBases : int
#     rbi : int 
#     leftOnBase : int 
#     sacBunts : int 
#     sacFlies : int 
#     babip : str 
#     groundOutsToAirouts : int
#     catchersInterference : int 
#     atBatsPerHomeRun : int

@dataclass
class Splits:
    def get_team(self):
        if isinstance(self.team, dict):
            return mlb.Team(**self.team)

    def get_player(self):
        if isinstance(self.player, dict):
            return mlb.Person(**self.player)
    
    def get_league(self):
        if isinstance(self.league, dict):
            return mlb.League(**self.league)

    def get_sport(self):
        if isinstance(self.sport, dict):
            return mlb.Sport(**self.sport)

# @dataclass
# class HittingSplits(Splits):
#     """
#     A class to represent a stat splits.
#     """
#     stat: HittingStat
#     league: Optional[dict] = None
#     season: Optional[dict] = None
#     team: Optional[dict] = None
#     player: Optional[dict] = None
#     opponent: Optional[dict] = None
#     date: Optional[dict] = None
#     sport: Optional[dict] = None
#     gameType: Optional[str] = None
#     isHome: Optional[str] = None
#     numTeams: Optional[str] = None
#     isWin: Optional[str] = None
#     game: Optional[str] = None
#     rank: Optional[str] = None
#     dayOfWeek: Optional[str] = None

# class PitchingSplits(Splits):
#     """
#     A class to represent a stat splits.
#     """
#     stat: PitchingStat
#     league: Optional[dict] = None
#     season: Optional[dict] = None
#     team: Optional[dict] = None
#     player: Optional[dict] = None
#     opponent: Optional[dict] = None
#     date: Optional[dict] = None
#     sport: Optional[dict] = None
#     gameType: Optional[str] = None
#     isHome: Optional[str] = None
#     numTeams: Optional[str] = None
#     isWin: Optional[str] = None
#     game: Optional[str] = None
#     rank: Optional[str] = None
#     dayOfWeek: Optional[str] = None


class HittingSplits(Splits):
    gamesPlayed : int
    groundOuts : int 
    airOuts : int
    runs : int
    doubles : int 
    triples : int 
    homeRuns : int 
    strikeOuts : int 
    baseOnBalls : int 
    intentionalWalks : int 
    hits : int 
    hitByPitch : int
    avg : str
    atBats : int 
    obp : str
    slg : str
    ops : str
    caughtStealing : int 
    stolenBases : int
    stolenBasePercentage : int 
    groundIntoDoublePlay : int 
    numberOfPitches : int 
    plateAppearances : int 
    totalBases : int
    rbi : int 
    leftOnBase : int 
    sacBunts : int 
    sacFlies : int 
    babip : str 
    groundOutsToAirouts : int
    catchersInterference : int 
    atBatsPerHomeRun : int

    def __init__(self, **kwargs):

        if 'stat' in kwargs:
            self.__dict__.update(kwargs['stat'])

        self.__dict__.update(kwargs)


class PitchingSplits(Splits):
    gamesPlayed: int
    gamesStarted: int
    groundOuts: int
    airOuts: int
    runs: int
    doubles: int
    triples: int
    homeRuns: int
    strikeOuts: int
    baseOnBalls: int
    intentionalWalks: int
    hits: int
    hitByPitch: int
    avg: str
    atBats: int
    obp: str
    slg: str
    ops: str
    caughtStealing: int
    stolenBases: int
    stolenBasePercentage: str
    groundIntoDoublePlay: int
    numberOfPitches: int
    era: str
    inningsPitched: str
    wins: int
    losses: int
    saves: int
    saveOpportunities: int
    holds: int
    blownSaves: int
    earnedRuns: int
    whip: str
    battersFaced: int
    outs: int
    gamesPitched: int
    completeGames: int
    shutouts: int
    strikes: int
    strikePercentage: str
    hitBatsmen: int
    balks: int
    wildPitches: int
    pickoffs: int
    totalBases: int
    groundOutsToAirouts: str
    winPercentage: str
    pitchesPerInning: str
    gamesFinished: int
    strikeoutWalkRatio: str
    strikeoutsPer9Inn: str
    walksPer9Inn: str
    hitsPer9Inn: str
    runsScoredPer9: str
    homeRunsPer9: str
    inheritedRunners: int
    inheritedRunnersScored: int
    catchersInterference: int
    sacBunts: int
    sacFlies: int

    def __init__(self, **kwargs):

        if 'stat' in kwargs:
            
            self.__dict__.update(kwargs['stat'])

        self.__dict__.update(kwargs)

