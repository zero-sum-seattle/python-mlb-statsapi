from typing import Union, Optional, List
from dataclasses import dataclass

from mlbstatsapi.models.venues import Venue
from mlbstatsapi.models.teams import Team
from mlbstatsapi.models.people import Person

@dataclass
class Eventtype:
    """
    The Eventtype class holds information about the type of an event.

    Attributes:
    ___________
    code : str
        The unique code of the event type.
    name : str
        The name of the event type.
    """
    code: str
    name: str

@dataclass
class Info:
    """
    The Info class holds information about an event.

    Attributes
    ----------
    id : int
        The unique identifier of the event.
    name : str
        The name of the event.
    eventtype : Eventtype
        The type of event. Can be an instance of the Eventtype class or a 
        dictionary containing the attributes for the Eventtype class.
    eventdate : str
        The date of the event.
    venue : Venue
        The venue of the event. Can be an instance of the Venue class or 
        a dictionary containing the attributes for the Venue class.
    ismultiday : bool
        Whether the event spans multiple days.
    isprimarycalendar : bool
        Whether the event is on the primary calendar.
    filecode : str
        The code of the file associated with the event.
    eventnumber : int
        The number of the event.
    publicfacing : bool
        Whether the event is public-facing.
    teams : List[Team]
        The teams participating in the event. Can be a list of instances of 
        the Team class or a list of dictionaries containing the attributes 
        for the Team class.
    """
    id: int
    name: str
    eventtype: Union[Eventtype, dict]
    eventdate: str
    venue: Union[Venue, dict]
    ismultiday: bool
    isprimarycalendar: bool
    filecode: str
    eventnumber: int
    publicfacing: bool
    teams: List[Union[Team, dict]]

    def __post_init__(self):
        self.eventtype = Eventtype(**self.eventtype)
        self.venue = Venue(**self.venue)
        self.teams = [Team(**team) for team in self.teams]

@dataclass
class Status:
    """
    A class representing the status of a round.

    Attributes
    ----------
    state : str
        The current state of the game or round (e.g. "in progress", "paused", 
        "ended")
    currentround : int
        The number of the current round in the game
    currentroundtimeleft : str
        The amount of time left in the current round, in a human-readable 
        format (e.g. "4:00")
    intiebreaker : bool
        Whether the game or round is currently in a tiebreaker
    tiebreakernum : int
        The number of the current tiebreaker, if applicable
    clockstopped : bool
        Whether the round clock is currently stopped
    bonustime : bool
        Whether the round is currently in bonus time
    """
    state: str
    currentround: int
    currentroundtimeleft: str
    intiebreaker: bool
    tiebreakernum: int
    clockstopped: bool
    bonustime: bool

@dataclass
class Coordinates:
    """"
    A class representing the coordinates of a hit

    Attributes
    ----------
    coordx : float
        The x-coordinate of the hit
    coordy : float
        The y-coordinate of the hit
    landingposx : float
        The x-coordinate of the hits's landing position, 
        if applicable
    landingposy : float
        The y-coordinate of the hits's landing position, 
        if applicable
    """
    coordx: float
    coordy: float
    landingposx: float
    landingposy: float

@dataclass
class Trajectorydata:
    """"
    A class representing data on a hit's trajectory in three-dimensional space.

    Attributes
    ----------
    trajectorypolynomialx : List[int]
        A list of coefficients for the polynomial representing the 
        x-coordinate of the hits's trajectory
    trajectorypolynomialy : List[int]
        A list of coefficients for the polynomial representing the 
        y-coordinate of the hits's trajectory
    trajectorypolynomialz : List[int]
        A list of coefficients for the polynomial representing the 
        z-coordinate of the hits's trajectory
    validtimeinterval : List[int]
        A list of two elements representing the start and end times for which 
        the polynomial coefficients are valid
    measuredtimeinterval : List[int]
        A list of two elements representing the start and end times of the 
        interval during which the hits's trajectory was measured
    """
    trajectorypolynomialx: List[int]
    trajectorypolynomialy: List[int]
    trajectorypolynomialz: List[int]
    validtimeinterval: List[int]
    measuredtimeinterval: List[int]

@dataclass
class Hitdata:
    """"
    A class representing data on a hit
    
    Attributes
    ----------
    launchspeed : float
        The speed at which the hit was launched
    totaldistance : int
        The total distance the hit traveled
    launchangle : float: None
        The angle at which the hit was launched, if applicable
    coordinates : Coordinates: None
        Coordinates for the hit
    trajectorydata : Trajectorydata: None
        Trajectory data for the hit
    """
    totaldistance: int
    launchspeed: Optional[float] = None
    launchangle: Optional[float] = None
    coordinates: Optional[Union[Coordinates, dict]] = None
    trajectorydata: Optional[Union[Trajectorydata, dict]] = None

    def __post_init__(self):
        self.coordinates = Coordinates(**self.coordinates) if self.coordinates else None
        self.trajectorydata = Trajectorydata(**self.trajectorydata) if self.trajectorydata else None

@dataclass
class Hits:
    """"
    A class representing a hit in the homerun derby

    Attributes
    ----------
    bonustime : bool
        A boolean indicating whether the hit occurred during bonus time.
    homerun : bool
        A boolean indicating whether the hit was a homerun.
    tiebreaker : bool
        A boolean indicating whether the hit occurred during a tiebreaker.
    hitdata : Hitdata
        An object containing the data for the hit. This can either be a 
        Hitdata object or a dictionary.
    ishomerun : bool
        A boolean indicating whether the hit was a homerun. This attribute 
        is a duplicate of the `homerun` attribute.
    playid : str
        A string containing the ID of the play in which the hit occurred.
    timeremaining : str
        A string indicating the amount of time remaining in the game when the 
        hit occurred.
    isbonustime : bool
        A boolean indicating whether the hit occurred during bonus time. This 
        attribute is a duplicate of the `bonustime` attribute.
    istiebreaker : bool
        A boolean indicating whether the hit occurred during a tiebreaker. 
        This attribute is a duplicate of the `tiebreaker` attribute.
    """
    bonustime: bool
    homerun: bool
    tiebreaker: bool
    hitdata: Union[Hitdata, dict]
    ishomerun: bool
    timeremaining: str
    isbonustime: bool
    istiebreaker: bool
    playid: Optional[str] = None

    def __post_init__(self):
        self.hitdata = Hitdata(**self.hitdata)

@dataclass
class Seed:
    """"
    A class representing either a high or a low seed in the matchup for
    the homerun derby.

    Attributes
    ----------
    complete : bool
        A boolean indicating whether the seed has been completed.
    started : bool
        A boolean indicating whether the seed has been started.
    winner : bool
        A boolean indicating whether the player for this seed is the winner 
        of the game.
    player : Person
        An object containing the data for the player associated with this 
        seed. This can either be a Person object or a dictionary.
    topderbyhitdata : Hitdata
        An object containing the data for the top hit in the seed. This can 
        either be a Hitdata object or a dictionary.
    hits : Hits
        An object containing the data for the hits in the seed. This can 
        either be a Hits object or a dictionary.
    seed : int
        An integer representing the seed number.
    order : int
        An integer representing the order in which the seed was played.
    iswinner : bool
        A boolean indicating whether the player for this seed is the winner 
        of the game. This attribute is a duplicate of the `winner` attribute.
    iscomplete : bool
        A boolean indicating whether the seed has been completed. This 
        attribute is a duplicate of the `complete` attribute.
    isstarted : bool
        A boolean indicating whether the seed has been started. This 
        attribute is a duplicate of the `started` attribute.
    numhomeruns : int
        An integer representing the number of homeruns hit in the seed.
    """
    complete: bool
    started: bool
    winner: bool
    player: Union[Person, dict]
    topderbyhitdata: Union[Hitdata, dict]
    hits: Union[Hits, dict]
    seed: int
    order: int
    iswinner: bool
    iscomplete: bool
    isstarted: bool
    numhomeruns: int

    def __post_init__(self):
        self.player = Person(**self.player)
        self.topderbyhitdata = Hitdata(**self.topderbyhitdata)
        self.hits = [Hits(**hit) for hit in self.hits]

@dataclass
class Matchup:
    """"
    A class representing a matchup in the homerun derby
    
    Attributes
    ----------
    topseed : Seed
        Containing the top seed in the matchup.
    bottomseed : Seed
        Containing the bottom seed in the matchup.
    """
    topseed: Union[Seed, dict]
    bottomseed: Union[Seed, dict]

    def __post_init__(self):
        self.topseed = Seed(**self.topseed)
        self.bottomseed = Seed(**self.bottomseed)  

@dataclass
class Round:
    """"
    A class representing a round in the homerun derby

    Attributes
    ----------
    round : int
        An integer representing the round number.
    numbatters : int
        An integer representing the number of batters in the round.
    matchups : List[Matchup]
        A list of objects containing the data for the matchups in the round.
    """
    round: int
    numbatters: int
    matchups: List[Union[Matchup, dict]]

    def __post_init__(self):
        self.matchups = [Matchup(**matchup) for matchup in self.matchups]