import requests
from dataclasses import dataclass, asdict

"""
Avaliable stats

projected
yearByYear
yearByYearAdvanced
career
careerAdvanced
season
seasonAdvanced
gameLog
expectedStatistics
lastXGames
byMonth
byDayOfWeek
"""

"""
URLS:

https://statsapi.mlb.com/api/v1/teams/110?hydrate=standings

https://statsapi.mlb.com/api/{ver}/teams/{teamId}/roster/40Man

https://statsapi.mlb.com/api/v1/teams/110/stats?stats=atGameStart&group=hitting,pitching,fielding,catching
"""

@dataclass(frozen=True)
class teamName:
    __slots__ = ['full','location','franchise','club','short','abbreviation']
    full: str
    location: str
    franchise: str
    club: str
    short: str
    abbreviation: str

    def __str__(self) -> str:
        return str(self.full)

    def __repr__(self) -> str:
        return str(self.full)

    def asdict(self):
        return asdict(self)

@dataclass(frozen=True)
class idName:
    __slots__ = ['Id','name']
    Id: int
    name: str

    def __str__(self) -> str:
        return str(self.name)

    def __repr__(self) -> str:
        return str(self.name)

    @property
    def id(self):
        return self.Id

    def asdict(self):
        return asdict(self)

@dataclass(frozen=True)
class teamRanking:
    __slots__ = ['division','league','wildCard','overall','gamesPlayed','gamesBack',
                'wildCardGamesBack','leagueGamesBack','springLeagueGamesBack',
                'overallGamesBack','divisionGamesBack','conferenceGamesBack']
    division: str
    league: str
    wildCard: str
    overall: str
    gamesPlayed: int
    gamesBack: str
    wildCardGamesBack: str
    leagueGamesBack: str
    springLeagueGamesBack: str
    overallGamesBack: str
    divisionGamesBack: str
    conferenceGamesBack: str

    def asdict(self):
        return asdict(self)

@dataclass(frozen=True)
class leagueRecord:
    __slots__ = ['wins','losses','ties','pct']
    wins: int
    losses: int
    ties: int
    pct: str

    def __str__(self) -> str:
        return str(self.pct)

    def __repr__(self) -> str:
        return str(self.pct)

    def asdict(self):
        return asdict(self)

@dataclass(frozen=True)
class splitRecordData:
    __slots__ = ['wins','losses','pct']
    wins: int
    losses: int
    pct: str

    def __str__(self) -> str:
        return str(self.pct)

    def __repr__(self) -> str:
        return str(self.pct)

    def asdict(self):
        return asdict(self)


@dataclass(frozen=True)
class splitRecord:
    __slots__ = ['sr_home','sr_way','sr_left','sr_right','sr_leftHome','sr_leftAway','sr_rightHome',
                'sr_rightAway','sr_lastTen','sr_extraInning','sr_oneRun','sr_winners','sr_day',
                'sr_night','sr_grass','sr_turf']


    sr_home: splitRecordData
    sr_away: splitRecordData
    sr_left: splitRecordData
    sr_right: splitRecordData
    sr_leftHome: splitRecordData
    sr_leftAway: splitRecordData
    sr_rightHome: splitRecordData
    sr_rightAway: splitRecordData
    sr_lastTen: splitRecordData
    sr_extraInning: splitRecordData
    sr_oneRun: splitRecordData
    sr_winners: splitRecordData
    sr_day: splitRecordData
    sr_night: splitRecordData
    sr_grass: splitRecordData
    sr_turf: splitRecordData


    @property
    def home(self):
        return self.sr_home

    @property
    def away(self):
        return self.sr_away

    @property
    def left(self):
        return self.sr_left

    @property
    def right(self):
        return self.sr_right

    @property
    def leftHome(self):
        return self.sr_leftHome

    @property
    def leftAway(self):
        return self.sr_leftAway

    @property
    def rightHome(self):
        return self.sr_rightHome

    @property
    def rightAway(self):
        return self.sr_rightAway

    @property
    def lastTen(self):
        return self.sr_lastTen

    @property
    def extraInning(self):
        return self.sr_extraInning

    @property
    def oneRun(self):
        return self.sr_oneRun

    @property
    def winners(self):
        return self.sr_winners

    @property
    def day(self):
        return self.sr_day

    @property
    def night(self):
        return self.sr_night

    @property
    def grass(self):
        return self.sr_grass

    @property
    def turf(self):
        return self.sr_turf

    def asdict(self):
        return asdict(self)




class Team():

    def __init__(self, teamId: int, season: int = None):

        group = "hitting,pitching,fielding"
        type = "season,seasonAdvanced,career,careerAdvanced,yearByYear,yearByYearAdvanced"

        team_base_url = f'https://statsapi.mlb.com/api/v1/teams/{teamId}'


        teamInfo = requests.get(team_base_url+"?hydrate=standings").json()['teams'][0]
        rosterData = requests.get(team_base_url+"/roster/40Man").json()
        statsData = requests.get(team_base_url+f'/stats?stats={type}&group={group}').json()

        self._teamId = teamId

        self._name = teamName(
            full = teamInfo['name'],
            location = teamInfo['locationName'],
            franchise = teamInfo['franchiseName'],
            club = teamInfo['clubName'],
            short = teamInfo['shortName'],
            abbreviation = teamInfo['abbreviation']
        )

        self._springLeague = idName(
            Id = teamInfo['springLeague']['id'],
            name = teamInfo['springLeague']['name']
        )
        self._league = idName(
            Id = teamInfo['league']['id'],
            name = teamInfo['league']['name']
        )
        self._division = idName(
            Id = teamInfo['division']['id'],
            name = teamInfo['division']['name']
        )
        self._venue = idName(
            Id = teamInfo['venue']['id'],
            name = teamInfo['venue']['name']
        )

        record = teamInfo['record']

        self._ranking = teamRanking (
            division = record['divisionRank'],
            league = record['leagueRank'],
            wildCard = record['wildCardRank'],
            overall = record['sportRank'],
            gamesPlayed = record['gamesPlayed'],
            gamesBack = record['gamesBack'],
            wildCardGamesBack = record['wildCardGamesBack'],
            leagueGamesBack = record['leagueGamesBack'],
            springLeagueGamesBack = record['springLeagueGamesBack'],
            overallGamesBack = record['sportGamesBack'],
            divisionGamesBack = record['divisionGamesBack'],
            conferenceGamesBack = record['conferenceGamesBack']
        )

        self._leagueRecord = leagueRecord (
            wins = record['leagueRecord']['wins'],
            losses = record['leagueRecord']['losses'],
            ties = record['leagueRecord']['ties'],
            pct = record['leagueRecord']['pct']
        )

        splitRecords = record['records']['splitRecords']

        splitRecordsDic = {
            "home": {},
            "away": {},
            "left": {},
            "right": {},
            "leftHome": {},
            "leftAway": {},
            "rightHome": {},
            "rightAway": {},
            "lastTen": {},
            "extraInning": {},
            "oneRun": {},
            "winners": {},
            "day": {},
            "night": {},
            "grass": {},
            "turf": {}
        }

        for sRec in splitRecords:
            splitRecordsDic[sRec["type"]] = sRec


        self._splitRecords = splitRecord (
            sr_home = splitRecordsDic['home'],
            sr_away = splitRecordsDic['away'],
            sr_left = splitRecordsDic['left'],
            sr_right = splitRecordsDic['right'],
            sr_leftHome = splitRecordsDic['leftHome'],
            sr_leftAway = splitRecordsDic['leftAway'],
            sr_rightHome = splitRecordsDic['rightHome'],
            sr_rightAway = splitRecordsDic['rightAway'],
            sr_lastTen = splitRecordsDic['lastTen'],
            sr_extraInning = splitRecordsDic['extraInning'],
            sr_oneRun = splitRecordsDic['oneRun'],
            sr_winners = splitRecordsDic['winners'],
            sr_day = splitRecordsDic['day'],
            sr_night = splitRecordsDic['night'],
            sr_grass = splitRecordsDic['grass'],
            sr_turf = splitRecordsDic['turf']
        )


    @property
    def teamId(self):
        return self._teamId

    @property
    def name(self):
        return self._name

    @property
    def springLeague(self):
        return self._springLeague

    @property
    def league(self):
        return self._league

    @property
    def division(self):
        return self._division

    @property
    def venue(self):
        return self._venue

    @property
    def ranking(self):
        return self._ranking

    @property
    def leagueRecord(self):
        return self._leagueRecord

    @property
    def splitRecords(self):
        return self._splitRecords
