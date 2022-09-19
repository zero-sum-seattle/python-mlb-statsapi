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
    __slots__ = ['id','name']
    id: int
    name: str

    def __str__(self) -> str:
        return str(self.name)

    def __repr__(self) -> str:
        return str(self.name)

    @property
    def id(self):
        return self.id

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

        self._teamId = teamInfo['']

        self._name = teamName(
            full = teamInfo['name']
            location = teamInfo['locationName']
            franchise = teamInfo['franchiseName']
            club = teamInfo['clubName']
            short = teamInfo['shortName']
            abbreviation = teamInfo['abbreviation']
        )

        self._springLeague = idName(
            id = teamInfo['springLeague']['id'],
            name = teamInfo['springLeague']['name']
        )
        self._league = idName(
            id = teamInfo['league']['id'],
            name = teamInfo['league']['name']
        )
        self._division = idName(
            id = teamInfo['division']['id'],
            name = teamInfo['division']['name']
        )
        self._venue = idName(
            id = teamInfo['venue']['id'],
            name = teamInfo['venue']['name']
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
