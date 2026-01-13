from typing import Optional, List, Dict, Any
from pydantic import Field, field_validator, model_validator
from mlbstatsapi.models.base import MLBBaseModel
from mlbstatsapi.models.venues import Venue
from mlbstatsapi.models.people import Person
from .attributes import (
    GameDataGame,
    GameDatetime,
    GameStatus,
    GameTeams,
    GameWeather,
    GameInfo,
    GameReview,
    GameFlags,
    GameProbablePitchers,
    MoundVisits,
)


class GameData(MLBBaseModel):
    """
    A class to represent a game's game data.

    Attributes
    ----------
    game : GameDataGame
        Game information about this game.
    datetime : GameDatetime
        Time and dates for this game.
    status : GameStatus
        Information on this game's status.
    teams : GameTeams
        Our two teams for this game, home and away.
    players : List[Person]
        A list of all the players for this game.
    venue : Venue
        Venue information for this game.
    official_venue : Venue
        The official venue for this game.
    weather : GameWeather
        The weather for this game.
    game_info : GameInfo
        Information on this game.
    review : GameReview
        Game review info and team challenges.
    flags : GameFlags
        Flag bools for this game.
    alerts : List
        Alerts.
    probable_pitchers : GameProbablePitchers
        Home and away probable pitchers for this game.
    official_scorer : Person
        The official scorer for this game.
    primary_data_caster : Person
        The official data caster for this game.
    secondary_data_caster : Person
        Secondary data caster for this game.
    mound_visits : MoundVisits
        Mound visits for this game.
    abs_challenges : List[dict]
        ABS challenges for this game.
    """
    game: GameDataGame
    datetime: GameDatetime
    status: GameStatus
    teams: GameTeams
    players: List[Person] = []
    venue: Venue
    official_venue: Venue = Field(alias="officialVenue")
    review: GameReview
    flags: GameFlags
    alerts: List = []
    probable_pitchers: GameProbablePitchers = Field(alias="probablePitchers")
    mound_visits: Optional[MoundVisits] = Field(default=None, alias="moundVisits")
    game_info: Optional[GameInfo] = Field(default=None, alias="gameInfo")
    weather: Optional[GameWeather] = None
    official_scorer: Optional[Person] = Field(default=None, alias="officialScorer")
    primary_data_caster: Optional[Person] = Field(default=None, alias="primaryDataCaster")
    secondary_data_caster: Optional[Person] = Field(default=None, alias="secondaryDataCaster")
    abs_challenges: Optional[List[dict]] = Field(default=None, alias="absChallenges")

    @model_validator(mode='before')
    @classmethod
    def handle_players_dict(cls, data: Dict[str, Any]) -> Dict[str, Any]:
        """Convert players dict to list of Person objects."""
        if isinstance(data, dict) and 'players' in data:
            players_data = data['players']
            if isinstance(players_data, dict):
                data['players'] = list(players_data.values())
        return data

    @field_validator('weather', 'game_info', 'official_scorer', 'primary_data_caster', 'secondary_data_caster', mode='before')
    @classmethod
    def empty_dict_to_none(cls, v: Any) -> Any:
        """Convert empty dicts to None."""
        if isinstance(v, dict) and not v:
            return None
        return v
