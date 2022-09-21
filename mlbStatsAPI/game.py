import requests
from dataclasses import dataclass, asdict

from .team import TeamName


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
        self._home = TeamName (
            Id = home['id'],
            full = home['name'],
            location = home['locationName'],
            franchise = home['franchiseName'],
            club = home['clubName'],
            short = home['shortName'],
            abbreviation = home['abbreviation']
        )

        away = gameData['teams']['away']
        self._away = TeamName (
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

    @property
    def gameId(self) -> int:
        """game Pk ID number"""
        return self.__gameId

    @property
    def datetime(self):
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
    def status(self):
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
    def home(self):
        """team.TeamName dataclass

        Keys/Attributes:
        ------------
        Id:             int
        full:           str
        location:       str
        franchise:      str
        club:           str
        short:          str
        abbreviation:   str
        """
        return self._home

    @property
    def away(self):
        """team.TeamName dataclass

        Keys/Attributes:
        ------------
        Id:             int
        full:           str
        location:       str
        franchise:      str
        club:           str
        short:          str
        abbreviation:   str
        """
        return self._away

    @property
    def venue(self):
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
    def weather(self):
        """weather dataclass

        Keys/Attributes:
        ------------
        condition:  str
        temp:       str
        wind:       str
        """
        return self._weather

    @property
    def flags(self):
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
    def lineScore(self):
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
