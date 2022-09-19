"""
Python Wrapper for the MLB Stats API - https://statsapi.mlb.com
"""

from .game import Game
from .person import Person
from .team import Team

game = Game
person = Person
team = Team

from .functions import lookup_player
from .functions import liveGames
from .functions import todaysGames
