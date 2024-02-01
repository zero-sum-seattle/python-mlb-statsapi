from pydantic import BaseModel, validator
from typing import Optional, Union, Dict, Any, InitVar

from .attributes import BatSide, Position, PitchHand, Status, Home, School
from mlbstatsapi.models.teams import Team
from mlbstatsapi.models.data import CodeDesc

class Person(BaseModel):
    """
    Represents a person with various personal and professional attributes within a sports context, including identification, physical attributes, team associations, and status.

    Attributes:
        id (int): The unique identifier of the person.
        link (str): API link to more detailed information about the person.
        primaryposition (Union[Position, Dict[str, Any]]): The primary position of the person in the sport.
        pitchhand (Union[PitchHand, Dict[str, Any]]): Information about the person's pitching hand.
        batside (Union[BatSide, Dict[str, Any]]): Information about the person's batting side.
        fullname (Optional[str]): The full name of the person.
        firstname (Optional[str]): The first name of the person.
        lastname (Optional[str]): The last name of the person.
        primarynumber (Optional[str]): The primary number associated with the person.
        birthdate (Optional[str]): The birth date of the person.
        currentteam (Optional[str]): The current team of the person.
        currentage (Optional[str]): The current age of the person.
        birthcity (Optional[str]): The birth city of the person.
        birthstateprovince (Optional[str]): The province/state of the person's birthplace.
        height (Optional[str]): The height of the person.
        weight (Optional[int]): The weight of the person.
        active (Optional[bool]): Indicates if the person is currently active in the sport.
        usename (Optional[str]): The name used to refer to the person.
        middlename (Optional[str]): The middle name of the person.
        boxscorename (Optional[str]): The name used in the box score for the person.
        nickname (Optional[str]): The nickname of the person.
        draftyear (Optional[int]): The draft year of the person.
        mlbdebutdate (Optional[str]): The MLB debut date of the person.
        namefirstlast (Optional[str]): The first and last name of the person.
        nameslug (Optional[str]): A slug representation of the person's name.
        firstlastname (Optional[str]): A combination of the first and last name of the person.
        lastfirstname (Optional[str]): A combination of the last and first name of the person.
        lastinitname (Optional[str]): The last name and the initial of the first name of the person.
        initlastname (Optional[str]): The initial of the first name and the last name of the person.
        fullfmlname (Optional[str]): The full first, middle, and last name of the person.
        fulllfmname (Optional[str]): The full last, first, and middle name of the person.
        uselastname (Optional[str]): The last name used for the person.
        birthcountry (Optional[str]): The birth country of the person.
        pronunciation (Optional[str]): The pronunciation of the person's name.
        strikezonetop (Optional[float]): The top of the strike zone for the person.
        strikezonebottom (Optional[float]): The bottom of the strike zone for the person.
        nametitle (Optional[str]): The title of the person.
        gender (Optional[str]): The gender of the person.
        isplayer (Optional[bool]): Indicates if the person is a player.
        isverified (Optional[bool]): Indicates if the person's identity is verified.
        namematrilineal (Optional[str]): The matrilineal name of the person.
        deathdate (Optional[str]): The death date of the person, if applicable.
        deathcity (Optional[str]): The city of the person's death, if applicable.
        deathcountry (Optional[str]): The country of the person's death, if applicable.
        lastplayeddate (Optional[str]): The last date the person played, if applicable.
        namesuffix (Optional[str]): The suffix of the person's name.
    """
    id: int
    link: str
    primaryposition: Union[Position, Dict[str, Any]]
    pitchhand: Union[PitchHand, Dict[str, Any]]
    batside: Union[BatSide, Dict[str, Any]]
    fullname: Optional[str] = None
    firstname: Optional[str] = None
    lastname: Optional[str] = None
    primarynumber: Optional[str] = None
    birthdate: Optional[str] = None
    currentteam: Optional[str] = None
    currentage: Optional[str] = None
    birthcity: Optional[str] = None
    birthstateprovince: Optional[str] = None
    height: Optional[str] = None
    weight: Optional[int] = None
    active: Optional[bool] = None
    usename: Optional[str] = None
    middlename: Optional[str] = None
    boxscorename: Optional[str] = None
    nickname: Optional[str] = None
    draftyear: Optional[int] = None
    mlbdebutdate: Optional[str] = None
    namefirstlast: Optional[str] = None
    nameslug: Optional[str] = None
    firstlastname: Optional[str] = None
    lastfirstname: Optional[str] = None
    lastinitname: Optional[str] = None
    initlastname: Optional[str] = None
    fullfmlname: Optional[str] = None
    fulllfmname: Optional[str] = None
    birthcountry: Optional[str] = None
    pronunciation: Optional[str] = None
    strikezonetop: Optional[float] = None
    strikezonebottom: Optional[float] = None
    nametitle: Optional[str] = None
    gender: Optional[str] = None
    isplayer: Optional[bool] = None
    isverified: Optional[bool] = None
    namematrilineal: Optional[str] = None
    deathdate: Optional[str] = None
    deathcity: Optional[str] = None
    deathcountry: Optional[str] = None
    deathstateprovince: Optional[str] = None
    lastplayeddate: Optional[str] = None
    uselastname: Optional[str] = None
    namesuffix: Optional[str] = None

    class Config:
        orm_mode = True

    # TODO read up on validators and understand wtf this is doing
    @validator('primaryposition', 'pitchhand', 'batside', pre=True)
    def parse_position(cls, v):
        return v if isinstance(v, dict) else v.dict()

class Player(BaseModel):
    """
    Represents a player, extending the person with specific attributes for players.
    
    Attributes:
        jerseynumber (str): The jersey number of the player.
        parentteamid (int): The ID of the player's parent team.
        position (dict): The player's position, initialized from a dictionary.
        status (Union[Status, dict]): The player's status, can be a Status object or a dictionary.
    """
    jerseynumber: str
    parentteamid: int
    position: InitVar[dict]
    status: Union[Status, dict]

    # Include post-initialization logic if necessary
    # TODO wtf is this?
    def __post_init_post_parse__(self, position: dict):
        if position:
            self.primaryposition = Position(**position)

class Coach(BaseModel):
    """
    Represents a coach, providing details about their role within the team.
    
    Attributes:
        jerseynumber (str): The jersey number of the coach.
        job (str): The specific job or role of the coach.
        jobid (str): The unique identifier for the coach's job.
        title (str): The title or official position of the coach.
        parentteamid (int): The ID of the coach's parent team.
    """
    jerseynumber: str
    job: str
    jobid: str
    title: str
    parentteamid: int


class Batter(BaseModel):
    """
    Represents a batter, essentially a Person specialized as a batter.
    """
    # Add any batter-specific attributes here if necessary

class Pitcher(BaseModel):
    """
    Represents a pitcher, essentially a Person specialized as a pitcher.
    """
    # Add any pitcher-specific attributes here if necessary


class DraftPick(BaseModel):
    """
    Represents a pick made in the MLB draft, detailing the player picked, the round, number, and value of the pick, along with additional information about the player and the drafting team.

    Attributes:
        bisplayerid (Optional[int]): The unique identifier of the player associated with this draft pick.
        pickround (str): The round of the draft in which this pick was made.
        picknumber (int): The number of the pick in the round.
        roundpicknumber (int): The number of the pick overall in the draft.
        rank (Optional[int]): The rank of the player among all players eligible for the draft.
        pickvalue (Optional[str]): The value of the pick, if known.
        signingbonus (Optional[str]): The signing bonus associated with this pick, if known.
        home (Union[Home, Dict[str, Any]]): Information about the player's home location.
        scoutingreport (Optional[str]): A scouting report on the player's abilities.
        school (Union[School, Dict[str, Any]]): Information about the player's school or college.
        blurb (Optional[str]): A brief summary of the player's background and accomplishments.
        headshotlink (str): A link to a headshot image of the player.
        team (Union[Team, Dict[str, Any]]): The team that made this draft pick.
        drafttype (Union[CodeDesc, Dict[str, Any]]): Information about the type of draft in which this pick was made.
        isdrafted (bool): Whether or not the player associated with this pick has been drafted.
        ispass (bool): Whether or not the team passed on making a pick in this round.
        year (str): The year in which the draft took place.
    """
    bisplayerid: Optional[int] = None
    pickround: str
    picknumber: int
    roundpicknumber: int
    rank: Optional[int] = None
    pickvalue: Optional[str] = None
    signingbonus: Optional[str] = None
    home: Union[Home, Dict[str, Any]]
    scoutingreport: Optional[str] = None
    school: Union[School, Dict[str, Any]]
    blurb: Optional[str] = None
    headshotlink: str
    team: Union[Team, Dict[str, Any]]
    drafttype: Union[CodeDesc, Dict[str, Any]]
    isdrafted: bool
    ispass: bool
    year: str

    def __repr__(self) -> str:
        kws = [f'{key}={value}' for key, value in self.__dict__.items() if value is not None and value]
        return "{}({})".format(type(self).__name__, ", ".join(kws))