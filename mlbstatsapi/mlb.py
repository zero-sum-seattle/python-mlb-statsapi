from typing import List, Dict
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

class GameMetaData():
    wait: int
    timeStamp: str
    gameEvents: List[str]
    logicalEvents: List[str]

    def __init__(self,
                wait: int,
                timeStamp: str,
                gameEvents: List[str],
                logicalEvents: List[str],
                **kwargs) -> None:
        self.wait = wait
        self.timeStamp = timeStamp
        self.gameEvents = gameEvents
        self.logicalEvents = logicalEvents

class GameGameDataGame():
    pk: int
    type: str
    doubleHeader: str
    id: str
    gamedayType: str
    tiebreaker: str
    gameNumber: int
    calendarEventID: str
    season: str
    seasonDisplay: str

    def __init__(self,
                pk: int,
                type: str,
                doubleHeader: str,
                id: str,
                gamedayType: str,
                tiebreaker: str,
                gameNumber: int,
                calendarEventID: str,
                season: str,
                seasonDisplay: str,
                **kwargs) -> None:
        self.pk = pk
        self.type = type
        self.doubleHeader = doubleHeader
        self.id = id
        self.gamedayType = gamedayType
        self.tiebreaker = tiebreaker
        self.gameNumber = gameNumber
        self.calendarEventID = calendarEventID
        self.season = season
        self.seasonDisplay = seasonDisplay

class GameGameDataDatetime():
    dateTime: str
    originalDate: str
    officialDate: str
    dayNight: str
    time: str
    ampm: str

    def __init__(self,
                dateTime: str,
                originalDate: str,
                officialDate: str,
                dayNight: str,
                time: str,
                ampm: str,
                **kwargs) -> None:
        self.dateTime = dateTime
        self.originalDate = originalDate
        self.officialDate = officialDate
        self.dayNight = dayNight
        self.time = time
        self.ampm = ampm

class GameGameDataStatus():
    abstractGameState: str
    codedGameState: str
    detailedState: str
    statusCode: str
    startTimeTBD: bool
    abstractGameCode: str

    def __init__(self,
                abstractGameState: str,
                codedGameState: str,
                detailedState: str,
                statusCode: str,
                startTimeTBD: bool,
                abstractGameCode: str,
                **kwargs) -> None:
        self.abstractGameState = abstractGameState
        self.codedGameState = codedGameState
        self.detailedState = detailedState
        self.statusCode = statusCode
        self.startTimeTBD = startTimeTBD
        self.abstractGameCode = abstractGameCode

class GameGameDataTeamsTeamRecord():
    gamesPlayed: int
    wildCardGamesBack: str
    leagueGamesBack: str
    springLeagueGamesBack: str
    sportGamesBack: str
    divisionGamesBack: str
    conferenceGamesBack: str
    leagueRecord: Dict
    records: Dict
    divisionLeader: bool
    wins: int
    losses: int
    winningPercentage: str

    def __init__(self,
                gamesPlayed: int,
                wildCardGamesBack: str,
                leagueGamesBack: str,
                springLeagueGamesBack: str,
                sportGamesBack: str,
                divisionGamesBack: str,
                conferenceGamesBack: str,
                leagueRecord: Dict,
                records: Dict,
                divisionLeader: bool,
                wins: int,
                losses: int,
                winningPercentage: str,
                **kwargs) -> None:
        self.gamesPlayed = gamesPlayed
        self.wildCardGamesBack = wildCardGamesBack
        self.leagueGamesBack = leagueGamesBack
        self.springLeagueGamesBack = springLeagueGamesBack
        self.sportGamesBack = sportGamesBack
        self.divisionGamesBack = divisionGamesBack
        self.conferenceGamesBack = conferenceGamesBack
        self.leagueRecord = leagueRecord
        self.records = records
        self.divisionLeader = divisionLeader
        self.wins = wins
        self.losses = losses
        self.winningPercentage = winningPercentage

class GameGameDataTeamsTeam():
    springLeague: League
    allStarStatus: str
    id: int
    name: str
    link: str
    season: int
    venue: Venue
    springVenue: Venue
    teamCode: str
    fileCode: str
    abbreviation: str
    teamName: str
    locationName: str
    firstYearOfPlay: str
    league: League
    division: Division
    sport: Sport
    shortName: str
    record: GameGameDataTeamsTeamRecord
    franchiseName: str
    clubName: str
    active: bool

    def __init__(self,
                springLeague: Dict,
                allStarStatus: str,
                id: int,
                name: str,
                link: str,
                season: int,
                venue: Dict,
                springVenue: Dict,
                teamCode: str,
                fileCode: str,
                abbreviation: str,
                teamName: str,
                locationName: str,
                firstYearOfPlay: str,
                league: Dict,
                division: Dict,
                sport: Dict,
                shortName: str,
                record: Dict,
                franchiseName: str,
                clubName: str,
                active: bool,
                **kwargs) -> None:
        self.springLeague = League(**springLeague)
        self.allStarStatus = allStarStatus
        self.id = id
        self.name = name
        self.link = link
        self.season = season
        self.venue = Venue(**venue)
        self.springVenue = Venue(**springVenue)
        self.teamCode = teamCode
        self.fileCode = fileCode
        self.abbreviation = abbreviation
        self.teamName = teamName
        self.locationName = locationName
        self.firstYearOfPlay = firstYearOfPlay
        self.league = League(**league)
        self.division = division
        self.sport = Sport(**sport)
        self.shortName = shortName
        self.record = GameGameDataTeamsTeamRecord(**record)
        self.franchiseName = franchiseName
        self.clubName = clubName
        self.active = active

class GameGameDataTeams():
    away: GameGameDataTeamsTeam
    home: GameGameDataTeamsTeam

    def __init__(self,
                away: Dict,
                home: Dict,
                **kwargs) -> None:
        self.away = GameGameDataTeamsTeam(**away)
        self.home = GameGameDataTeamsTeam(**home)

# class GameGameDataPlayers():
#
#     def __init__(self, **kwargs) -> None:

class GameGameDataVenueLocationCoordinates:
    latitude: float
    longitude: float

    def __init__(self, latitude: float, longitude: float) -> None:
        self.latitude = latitude
        self.longitude = longitude


class GameGameDataVenueLocation():
    address1: str
    city: str
    state: str
    stateAbbrev: str
    postalCode: str
    defaultCoordinates: GameGameDataVenueLocationCoordinates
    country: str
    phone: str

    def __init__(self,
                address1: str,
                city: str,
                state: str,
                stateAbbrev: str,
                postalCode: str,
                defaultCoordinates: dict,
                country: str,
                phone: str,
                **kwargs) -> None:
        self.address1 = address1
        self.city = city
        self.state = state
        self.stateAbbrev = stateAbbrev
        self.postalCode = postalCode
        self.defaultCoordinates = GameGameDataVenueLocationCoordinates(**defaultCoordinates)
        self.country = country
        self.phone = phone

class GameGameDataVenueTimeZone:
    id: str
    offset: int
    tz: str

    def __init__(self, id: str, offset: int, tz: str) -> None:
        self.id = id
        self.offset = offset
        self.tz = tz


class GameGameDataVenueFieldInfo():
    capacity: int
    turfType: str
    roofType: str
    leftLine: int
    left: int
    leftCenter: int
    center: int
    rightCenter: int
    rightLine: int

    def __init__(self,
                capacity: int,
                turfType: str,
                roofType: str,
                leftLine: int,
                left: int,
                leftCenter: int,
                center: int,
                rightCenter: int,
                rightLine: int,
                **kwargs) -> None:
        self.capacity = capacity
        self.turfType = turfType
        self.roofType = roofType
        self.leftLine = leftLine
        self.left = left
        self.leftCenter = leftCenter
        self.center = center
        self.rightCenter = rightCenter
        self.rightLine = rightLine


class GameGameDataVenue():
    id: int
    name: str
    link: str
    location: GameGameDataVenueLocation
    timeZone: GameGameDataVenueTimeZone
    fieldInfo: GameGameDataVenueFieldInfo
    active: bool

    def __init__(self,
                id: int,
                name: str,
                link: str,
                location: Dict,
                timeZone: Dict,
                fieldInfo: Dict,
                active: bool,
                **kwargs) -> None:
        self.id = id
        self.name = name
        self.link = link
        self.location = GameGameDataVenueLocation(**location)
        self.timeZone = GameGameDataVenueTimeZone(**timeZone)
        self.fieldInfo = GameGameDataVenueFieldInfo(**fieldInfo)
        self.active = active

class GameGameDataWeather():
    condition: str
    temp: str
    wind: str

    def __init__(self,
                condition: str,
                temp: str,
                wind: str,
                **kwargs) -> None:
        self.condition = condition
        self.temp = temp
        self.wind = wind

class GameGameDataGameInfo():
    attendance: int
    firstPitch: str
    gameDurationMinutes: int
    delayDurationMinutes: int

    def __init__(self,
                attendance: int,
                firstPitch: str,
                gameDurationMinutes: int,
                delayDurationMinutes: int,
                **kwargs) -> None:
        self.attendance = attendance
        self.firstPitch = firstPitch
        self.gameDurationMinutes = gameDurationMinutes
        self.delayDurationMinutes = delayDurationMinutes

class GameGameDataReviewTeam():
    used: int
    remaining: int

    def __init__(self,
                used: int,
                remaining: int,
                **kwargs) -> None:
        self.used = used
        self.remaining = remaining

class GameGameDataReview():
    hasChallenges: bool
    away: GameGameDataReviewTeam
    home: GameGameDataReviewTeam

    def __init__(self,
                hasChallenges: bool,
                away: Dict,
                home: Dict,
                **kwargs) -> None:
        self.hasChallenges = hasChallenges
        self.away = GameGameDataReviewTeam(**away)
        self.home = GameGameDataReviewTeam(**home)

class GameGameDataFlags():
    noHitter: bool
    perfectGame: bool
    awayTeamNoHitter: bool
    awayTeamPerfectGame: bool
    homeTeamNoHitter: bool
    homeTeamPerfectGame: bool

    def __init__(self,
                noHitter: bool,
                perfectGame: bool,
                awayTeamNoHitter: bool,
                awayTeamPerfectGame: bool,
                homeTeamNoHitter: bool,
                homeTeamPerfectGame: bool,
                **kwargs) -> None:
        self.noHitter = noHitter
        self.perfectGame = perfectGame
        self.awayTeamNoHitter = awayTeamNoHitter
        self.awayTeamPerfectGame = awayTeamPerfectGame
        self.homeTeamNoHitter = homeTeamNoHitter
        self.homeTeamPerfectGame = homeTeamPerfectGame

class GameGameDataProbablePitchers():
    away: Person
    home: Person

    def __init__(self,
                away: dict,
                home: dict,
                **kwargs) -> None:
        self.away = Person(**away)
        self.home = Person(**home)

class GameGameData():
    game: GameGameDataGame
    datetime: GameGameDataDatetime
    status: GameGameDataStatus
    teams: GameGameDataTeams
    players: List[Person]
    venue: GameGameDataVenue
    officialVenue: Venue
    weather: GameGameDataWeather
    gameInfo: GameGameDataGameInfo
    review: GameGameDataReview
    flags: GameGameDataFlags
    alerts: List
    probablePitchers: GameGameDataProbablePitchers

    def __init__(self,
                game: Dict,
                datetime: Dict,
                status: Dict,
                teams: Dict,
                players: Dict,
                venue: Dict,
                officialVenue: Dict,
                weather: Dict,
                gameInfo: Dict,
                review: Dict,
                flags: Dict,
                alerts: List,
                probablePitchers: Dict,
                **kwargs) -> None:
        self.game = GameGameDataGame(**game)
        self.datetime = GameGameDataDatetime(**datetime)
        self.status = GameGameDataStatus(**status)
        self.teams = GameGameDataTeams(**teams)
        # self.players = players
        self.players = []
        self.venue = GameGameDataVenue(**venue)
        self.officialVenue = Venue(**officialVenue)
        self.weather = GameGameDataWeather(**weather)
        self.gameInfo = GameGameDataGameInfo(**gameInfo)
        self.review = GameGameDataReview(**review)
        self.flags = GameGameDataFlags(**flags)
        self.alerts = alerts
        self.probablePitchers = GameGameDataProbablePitchers(**probablePitchers)

        for key, value in players.items():
            self.players.append(Person(**value))

class GameLiveDataPlaysPlayCount():
    balls: int
    strikes: int
    outs: int

    def __init__(self, balls: int, strikes: int, outs: int) -> None:
        self.balls = balls
        self.strikes = strikes
        self.outs = outs

class GameLiveDataPlaysPlayResult():
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

class GameLiveDataPlaysPlayAbout():
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

class GameLiveDataPlaysPlayMatchupSide():
    code: str
    description: str

    def __init__(self,
                code: str,
                description: str,
                **kwargs) -> None:
        self.code = code
        self.description = description

class GameLiveDataPlaysPlayMatchupSplits():
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


class GameLiveDataPlaysPlayMatchup():
    batter: Person
    batSide: GameLiveDataPlaysPlayMatchupSide
    pitcher: Person
    pitchHand: GameLiveDataPlaysPlayMatchupSide
    batterHotColdZones: List
    pitcherHotColdZones: List
    splits: GameLiveDataPlaysPlayMatchupSplits

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
        self.batSide = GameLiveDataPlaysPlayMatchupSide(**batSide)
        self.pitcher = Person(**pitcher)
        self.pitchHand = GameLiveDataPlaysPlayMatchupSide(**pitchHand)
        self.batterHotColdZones = batterHotColdZones
        self.pitcherHotColdZones = pitcherHotColdZones
        self.splits = GameLiveDataPlaysPlayMatchupSplits(**splits)

class GameLiveDataPlaysPlayRunnersMovement():
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

class GameLiveDataPlaysPlayRunnersDetails():
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

class GameLiveDataPlaysPlayRunnersCreditsPosition():
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

class GameLiveDataPlaysPlayRunnersCredits():
    player: Person
    position: GameLiveDataPlaysPlayRunnersCreditsPosition
    credit: str

    def __init__(self,
                player: Dict,
                position: Dict,
                credit: str,
                **kwargs) -> None:
        self.player = Person(**player)
        self.position = GameLiveDataPlaysPlayRunnersCreditsPosition(**position)
        self.credit = credit

class GameLiveDataPlaysPlayRunners():
    movement: GameLiveDataPlaysPlayRunnersMovement
    details: GameLiveDataPlaysPlayRunnersDetails
    credits: List[GameLiveDataPlaysPlayRunnersCredits]

    def __init__(self,
                movement: Dict,
                details: Dict,
                credits: List,
                **kwargs) -> None:
        self.movement = GameLiveDataPlaysPlayRunnersMovement(**movement)
        self.details = GameLiveDataPlaysPlayRunnersDetails(**details)
        self.credits = [GameLiveDataPlaysPlayRunnersCredits(**credit) for credit in credits]

class GameLiveDataPlaysPlayPlayEventsDetailsCallType():
    code: str
    description: str

    def __init__(self, code: str, description: str) -> None:
        self.code = code
        self.description = description

class GameLiveDataPlaysPlayPlayEventsDetails():
    call: GameLiveDataPlaysPlayPlayEventsDetailsCallType
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
    type: GameLiveDataPlaysPlayPlayEventsDetailsCallType
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
        self.call = GameLiveDataPlaysPlayPlayEventsDetailsCallType(**call) if call else call
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
        self.type = GameLiveDataPlaysPlayPlayEventsDetailsCallType(**type) if type else type
        self.hasReview = hasReview
        self.fromCatcher = fromCatcher
        self.runnerGoing = runnerGoing

class GameLiveDataPlaysPlayPlayEvents():
    details: GameLiveDataPlaysPlayPlayEventsDetails
    count: GameLiveDataPlaysPlayCount
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
        self.details = GameLiveDataPlaysPlayPlayEventsDetails(**details)
        self.count = GameLiveDataPlaysPlayCount(**count) if count else count
        self.index = index
        self.startTime = startTime
        self.endTime = endTime
        self.isPitch = isPitch
        self.type = type
        self.player = Person(**player) if player else player


class GameLiveDataPlaysPlay():
    result: GameLiveDataPlaysPlayResult
    about: GameLiveDataPlaysPlayAbout
    count: GameLiveDataPlaysPlayCount
    matchup: GameLiveDataPlaysPlayMatchup
    pitchIndex: List[int]
    actionIndex: List[int]
    runnerIndex: List[int]
    runners: List[GameLiveDataPlaysPlayRunners]
    playEvents: List[GameLiveDataPlaysPlayPlayEvents]
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
        self.result = GameLiveDataPlaysPlayResult(**result)
        self.about = GameLiveDataPlaysPlayAbout(**about)
        self.count = GameLiveDataPlaysPlayCount(**count)
        self.matchup = GameLiveDataPlaysPlayMatchup(**matchup)
        self.pitchIndex = pitchIndex
        self.actionIndex = actionIndex
        self.runnerIndex = runnerIndex
        self.runners = [GameLiveDataPlaysPlayRunners(**runner) for runner in runners]
        self.playEvents = [GameLiveDataPlaysPlayPlayEvents(**playEvent) for playEvent in playEvents]
        self.playEndTime = playEndTime
        self.atBatIndex = atBatIndex

class GameLiveDataPlaysPlayByInningHitsByTeamHitCoordinates():
    x: float
    y: float

    def __init__(self, x: float, y: float, **kwargs) -> None:
        self.x = x
        self.y = y


class GameLiveDataPlaysPlayByInningHitsByTeam():
    team: Team
    inning: int
    pitcher: Person
    batter: Person
    coordinates: GameLiveDataPlaysPlayByInningHitsByTeamHitCoordinates
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
        self.coordinates = GameLiveDataPlaysPlayByInningHitsByTeamHitCoordinates(**coordinates)
        self.type = type
        self.description = description


class GameLiveDataPlaysPlayByInningHits():
    home: List[GameLiveDataPlaysPlayByInningHitsByTeam]
    away: List[GameLiveDataPlaysPlayByInningHitsByTeam]

    def __init__(self,
                home: List,
                away: List,
                **kwargs) -> None:
        self.home = [GameLiveDataPlaysPlayByInningHitsByTeam(**home_hit) for home_hit in home]
        self.away = [GameLiveDataPlaysPlayByInningHitsByTeam(**away_hit) for away_hit in away]

class GameLiveDataPlaysPlayByInning():
    startIndex: int
    endIndex: int
    top: List[int]
    bottom: List[int]
    hits: GameLiveDataPlaysPlayByInningHits

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
        self.hits = GameLiveDataPlaysPlayByInningHits(**hits)


class GameLiveDataPlays():
    allPlays: List[GameLiveDataPlaysPlay]
    currentPlay: GameLiveDataPlaysPlay
    scoringPlays: List[int]
    playsByInning: List[GameLiveDataPlaysPlayByInning]

    def __init__(self,
                currentPlay: Dict,
                scoringPlays: List,
                playsByInning: List,
                allPlays: List = None,
                **kwargs) -> None:
        self.allPlays = [GameLiveDataPlaysPlay(**play) for play in allPlays if play]
        self.currentPlay = GameLiveDataPlaysPlay(**currentPlay)
        self.scoringPlays = scoringPlays
        self.playsByInning = [GameLiveDataPlaysPlayByInning(**inning) for inning in playsByInning if inning]





class GameLiveDataLinescoreTeamScoreInfo():
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

class GameLiveDataLinescoreInning():
    num: int
    ordinalNum: str
    home: GameLiveDataLinescoreTeamScoreInfo
    away: GameLiveDataLinescoreTeamScoreInfo

    def __init__(self,
                num: int,
                ordinalNum: str,
                home: Dict,
                away: Dict,
                **kwargs) -> None:
        self.num = num
        self.ordinalNum = ordinalNum
        self.home = GameLiveDataLinescoreTeamScoreInfo(**home)
        self.away = GameLiveDataLinescoreTeamScoreInfo(**away)

class GameLiveDataLinescoreTeams():
    home: GameLiveDataLinescoreTeamScoreInfo
    away: GameLiveDataLinescoreTeamScoreInfo

    def __init__(self,
                home: Dict,
                away: Dict,
                **kwargs) -> None:
        self.home = GameLiveDataLinescoreTeamScoreInfo(**home)
        self.away = GameLiveDataLinescoreTeamScoreInfo(**away)

class GameLiveDataLinescoreDefense():
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

class GameLiveDataLinescoreOffenseOnBase():
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


class GameLiveDataLinescoreOffense():
    batter: Person
    onDeck: Person
    inHole: Person
    pitcher: Person
    battingOrder: int
    team: Team
    onBase: GameLiveDataLinescoreOffenseOnBase

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
        self.onBase = GameLiveDataLinescoreOffenseOnBase(**onBase) if onBase else onBase

class GameLiveDataLinescore():
    currentInning: int
    currentInningOrdinal: str
    inningState: str
    inningHalf: str
    isTopInning: bool
    scheduledInnings: int
    innings: List[GameLiveDataLinescoreInning]
    teams: GameLiveDataLinescoreTeams
    defense: GameLiveDataLinescoreDefense
    offense: GameLiveDataLinescoreOffense
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
        self.innings = [GameLiveDataLinescoreInning(**inning) for inning in innings]
        self.teams = GameLiveDataLinescoreTeams(**teams)
        self.defense = GameLiveDataLinescoreDefense(**defense)
        self.offense = GameLiveDataLinescoreOffense(**offense)
        self.balls = balls
        self.strikes = strikes
        self.outs = outs

class GameLiveDataBoxScoreVL():
    label: str
    value: str

    def __init__(self, label: str, value: str = None, **kwargs) -> None:
        self.label = label
        self.value = value

class GameLiveDataBoxScoreTeamsTeamInfoGroup():
    title: str
    fieldList: List[GameLiveDataBoxScoreVL]

    def __init__(self, title: str, fieldList: List, **kwargs) -> None:
        self.title = title
        self.fieldList = [GameLiveDataBoxScoreVL(**fieldLists) for fieldLists in fieldList]

class GameLiveDataBoxScoreTeamsTeam():
    team: Team
    teamStats: Dict
    players: Dict
    batters: List[int]
    pitchers: List[int]
    bench: List[int]
    bullpen: List[int]
    battingOrder: List[int]
    info: List[GameLiveDataBoxScoreTeamsTeamInfoGroup]
    note: List[str]

    def __init__(self,
                team: Dict,
                teamStats: Dict,
                players: Dict,
                batters: List,
                pitchers: List,
                bench: List,
                bullpen: List,
                battingOrder: List,
                info: List,
                note: List,
                **kwargs) -> None:
        self.team = Team(**team)
        self.teamStats = teamStats
        self.players = players
        self.batters = batters
        self.pitchers = pitchers
        self.bench = bench
        self.bullpen = bullpen
        self.battingOrder = battingOrder
        self.info = [GameLiveDataBoxScoreTeamsTeamInfoGroup(**infos) for infos in info]
        self.note = note

class GameLiveDataBoxScoreTeams():
    home: GameLiveDataBoxScoreTeamsTeam
    away: GameLiveDataBoxScoreTeamsTeam

    def __init__(self, home: Dict, away: Dict, **kwargs) -> None:
        self.home = GameLiveDataBoxScoreTeamsTeam(**home)
        self.away = GameLiveDataBoxScoreTeamsTeam(**away)

class GameLiveDataBoxScoreOffical():
    official: Person
    officialType: str

    def __init__(self, official: Dict, officialType: str, **kwargs) -> None:
        self.official = Person(**official)
        self.officialType = officialType

class GameLiveDataBoxScore():
    teams: GameLiveDataBoxScoreTeams
    officials: List[GameLiveDataBoxScoreOffical]
    info: List[GameLiveDataBoxScoreVL]
    pitchingNotes: List[str]

    def __init__(self,
                teams: Dict,
                officials: List,
                info: List,
                pitchingNotes: List,
                **kwargs) -> None:
        self.teams = GameLiveDataBoxScoreTeams(**teams)
        self.officials = [GameLiveDataBoxScoreOffical(**official) for official in officials]
        self.info = [GameLiveDataBoxScoreVL(**infos) for infos in info]
        self.pitchingNotes = pitchingNotes

class GameLiveDataDecisions():
    winner: Person
    loser: Person
    def __init__(self,
                winner: Dict,
                loser: Dict,
                **kwargs) -> None:
        self.winner = Person(**winner)
        self.loser = Person(**loser)

class GameLiveDataLeaders():
    # Dont know what this populated looks like. Every game ive seen its three empty dicts?
    hitDistance: Dict
    hitSpeed: Dict
    pitchSpeed: Dict

    def __init__(self,
                hitDistance: Dict,
                hitSpeed: Dict,
                pitchSpeed: Dict,
                **kwargs) -> None:
        self.hitDistance = hitDistance
        self.hitSpeed = hitSpeed
        self.pitchSpeed = pitchSpeed

class GameLiveData():
    plays: GameLiveDataPlays
    linescore: GameLiveDataLinescore
    boxscore: GameLiveDataBoxScore
    decisions: GameLiveDataDecisions
    leaders: GameLiveDataLeaders

    def __init__(self,
                plays: Dict,
                linescore: Dict,
                boxscore: Dict,
                leaders: Dict,
                decisions: Dict = None,
                **kwargs) -> None:
        self.plays = GameLiveDataPlays(**plays)
        self.linescore = GameLiveDataLinescore(**linescore)
        self.boxscore = GameLiveDataBoxScore(**boxscore)
        self.decisions = GameLiveDataDecisions(**decisions) if decisions else decisions
        self.leaders = GameLiveDataLeaders(**leaders)

class Game():
    id: int
    metaData: GameMetaData
    gameData: GameGameData
    liveData: GameLiveData

    def __init__(self, id: int,
                    metaData: Dict,
                    gameData: Dict,
                    liveData: Dict,
                    **kwargs) -> None:
        self.id = id
        self.metaData = GameMetaData(**metaData)
        self.gameData = GameGameData(**gameData)
        self.liveData = GameLiveData(**liveData)

class Stats():
    group: str
    statype: str

    def __init__(self, group: str, type: str, **kwargs) -> None:
        self.group = group
        self.type = type
        self.__dict__.update(kwargs)
