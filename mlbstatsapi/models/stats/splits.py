from dataclasses import dataclass
from mlbstatsapi.models.team import Team
from mlbstatsapi.models.person import Person
from mlbstatsapi.models.sport import Sport
from mlbstatsapi.models.league import League

@dataclass
class Splits:
    def get_team(self):
        if isinstance(self.team, dict):
            return Team(**self.team)

    def get_player(self):
        if isinstance(self.player, dict):
            return Person(**self.player)

    def get_league(self):
        if isinstance(self.league, dict):
            return League(**self.league)

    def get_sport(self):
        if isinstance(self.sport, dict):
            return Sport(**self.sport)

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