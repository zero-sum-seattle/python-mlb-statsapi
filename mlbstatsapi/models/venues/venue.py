from typing import Optional, Union
from pydantic import BaseModel
from .attributes import Location, TimeZone, FieldInfo

class Venue(BaseModel):
    """Represents a venue.

    Attributes:
        id (int): ID for this venue.
        name (Optional[str]): Name of this venue.
        link (str): Link to venue's endpoint.
        location (Location): Location of this venue.
        active (Optional[bool]): Indicates if this venue is currently active.
        season (Optional[str]): The season this venue is associated with.
    """
    id: int
    link: str
    name: Optional[str] = None
    active: Optional[bool] = None
    season: Optional[str] = None
