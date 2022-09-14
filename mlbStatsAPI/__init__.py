"""
Python Wrapper for the MLB Stats API - https://statsapi.mlb.com
"""

from .game import Game
from .person import Person

game = Game
person = Person

from .functions import liveGames_print
from .functions import liveGames_data
