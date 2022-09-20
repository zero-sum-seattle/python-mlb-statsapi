import requests
from dataclasses import dataclass, asdict

from .team import TeamName

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
            condition = weather['condition'],
            temp = weather['temp'],
            wind = weather['wind']
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
