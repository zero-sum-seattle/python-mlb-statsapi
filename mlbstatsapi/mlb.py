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
    players: Dict
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
        self.players = players
        self.venue = GameGameDataVenue(**venue)
        self.officialVenue = Venue(**officialVenue)
        self.weather = GameGameDataWeather(**weather)
        self.gameInfo = GameGameDataGameInfo(**gameInfo)
        self.review = GameGameDataReview(**review)
        self.flags = GameGameDataFlags(**flags)
        self.alerts = alerts
        self.probablePitchers = GameGameDataProbablePitchers(**probablePitchers)


class GameLiveData():
    plays: Dict
    linescore: Dict
    boxscore: Dict
    decisions: Dict
    leaders: Dict

    def __init__(self,
                plays: Dict,
                linescore: Dict,
                boxscore: Dict,
                leaders: Dict,
                decisions: Dict = None,
                **kwargs) -> None:
        self.plays = plays
        self.linescore = linescore
        self.boxscore = boxscore
        self.decisions = decisions
        self.leaders = leaders

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
