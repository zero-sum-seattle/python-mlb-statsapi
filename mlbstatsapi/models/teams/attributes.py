from dataclasses import dataclass

@dataclass
class TeamRecord:
    """
    A class to represent a teams current record.

    Attributes 
    ----------
    gamesplayed : int
        Number of game played by team
    wildcardgamesback : str
        Number of game back from wildcard
    leaguegamesback : str
        Number of league games back
    springleaguegamesback : str
        Number of game back in spring league
    sportgamesback : str
        Number of games back in sport
    divisiongamesback : str
        Number of games back in division
    conferencegamesback : str
        Number of games back in conference
    leaguerecord : Dict
        Record in league
    records : Dict
        Records
    divisionleader : bool
        Is this team a divison leader
    wins : int
        Number of wins
    losses : int
        Number of losses
    winningpercentage : str
        Winning percentage
    """
    gamesplayed:            int
    wildcardgamesback:      str
    leaguegamesback:        str
    springleaguegamesback:  str
    sportgamesback:         str
    divisiongamesback:      str
    conferencegamesback:    str
    leaguerecord:           dict
    records:                dict
    divisionleader:         bool
    wins:                   int
    losses:                 int
    winningpercentage:      str