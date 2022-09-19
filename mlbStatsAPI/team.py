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
