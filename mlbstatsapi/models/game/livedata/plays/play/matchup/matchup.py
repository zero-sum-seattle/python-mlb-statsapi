from typing import Optional, List, Any
from pydantic import Field, field_validator
from mlbstatsapi.models.base import MLBBaseModel
from mlbstatsapi.models.people import Person
from mlbstatsapi.models.data import CodeDesc
from .attributes import PlayMatchupSplits


class PlayMatchup(MLBBaseModel):
    """
    A class to represent a play matchup.

    Attributes
    ----------
    batter : Person
        Matchup batter.
    bat_side : CodeDesc
        Batter's bat side.
    pitcher : Person
        Matchup pitcher.
    pitch_hand : CodeDesc
        Pitcher's side.
    pitcher_hot_cold_zones : List
        Pitcher hot cold zone stats.
    splits : PlayMatchupSplits
        Play matchup splits.
    batter_hot_cold_zone_stats : List
        Batter hot cold zone stats.
    post_on_first : Person
        Runner on first.
    post_on_second : Person
        Runner on second.
    post_on_third : Person
        Runner on third.
    """
    batter: Person
    bat_side: CodeDesc = Field(alias="batSide")
    pitcher: Person
    pitch_hand: CodeDesc = Field(alias="pitchHand")
    batter_hot_cold_zones: List = Field(alias="batterHotColdZones")
    pitcher_hot_cold_zones: List = Field(alias="pitcherHotColdZones")
    splits: PlayMatchupSplits
    batter_hot_cold_zone_stats: Optional[List] = Field(default=None, alias="batterHotColdZoneStats")
    pitcher_hot_cold_zone_stats: Optional[List] = Field(default=None, alias="pitcherHotColdZoneStats")
    post_on_first: Optional[Person] = Field(default=None, alias="postOnFirst")
    post_on_second: Optional[Person] = Field(default=None, alias="postOnSecond")
    post_on_third: Optional[Person] = Field(default=None, alias="postOnThird")

    @field_validator('batter_hot_cold_zone_stats', 'pitcher_hot_cold_zone_stats', mode='before')
    @classmethod
    def extract_stats(cls, v: Any) -> Any:
        """Extract stats from nested dict if present."""
        if isinstance(v, dict) and 'stats' in v:
            return v['stats']
        return v
