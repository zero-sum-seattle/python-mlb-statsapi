from dataclasses import dataclass, field
from typing import Optional, Union

from .stats import Stats

@dataclass
class SeasonPitching(Stats):
    type_ = "season"
    gamesplayed: int
    gamesstarted: int
    groundouts: int
    airouts: int
    runs: int
    doubles: int
    triples: int
    homeruns: int
    strikeouts: int
    baseonballs: int
    intentionalwalks: int
    hits: int
    hitbypitch: int
    avg: str
    atbats: int
    obp: str
    slg: str
    ops: str
    caughtstealing: int
    stolenbases: int
    stolenbasepercentage: str
    groundintodoubleplay: int
    numberofpitches: int
    era: str
    inningspitched: str
    wins: int
    losses: int
    saves: int
    saveopportunities: int
    holds: int
    blownsaves: int
    earnedruns: int
    whip: str
    battersFaced: int
    outs: int
    gamespitched: int
    completegames: int
    shutouts: int
    strikes: int
    strikepercentage: str
    hitbatsmen: int
    balks: int
    wildpitches: int
    pickoffs: int
    totalbases: int
    groundoutstoairouts: str
    winpercentage: str
    pitchesperinning: str
    gamesfinished: int
    strikeoutwalkratio: str
    strikeoutsper9inn: str
    walksper9inn: str
    hitsper9inn: str
    runsscoredper9: str
    homerunsper9: str
    inheritedrunners: int
    inheritedrunnersscored: int
    catchersinterference: int
    sacbunts: int
    sacflies: int
    stat_type : Optional[str] = None
    stat_group : Optional[str] = None
    gametype : Optional[str] = None
    numteams : Optional[str] = None
    season : Optional[str] = None
