from typing import List
from dataclasses import dataclass, field

from .attributes import ScheduleDates

@dataclass
class Schedule:
    """
    A class to represent a Schedule.

    Attributes
    ----------
    copyright : str
        Copyright
    totalitems : int 
        Total items in schedule
    totalevents : int
        Total events in schedule
    totalgames : int
        Total games in schedule
    totalgamesinprogress : int
        Total games in progress in schedule
    dates : ScheduleDates
        List of dates with games in schedule
    """
    totalitems: int 
    totalevents: int
    totalgames: int
    totalgamesinprogress: int
    dates: List[ScheduleDates] = field(default_factory=list)

    def __post_init__(self):
        self.dates = [ScheduleDates(**date) for date in self.dates if self.dates]

    def get_games_with_status(self, abstractgamestate: str = None, codedgamestate: str = None,
                                    detailedstate: str = None, statuscode: str = None,
                                    reason: str = None, abstractgamecode: str = None) -> List[int]:
        """
        returns a list of game ids.

        Parameters
        ----------
        abstractgamestate : str
            Abstract game state
        codedgamestate : str
            coded game state
        detailedstate : str
            details of the game state
        statuscode : str
            status code of the game
        reason : str
            reason of the game
        abstractgamecode : str

        Returns
        -------
        list of ints
        """       
        gamestatuses = {'abstractgamestate': abstractgamestate,
                        'codedgamestate': codedgamestate,
                        'detailedstate': detailedstate,
                        'statuscode': statuscode,
                        'reason': reason,
                        'abstractgamecode': abstractgamecode}
        gameids = []

        if all(gamestatuses[status] == None for status in gamestatuses):
            return gameids 
        else:
            for date in self.dates:
                for game in date.games:
                    gamestatus = game.status                    
                    if all(gamestatuses[status] == getattr(gamestatus,f'{status}') for status in gamestatuses if gameStatuses[status]):
                        gameids.append(game.gamepk)
            return gameids

    def get_games_inProgress(self) -> List[int]:
        return self.get_games_with_status(abstractgamestate='Live')

    def get_games_finished(self) -> List[int]:
        return self.get_games_with_status(abstractgamestate='Final')
