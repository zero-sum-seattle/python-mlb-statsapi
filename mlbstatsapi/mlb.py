from typing import List, Dict
from dataclasses import dataclass
from mlbstatsapi.mlbdataadapter import MlbDataAdapter
from .exceptions import TheMlbStatsApiException



class MlbObject:
    _mlb_adapter = MlbDataAdapter()

    def generate_stats(self, stattypes: List[str] = ["season"], group: List[str] = ["hitting"]):
        # This should work for both Teams and Person
        statList = [] # Empty List to hold Stats while they are created
        if type(self) is Person or Team: # if self is a Person, Team
            # mlb_class = "people" if self is Person else ("team" if self is Team else "people") # this is so hacky until I figure out the best way to return class name as string
            for statType in stattypes: # for statType in type: List[str]
                statdata = self._mlb_adapter.get(endpoint=f"/{self.mlb_class}/{self.id}/stats?stats={statType}&group=hitting") # get stats
                statList += [ Stats(**stat) for stat in statdata.data['stats'] if "stats" in statdata.data ] # Add Stat to List[statList]
            self.stats = statList # Apply Stat Objects to self
        else:
            # implement other class stats for leagues, etc, also you shouldn't be able to call this on the MlbObject
            pass

    # Timezone conversion

class Person(MlbObject):
    # Basic Person Class
    id: int
    full_name: str
    link: str
    mlb_class = "people"
    stats: List

    def __init__(self, id: int, fullName: str = None, link: str = None, reload: bool = False, **kwargs) -> None:
        self.id = id # person id
        self.full_name = fullName # person full_name
        self.link = link# person link
        self.__dict__.update(kwargs) # let's do this for a sloppy apply


class Team(MlbObject):
    id: int
    name: str
    link: str
    mlb_class = "team"

    def __init__(self, id: int, name: str, link: str, **kwargs) -> None:
        self.id = id
        self.name = name
        self.link = link
        self.__dict__.update(kwargs)

class Sport():
    id: int
    link: str
    name: str

    def __init__(self, id: int, link: str, name: str, **kwargs) -> None:
        self.id = id
        self.link = link
        self.name = name

class League():
    id: int
    name: str
    link: str
    abbreviation: str

    def __init__(self, id: int, name: str, link: str, abbreviation: str = None) -> None:
        self.id = id
        self.name = name
        self.link = link

class Venue():
    id: int
    name: str
    link: str
    active: bool

    def __init__(self, id: int, link: str, name: str = None, active: bool = None) -> None:
        self.id = id
        self.name = name
        self.link = link
        self.active = active

class Division():
    id: int
    name: str
    link: str

    def __init__(self, id: int, link: str, name: str) -> None:
        self.id = id
        self.name = name
        self.link = link


# class GameGameDataPlayers():
#
#     def __init__(self, **kwargs) -> None:



class PlaysPlayCount():
    balls: int
    strikes: int
    outs: int

    def __init__(self, balls: int, strikes: int, outs: int) -> None:
        self.balls = balls
        self.strikes = strikes
        self.outs = outs

class PlaysPlayResult():
    type: str
    event: str
    eventType: str
    description: str
    rbi: int
    awayScore: int
    homeScore: int

    def __init__(self,
                type: str,
                event: str,
                eventType: str,
                description: str,
                rbi: int,
                awayScore: int,
                homeScore: int,
                **kwargs) -> None:
        self.type = type
        self.event = event
        self.eventType = eventType
        self.description = description
        self.rbi = rbi
        self.awayScore = awayScore
        self.homeScore = homeScore

class PlaysPlayAbout():
    atBatIndex: int
    halfInning: str
    isTopInning: bool
    inning: int
    startTime: str
    endTime: str
    isComplete: bool
    isScoringPlay: bool
    hasReview: bool
    hasOut: bool
    captivatingIndex: int

    def __init__(self,
                atBatIndex: int,
                halfInning: str,
                isTopInning: bool,
                inning: int,
                startTime: str,
                endTime: str,
                isComplete: bool,
                isScoringPlay: bool,
                hasReview: bool,
                hasOut: bool,
                captivatingIndex: int,
                **kwargs) -> None:
        self.atBatIndex = atBatIndex
        self.halfInning = halfInning
        self.isTopInning = isTopInning
        self.inning = inning
        self.startTime = startTime
        self.endTime = endTime
        self.isComplete = isComplete
        self.isScoringPlay = isScoringPlay
        self.hasReview = hasReview
        self.hasOut = hasOut
        self.captivatingIndex = captivatingIndex

class PlaysPlayMatchupSide():
    code: str
    description: str

    def __init__(self,
                code: str,
                description: str,
                **kwargs) -> None:
        self.code = code
        self.description = description

class PlaysPlayMatchupSplits():
    batter: str
    pitcher: str
    menOnBase: str

    def __init__(self,
                batter: str,
                pitcher: str,
                menOnBase: str,
                **kwargs) -> None:
        self.batter = batter
        self.pitcher = pitcher
        self.menOnBase = menOnBase


class PlaysPlayMatchup():
    batter: Person
    batSide: PlaysPlayMatchupSide
    pitcher: Person
    pitchHand: PlaysPlayMatchupSide
    batterHotColdZones: List
    pitcherHotColdZones: List
    splits: PlaysPlayMatchupSplits

    def __init__(self,
                batter: Dict,
                batSide: Dict,
                pitcher: Dict,
                pitchHand: Dict,
                batterHotColdZones: List,
                pitcherHotColdZones: List,
                splits: Dict,
                **kwargs) -> None:
        self.batter = Person(**batter)
        self.batSide = PlaysPlayMatchupSide(**batSide)
        self.pitcher = Person(**pitcher)
        self.pitchHand = PlaysPlayMatchupSide(**pitchHand)
        self.batterHotColdZones = batterHotColdZones
        self.pitcherHotColdZones = pitcherHotColdZones
        self.splits = PlaysPlayMatchupSplits(**splits)

class PlaysPlayRunnersMovement():
    originBase: str
    start: str
    end: str
    outBase: str
    isOut: bool
    outNumber: int

    def __init__(self,
                isOut: bool,
                outNumber: int,
                originBase: str = None,
                start: str = None,
                end: str = None,
                outBase: str = None,
                **kwargs) -> None:

        self.originBase = originBase
        self.start = start
        self.end = end
        self.outBase = outBase
        self.isOut = isOut
        self.outNumber = outNumber

class PlaysPlayRunnersDetails():
    event: str
    eventType: str
    movementReason: str
    runner: Person
    responsiblePitcher: Person
    isScoringEvent: bool
    rbi: bool
    earned: bool
    teamUnearned: bool
    playIndex: int

    def __init__(self,
                event: str,
                eventType: str,
                runner: dict,
                isScoringEvent: bool,
                rbi: bool,
                earned: bool,
                teamUnearned: bool,
                playIndex: int,
                movementReason: str = None,
                responsiblePitcher: dict = None,
                **kwargs) -> None:

        self.event = event
        self.eventType = eventType
        self.movementReason = movementReason
        self.runner = Person(**runner)
        self.responsiblePitcher = Person(**responsiblePitcher) if responsiblePitcher else responsiblePitcher
        self.isScoringEvent = isScoringEvent
        self.rbi = rbi
        self.earned = earned
        self.teamUnearned = teamUnearned
        self.playIndex = playIndex

class PlaysPlayRunnersCreditsPosition():
    code: str
    name: str
    type: str
    abbreviation: str

    def __init__(self,
                code: str,
                name: str,
                type: str,
                abbreviation: str,
                **kwargs) -> None:
        self.code = code
        self.name = name
        self.type = type
        self.abbreviation = abbreviation

class PlaysPlayRunnersCredits():
    player: Person
    position: PlaysPlayRunnersCreditsPosition
    credit: str

    def __init__(self,
                player: Dict,
                position: Dict,
                credit: str,
                **kwargs) -> None:
        self.player = Person(**player)
        self.position = PlaysPlayRunnersCreditsPosition(**position)
        self.credit = credit

class PlaysPlayRunners():
    movement: PlaysPlayRunnersMovement
    details: PlaysPlayRunnersDetails
    credits: List[PlaysPlayRunnersCredits]

    def __init__(self,
                movement: Dict,
                details: Dict,
                credits: List,
                **kwargs) -> None:
        self.movement = PlaysPlayRunnersMovement(**movement)
        self.details = PlaysPlayRunnersDetails(**details)
        self.credits = [PlaysPlayRunnersCredits(**credit) for credit in credits]

class PlaysPlayPlayEventsDetailsCallType():
    code: str
    description: str

    def __init__(self, code: str, description: str) -> None:
        self.code = code
        self.description = description

class PlaysPlayPlayEventsDetails():
    call: PlaysPlayPlayEventsDetailsCallType
    description: str
    event: str
    eventType: str
    code: str
    ballColor: str
    trailColor: str
    awayScore: int
    homeScore: int
    isInPlay: bool
    isStrike: bool
    isBall: bool
    isScoringPlay: bool
    type: PlaysPlayPlayEventsDetailsCallType
    hasReview: bool
    fromCatcher: bool
    runnerGoing: bool

    def __init__(self,
                description: str,
                hasReview: bool,

                call: Dict = None,
                event: str = None,
                eventType: str = None,
                code: str = None,
                ballColor: str = None,
                trailColor: str = None,
                awayScore: int = None,
                homeScore: int = None,
                isInPlay: bool = None,
                isStrike: bool = None,
                isBall: bool = None,
                isScoringPlay: bool = None,
                type: Dict = None,
                fromCatcher: bool = None,
                runnerGoing: bool = None,
                **kwargs) -> None:
        self.call = PlaysPlayPlayEventsDetailsCallType(**call) if call else call
        self.description = description
        self.event = event
        self.eventType = eventType
        self.code = code
        self.ballColor = ballColor
        self.trailColor = trailColor
        self.awayScore = awayScore
        self.homeScore = homeScore
        self.isInPlay = isInPlay
        self.isStrike = isStrike
        self.isBall = isBall
        self.isScoringPlay = isScoringPlay
        self.type = PlaysPlayPlayEventsDetailsCallType(**type) if type else type
        self.hasReview = hasReview
        self.fromCatcher = fromCatcher
        self.runnerGoing = runnerGoing

class PlaysPlayPlayEvents():
    details: PlaysPlayPlayEventsDetails
    count: PlaysPlayCount
    index: int
    startTime: str
    endTime: str
    isPitch: bool
    type: str
    player: Person

    def __init__(self,
                details: dict,
                index: int,
                startTime: str,
                endTime: str,
                isPitch: bool,
                type: str,
                count: dict = None,
                player: dict = None,
                **kwargs) -> None:
        self.details = PlaysPlayPlayEventsDetails(**details)
        self.count = PlaysPlayCount(**count) if count else count
        self.index = index
        self.startTime = startTime
        self.endTime = endTime
        self.isPitch = isPitch
        self.type = type
        self.player = Person(**player) if player else player


class PlaysPlay():
    result: PlaysPlayResult
    about: PlaysPlayAbout
    count: PlaysPlayCount
    matchup: PlaysPlayMatchup
    pitchIndex: List[int]
    actionIndex: List[int]
    runnerIndex: List[int]
    runners: List[PlaysPlayRunners]
    playEvents: List[PlaysPlayPlayEvents]
    playEndTime: str
    atBatIndex: int

    def __init__(self,
                result: Dict,
                about: Dict,
                count: Dict,
                matchup: Dict,
                pitchIndex: List,
                actionIndex: List,
                runnerIndex: List,
                runners: List,
                playEvents: List,
                playEndTime: str,
                atBatIndex: int,
                **kwargs) -> None:
        self.result = PlaysPlayResult(**result)
        self.about = PlaysPlayAbout(**about)
        self.count = PlaysPlayCount(**count)
        self.matchup = PlaysPlayMatchup(**matchup)
        self.pitchIndex = pitchIndex
        self.actionIndex = actionIndex
        self.runnerIndex = runnerIndex
        self.runners = [PlaysPlayRunners(**runner) for runner in runners]
        self.playEvents = [PlaysPlayPlayEvents(**playEvent) for playEvent in playEvents]
        self.playEndTime = playEndTime
        self.atBatIndex = atBatIndex

class PlaysPlayByInningHitsByTeamHitCoordinates():
    x: float
    y: float

    def __init__(self, x: float, y: float, **kwargs) -> None:
        self.x = x
        self.y = y


class PlaysPlayByInningHitsByTeam():
    team: Team
    inning: int
    pitcher: Person
    batter: Person
    coordinates: PlaysPlayByInningHitsByTeamHitCoordinates
    type: str
    description: str

    def __init__(self,
                team: Dict,
                inning: int,
                pitcher: Dict,
                batter: Dict,
                coordinates: Dict,
                type: str,
                description: str,
                **kwargs) -> None:
        self.team = Team(**team)
        self.inning = inning
        self.pitcher = Person(**pitcher)
        self.batter = Person(**batter)
        self.coordinates = PlaysPlayByInningHitsByTeamHitCoordinates(**coordinates)
        self.type = type
        self.description = description


class PlaysPlayByInningHits():
    home: List[PlaysPlayByInningHitsByTeam]
    away: List[PlaysPlayByInningHitsByTeam]

    def __init__(self,
                home: List,
                away: List,
                **kwargs) -> None:
        self.home = [PlaysPlayByInningHitsByTeam(**home_hit) for home_hit in home]
        self.away = [PlaysPlayByInningHitsByTeam(**away_hit) for away_hit in away]

class PlaysPlayByInning():
    startIndex: int
    endIndex: int
    top: List[int]
    bottom: List[int]
    hits: PlaysPlayByInningHits

    def __init__(self,
                startIndex: int,
                endIndex: int,
                top: List,
                bottom: List,
                hits: Dict,
                **kwargs) -> None:
        self.startIndex = startIndex
        self.endIndex = endIndex
        self.top = top
        self.bottom = bottom
        self.hits = PlaysPlayByInningHits(**hits)


class Plays():
    allPlays: List[PlaysPlay]
    currentPlay: PlaysPlay
    scoringPlays: List[int]
    playsByInning: List[PlaysPlayByInning]

    def __init__(self,
                currentPlay: Dict,
                scoringPlays: List,
                playsByInning: List,
                allPlays: List = None,
                **kwargs) -> None:
        self.allPlays = [PlaysPlay(**play) for play in allPlays if play]
        self.currentPlay = PlaysPlay(**currentPlay)
        self.scoringPlays = scoringPlays
        self.playsByInning = [PlaysPlayByInning(**inning) for inning in playsByInning if inning]





class LinescoreTeamScoreInfo():
    runs: int
    hits: int
    errors: int
    leftOnBase: int

    def __init__(self,
                hits: int,
                errors: int,
                leftOnBase: int,
                runs: int = None,
                **kwargs) -> None:
        self.runs = runs
        self.hits = hits
        self.errors = errors
        self.leftOnBase = leftOnBase

class LinescoreInning():
    num: int
    ordinalNum: str
    home: LinescoreTeamScoreInfo
    away: LinescoreTeamScoreInfo

    def __init__(self,
                num: int,
                ordinalNum: str,
                home: Dict,
                away: Dict,
                **kwargs) -> None:
        self.num = num
        self.ordinalNum = ordinalNum
        self.home = LinescoreTeamScoreInfo(**home)
        self.away = LinescoreTeamScoreInfo(**away)

class LinescoreTeams():
    home: LinescoreTeamScoreInfo
    away: LinescoreTeamScoreInfo

    def __init__(self,
                home: Dict,
                away: Dict,
                **kwargs) -> None:
        self.home = LinescoreTeamScoreInfo(**home)
        self.away = LinescoreTeamScoreInfo(**away)

class LinescoreDefense():
    pitcher: Person
    catcher: Person
    first: Person
    second: Person
    third: Person
    shortstop: Person
    left: Person
    center: Person
    right: Person
    batter: Person
    onDeck: Person
    inHole: Person
    battingOrder: int
    team: Team

    def __init__(self,
                pitcher: Dict,
                catcher: Dict,
                first: Dict,
                second: Dict,
                third: Dict,
                shortstop: Dict,
                left: Dict,
                center: Dict,
                right: Dict,
                batter: Dict,
                onDeck: Dict,
                inHole: Dict,
                battingOrder: int,
                team: Dict,
                **kwargs) -> None:
        self.pitcher = Person(**pitcher)
        self.catcher = Person(**catcher)
        self.first = Person(**first)
        self.second = Person(**second)
        self.third = Person(**third)
        self.shortstop = Person(**shortstop)
        self.left = Person(**left)
        self.center = Person(**center)
        self.right = Person(**right)
        self.batter = Person(**batter)
        self.onDeck = Person(**onDeck)
        self.inHole = Person(**inHole)
        self.battingOrder = battingOrder
        self.team = Team(**team)

class LinescoreOffenseOnBase():
    first: Person
    second: Person
    third: Person
    def __init__(self,
                first: Dict = None,
                second: Dict = None,
                third: Dict = None,
                **kwargs) -> None:
        self.first = Person(**first) if first else first
        self.second = Person(**second) if second else second
        self.third = Person(**third) if third else third


class LinescoreOffense():
    batter: Person
    onDeck: Person
    inHole: Person
    pitcher: Person
    battingOrder: int
    team: Team
    onBase: LinescoreOffenseOnBase

    def __init__(self,
                batter: Dict,
                onDeck: Dict,
                inHole: Dict,
                pitcher: Dict,
                battingOrder: int,
                team: Dict,
                onBase: Dict = None,
                **kwargs) -> None:
        self.batter = Person(**batter)
        self.onDeck = Person(**onDeck)
        self.inHole = Person(**inHole)
        self.pitcher = Person(**pitcher)
        self.battingOrder = battingOrder
        self.team = Team(**team)
        self.onBase = LinescoreOffenseOnBase(**onBase) if onBase else onBase

class Linescore():
    currentInning: int
    currentInningOrdinal: str
    inningState: str
    inningHalf: str
    isTopInning: bool
    scheduledInnings: int
    innings: List[LinescoreInning]
    teams: LinescoreTeams
    defense: LinescoreDefense
    offense: LinescoreOffense
    balls: int
    strikes: int
    outs: int

    def __init__(self,
                currentInning: int,
                currentInningOrdinal: str,
                inningState: str,
                inningHalf: str,
                isTopInning: bool,
                scheduledInnings: int,
                innings: List,
                teams: Dict,
                defense: Dict,
                offense: Dict,
                balls: int,
                strikes: int,
                outs: int,
                **kwargs) -> None:
        self.currentInning = currentInning
        self.currentInningOrdinal = currentInningOrdinal
        self.inningState = inningState
        self.inningHalf = inningHalf
        self.isTopInning = isTopInning
        self.scheduledInnings = scheduledInnings
        self.innings = [LinescoreInning(**inning) for inning in innings]
        self.teams = LinescoreTeams(**teams)
        self.defense = LinescoreDefense(**defense)
        self.offense = LinescoreOffense(**offense)
        self.balls = balls
        self.strikes = strikes
        self.outs = outs








class Stats():
    group: str
    statype: str

    def __init__(self, group: str, type: str, **kwargs) -> None:
        self.group = group
        self.type = type
        self.__dict__.update(kwargs)
