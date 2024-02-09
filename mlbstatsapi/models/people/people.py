from pydantic import BaseModel, validator
from typing import Optional, Union, Dict, Any

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
    fullName: Optional[str] = None
    link: str
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    primaryNumber: Optional[str] = None
    birthDate: Optional[str] = None
    currentAge: Optional[int] = None
    birthCity: Optional[str] = None
    birthStateProvince: Optional[str] = None
    birthCountry: Optional[str] = None
    height: Optional[str] = None
    weight: Optional[int] = None
    active: Optional[bool] = None
    primaryPosition: Optional[Position] = None
    useName: Optional[str] = None
    middleName: Optional[str] = None
    boxscoreName: Optional[str] = None
    nickname: Optional[str] = None
    draftYear: Optional[int] = None
    mlbDebutDate: Optional[str] = None
    batSide: Optional[BatSide] = None
    pitchHand: Optional[PitchHand] = None
    nameFirstLast: Optional[str] = None
    nameSlug: Optional[str] = None
    firstLastName: Optional[str] = None
    lastFirstName: Optional[str] = None
    lastInitName: Optional[str] = None
    initLastName: Optional[str] = None
    fullFMLName: Optional[str] = None
    fullLFMName: Optional[str] = None
    useLastName: Optional[str] = None
    pronunciation: Optional[str] = None
    strikeZoneTop: Optional[float] = None
    strikeZoneBottom: Optional[float] = None
    nameTitle: Optional[str] = None
    gender: Optional[str] = None
    isPlayer: Optional[bool] = None
    isVerified: Optional[bool] = None
    nameMatrilineal: Optional[str] = None
    deathDate: Optional[str] = None
    deathCity: Optional[str] = None
    deathCountry: Optional[str] = None
    deathStateProvince: Optional[str] = None
    lastPlayedDate: Optional[str] = None
    nameSuffix: Optional[str] = None



class Player(BaseModel):
    """
    Represents a player, extending the person with specific attributes for players.
    
    Attributes:
        jerseynumber (str): The jersey number of the player.
        parentteamid (int): The ID of the player's parent team.
        position (dict): The player's position, initialized from a dictionary.
        status (Union[Status, dict]): The player's status, can be a Status object or a dictionary.
    """
    jerseyNumber: str
    parentTeamId: int
    # position: InitVar[dict] #TODO WTF IS THIS AGAIN
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
    jerseyNumber: str
    job: str
    jobId: str
    title: str
    parentTeamId: Optional[int] = None


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



