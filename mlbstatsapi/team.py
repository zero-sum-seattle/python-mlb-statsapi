from typing import List, Dict
from .stat import Stats

class Team(): # basic Team class
    id: int
    name: str
    link: str

    def __init__(self, id: int, name: str, link: str, **kwargs) -> None:
        self.id = id
        self.name = name
        self.link = link
        self.__dict__.update(kwargs) # let's do this for a sloppy apply

