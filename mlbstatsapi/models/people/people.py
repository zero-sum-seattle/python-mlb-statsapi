from __future__ import annotations
from typing import Optional, Any, TYPE_CHECKING
from pydantic import Field, field_validator, model_validator
from mlbstatsapi.models.base import MLBBaseModel
from .attributes import BatSide, Position, PitchHand, Status, Home, School
from mlbstatsapi.models.teams import Team
from mlbstatsapi.models.data import CodeDesc


class Person(MLBBaseModel):
    """
    A class to represent a Person.

    Attributes
    ----------
    id : int
        ID number of the person.
    link : str
        API link to person.
    primary_position : Position
        Primary position of the person.
    pitch_hand : PitchHand
        Pitch hand of the person.
    bat_side : BatSide
        Bat side of the person.
    full_name : str
        Full name of the person.
    first_name : str
        First name of the person.
    last_name : str
        Last name of the person.
    primary_number : str
        Primary number of the person.
    birth_date : str
        Birth date of the person.
    current_team : Team
        The current team of the person.
    current_age : int
        The current age of the person.
    birth_city : str
        The birth city of the person.
    birth_state_province : str
        The province of the birth state.
    height : str
        The height of the person.
    weight : int
        The weight of the person.
    active : bool
        The active status of the person.
    use_name : str
        The use name of the person.
    middle_name : str
        The middle name of the person.
    boxscore_name : str
        The box score name of the person.
    nickname : str
        The nickname of the person.
    draft_year : int
        The draft year of the person.
    mlb_debut_date : str
        The MLB debut date of the person.
    name_first_last : str
        The first and last name of the person.
    name_slug : str
        The name slug of the person.
    first_last_name : str
        The first and last name of the person.
    last_first_name : str
        The last and first name of the person.
    last_init_name : str
        The last init name of the person.
    init_last_name : str
        The init last name of the person.
    full_fml_name : str
        The full FML name of the person.
    full_lfm_name : str
        The full LFM name of the person.
    use_last_name : str
        The use last name of the person.
    birth_country : str
        The birth country of the person.
    pronunciation : str
        The pronunciation of the person's name.
    strike_zone_top : float
        The strike zone top of the person.
    strike_zone_bottom : float
        The strike zone bottom of the person.
    name_title : str
        The name title of the person.
    gender : str
        The gender of the person.
    is_player : bool
        The player status of the person.
    is_verified : bool
        The verification of the person.
    name_matrilineal : str
        The name matrilineal of the person.
    death_date : str
        The death date of the person.
    death_city : str
        The death city of the person.
    death_country : str
        The death country of the person.
    death_state_province : str
        The death state province of the person.
    last_played_date : str
        The last played date of the person.
    name_suffix : str
        The name suffix of the person.
    """
    id: int
    link: str
    primary_position: Optional[Position] = Field(default=None, alias="primaryPosition")
    pitch_hand: Optional[PitchHand] = Field(default=None, alias="pitchHand")
    bat_side: Optional[BatSide] = Field(default=None, alias="batSide")
    full_name: Optional[str] = Field(default=None, alias="fullName")
    first_name: Optional[str] = Field(default=None, alias="firstName")
    last_name: Optional[str] = Field(default=None, alias="lastName")
    primary_number: Optional[str] = Field(default=None, alias="primaryNumber")
    birth_date: Optional[str] = Field(default=None, alias="birthDate")
    current_team: Optional[Team] = Field(default=None, alias="currentTeam")
    current_age: Optional[int] = Field(default=None, alias="currentAge")
    birth_city: Optional[str] = Field(default=None, alias="birthCity")
    birth_state_province: Optional[str] = Field(default=None, alias="birthStateProvince")
    height: Optional[str] = None
    weight: Optional[int] = None
    active: Optional[bool] = None
    use_name: Optional[str] = Field(default=None, alias="useName")
    middle_name: Optional[str] = Field(default=None, alias="middleName")
    boxscore_name: Optional[str] = Field(default=None, alias="boxscoreName")
    nickname: Optional[str] = Field(default=None, alias="nickName")
    draft_year: Optional[int] = Field(default=None, alias="draftYear")
    mlb_debut_date: Optional[str] = Field(default=None, alias="mlbDebutDate")
    name_first_last: Optional[str] = Field(default=None, alias="nameFirstLast")
    name_slug: Optional[str] = Field(default=None, alias="nameSlug")
    first_last_name: Optional[str] = Field(default=None, alias="firstLastName")
    last_first_name: Optional[str] = Field(default=None, alias="lastFirstName")
    last_init_name: Optional[str] = Field(default=None, alias="lastInitName")
    init_last_name: Optional[str] = Field(default=None, alias="initLastName")
    full_fml_name: Optional[str] = Field(default=None, alias="fullFMLName")
    full_lfm_name: Optional[str] = Field(default=None, alias="fullLFMName")
    birth_country: Optional[str] = Field(default=None, alias="birthCountry")
    pronunciation: Optional[str] = None
    strike_zone_top: Optional[float] = Field(default=None, alias="strikeZoneTop")
    strike_zone_bottom: Optional[float] = Field(default=None, alias="strikeZoneBottom")
    name_title: Optional[str] = Field(default=None, alias="nameTitle")
    gender: Optional[str] = None
    is_player: Optional[bool] = Field(default=None, alias="isPlayer")
    is_verified: Optional[bool] = Field(default=None, alias="isVerified")
    name_matrilineal: Optional[str] = Field(default=None, alias="nameMatrilineal")
    death_date: Optional[str] = Field(default=None, alias="deathDate")
    death_city: Optional[str] = Field(default=None, alias="deathCity")
    death_country: Optional[str] = Field(default=None, alias="deathCountry")
    death_state_province: Optional[str] = Field(default=None, alias="deathStateProvince")
    last_played_date: Optional[str] = Field(default=None, alias="lastPlayedDate")
    use_last_name: Optional[str] = Field(default=None, alias="useLastName")
    name_suffix: Optional[str] = Field(default=None, alias="nameSuffix")


class Player(Person):
    """
    A class to represent a Player.

    Attributes
    ----------
    jersey_number : str
        Jersey number of the player.
    status : Status
        Status of the player.
    parent_team_id : int
        Parent team ID.
    note : str
        Optional note about the player (e.g., injury notes).
    position : Position
        Position of the player (alias for primary_position).
    """
    jersey_number: str = Field(alias="jerseyNumber")
    status: Status
    parent_team_id: Optional[int] = Field(default=None, alias="parentTeamId")
    note: Optional[str] = None

    @model_validator(mode='before')
    @classmethod
    def handle_position_alias(cls, data):
        """Handle 'position' field as alias for 'primary_position'."""
        if isinstance(data, dict) and 'position' in data and 'primary_position' not in data:
            data['primary_position'] = data.pop('position')
        return data


class Coach(Person):
    """
    A class to represent a Coach.

    Attributes
    ----------
    jersey_number : str
        Jersey number of the coach.
    job : str
        Job of the coach.
    job_id : str
        Job ID of the coach.
    title : str
        Title of the coach.
    """
    jersey_number: str = Field(alias="jerseyNumber")
    job: str
    job_id: str = Field(alias="jobId")
    title: str


class Batter(Person):
    """
    A class to represent a Batter.
    """
    pass


class Pitcher(Person):
    """
    A class to represent a Pitcher.
    """
    pass


class DraftPick(Person):
    """
    A class to represent a pick made in the MLB draft.

    Attributes
    ----------
    bis_player_id : int
        The unique identifier of the player associated with this draft pick.
    pick_round : str
        The round of the draft in which this pick was made.
    pick_number : int
        The number of the pick in the round.
    round_pick_number : int
        The number of the pick overall in the draft.
    rank : int
        The rank of the player among all players eligible for the draft.
    pick_value : str
        The value of the pick, if known.
    signing_bonus : str
        The signing bonus associated with this pick, if known.
    home : Home
        Information about the player's home location.
    scouting_report : str
        A scouting report on the player's abilities.
    school : School
        Information about the player's school or college.
    blurb : str
        A brief summary of the player's background and accomplishments.
    headshot_link : str
        A link to a headshot image of the player.
    team : Team
        The team that made this draft pick.
    draft_type : CodeDesc
        Information about the type of draft in which this pick was made.
    is_drafted : bool
        Whether or not the player associated with this pick has been drafted.
    is_pass : bool
        Whether or not the team passed on making a pick in this round.
    year : str
        The year in which the draft took place.
    """
    pick_round: str = Field(alias="pickRound")
    pick_number: int = Field(alias="pickNumber")
    round_pick_number: int = Field(alias="roundPickNumber")
    home: Home
    school: School
    headshot_link: str = Field(alias="headshotLink")
    team: Team
    draft_type: CodeDesc = Field(alias="draftType")
    is_drafted: bool = Field(alias="isDrafted")
    is_pass: bool = Field(alias="isPass")
    year: str
    bis_player_id: Optional[int] = Field(default=None, alias="bisPlayerId")
    rank: Optional[int] = None
    pick_value: Optional[str] = Field(default=None, alias="pickValue")
    signing_bonus: Optional[str] = Field(default=None, alias="signingBonus")
    scouting_report: Optional[str] = Field(default=None, alias="scoutingReport")
    blurb: Optional[str] = None
