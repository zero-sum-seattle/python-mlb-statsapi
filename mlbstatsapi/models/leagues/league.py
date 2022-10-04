from dataclasses import dataclass

@dataclass
class LeagueRecord:
    """
    A class to represent a leaguerecord.

    Attributes
    ----------
    wins : int
        number of wins in leaguerecord 
    losses: int
        number of losses in leaguerecord
    ties: int
        number of ties in leaguerecord
    pct: str
        winning pct of leaguerecord
    """
    wins: int
    losses: int
    ties: int
    pct: str

@dataclass
class League:
    """
    A class to represent a division.

    Attributes
    ----------
    id : int
        id number of the divison
    name: str
        name of the division
    link : str
        link of the division
    abbreviation : str
        abbreviation the venue
    """
    id: int
    name: str
    link: str
    abbreviation: str = None