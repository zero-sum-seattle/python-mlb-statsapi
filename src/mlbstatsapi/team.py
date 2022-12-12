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

https://statsapi.mlb.com/api/v1/teams/{teamId}?hydrate=standings

https://statsapi.mlb.com/api/{ver}/teams/{teamId}/roster/40Man

https://statsapi.mlb.com/api/v1/teams/{teamId}/stats?stats=atGameStart&group=hitting,pitching,fielding,catching
"""

@dataclass(frozen=True)
class TeamName:
    __slots__ = ['Id','full','location','franchise','club','short','abbreviation']
    Id: int
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

    @property
    def id(self):
        return self.Id

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
    __slots__ = ['home','away','left','right','leftHome','leftAway','rightHome',
                'rightAway','lastTen','extraInning','oneRun','winners','day',
                'night','grass','turf']

    home: splitRecordData
    away: splitRecordData
    left: splitRecordData
    right: splitRecordData
    leftHome: splitRecordData
    leftAway: splitRecordData
    rightHome: splitRecordData
    rightAway: splitRecordData
    lastTen: splitRecordData
    extraInning: splitRecordData
    oneRun: splitRecordData
    winners: splitRecordData
    day: splitRecordData
    night: splitRecordData
    grass: splitRecordData
    turf: splitRecordData

    def asdict(self):
        return asdict(self)

@dataclass(frozen=True)
class teamRecord:
    __slots__ = ['runsAllowed','runsScored','wins','losses','runDifferential','winningPercentage']
    runsAllowed: int
    runsScored: int
    wins: int
    losses: int
    runDifferential: int
    winningPercentage: str

    def asdict(self):
        return asdict(self)

@dataclass(frozen=True)
class teamStats:
    __slots__ = ['season_hitting','season_pitching','season_fielding',
                'seasonAdvanced_hitting','seasonAdvanced_pitching',
                'seasonAdvanced_fielding','career_hitting','career_pitching',
                'career_fielding','careerAdvanced_hitting','careerAdvanced_pitching',
                'careerAdvanced_fielding']
    season_hitting: dict
    season_pitching: dict
    season_fielding: dict
    seasonAdvanced_hitting: dict
    seasonAdvanced_pitching: dict
    seasonAdvanced_fielding: dict
    career_hitting: dict
    career_pitching: dict
    career_fielding: dict
    careerAdvanced_hitting: dict
    careerAdvanced_pitching: dict
    careerAdvanced_fielding: dict

    def asdict(self):
        return asdict(self)



"""
 Team

    Parameters
    ----------
    teamId : int
        Team id number ex: 110
    season : int:None
        Season number as year ex: 2022

    Methods:
    --------

"""

class Team():

    def __init__(self, teamId: int, season: int = None):

        group = "hitting,pitching,fielding"
        type = "season,seasonAdvanced,career,careerAdvanced,yearByYear,yearByYearAdvanced"

        team_base_url = f'https://statsapi.mlb.com/api/v1/teams/{teamId}'


        teamInfo = requests.get(team_base_url+"?hydrate=standings").json()['teams'][0]
        # rosterData = requests.get(team_base_url+"/roster/40Man").json()
        statsData = requests.get(team_base_url+f'/stats?stats={type}&group={group}').json()

        self._teamId = teamId

        self._name = TeamName(
            Id = teamInfo['id'],
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
            home = splitRecordData (
                wins = splitRecordsDic['home']['wins'],
                losses = splitRecordsDic['home']['losses'],
                pct = splitRecordsDic['home']['pct']
            ),
            away = splitRecordData (
                wins = splitRecordsDic['away']['wins'],
                losses = splitRecordsDic['away']['losses'],
                pct = splitRecordsDic['away']['pct']
            ),
            left = splitRecordData (
                wins = splitRecordsDic['left']['wins'],
                losses = splitRecordsDic['left']['losses'],
                pct = splitRecordsDic['left']['pct']
            ),
            right = splitRecordData (
                wins = splitRecordsDic['right']['wins'],
                losses = splitRecordsDic['right']['losses'],
                pct = splitRecordsDic['right']['pct']
            ),
            leftHome = splitRecordData (
                wins = splitRecordsDic['leftHome']['wins'],
                losses = splitRecordsDic['leftHome']['losses'],
                pct = splitRecordsDic['leftHome']['pct']
            ),
            leftAway = splitRecordData (
                wins = splitRecordsDic['leftAway']['wins'],
                losses = splitRecordsDic['leftAway']['losses'],
                pct = splitRecordsDic['leftAway']['pct']
            ),
            rightHome = splitRecordData (
                wins = splitRecordsDic['rightHome']['wins'],
                losses = splitRecordsDic['rightHome']['losses'],
                pct = splitRecordsDic['rightHome']['pct']
            ),
            rightAway = splitRecordData (
                wins = splitRecordsDic['rightAway']['wins'],
                losses = splitRecordsDic['rightAway']['losses'],
                pct = splitRecordsDic['rightAway']['pct']
            ),
            lastTen = splitRecordData (
                wins = splitRecordsDic['lastTen']['wins'],
                losses = splitRecordsDic['lastTen']['losses'],
                pct = splitRecordsDic['lastTen']['pct']
            ),
            extraInning = splitRecordData (
                wins = splitRecordsDic['extraInning']['wins'],
                losses = splitRecordsDic['extraInning']['losses'],
                pct = splitRecordsDic['extraInning']['pct']
            ),
            oneRun = splitRecordData (
                wins = splitRecordsDic['oneRun']['wins'],
                losses = splitRecordsDic['oneRun']['losses'],
                pct = splitRecordsDic['oneRun']['pct']
            ),
            winners = splitRecordData (
                wins = splitRecordsDic['winners']['wins'],
                losses = splitRecordsDic['winners']['losses'],
                pct = splitRecordsDic['winners']['pct']
            ),
            day = splitRecordData (
                wins = splitRecordsDic['day']['wins'],
                losses = splitRecordsDic['day']['losses'],
                pct = splitRecordsDic['day']['pct']
            ),
            night = splitRecordData (
                wins = splitRecordsDic['night']['wins'],
                losses = splitRecordsDic['night']['losses'],
                pct = splitRecordsDic['night']['pct']
            ),
            grass = splitRecordData (
                wins = splitRecordsDic['grass']['wins'],
                losses = splitRecordsDic['grass']['losses'],
                pct = splitRecordsDic['grass']['pct']
            ),
            turf = splitRecordData (
                wins = splitRecordsDic['turf']['wins'],
                losses = splitRecordsDic['turf']['losses'],
                pct = splitRecordsDic['turf']['pct']
            )
        )

        self._record = teamRecord (
            runsAllowed = record['runsAllowed'],
            runsScored = record['runsScored'],
            wins = record['wins'],
            losses = record['losses'],
            runDifferential = record['runDifferential'],
            winningPercentage = record['winningPercentage']
        )


        statDic = {
            "season_hitting" : {},
            "season_pitching" : {},
            "season_fielding" : {},
            "seasonAdvanced_hitting" : {},
            "seasonAdvanced_pitching" : {},
            "seasonAdvanced_fielding" : {},
            "career_hitting" : {},
            "career_pitching" : {},
            "career_fielding" : {},
            "careerAdvanced_hitting" : {},
            "careerAdvanced_pitching" : {},
            "careerAdvanced_fielding" : {}
        }

        for s in statsData["stats"]:
            statDic[s["type"]["displayName"]+"_"+s["group"]["displayName"]] = s["splits"][0]['stat']


        self._stats = teamStats (
            season_hitting = statDic["season_hitting"],
            season_pitching = statDic["season_pitching"],
            season_fielding = statDic["season_fielding"],
            seasonAdvanced_hitting = statDic["seasonAdvanced_hitting"],
            seasonAdvanced_pitching = statDic["seasonAdvanced_pitching"],
            seasonAdvanced_fielding = statDic["seasonAdvanced_fielding"],
            career_hitting = statDic["career_hitting"],
            career_pitching = statDic["career_pitching"],
            career_fielding = statDic["career_fielding"],
            careerAdvanced_hitting = statDic["careerAdvanced_hitting"],
            careerAdvanced_pitching = statDic["careerAdvanced_pitching"],
            careerAdvanced_fielding = statDic["careerAdvanced_fielding"]
        )


    @property
    def teamId(self) -> int:
        """Team Id"""
        return self._teamId

    @property
    def name(self) -> TeamName:
        """Team name dataclass

        Keys/Attributes:
        ------------
        full:           str
        location:       str
        franchise:      str
        club:           str
        short:          str
        abbreviation:   str

        Usage:
        ------------
        name.location returns the location as a string
        """
        return self._name

    @property
    def springLeague(self) -> idName:
        """springLeague
        Name and id for the teams spring league

        Keys/Attributes:
        ------------
        Id:     int
        name:   str
        """
        return self._springLeague

    @property
    def league(self) -> idName:
        """league
        Name and id for the teams league (normal season)

        Keys/Attributes:
        ------------
        Id:     int
        name:   str
        """
        return self._league

    @property
    def division(self) -> idName:
        """division
        Name and id for the teams division

        Keys/Attributes:
        ------------
        Id:     int
        name:   str
        """
        return self._division

    @property
    def venue(self) -> idName:
        """venue
        Name and id for the teams home venue

        Keys/Attributes:
        ------------
        Id:     int
        name:   str
        """
        return self._venue

    @property
    def ranking(self) -> teamRanking:
        """teamRanking Dataclass

        Keys/Attributes:
        ------------
        division:               str
        league:                 str
        wildCard:               str
        overall:                str
        gamesPlayed:            int
        gamesBack:              str
        wildCardGamesBack:      str
        leagueGamesBack:        str
        springLeagueGamesBack:  str
        overallGamesBack:       str
        divisionGamesBack:      str
        conferenceGamesBack:    str
        """
        return self._ranking

    @property
    def leagueRecord(self) -> leagueRecord:
        """LeagueRecord dataclass

        Keys/Attributes:
        ------------
        wins:   int
        losses: int
        ties:   int
        pct:    str
        """
        return self._leagueRecord

    @property
    def splitRecords(self) -> splitRecord:
        """splitRecords

        Split records Groups:
        ------------
        home:           splitRecordData
        away:           splitRecordData
        left:           splitRecordData
        right:          splitRecordData
        leftHome:       splitRecordData
        leftAway:       splitRecordData
        rightHome:      splitRecordData
        rightAway:      splitRecordData
        lastTen:        splitRecordData
        extraInning:    splitRecordData
        oneRun:         splitRecordData
        winners:        splitRecordData
        day:            splitRecordData
        night:          splitRecordData
        grass:          splitRecordData
        turf:           splitRecordData

        splitRecordData Keys/Attributes:
        ------------
        wins:   int
        losses: int
        pct:    str

        Usage:
        ------------
        extraInning.wins
        """
        return self._splitRecords

    @property
    def record(self) -> teamRecord:
        """record  teamRecord dataClass
        Team records for season

        Keys/Attributes:
        ------------
        runsAllowed:        int
        runsScored:         int
        wins:               int
        losses:             int
        runDifferential:    int
        winningPercentage:  str
        """
        return self._record

    @property
    def stats(self) -> teamStats:
        """stats teamStats dataClass

        Keys/Attributes:
        ------------
        season_hitting:             dict
        season_pitching:            dict
        season_fielding:            dict
        seasonAdvanced_hitting:     dict
        seasonAdvanced_pitching:    dict
        seasonAdvanced_fielding:    dict
        career_hitting:             dict
        career_pitching:            dict
        career_fielding:            dict
        careerAdvanced_hitting:     dict
        careerAdvanced_pitching:    dict
        careerAdvanced_fielding:    dict
        """
        return self._stats
