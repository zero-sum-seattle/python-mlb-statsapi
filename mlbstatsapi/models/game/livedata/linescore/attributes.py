from typing import Optional, Any
from pydantic import Field, field_validator
from mlbstatsapi.models.base import MLBBaseModel
from mlbstatsapi.models.people import Person
from mlbstatsapi.models.teams import Team


class LinescoreTeamScoring(MLBBaseModel):
    """
    A class to represent a games linescore team scoring.

    Attributes
    ----------
    hits : int
        Team hits for this inning.
    errors : int
        Team errors for this inning.
    left_on_base : int
        Players left on base for this inning.
    runs : int
        Team runs for this inning.
    is_winner : bool
        If team is winner.
    """
    hits: int
    errors: int
    left_on_base: int = Field(alias="leftOnBase")
    runs: Optional[int] = None
    is_winner: Optional[bool] = Field(default=None, alias="isWinner")


class LinescoreInning(MLBBaseModel):
    """
    A class to represent an inning for a game's linescore.

    Attributes
    ----------
    num : int
        Inning number.
    ordinal_num : str
        Inning ordinal.
    home : LinescoreTeamScoring
        Home team inning info.
    away : LinescoreTeamScoring
        Away team inning info.
    """
    num: int
    ordinal_num: str = Field(alias="ordinalNum")
    home: Optional[LinescoreTeamScoring] = None
    away: Optional[LinescoreTeamScoring] = None

    @field_validator('home', 'away', mode='before')
    @classmethod
    def empty_dict_to_none(cls, v: Any) -> Any:
        """Convert empty dicts to None."""
        if isinstance(v, dict) and not v:
            return None
        return v


class LinescoreTeams(MLBBaseModel):
    """
    A class to represent home and away teams in the linescore.

    Attributes
    ----------
    home : LinescoreTeamScoring
        Home team current inning info.
    away : LinescoreTeamScoring
        Away team current inning info.
    """
    home: Optional[LinescoreTeamScoring] = None
    away: Optional[LinescoreTeamScoring] = None

    @field_validator('home', 'away', mode='before')
    @classmethod
    def empty_dict_to_none(cls, v: Any) -> Any:
        """Convert empty dicts to None."""
        if isinstance(v, dict) and not v:
            return None
        return v


class LinescoreOffense(MLBBaseModel):
    """
    A class to represent a game's current offense.

    Attributes
    ----------
    batter : Person
        Current batter.
    on_deck : Person
        Current on deck batter.
    in_hole : Person
        Current in the hole batter.
    pitcher : Person
        Who is this team's pitcher.
    batting_order : int
        Number in the batting order.
    team : Team
        The team currently on offense.
    first : str
        Runner on first (if any).
    second : str
        Runner on second (if any).
    third : str
        Runner on third (if any).
    """
    team: Team
    batter: Optional[Person] = None
    on_deck: Optional[Person] = Field(default=None, alias="onDeck")
    in_hole: Optional[Person] = Field(default=None, alias="inHole")
    pitcher: Optional[Person] = None
    batting_order: Optional[int] = Field(default=None, alias="battingOrder")
    # MLB API sometimes returns these as person objects (id/link/fullName).
    first: Optional[Person] = None
    second: Optional[Person] = None
    third: Optional[Person] = None

    @field_validator('batter', 'on_deck', 'in_hole', 'pitcher', 'first', 'second', 'third', mode='before')
    @classmethod
    def empty_dict_to_none(cls, v: Any) -> Any:
        """Convert empty dicts to None."""
        if isinstance(v, dict) and not v:
            return None
        return v


class LinescoreDefense(MLBBaseModel):
    """
    A class to represent a game's current defense.

    Attributes
    ----------
    pitcher : Person
        Current pitcher.
    catcher : Person
        Current catcher.
    first : Person
        Current first baseman.
    second : Person
        Current second baseman.
    third : Person
        Current third baseman.
    shortstop : Person
        Current shortstop.
    left : Person
        Current left fielder.
    center : Person
        Current center fielder.
    right : Person
        Current right fielder.
    batter : Person
        The next batter when this team switches to offense.
    on_deck : Person
        The next on deck batter when this team switches to offense.
    in_hole : Person
        The next in hole batter when this team switches to offense.
    batting_order : int
        Number this team is in the batting order.
    team : Team
        The team that is playing defense currently.
    """
    team: Team
    pitcher: Optional[Person] = None
    catcher: Optional[Person] = None
    first: Optional[Person] = None
    second: Optional[Person] = None
    third: Optional[Person] = None
    shortstop: Optional[Person] = None
    left: Optional[Person] = None
    center: Optional[Person] = None
    right: Optional[Person] = None
    batter: Optional[Person] = None
    on_deck: Optional[Person] = Field(default=None, alias="onDeck")
    in_hole: Optional[Person] = Field(default=None, alias="inHole")
    batting_order: Optional[int] = Field(default=None, alias="battingOrder")

    @field_validator(
        'pitcher', 'catcher', 'first', 'second', 'third', 'shortstop',
        'left', 'center', 'right', 'batter', 'on_deck', 'in_hole',
        mode='before'
    )
    @classmethod
    def empty_dict_to_none(cls, v: Any) -> Any:
        """Convert empty dicts to None."""
        if isinstance(v, dict) and not v:
            return None
        return v
