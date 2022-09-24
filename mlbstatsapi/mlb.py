from typing import List, Dict
from mlbstatsapi.mlbdataadapter import MlbDataAdapter

class MlbObject:
    def __init__(self):
        self._load_stats = MlbDataAdapter()

class Person(MlbObject):
    # Basic Person Class
    id: int
    full_name: str
    link: str
    preload_stats: bool

    def __init__(self, id: int, fullName: str, link: str, preload: bool = False, **kwargs) -> None:
        self.id = id # person id
        self.full_name = fullName # person full_name
        self.link = link # person link
        self.__dict__.update(kwargs) # let's do this for a sloppy apply

        if preload:
            statobjects = []
            for group in ('hitting', 'fielding'):
                 for type in ('season', 'career'):
                    statdata = self._load_stats.get(endpoint=f"/people/{self.id}/stats?stats={type}&group={group}")
                    statobjects.append(Stats(**stat) for stat in statdata.data['stats'] if "stats" in statdata.data)
            self.stats = statobjects
        else:
            self.stats = []


class Team():
    id: int
    name: str
    link: str

    def __init__(self, id: int, name: str, link: str, **kwargs) -> None:
        self.id = id
        self.name = name
        self.link = link
        self.__dict__.update(kwargs)

class Sport():
    id: int
    link: str
    abbreviation: str

    def __init__(self, id: int, link: str, abbreviation: str) -> None:
        self.id = id
        self.link = link
        self.abbreviation = abbreviation

class Stats():
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

