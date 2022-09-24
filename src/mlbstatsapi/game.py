import requests
from dataclasses import dataclass, asdict
from typing import Union

from .team import TeamName
from .person import Position as PersonPosition


@dataclass(frozen=True)
class NameAndId:
    __slots__ = ['Id','name']
    Id: int
    name: str

    def __str__(self) -> str:
        return f'{self.name}'

    def __repr__(self) -> str:
        return f'{self.name}'

    @property
    def id(self):
        return self.Id

    def asdict(self):
        return asdict(self)

@dataclass(frozen=True)
class GameTime:
    __slots__ = ['dateTime','originalDate','officialDate','dayNight','time','ampm']
    dateTime: str
    originalDate: str
    officialDate: str
    dayNight: str
    time: str
    ampm: str

    def __str__(self) -> str:
        return f'{self.officialDate} {self.time} {self.ampm}'

    def __repr__(self) -> str:
        return f'{self.officialDate} {self.time} {self.ampm}'

    def asdict(self):
        return asdict(self)

@dataclass(frozen=True)
class Status:
    __slots__ = ['abstractGameState','codedGameState','detailedState','statusCode',
                'startTimeTBD','abstractGameCode']
    abstractGameState: str
    codedGameState: str
    detailedState: str
    statusCode: str
    startTimeTBD: bool
    abstractGameCode: str

    def __str__(self) -> str:
        return f'{self.abstractGameState}: {self.detailedState}'

    def __repr__(self) -> str:
        return f'{self.abstractGameState}: {self.detailedState}'

    def asdict(self):
        return asdict(self)

@dataclass(frozen=True)
class Venue:
    __slots__ = ['venueId','name','address1','address2','city','state','stateAbbrev',
                'country','latitude','longitude','timeZone','capacity','turfType',
                'roofType','leftLine','leftCenter','center','rightCenter','rightLine']
    venueId: int
    name: str

    address1: str
    address2: str
    city: str
    state: str
    stateAbbrev: str
    country: str
    latitude: float
    longitude: float

    timeZone: str

    capacity: int
    turfType: str
    roofType: str
    leftLine: int
    leftCenter: int
    center: int
    rightCenter: int
    rightLine: int

    def __str__(self) -> str:
        return str(self.name)

    def __repr__(self) -> str:
        return str(self.name)

    @property
    def id(self):
        return self.venueId

    def asdict(self):
        return asdict(self)

@dataclass(frozen=True)
class Weather:
    __slots__ = ['condition','temp','wind']
    condition: str
    temp: str
    wind: str

    def __str__(self) -> str:
        return str(self.condition)

    def __repr__(self) -> str:
        return str(self.condition)

    def asdict(self):
        return asdict(self)

@dataclass(frozen=True)
class Flags:
    __slots__ = ['noHitter','perfectGame','awayTeamNoHitter',
                'awayTeamPerfectGame','homeTeamNoHitter','homeTeamPerfectGame']
    noHitter: bool
    perfectGame: bool
    awayTeamNoHitter: bool
    awayTeamPerfectGame: bool
    homeTeamNoHitter: bool
    homeTeamPerfectGame: bool

    def asdict(self):
        return asdict(self)


@dataclass(frozen=True)
class HitCoordinate:
    __slots__ = ['x', 'y']
    x: int
    y: int

    def __str__(self):
        return f'{self.x},{self.y}'

    def __repr__(self):
        return f'{self.x},{self.y}'

    def asdict(self):
        return asdict(self)

@dataclass(frozen=True)
class HitData_P:
    __slots__ = ['launchSpeed','launchAngle','totalDistance','trajectory',
                'hardness','location','coordinates']
    launchSpeed: float
    launchAngle: int
    totalDistance: int
    trajectory: str
    hardness: str
    location: str
    coordinates: HitCoordinate

    def asdict(self):
        return asdict(self)


@dataclass(frozen=True)
class PitchBreaks:
    __slots__ = ['breakAngle','breakLength','breakY','spinRate','spinDirection']
    breakAngle: float
    breakLength: float
    breakY: int
    spinRate: int
    spinDirection: int

    def asdict(self):
        return asdict(self)


@dataclass(frozen=True)
class PitchCoordinates:
    __slots__ = ['aY6','aZ','pfxX','pfxZ','pX','pZ','vX0','vY0','vZ0','x','y',
                'x0','y0','z0','aX']
    aY6: float
    aZ: float
    pfxX: float
    pfxZ: float
    pX: float
    pZ: float
    vX0: float
    vY0: float
    vZ0: float
    x: float
    y: float
    x0: float
    y0: float
    z0: float
    aX: float

    def asdict(self):
        return asdict(self)


@dataclass(frozen=True)
class PitchData_P:
    __slots__ = ['startSpeed','endSpeed','strikeZoneTop','strikeZoneBottom',
                'coordinates','breaks','zone','typeConfidence','plateTime',
                'extension']
    startSpeed: float
    endSpeed: float
    strikeZoneTop: float
    strikeZoneBottom: float
    coordinates: PitchCoordinates
    breaks: PitchBreaks
    zone: int
    typeConfidence: float
    plateTime: float
    extension: float

    def asdict(self):
        return asdict(self)


@dataclass(frozen=True)
class Count:
    __slots__ = ['balls','strikes','outs']
    balls: int
    strikes: int
    outs: int

    def __str__(self):
        return f'{self.balls}-{self.strikes}'

    def __repr__(self):
        return f'{self.balls}-{self.strikes}'

    def asdict(self):
        return asdict(self)


@dataclass(frozen=True)
class PitchType:
    __slots__ = ['code','description']
    code: Union[str, None]
    description: Union[str, None]

    def __str__(self):
        return str(self.description)

    def __repr__(self):
        return str(self.description)

    def asdict(self):
        return asdict(self)


@dataclass(frozen=True)
class PlayEvent:
    __slots__ = ['description','event','eventType','code','ballColor','trailColor',
                'isInPlay','isStrike','isBall','hasReview','pitchType','count',
                'pitchData','hitData','index','playId','type','isPitch','pitchNumber',
                'startTime','endTime']
    description: str
    event: Union[str, None]
    eventType: Union[str, None]
    code: Union[str, None]
    ballColor: Union[str, None]
    trailColor: Union[str, None]
    isInPlay: Union[bool, None]
    isStrike: Union[bool, None]
    isBall: Union[bool, None]
    hasReview: bool
    pitchType: PitchType
    count: Count
    pitchData: PitchData_P
    hitData: HitData_P
    index: int
    playId: Union[str, None]
    type: str
    isPitch: bool
    pitchNumber: Union[int, None]
    startTime: str
    endTime: str

    def __str__(self):
        return str(self.description)

    def __repr__(self):
        return str(self.description)

    @property
    def eventNumber(self):
        return self.index

    def asdict(self):
        return asdict(self)


@dataclass(frozen=True)
class Credits_Play:
    __slots__ = ['player','position','credit']
    player: NameAndId
    position: PersonPosition
    credit: str

    def __str__(self):
        return str(self.credit)

    def __repr__(self):
        return str(self.credit)

    def asdict(self):
        return asdict(self)


@dataclass(frozen=True)
class Runners:
    __slots__ = ['originBase','start','end','outBase','isOut','outNumber','event',
                'eventType','movementReason','isScoringEvent','rbi','earned',
                'teamUnearned','playIndex','responsiblePitcher','runner','credits']
    originBase: Union[int, None]
    start: Union[int, None]
    end: Union[int, None]
    outBase: Union[int, None]
    isOut: bool
    outNumber: Union[int, None]
    event: str
    eventType: str
    movementReason: Union[str, None]
    isScoringEvent: bool
    rbi: bool
    earned: bool
    teamUnearned: bool
    playIndex: int
    responsiblePitcher: Union[NameAndId, None]
    runner: Union[NameAndId, None]
    credits: list # List [Credits_Play obj]

    def asdict(self):
        return asdict(self)



@dataclass(frozen=True)
class MatchupSplits:
    __slots__ = ['batter','pitcher','menOnBase']
    batter: str
    pitcher: str
    menOnBase: str

    def __str__(self):
        return f'{self.batter},{self.pitcher},{self.menOnBase}'

    def __repr__(self):
        return f'{self.batter},{self.pitcher},{self.menOnBase}'

    def asdict(self):
        return asdict(self)


@dataclass(frozen=True)
class Matchup_Play:
    __slots__ = ['batter','batSide','pitcher','pitchHand','batterHotColdZones',
                'pitcherHotColdZones','splits']
    batter: NameAndId
    batSide: str
    pitcher: NameAndId
    pitchHand: str
    batterHotColdZones: list
    pitcherHotColdZones: list
    splits: MatchupSplits

    def __str__(self):
        return f'{self.pitcher.name} vs {self.batter.name}'

    def __repr__(self):
        return f'{self.pitcher.name} vs {self.batter.name}'

    def asdict(self):
        return asdict(self)


@dataclass(frozen=True)
class Play:
    __slots__ = ['type','event','eventType','description','rbi','awayScore',
                'homeScore','atBatIndex','halfInning','isTopInning','inning',
                'startTime','endTime','isComplete','isScoringPlay','hasReview',
                'hasOut','captivatingIndex','count','matchup','pitchIndex',
                'actionIndex','runnerIndex','runners','playEvents','playEndTime']
    type: str
    event: str
    eventType: str
    description: str
    rbi: int
    awayScore: int
    homeScore: int
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
    count: Count
    matchup: Matchup_Play
    pitchIndex: list # list[int]
    actionIndex: list # list[int]
    runnerIndex: list # list[int]
    runners: list # list[Runners OBJ}
    playEvents: list # list[PlayEvent OBJ}
    playEndTime: str

    def __str__(self):
        return str(self.description)

    def __repr__(self):
        return str(self.description)

    def asdict(self):
        return asdict(self)


@dataclass(frozen=True)
class Hit_LD:
    __slots__ = ['inning','pitcher','batter','coordinates','type','description']
    inning: int
    pitcher: NameAndId
    batter: NameAndId
    coordinates: HitCoordinate
    type: str
    description: str

    def __str__(self) -> str:
        return str(self.description)

    def __repr__(self) -> str:
        return str(self.description)

    def asdict(self):
        return asdict(self)


@dataclass(frozen=True)
class Inning_LD:
    __slots__ = ['startIndex','endIndex','top','bottom','homeHits','awayHits']
    startIndex: int
    endIndex: int
    top: list # list[int]
    bottom: list # list[int]
    homeHits: list # list[Hit_LD]
    awayHits: list # list[Hit_LD]

    def asdict(self):
        return asdict(self)

@dataclass(frozen=True)
class Fielding:
    __slots__ = ['team','pitcher','catcher','first','second','third','shortstop',
                'left','center','right','batter','onDeck','inHole','battingOrder']
    team: NameAndId
    pitcher: NameAndId
    catcher: NameAndId
    first: NameAndId
    second: NameAndId
    third: NameAndId
    shortstop: NameAndId
    left: NameAndId
    center: NameAndId
    right: NameAndId
    batter: NameAndId
    onDeck: NameAndId
    inHole: NameAndId
    battingOrder: int

    def __str__(self) -> str:
        return str(self.team)

    def __repr__(self) -> str:
        return str(self.team)

    def asdict(self):
        return asdict(self)

@dataclass(frozen=True)
class OnBase:
    __slots__ = ['onBase','onFirst','onSecond','onThird','first','second','third']
    onBase: bool
    onFirst: bool
    onSecond: bool
    onThird: bool
    first: NameAndId
    second: NameAndId
    third: NameAndId

    def __str__(self) -> str:
        return str(self.onBase)

    def __repr__(self) -> str:
        return str(self.onBase)

    def asdict(self):
        return asdict(self)

@dataclass(frozen=True)
class Hitting:
    __slots__ = ['team','battingOrder','batter','onDeck','inHole','pitcher','onBase']
    team: NameAndId
    battingOrder: int
    batter: NameAndId
    onDeck: NameAndId
    inHole: NameAndId
    pitcher: NameAndId
    onBase: OnBase

    def __str__(self) -> str:
        return str(self.team)

    def __repr__(self) -> str:
        return str(self.team)

    def asdict(self):
        return asdict(self)

@dataclass(frozen=True)
class HomeAndAway_ls:
    __slots__ = ['home','away']
    home: int
    away: int

    def asdict(self):
        return asdict(self)

@dataclass(frozen=True)
class LineScore:
    __slots__ = ['currentInning','currentInningOrdinal','inningState','inningHalf',
                'isTopInning','scheduledInnings','innings','fielding','hitting',
                'balls','strikes','outs','runs','hits','errors','leftOnBase']
    currentInning: int
    currentInningOrdinal: str
    inningState: str
    inningHalf: str
    isTopInning: bool
    scheduledInnings: int
    innings: list
    fielding: Fielding
    hitting: Hitting
    balls: int
    strikes: int
    outs: int
    runs: HomeAndAway_ls
    hits: HomeAndAway_ls
    errors: HomeAndAway_ls
    leftOnBase: HomeAndAway_ls

    # def __str__(self) -> str:
    #     return str(self.team)
    #
    # def __repr__(self) -> str:
    #     return str(self.team)

    def asdict(self):
        return asdict(self)


@dataclass(frozen=True)
class Stats_BSHA:
    __slots__ = ['batting','pitching','fielding']
    batting: dict
    pitching: dict
    fielding: dict

    # def __str__(self) -> str:
    #     return str(self.team)
    #
    # def __repr__(self) -> str:
    #     return str(self.team)

    def asdict(self):
        return asdict(self)


@dataclass(frozen=True)
class players_BSHA:
    __slots__ = ['playerId','name','parentTeamId','jerseyNumber','position',
                'gameStats','seasonStats','battingOrder','isCurrentBatter',
                'isCurrentPitcher','isOnBench','isSubstitute']
    playerId: int
    name: str
    parentTeamId: int
    jerseyNumber: str
    position: PersonPosition
    gameStats: Stats_BSHA
    seasonStats: Stats_BSHA
    battingOrder: str
    isCurrentBatter: bool
    isCurrentPitcher: bool
    isOnBench: bool
    isSubstitute: bool

    def __str__(self) -> str:
        return str(self.name)

    def __repr__(self) -> str:
        return str(self.name)

    @property
    def id(self):
        return self.playerId

    def asdict(self):
        return asdict(self)


@dataclass(frozen=True)
class Team_BSHA:
    __slots__ = ['teamId','name','teamStats','players','batters','pitchers',
                'bench','bullpen','battingOrder']
    teamId: int
    name: TeamName
    teamStats: Stats_BSHA
    players: dict # dict{str(id):players_BSHA}
    batters: list # list[int(id)]
    pitchers: list # list[int(id)]
    bench: list # list[int(id)]
    bullpen: list # list[int(id)]
    battingOrder: str

    def __str__(self) -> str:
        return str(self.name)

    def __repr__(self) -> str:
        return str(self.name)

    @property
    def id(self):
        return self.teamId

    def asdict(self):
        return asdict(self)


@dataclass(frozen=True)
class Decisions:
    __slots__ = ['winner','looser','save']
    winner: NameAndId
    looser: NameAndId
    save: NameAndId

    def asdict(self):
        return asdict(self)

class Game():

    def __init__(self, game_pk: int, timecode=None):
        """# Game
        MLB Game instance
        Paramaters
        ----------
        Required:
            game_pk : int or str
                Unique primary key for specific game
        Optonal:
            timecode : str
                specify a value to retrieve a "snapshot" of the game at a specific
                point in time
                Format = "YYYYmmdd_HHMMDD"

        """

        if timecode == '':
            timecode = None
        if timecode is not None and timecode.find('_') == -1:
            timecode = parse(timecode).strftime(r'%Y%m%d_%H%M%S')

        game_url = f'https://statsapi.mlb.com/api/v1.1/game/{game_pk}/feed/live?'

        params = {'timecode':timecode}

        gm = requests.get(game_url,params=params).json()



        self.__gameId = game_pk

        self._raw_game_data = gm

        self.meta = gm['metaData']
        gameData = gm['gameData']
        liveData = gm['liveData']


        # gameData
        # --------
        datetime = gameData['datetime']
        self._datetime = GameTime (
            dateTime = datetime['dateTime'],
            originalDate = datetime['originalDate'],
            officialDate = datetime['officialDate'],
            dayNight = datetime['dayNight'],
            time = datetime['time'],
            ampm = datetime['ampm']
        )

        status = gameData['status']
        self._status = Status (
            abstractGameState = status['abstractGameState'],
            codedGameState = status['codedGameState'],
            detailedState = status['detailedState'],
            statusCode = status['statusCode'],
            startTimeTBD = status['startTimeTBD'],
            abstractGameCode = status['abstractGameCode']
        )

        home = gameData['teams']['home']
        home_name = TeamName (
            Id = home['id'],
            full = home['name'],
            location = home['locationName'],
            franchise = home['franchiseName'],
            club = home['clubName'],
            short = home['shortName'],
            abbreviation = home['abbreviation']
        )

        away = gameData['teams']['away']
        away_name = TeamName (
            Id = away['id'],
            full = away['name'],
            location = away['locationName'],
            franchise = away['franchiseName'],
            club = away['clubName'],
            short = away['shortName'],
            abbreviation = away['abbreviation']
        )

        venue = gameData['venue']
        self._venue = Venue (
            venueId = venue['id'],
            name = venue['name'],

            address1 = venue["location"]['address1'],
            address2 = venue["location"].get('address2',''),
            city = venue["location"]['city'],
            state = venue["location"]['state'],
            stateAbbrev = venue["location"]['stateAbbrev'],
            country = venue["location"]['country'],
            latitude = venue["location"]["defaultCoordinates"]['latitude'],
            longitude = venue["location"]["defaultCoordinates"]['longitude'],

            timeZone = venue["timeZone"]['tz'],

            capacity = venue["fieldInfo"]['capacity'],
            turfType = venue["fieldInfo"]['turfType'],
            roofType = venue["fieldInfo"]['roofType'],
            leftLine = venue["fieldInfo"]['leftLine'],
            leftCenter = venue["fieldInfo"]['leftCenter'],
            center = venue["fieldInfo"]['center'],
            rightCenter = venue["fieldInfo"]['rightCenter'],
            rightLine = venue["fieldInfo"]['rightLine']
        )

        weather = gameData['weather']
        self._weather = Weather (
            condition = weather.get('condition', ''),
            temp = weather.get('temp', ''),
            wind =weather.get('wind', '')
        )

        flags = gameData['flags']
        self._flags = Flags (
            noHitter = flags['noHitter'],
            perfectGame = flags['perfectGame'],
            awayTeamNoHitter = flags['awayTeamNoHitter'],
            awayTeamPerfectGame = flags['awayTeamPerfectGame'],
            homeTeamNoHitter = flags['homeTeamNoHitter'],
            homeTeamPerfectGame = flags['homeTeamPerfectGame']
        )


        # liveData
        # --------

        # Plays
        plays = liveData["plays"]


        # allPlays
        # self._allPlays = plays["allPlays"]
        allPlays = plays["allPlays"]
        self._allPlays = []

        for play in allPlays:

            runners_P = []

            for runer_p in play.get('runners', []):

                play_credits = []

                for credit in runer_p['credits']:
                    play_credits.append(Credits_Play(
                        player = NameAndId (
                            Id = credit['player']['id'],
                            name = credit['player'].get('fullName', None)
                        ),
                        position = PersonPosition (
                            code = credit['position']['code'],
                            name = credit['position']['name'],
                            type = credit['position']['type'],
                            abbreviation = credit['position']['abbreviation']
                        ),
                        credit = credit['credit']
                    ))

                if runer_p['details']['responsiblePitcher'] == None:
                    responsiblePitcher_p = None
                else:
                    responsiblePitcher_p = NameAndId (
                        Id = runer_p['details']['responsiblePitcher'].get('id', None),
                        name = runer_p['details']['responsiblePitcher'].get('fullName', None)
                    )

                runners_P.append(Runners (
                    originBase = runer_p['movement']['originBase'],
                    start = runer_p['movement']['start'],
                    end = runer_p['movement']['end'],
                    outBase = runer_p['movement']['outBase'],
                    isOut = runer_p['movement']['isOut'],
                    outNumber = runer_p['movement']['outNumber'],

                    event = runer_p['details']['event'],
                    eventType = runer_p['details']['eventType'],
                    movementReason = runer_p['details']['movementReason'],
                    isScoringEvent = runer_p['details']['isScoringEvent'],
                    rbi = runer_p['details']['rbi'],
                    earned = runer_p['details']['earned'],
                    teamUnearned = runer_p['details']['teamUnearned'],
                    playIndex = runer_p['details']['playIndex'],

                    responsiblePitcher = responsiblePitcher_p,

                    runner = NameAndId (
                        Id = runer_p['details']['runner']['id'],
                        name = runer_p['details']['runner']['fullName']
                    ),

                    credits = play_credits
                ))




            playEvents_P = []

            for playEvent_cp in play.get('playEvents', []):

                pE_CP_pitchData = playEvent_cp.get('pitchData', {})
                pE_CP_pitchData_coordinates = pE_CP_pitchData.get('coordinates', {})
                pE_CP_pitchData_breaks = pE_CP_pitchData.get('breaks', {})

                pE_CP_hitData = playEvent_cp.get('hitData', {})

                playEvents_P.append(PlayEvent (
                    # call()
                    description = playEvent_cp['details']['description'],
                    event = playEvent_cp['details'].get('event', None),
                    eventType = playEvent_cp['details'].get('eventType', None),
                    code = playEvent_cp['details'].get('code', None),
                    ballColor = playEvent_cp['details'].get('ballColor', None),
                    trailColor = playEvent_cp['details'].get('trailColor', None),
                    isInPlay = playEvent_cp['details'].get('isInPlay', None),
                    isStrike = playEvent_cp['details'].get('isStrike', None),
                    isBall = playEvent_cp['details'].get('isBall', None),
                    hasReview = playEvent_cp['details']['hasReview'],
                    pitchType = PitchType (
                        code = playEvent_cp['details'].get('type', {}).get('code', None),
                        description = playEvent_cp['details'].get('type', {}).get('description', None)
                    ),

                    count = Count (
                        balls = playEvent_cp['count']['balls'],
                        strikes = playEvent_cp['count']['strikes'],
                        outs = playEvent_cp['count']['outs']
                    ),

                    pitchData = PitchData_P (
                        startSpeed = pE_CP_pitchData.get('startSpeed', 0),
                        endSpeed = pE_CP_pitchData.get('endSpeed', 0),
                        strikeZoneTop = pE_CP_pitchData.get('strikeZoneTop', 0),
                        strikeZoneBottom = pE_CP_pitchData.get('strikeZoneBottom', 0),
                        coordinates = PitchCoordinates (
                            aY6 = pE_CP_pitchData_coordinates.get('aY6', 0),
                            aZ = pE_CP_pitchData_coordinates.get('aZ', 0),
                            pfxX = pE_CP_pitchData_coordinates.get('pfxX', 0),
                            pfxZ = pE_CP_pitchData_coordinates.get('pfxZ', 0),
                            pX = pE_CP_pitchData_coordinates.get('pX', 0),
                            pZ = pE_CP_pitchData_coordinates.get('pZ', 0),
                            vX0 = pE_CP_pitchData_coordinates.get('vX0', 0),
                            vY0 = pE_CP_pitchData_coordinates.get('vY0', 0),
                            vZ0 = pE_CP_pitchData_coordinates.get('vZ0', 0),
                            x = pE_CP_pitchData_coordinates.get('x', 0),
                            y = pE_CP_pitchData_coordinates.get('y', 0),
                            x0 = pE_CP_pitchData_coordinates.get('x0', 0),
                            y0 = pE_CP_pitchData_coordinates.get('y0', 0),
                            z0 = pE_CP_pitchData_coordinates.get('z0', 0),
                            aX = pE_CP_pitchData_coordinates.get('aX', 0)
                        ),
                        breaks = PitchBreaks (
                            breakAngle = pE_CP_pitchData_breaks.get('breakAngle', 0),
                            breakLength = pE_CP_pitchData_breaks.get('breakLength', 0),
                            breakY = pE_CP_pitchData_breaks.get('breakY', 0),
                            spinRate = pE_CP_pitchData_breaks.get('spinRate', 0),
                            spinDirection = pE_CP_pitchData_breaks.get('spinDirection', 0)
                        ),
                        zone = pE_CP_pitchData.get('zone', 0),
                        typeConfidence = pE_CP_pitchData.get('typeConfidence', 0),
                        plateTime = pE_CP_pitchData.get('plateTime', 0),
                        extension = pE_CP_pitchData.get('extension', 0)
                    ),

                    hitData = HitData_P (
                        launchSpeed = pE_CP_hitData.get('launchSpeed', 0),
                        launchAngle = pE_CP_hitData.get('launchAngle', 0),
                        totalDistance = pE_CP_hitData.get('totalDistance', 0),
                        trajectory = pE_CP_hitData.get('trajectory', None),
                        hardness = pE_CP_hitData.get('hardness', None),
                        location = pE_CP_hitData.get('location', None),
                        coordinates = HitCoordinate (
                            x = pE_CP_hitData.get('coordinates', {}).get('x', 0),
                            y = pE_CP_hitData.get('coordinates', {}).get('y', 0)
                        )
                    ),

                    index = playEvent_cp['index'],
                    playId = playEvent_cp.get('playId', None),
                    type = playEvent_cp['type'],
                    isPitch = playEvent_cp['isPitch'],
                    pitchNumber = playEvent_cp.get('pitchNumber', None),
                    startTime = playEvent_cp['startTime'],
                    endTime = playEvent_cp['endTime']
                ))



            result_p = play.get('result', {})
            about_p = play.get('about', {})
            matchup_p = play.get('matchup', {})

            self._allPlays.append( Play (
                type = result_p.get('type', 'none'),
                event = result_p.get('event', 'none'),
                eventType = result_p.get('eventType', 'none'),
                description = result_p.get('description', 'none'),
                rbi = result_p.get('rbi', 0),
                awayScore = result_p.get('awayScore', 0),
                homeScore = result_p.get('homeScore', 0),

                atBatIndex = about_p.get('atBatIndex', 0),
                halfInning = about_p.get('halfInning', 'none'),
                isTopInning = about_p.get('isTopInning', True),
                inning = about_p.get('inning', 0),
                startTime = about_p.get('startTime', 'none'),
                endTime = about_p.get('endTime', 'none'),
                isComplete = about_p.get('isComplete', False),
                isScoringPlay = about_p.get('isScoringPlay', False),
                hasReview = about_p.get('hasReview', False),
                hasOut = about_p.get('hasOut', False),
                captivatingIndex = about_p.get('captivatingIndex', 0),

                count = Count (
                    balls = play.get('count', {}).get('balls', 0),
                    strikes = play.get('count', {}).get('strikes', 0),
                    outs = play.get('count', {}).get('outs', 0)
                ),

                matchup = Matchup_Play (
                    batter = NameAndId (
                        Id = matchup_p.get('batter', {}).get('id', 0),
                        name = matchup_p.get('batter', {}).get('fullName', 'none')
                    ),
                    batSide = matchup_p.get('batSide', {}).get('description', 'None'),
                    pitcher = NameAndId (
                        Id = matchup_p.get('pitcher', {}).get('id', 0),
                        name = matchup_p.get('pitcher', {}).get('fullName', 'none')
                    ),
                    pitchHand = matchup_p.get('pitchHand', {}).get('description', 'None'),
                    batterHotColdZones = matchup_p.get('batterHotColdZones', []),
                    pitcherHotColdZones = matchup_p.get('pitcherHotColdZones', []),
                    splits = MatchupSplits (
                        batter = matchup_p.get('splits', {}).get('batter', 'none'),
                        pitcher = matchup_p.get('splits', {}).get('pitcher', 'none'),
                        menOnBase = matchup_p.get('splits', {}).get('menOnBase', 'none')
                    )
                ),

                pitchIndex = play.get('pitchIndex', []),
                actionIndex = play.get('actionIndex', []),
                runnerIndex = play.get('runnerIndex', []),
                runners = runners_P,
                playEvents = playEvents_P,
                playEndTime = play.get('playEndTime', 'none')
            )
        )


        # currentPlay
        currentPlay = plays.get('currentPlay', {})

        runners_CP = []

        for runer_cp in currentPlay.get('runners', []):

            currentPlay_credits = []

            for credit in runer_cp['credits']:
                currentPlay_credits.append(Credits_Play(
                    player = NameAndId (
                        Id = credit['player']['id'],
                        name = credit['player'].get('fullName', None)
                    ),
                    position = PersonPosition (
                        code = credit['position']['code'],
                        name = credit['position']['name'],
                        type = credit['position']['type'],
                        abbreviation = credit['position']['abbreviation']
                    ),
                    credit = credit['credit']
                ))

            if runer_p['details']['responsiblePitcher'] == None:
                responsiblePitcher_p = None
            else:
                responsiblePitcher_p = NameAndId (
                    Id = runer_p['details']['responsiblePitcher'].get('id', None),
                    name = runer_p['details']['responsiblePitcher'].get('fullName', None)
                )

            runners_CP.append(Runners (
                originBase = runer_cp['movement']['originBase'],
                start = runer_cp['movement']['start'],
                end = runer_cp['movement']['end'],
                outBase = runer_cp['movement']['outBase'],
                isOut = runer_cp['movement']['isOut'],
                outNumber = runer_cp['movement']['outNumber'],

                event = runer_cp['details']['event'],
                eventType = runer_cp['details']['eventType'],
                movementReason = runer_cp['details']['movementReason'],
                isScoringEvent = runer_cp['details']['isScoringEvent'],
                rbi = runer_cp['details']['rbi'],
                earned = runer_cp['details']['earned'],
                teamUnearned = runer_cp['details']['teamUnearned'],
                playIndex = runer_cp['details']['playIndex'],

                responsiblePitcher = responsiblePitcher_p,

                runner = NameAndId (
                    Id = runer_cp['details']['runner']['id'],
                    name = runer_cp['details']['runner']['fullName']
                ),

                credits = currentPlay_credits
            ))




        playEvents_CP = []

        for playEvent_cp in currentPlay.get('playEvents', []):

            pE_CP_pitchData = playEvent_cp.get('pitchData', {})
            pE_CP_pitchData_coordinates = pE_CP_pitchData.get('coordinates', {})
            pE_CP_pitchData_breaks = pE_CP_pitchData.get('breaks', {})

            pE_CP_hitData = playEvent_cp.get('hitData', {})

            playEvents_CP.append(PlayEvent (
                # call()
                description = playEvent_cp['details']['description'],
                event = playEvent_cp['details'].get('event', None),
                eventType = playEvent_cp['details'].get('eventType', None),
                code = playEvent_cp['details'].get('code', None),
                ballColor = playEvent_cp['details'].get('ballColor', None),
                trailColor = playEvent_cp['details'].get('trailColor', None),
                isInPlay = playEvent_cp['details'].get('isInPlay', None),
                isStrike = playEvent_cp['details'].get('isStrike', None),
                isBall = playEvent_cp['details'].get('isBall', None),
                hasReview = playEvent_cp['details']['hasReview'],
                pitchType = PitchType (
                    code = playEvent_cp['details'].get('type', {}).get('code', None),
                    description = playEvent_cp['details'].get('type', {}).get('description', None)
                ),

                count = Count (
                    balls = playEvent_cp['count']['balls'],
                    strikes = playEvent_cp['count']['strikes'],
                    outs = playEvent_cp['count']['outs']
                ),

                pitchData = PitchData_P (
                    startSpeed = pE_CP_pitchData.get('startSpeed', 0),
                    endSpeed = pE_CP_pitchData.get('endSpeed', 0),
                    strikeZoneTop = pE_CP_pitchData.get('strikeZoneTop', 0),
                    strikeZoneBottom = pE_CP_pitchData.get('strikeZoneBottom', 0),
                    coordinates = PitchCoordinates (
                        aY6 = pE_CP_pitchData_coordinates.get('aY6', 0),
                        aZ = pE_CP_pitchData_coordinates.get('aZ', 0),
                        pfxX = pE_CP_pitchData_coordinates.get('pfxX', 0),
                        pfxZ = pE_CP_pitchData_coordinates.get('pfxZ', 0),
                        pX = pE_CP_pitchData_coordinates.get('pX', 0),
                        pZ = pE_CP_pitchData_coordinates.get('pZ', 0),
                        vX0 = pE_CP_pitchData_coordinates.get('vX0', 0),
                        vY0 = pE_CP_pitchData_coordinates.get('vY0', 0),
                        vZ0 = pE_CP_pitchData_coordinates.get('vZ0', 0),
                        x = pE_CP_pitchData_coordinates.get('x', 0),
                        y = pE_CP_pitchData_coordinates.get('y', 0),
                        x0 = pE_CP_pitchData_coordinates.get('x0', 0),
                        y0 = pE_CP_pitchData_coordinates.get('y0', 0),
                        z0 = pE_CP_pitchData_coordinates.get('z0', 0),
                        aX = pE_CP_pitchData_coordinates.get('aX', 0)
                    ),
                    breaks = PitchBreaks (
                        breakAngle = pE_CP_pitchData_breaks.get('breakAngle', 0),
                        breakLength = pE_CP_pitchData_breaks.get('breakLength', 0),
                        breakY = pE_CP_pitchData_breaks.get('breakY', 0),
                        spinRate = pE_CP_pitchData_breaks.get('spinRate', 0),
                        spinDirection = pE_CP_pitchData_breaks.get('spinDirection', 0)
                    ),
                    zone = pE_CP_pitchData.get('zone', 0),
                    typeConfidence = pE_CP_pitchData.get('typeConfidence', 0),
                    plateTime = pE_CP_pitchData.get('plateTime', 0),
                    extension = pE_CP_pitchData.get('extension', 0)
                ),

                hitData = HitData_P (
                    launchSpeed = pE_CP_hitData.get('launchSpeed', 0),
                    launchAngle = pE_CP_hitData.get('launchAngle', 0),
                    totalDistance = pE_CP_hitData.get('totalDistance', 0),
                    trajectory = pE_CP_hitData.get('trajectory', None),
                    hardness = pE_CP_hitData.get('hardness', None),
                    location = pE_CP_hitData.get('location', None),
                    coordinates = HitCoordinate (
                        x = pE_CP_hitData.get('coordinates', {}).get('x', 0),
                        y = pE_CP_hitData.get('coordinates', {}).get('y', 0)
                    )
                ),

                index = playEvent_cp['index'],
                playId = playEvent_cp.get('playId', None),
                type = playEvent_cp['type'],
                isPitch = playEvent_cp['isPitch'],
                pitchNumber = playEvent_cp.get('pitchNumber', None),
                startTime = playEvent_cp['startTime'],
                endTime = playEvent_cp['endTime']
            ))



        result_cp = currentPlay.get('result', {})
        about_cp = currentPlay.get('about', {})
        matchup_cp = currentPlay.get('matchup', {})

        self._currentPlay = Play (
            type = result_cp.get('type', 'none'),
            event = result_cp.get('event', 'none'),
            eventType = result_cp.get('eventType', 'none'),
            description = result_cp.get('description', 'none'),
            rbi = result_cp.get('rbi', 0),
            awayScore = result_cp.get('awayScore', 0),
            homeScore = result_cp.get('homeScore', 0),

            atBatIndex = about_cp.get('atBatIndex', 0),
            halfInning = about_cp.get('halfInning', 'none'),
            isTopInning = about_cp.get('isTopInning', True),
            inning = about_cp.get('inning', 0),
            startTime = about_cp.get('startTime', 'none'),
            endTime = about_cp.get('endTime', 'none'),
            isComplete = about_cp.get('isComplete', False),
            isScoringPlay = about_cp.get('isScoringPlay', False),
            hasReview = about_cp.get('hasReview', False),
            hasOut = about_cp.get('hasOut', False),
            captivatingIndex = about_cp.get('captivatingIndex', 0),

            count = Count (
                balls = currentPlay.get('count', {}).get('balls', 0),
                strikes = currentPlay.get('count', {}).get('strikes', 0),
                outs = currentPlay.get('count', {}).get('outs', 0)
            ),

            matchup = Matchup_Play (
                batter = NameAndId (
                    Id = matchup_cp.get('batter', {}).get('id', 0),
                    name = matchup_cp.get('batter', {}).get('fullName', 'none')
                ),
                batSide = matchup_cp.get('batSide', {}).get('description', 'None'),
                pitcher = NameAndId (
                    Id = matchup_cp.get('pitcher', {}).get('id', 0),
                    name = matchup_cp.get('pitcher', {}).get('fullName', 'none')
                ),
                pitchHand = matchup_cp.get('pitchHand', {}).get('description', 'None'),
                batterHotColdZones = matchup_cp.get('batterHotColdZones', []),
                pitcherHotColdZones = matchup_cp.get('pitcherHotColdZones', []),
                splits = MatchupSplits (
                    batter = matchup_cp.get('splits', {}).get('batter', 'none'),
                    pitcher = matchup_cp.get('splits', {}).get('pitcher', 'none'),
                    menOnBase = matchup_cp.get('splits', {}).get('menOnBase', 'none')
                )
            ),

            pitchIndex = currentPlay.get('pitchIndex', []),
            actionIndex = currentPlay.get('actionIndex', []),
            runnerIndex = currentPlay.get('runnerIndex', []),
            runners = runners_CP,
            playEvents = playEvents_CP,
            playEndTime = currentPlay.get('playEndTime', 'none')
        )



        # scoringPlays
        self._scoringPlays = plays.get('scoringPlays', [])

        # playsByInning
        self._playsByInning = []

        for inning in plays["playsByInning"]:

            hits_home = []
            hits_away = []

            for hit in inning["hits"]["home"]:
                hit = Hit_LD (
                    inning = hit["inning"],
                    pitcher = NameAndId (
                        Id = hit["pitcher"]["id"],
                        name = hit["pitcher"]["fullName"]
                    ),
                    batter = NameAndId (
                        Id = hit["batter"]["id"],
                        name = hit["batter"]["fullName"]
                    ),
                    coordinates = HitCoordinate (
                        x = hit["coordinates"]["x"],
                        y = hit["coordinates"]["y"]
                    ),
                    type = hit["type"],
                    description = hit["description"]

                )
                hits_home.append(hit)

            for hit in inning["hits"]["away"]:
                hit = Hit_LD (
                    inning = hit["inning"],
                    pitcher = NameAndId (
                        Id = hit["pitcher"]["id"],
                        name = hit["pitcher"]["fullName"]
                    ),
                    batter = NameAndId (
                        Id = hit["batter"]["id"],
                        name = hit["batter"]["fullName"]
                    ),
                    coordinates = HitCoordinate (
                        x = hit["coordinates"]["x"],
                        y = hit["coordinates"]["y"]
                    ),
                    type = hit["type"],
                    description = hit["description"]

                )
                hits_away.append(hit)

            inningInfo = Inning_LD (
                startIndex = inning["startIndex"],
                endIndex = inning["endIndex"],
                top = inning["top"],
                bottom = inning["bottom"],
                homeHits = hits_home,
                awayHits = hits_away,
            )

            self._playsByInning.append(inningInfo)



        # LineScore
        lineScore = liveData["linescore"]
        fielding = lineScore.get("defense", {})
        hitting = lineScore.get("offense", {})
        fBase = hitting.get('first', {})
        sBase = hitting.get('second', {})
        tBase = hitting.get('third', {})

        if not fBase:
            fBaseB = False
        else:
            fBaseB = True

        if not sBase:
            sBaseB = False
        else:
            sBaseB = True

        if not tBase:
            tBaseB = False
        else:
            tBaseB = True

        if fBaseB or sBaseB or tBaseB:
            onBaseB = True
        else:
            onBaseB = False


        self._lineScore = LineScore (
            currentInning = lineScore.get('currentInning', 0),
            currentInningOrdinal = lineScore.get('currentInningOrdinal', ''),
            inningState = lineScore.get('inningState', 'None'),
            inningHalf = lineScore.get('inningHalf', 'None'),
            isTopInning = lineScore.get('isTopInning', False),
            scheduledInnings = lineScore.get('scheduledInnings', 9),
            innings = lineScore.get('innings', []),
            fielding = Fielding (
                team = NameAndId (
                    Id = fielding.get('team', {}).get('id'),
                    name = fielding.get('team', {}).get('name', '')
                ),
                pitcher = NameAndId (
                    Id = fielding.get('pitcher', {}).get('id'),
                    name = fielding.get('pitcher', {}).get('fullName', '')
                ),
                catcher = NameAndId (
                    Id = fielding.get('catcher', {}).get('id'),
                    name = fielding.get('catcher', {}).get('fullName', '')
                ),
                first = NameAndId (
                    Id = fielding.get('first', {}).get('id'),
                    name = fielding.get('first', {}).get('fullName', '')
                ),
                second = NameAndId (
                    Id = fielding.get('second', {}).get('id'),
                    name = fielding.get('second', {}).get('fullName', '')
                ),
                third = NameAndId (
                    Id = fielding.get('third', {}).get('id'),
                    name = fielding.get('third', {}).get('fullName', '')
                ),
                shortstop = NameAndId (
                    Id = fielding.get('shortstop', {}).get('id'),
                    name = fielding.get('shortstop', {}).get('fullName', '')
                ),
                left = NameAndId (
                    Id = fielding.get('left', {}).get('id'),
                    name = fielding.get('left', {}).get('fullName', '')
                ),
                center = NameAndId (
                    Id = fielding.get('center', {}).get('id'),
                    name = fielding.get('center', {}).get('fullName', '')
                ),
                right = NameAndId (
                    Id = fielding.get('right', {}).get('id'),
                    name = fielding.get('right', {}).get('fullName', '')
                ),
                batter = NameAndId (
                    Id = fielding.get('batter', {}).get('id'),
                    name = fielding.get('batter', {}).get('fullName', '')
                ),
                onDeck = NameAndId (
                    Id = fielding.get('onDeck', {}).get('id'),
                    name = fielding.get('onDeck', {}).get('fullName', '')
                ),
                inHole = NameAndId (
                    Id = fielding.get('inHole', {}).get('id'),
                    name = fielding.get('inHole', {}).get('fullName', '')
                ),
                battingOrder = fielding.get('battingOrder')
            ),
            hitting = Hitting (
                team = NameAndId (
                    Id = hitting.get('team', {}).get('id'),
                    name = hitting.get('team', {}).get('name', '')
                ),
                battingOrder = hitting.get('battingOrder'),
                batter = NameAndId (
                    Id = hitting.get('batter', {}).get('id'),
                    name = hitting.get('batter', {}).get('fullName', '')
                ),
                onDeck = NameAndId (
                    Id = hitting.get('onDeck', {}).get('id'),
                    name = hitting.get('onDeck', {}).get('fullName', '')
                ),
                inHole = NameAndId (
                    Id = hitting.get('inHole', {}).get('id'),
                    name = hitting.get('inHole', {}).get('fullName', '')
                ),
                pitcher = NameAndId (
                    Id = hitting.get('pitcher', {}).get('id'),
                    name = hitting.get('pitcher', {}).get('fullName', '')
                ),
                onBase = OnBase (
                    onBase = onBaseB,
                    onFirst = fBaseB,
                    onSecond = sBaseB,
                    onThird = tBaseB,
                    first = NameAndId (
                        Id = fBase.get('id'),
                        name = fBase.get('fullName')
                    ),
                    second = NameAndId (
                        Id = sBase.get('id'),
                        name = sBase.get('fullName')
                    ),
                    third = NameAndId (
                        Id = tBase.get('id'),
                        name = tBase.get('fullName')
                    )
                )
            ),
            balls = lineScore.get('balls', 0),
            strikes = lineScore.get('strikes', 0),
            outs = lineScore.get('outs', 0),
            runs = HomeAndAway_ls (
                home = lineScore.get('teams', {}).get('home', {}).get('runs'),
                away = lineScore.get('teams', {}).get('away', {}).get('runs')
            ),
            hits = HomeAndAway_ls (
                home = lineScore.get('teams', {}).get('home', {}).get('hits'),
                away = lineScore.get('teams', {}).get('away', {}).get('hits')
            ),
            errors = HomeAndAway_ls (
                home = lineScore.get('teams', {}).get('home', {}).get('errors'),
                away = lineScore.get('teams', {}).get('away', {}).get('errors')
            ),
            leftOnBase = HomeAndAway_ls (
                home = lineScore.get('teams', {}).get('home', {}).get('leftOnBase'),
                away = lineScore.get('teams', {}).get('away', {}).get('leftOnBase')
            )
        )

        # BoxScore
        boxScore = liveData["boxscore"]
        BS_homeTeam = boxScore['teams']['home']
        BS_awayTeam = boxScore['teams']['away']

        homePlayerDict = {}
        awayPlayerDict = {}

        for homePlayer in BS_homeTeam["players"].keys():
            if homePlayer[:2] == "ID":
                pIdKey = homePlayer[2:]
            else:
                pIdKey = homePlayer

            value = BS_homeTeam["players"][homePlayer]

            homePlayerDict["pIdKey"] = players_BSHA (
                playerId = value["person"]["id"],
                name = value["person"]["fullName"],
                parentTeamId = value["parentTeamId"],
                jerseyNumber = value.get("jerseyNumber"),
                position = PersonPosition (
                    code = value["position"]["code"],
                    name = value["position"]["name"],
                    type = value["position"]["type"],
                    abbreviation = value["position"]["abbreviation"]
                ),
                gameStats = Stats_BSHA (
                    batting = value["stats"]["batting"],
                    pitching = value["stats"]["pitching"],
                    fielding = value["stats"]["fielding"]
                ),
                seasonStats = Stats_BSHA (
                    batting = value["seasonStats"]["batting"],
                    pitching = value["seasonStats"]["pitching"],
                    fielding = value["seasonStats"]["fielding"]
                ),
                battingOrder = value.get("battingOrder"),
                isCurrentBatter = value["gameStatus"]["isCurrentBatter"],
                isCurrentPitcher = value["gameStatus"]["isCurrentPitcher"],
                isOnBench = value["gameStatus"]["isOnBench"],
                isSubstitute = value["gameStatus"]["isSubstitute"]
            )

        for awayPlayer in BS_awayTeam["players"].keys():
            if awayPlayer[:2] == "ID":
                pIdKey = awayPlayer[2:]
            else:
                pIdKey = awayPlayer

            value = BS_awayTeam["players"][awayPlayer]

            awayPlayerDict["pIdKey"] = players_BSHA (
                playerId = value["person"]["id"],
                name = value["person"]["fullName"],
                parentTeamId = value["parentTeamId"],
                jerseyNumber = value.get("jerseyNumber"),
                position = PersonPosition (
                    code = value["position"]["code"],
                    name = value["position"]["name"],
                    type = value["position"]["type"],
                    abbreviation = value["position"]["abbreviation"]
                ),
                gameStats = Stats_BSHA (
                    batting = value["stats"]["batting"],
                    pitching = value["stats"]["pitching"],
                    fielding = value["stats"]["fielding"]
                ),
                seasonStats = Stats_BSHA (
                    batting = value["seasonStats"]["batting"],
                    pitching = value["seasonStats"]["pitching"],
                    fielding = value["seasonStats"]["fielding"]
                ),
                battingOrder = value.get("battingOrder"),
                isCurrentBatter = value["gameStatus"]["isCurrentBatter"],
                isCurrentPitcher = value["gameStatus"]["isCurrentPitcher"],
                isOnBench = value["gameStatus"]["isOnBench"],
                isSubstitute = value["gameStatus"]["isSubstitute"]
            )

        self._homeTeam = Team_BSHA (
            teamId = BS_homeTeam["team"]["id"],
            name = home_name,
            teamStats = Stats_BSHA (
                batting = BS_homeTeam['teamStats']['batting'],
                pitching = BS_homeTeam['teamStats']['pitching'],
                fielding = BS_homeTeam['teamStats']['fielding']
            ),
            players = homePlayerDict,
            # playerStats
            batters = BS_homeTeam['batters'],
            pitchers = BS_homeTeam['pitchers'],
            bench = BS_homeTeam['bench'],
            bullpen = BS_homeTeam['bullpen'],
            battingOrder = BS_homeTeam['battingOrder']
        )

        self._awayTeam = Team_BSHA (
            teamId = BS_awayTeam["team"]["id"],
            name = away_name,
            teamStats = Stats_BSHA (
                batting = BS_awayTeam['teamStats']['batting'],
                pitching = BS_awayTeam['teamStats']['pitching'],
                fielding = BS_awayTeam['teamStats']['fielding']
            ),
            players = awayPlayerDict,
            # playerStats
            batters = BS_awayTeam['batters'],
            pitchers = BS_awayTeam['pitchers'],
            bench = BS_awayTeam['bench'],
            bullpen = BS_awayTeam['bullpen'],
            battingOrder = BS_awayTeam['battingOrder']
        )



        # decisions
        decisions = liveData.get('decisions', {})

        self._decisions = Decisions (
            winner = NameAndId (
                Id = decisions.get('winner', {}).get('id'),
                name = decisions.get('winner', {}).get('fullName', '')
            ),
            looser = NameAndId (
                Id = decisions.get('looser', {}).get('id'),
                name = decisions.get('looser', {}).get('fullName', '')
            ),
            save = NameAndId (
                Id = decisions.get('save', {}).get('id'),
                name = decisions.get('save', {}).get('fullName', '')
            )
        )



    @property
    def gameId(self) -> int:
        """game Pk ID number"""
        return self.__gameId

    @property
    def datetime(self) -> GameTime:
        """datetime dataclass

        Keys/Attributes:
        ------------
        dateTime:       str
        originalDate:   str
        officialDate:   str
        dayNight:       str
        time:           str
        ampm:           str
        """
        return self._datetime

    @property
    def status(self) -> Status:
        """status dataclass

        Keys/Attributes:
        ------------
        abstractGameState:  str
        codedGameState:     str
        detailedState:      str
        statusCode:         str
        startTimeTBD:       bool
        abstractGameCode:   str
        """
        return self._status

    @property
    def venue(self) -> Venue:
        """venue dataclass

        Keys/Attributes:
        ------------
        venueId:        int
        name:           str

        address1:       str
        address2:       str
        city:           str
        state:          str
        stateAbbrev:    str
        country:        str
        latitude:       float
        longitude:      float

        timeZone:       str

        capacity:       int
        turfType:       str
        roofType:       str
        leftLine:       int
        leftCenter:     int
        center:         int
        rightCenter:    int
        rightLine:      int
        """
        return self._venue

    @property
    def weather(self) -> Weather:
        """weather dataclass

        Keys/Attributes:
        ------------
        condition:  str
        temp:       str
        wind:       str
        """
        return self._weather

    @property
    def flags(self) -> Flags:
        """flags dataclass

        Keys/Attributes:
        ------------
        noHitter:               bool
        perfectGame:            bool
        awayTeamNoHitter:       bool
        awayTeamPerfectGame:    bool
        homeTeamNoHitter:       bool
        homeTeamPerfectGame:    bool
        """
        return self._flags

    @property
    def allPlays(self):
        """allPlays

        List [ Play ]


        Play dataclass

        Keys/Attributes:
        ------------
        type:               str
        event:              str
        eventType:          str
        description:        str
        rbi:                int
        awayScore:          int
        homeScore:          int
        atBatIndex:         int
        halfInning:         str
        isTopInning:        bool
        inning:             int
        startTime:          str
        endTime:            str
        isComplete:         bool
        isScoringPlay:      bool
        hasReview:          bool
        hasOut:             bool
        captivatingIndex:   int
        count:              Count
        matchup:            Matchup_Play
        pitchIndex:         list -> list[int]
        actionIndex:        list -> list[int]
        runnerIndex:        list -> list[int]
        runners:            list -> list[Runners]
        playEvents:         list -> list[PlayEvent]
        playEndTime:        str



        Count Keys/Attributes:
        ------------
        balls:      int
        strikes:    int
        outs:       int

        Matchup_Play Keys/Attributes:
        ------------
        batter:                 NameAndId
        batSide:                str
        pitcher:                NameAndId
        pitchHand:              str
        batterHotColdZones:     list
        pitcherHotColdZones:    list
        splits:                 MatchupSplits

        Runners Keys/Attributes:
        ------------
        originBase:         int, None
        start:              int, None
        end:                int, None
        outBase:            int, None
        isOut:              bool
        outNumber:          int, None
        event:              str
        eventType:          str
        movementReason:     str, None
        isScoringEvent:     bool
        rbi:                bool
        earned:             bool
        teamUnearned:       bool
        playIndex:          int
        responsiblePitcher: NameAndId, None
        runner:             NameAndId, None
        credits:            list -> List[Credits_Play]

        PlayEvent Keys/Attributes:
        ------------
        description:    str
        event:          str, None
        eventType:      str, None
        code:           str, None
        ballColor:      str, None
        trailColor:     str, None
        isInPlay:       bool, None
        isStrike:       bool, None
        isBall:         bool, None
        hasReview:      bool
        pitchType:      PitchType
        count:          Count
        pitchData:      PitchData_P
        hitData:        HitData_P
        index:          int
        playId:         str, None
        type:           str
        isPitch:        bool
        pitchNumber:    int, None
        startTime:      str
        endTime:        str



        NameAndId Keys/Attributes:
        ------------
        Id:     int
        name:   str

        MatchupSplits Keys/Attributes:
        ------------
        batter:     str
        pitcher:    str
        menOnBase:  str

        Credits_Play Keys/Attributes:
        ------------
        player:     NameAndId
        position:   PersonPosition
        credit:     str

        PitchType Keys/Attributes:
        ------------
        code:           str, None
        description:    str, None

        PitchData_P Keys/Attributes:
        ------------
        startSpeed:         float
        endSpeed:           float
        strikeZoneTop:      float
        strikeZoneBottom:   float
        coordinates:        PitchCoordinates
        breaks:             PitchBreaks
        zone:               int
        typeConfidence:     float
        plateTime:          float
        extension:          float

        HitData_P Keys/Attributes:
        ------------
        launchSpeed:    float
        launchAngle:    int
        totalDistance:  int
        trajectory:     str
        hardness:       str
        location:       str
        coordinates:    HitCoordinate


        From person.py
        PersonPosition Keys/Attributes:
        ------------
        code:           str
        name:           str
        type:           str
        abbreviation:   str

        PitchCoordinates Keys/Attributes:
        ------------
        aY6:    float
        aZ:     float
        pfxX:   float
        pfxZ:   float
        pX:     float
        pZ:     float
        vX0:    float
        vY0:    float
        vZ0:    float
        x:      float
        y:      float
        x0:     float
        y0:     float
        z0:     float
        aX:     float

        PitchBreaks Keys/Attributes:
        ------------
        breakAngle:     float
        breakLength:    float
        breakY:         int
        spinRate:       int
        spinDirection:  int

        HitCoordinate Keys/Attributes:
        ------------
        x: int
        y: int
        """
        return self._allPlays

    # currentPlay
    @property
    def currentPlay(self) -> Play:
        """Play dataclass

        Keys/Attributes:
        ------------
        type:               str
        event:              str
        eventType:          str
        description:        str
        rbi:                int
        awayScore:          int
        homeScore:          int
        atBatIndex:         int
        halfInning:         str
        isTopInning:        bool
        inning:             int
        startTime:          str
        endTime:            str
        isComplete:         bool
        isScoringPlay:      bool
        hasReview:          bool
        hasOut:             bool
        captivatingIndex:   int
        count:              Count
        matchup:            Matchup_Play
        pitchIndex:         list -> list[int]
        actionIndex:        list -> list[int]
        runnerIndex:        list -> list[int]
        runners:            list -> list[Runners]
        playEvents:         list -> list[PlayEvent]
        playEndTime:        str



        Count Keys/Attributes:
        ------------
        balls:      int
        strikes:    int
        outs:       int

        Matchup_Play Keys/Attributes:
        ------------
        batter:                 NameAndId
        batSide:                str
        pitcher:                NameAndId
        pitchHand:              str
        batterHotColdZones:     list
        pitcherHotColdZones:    list
        splits:                 MatchupSplits

        Runners Keys/Attributes:
        ------------
        originBase:         int, None
        start:              int, None
        end:                int, None
        outBase:            int, None
        isOut:              bool
        outNumber:          int, None
        event:              str
        eventType:          str
        movementReason:     str, None
        isScoringEvent:     bool
        rbi:                bool
        earned:             bool
        teamUnearned:       bool
        playIndex:          int
        responsiblePitcher: NameAndId, None
        runner:             NameAndId, None
        credits:            list -> List[Credits_Play]

        PlayEvent Keys/Attributes:
        ------------
        description:    str
        event:          str, None
        eventType:      str, None
        code:           str, None
        ballColor:      str, None
        trailColor:     str, None
        isInPlay:       bool, None
        isStrike:       bool, None
        isBall:         bool, None
        hasReview:      bool
        pitchType:      PitchType
        count:          Count
        pitchData:      PitchData_P
        hitData:        HitData_P
        index:          int
        playId:         str, None
        type:           str
        isPitch:        bool
        pitchNumber:    int, None
        startTime:      str
        endTime:        str



        NameAndId Keys/Attributes:
        ------------
        Id:     int
        name:   str

        MatchupSplits Keys/Attributes:
        ------------
        batter:     str
        pitcher:    str
        menOnBase:  str

        Credits_Play Keys/Attributes:
        ------------
        player:     NameAndId
        position:   PersonPosition
        credit:     str

        PitchType Keys/Attributes:
        ------------
        code:           str, None
        description:    str, None

        PitchData_P Keys/Attributes:
        ------------
        startSpeed:         float
        endSpeed:           float
        strikeZoneTop:      float
        strikeZoneBottom:   float
        coordinates:        PitchCoordinates
        breaks:             PitchBreaks
        zone:               int
        typeConfidence:     float
        plateTime:          float
        extension:          float

        HitData_P Keys/Attributes:
        ------------
        launchSpeed:    float
        launchAngle:    int
        totalDistance:  int
        trajectory:     str
        hardness:       str
        location:       str
        coordinates:    HitCoordinate


        From person.py
        PersonPosition Keys/Attributes:
        ------------
        code:           str
        name:           str
        type:           str
        abbreviation:   str

        PitchCoordinates Keys/Attributes:
        ------------
        aY6:    float
        aZ:     float
        pfxX:   float
        pfxZ:   float
        pX:     float
        pZ:     float
        vX0:    float
        vY0:    float
        vZ0:    float
        x:      float
        y:      float
        x0:     float
        y0:     float
        z0:     float
        aX:     float

        PitchBreaks Keys/Attributes:
        ------------
        breakAngle:     float
        breakLength:    float
        breakY:         int
        spinRate:       int
        spinDirection:  int

        HitCoordinate Keys/Attributes:
        ------------
        x: int
        y: int
        """
        return self._currentPlay

    @property
    def scoringPlays(self):
        """scoringPlays

        List[int]

        List that holds ints that represent which play was a scoring play
        """
        return self._scoringPlays

    # playsByInning
    @property
    def playsByInning(self):
        """playsByInning

        List[Inning_LD]

        List that holds Inning_LD objects that hold the plays for that inning

        Inning_LD Keys/Attributes:
        ------------
        startIndex: int
        endIndex:   int
        top:        list # list[int]
        bottom:     list # list[int]
        homeHits:   list # list[Hit_LD]
        awayHits:   list # list[Hit_LD]


        Hit_LD Keys/Attributes:
        ------------
        inning:         int
        pitcher:        NameAndId
        batter:         NameAndId
        coordinates:    HitCoordinate
        type:           str
        description:    str


        HitCoordinate Keys/Attributes:
        ------------
        x: int
        y: int
        """
        return self._playsByInning


    @property
    def lineScore(self) -> LineScore:
        """lineScore dataclass

        Keys/Attributes:
        ------------
        currentInning:          int
        currentInningOrdinal:   str
        inningState:            str
        inningHalf:             str
        isTopInning:            bool
        scheduledInnings:       int
        innings:                list[dict]
        fielding:               Fielding
        hitting:                Hitting
        balls:                  int
        strikes:                int
        outs:                   int
        runs:                   HomeAndAway_ls
        hits:                   HomeAndAway_ls
        errors:                 HomeAndAway_ls
        leftOnBase:             HomeAndAway_ls

        HomeAndAway_ls Keys/Attributes:
        ------------
        home:   int
        away:   int

        Fielding Keys/Attributes:
        ------------
        team:           NameAndId
        pitcher:        NameAndId
        catcher:        NameAndId
        first:          NameAndId
        second:         NameAndId
        third:          NameAndId
        shortstop:      NameAndId
        left:           NameAndId
        center:         NameAndId
        right:          NameAndId
        batter:         NameAndId
        onDeck:         NameAndId
        inHole:         NameAndId
        battingOrder:   int

        Hitting  Keys/Attributes:
        ------------
        team:           NameAndId
        battingOrder:   int
        batter:         NameAndId
        onDeck:         NameAndId
        inHole:         NameAndId
        pitcher:        NameAndId
        onBase:         OnBase

        OnBase Keys/Attributes:
        ------------
        onBase:     bool
        onFirst:    bool
        onSecond:   bool
        onThird:    bool
        first:      NameAndId
        second:     NameAndId
        third:      NameAndId

        NameAndId Keys/Attributes:
        ------------
        Id:     int
        name:   str
        """
        return self._lineScore


    @property
    def home(self) -> Team_BSHA:
        """Team_BSHA dataclass

        Keys/Attributes:
        ------------
        teamId:         int
        name:           TeamName
        teamStats:      Stats_BSHA
        players:        dict # dict{str(id):players_BSHA}
        batters:        list # list[int(id)]
        pitchers:       list # list[int(id)]
        bench:          list # list[int(id)]
        bullpen:        list # list[int(id)]
        battingOrder:   str


        team.teamName
        TeamName Keys/Attributes:
        ------------
        Id:             int
        full:           str
        location:       str
        franchise:      str
        club:           str
        short:          str
        abbreviation:   str

        players_BSHA dict{str(id):players_BSHA} Keys/Attributes:
        ------------
        playerId:           int
        name:               str
        parentTeamId:       int
        jerseyNumber:       str
        position:           PersonPosition
        gameStats:          Stats_BSHA
        seasonStats:        Stats_BSHA
        battingOrder:       str
        isCurrentBatter:    bool
        isCurrentPitcher:   bool
        isOnBench:          bool
        isSubstitute:       bool

        person.position
        PersonPosition Keys/Attributes:
        ------------
        code:           str
        name:           str
        type:           str
        abbreviation:   str

        Stats_BSHA Keys/Attributes:
        ------------
        batting:    dict
        pitching:   dict
        fielding:   dict
        """
        return self._home

    @property
    def away(self) -> Team_BSHA:
        """Team_BSHA dataclass

        Keys/Attributes:
        ------------
        teamId:         int
        name:           TeamName
        teamStats:      Stats_BSHA
        players:        dict # dict{str(id):players_BSHA}
        batters:        list # list[int(id)]
        pitchers:       list # list[int(id)]
        bench:          list # list[int(id)]
        bullpen:        list # list[int(id)]
        battingOrder:   str

        team.teamName
        TeamName Keys/Attributes:
        ------------
        Id:             int
        full:           str
        location:       str
        franchise:      str
        club:           str
        short:          str
        abbreviation:   str

        players_BSHA dict{str(id):players_BSHA} Keys/Attributes:
        ------------
        playerId:           int
        name:               str
        parentTeamId:       int
        jerseyNumber:       str
        position:           PersonPosition
        gameStats:          Stats_BSHA
        seasonStats:        Stats_BSHA
        battingOrder:       str
        isCurrentBatter:    bool
        isCurrentPitcher:   bool
        isOnBench:          bool
        isSubstitute:       bool

        PersonPosition Keys/Attributes:
        ------------
        code:           str
        name:           str
        type:           str
        abbreviation:   str

        Stats_BSHA Keys/Attributes:
        ------------
        batting:    dict
        pitching:   dict
        fielding:   dict
        """
        return self._away


    # Should this be brought out to three seperate?
    # From decisions to:
    #   winner
    #   looser
    #   save
    #
    # So you would just call game.winner instead of game.decisions.winner ?
    @property
    def decisions(self) -> Decisions:
        """Decisions dataclass

        Keys/Attributes:
        ------------
        winner: NameAndId
        looser: NameAndId
        save:   NameAndId

        NameAndId Keys/Attributes:
        ------------
        Id:     int
        name:   str
        """
        return self._decisions

    def hasUpdated() -> bool:
        """Returns true if game has updated"""

        lookupUrl = f'https://statsapi.mlb.com/api/v1/game/{gamePk}/playByPlay'
        r = requests.get(lookupUrl).json()

        if r["currentPlay"]["about"]["atBatIndex"] > self._currentPlay.atBatIndex:
            return True
        else:
            if len(r["currentPlay"]["actionIndex"]) > len(self._currentPlay.actionIndex):
                return True

        return False
