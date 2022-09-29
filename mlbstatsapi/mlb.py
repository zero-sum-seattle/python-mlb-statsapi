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
    abbreviation: str

    def __init__(self, id: int, link: str, abbreviation: str, **kwargs) -> None:
        self.id = id
        self.link = link
        self.abbreviation = abbreviation


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


class GameGameData():
    game: Dict
    datetime: Dict
    status: Dict
    teams: Dict
    players: Dict
    venue: Dict
    officialVenue: Dict
    weather: Dict
    gameInfo: Dict
    review: Dict
    flags: Dict
    alerts: List
    probablePitchers: Dict

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
        self.game = game
        self.datetime = datetime
        self.status = status
        self.teams = teams
        self.players = players
        self.venue = venue
        self.officialVenue = officialVenue
        self.weather = weather
        self.gameInfo = gameInfo
        self.review = review
        self.flags = flags
        self.alerts = alerts
        self.probablePitchers = probablePitchers


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

    metaData: Game_MetaData
    gameData: Game_GameData
    liveData: Game_LiveData

    def __init__(self, id: int,
                    metaData: Dict,
                    gameData: Dict,
                    liveData: Dict,
                    **kwargs) -> None:
        self.id = id
        self.metaData = Game_MetaData(**metaData)
        self.gameData = Game_GameData(**gameData)
        self.liveData = Game_LiveData(**liveData)

class Stats():
    group: str
    statype: str

    def __init__(self, group: str, type: str, **kwargs) -> None:
        self.group = group
        self.type = type
        self.__dict__.update(kwargs)

class League():
    id: int
    name: str
    link: str

    def __init__(self, id: int, name: str, link: str) -> None:
        self.id = id
        self.name = name
        self.link = link
