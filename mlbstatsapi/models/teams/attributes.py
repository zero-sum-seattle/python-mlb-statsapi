from dataclasses import dataclass

@dataclass
class TeamRecord:
    """
    A class to represent a teams current record.

    Attributes 
    ----------
    gamesPlayed : int
        Number of game played by team
    wildCardGamesBack : str
        Number of game back from wildcard
    leagueGamesBack : str
        Number of league games back
    springLeagueGamesBack : str
        Number of game back in spring league
    sportGamesBack : str
        Number of games back in sport
    divisionGamesBack : str
        Number of games back in division
    conferenceGamesBack : str
        Number of games back in conference
    leagueRecord : Dict
        Record in league
    records : Dict
        Records
    divisionLeader : bool
        Is this team a divison leader
    wins : int
        Number of wins
    losses : int
        Number of losses
    winningPercentage : str
        Winning percentage
    """
    gamesPlayed:            int
    wildCardGamesBack:      str
    leagueGamesBack:        str
    springLeagueGamesBack:  str
    sportGamesBack:         str
    divisionGamesBack:      str
    conferenceGamesBack:    str
    leagueRecord:           dict
    records:                dict
    divisionLeader:         bool
    wins:                   int
    losses:                 int
    winningPercentage:      str