from pydantic import BaseModel


class BatSide(BaseModel):
    """
    Represents the side of the plate from which a player bats.
    
    Attributes:
        code (str): The code representing the batting side.
        description (str): A description of the batting side.
    """
    code: str
    description: str


class PitchHand(BaseModel):
    """
    Represents the hand a player uses to pitch.
    
    Attributes:
        code (str): The code representing the pitching hand.
        description (str): A description of the pitching hand.
    """
    code: str
    description: str


class Position(BaseModel):
    """
    Represents the position a player holds in the team.
    
    Attributes:
        code (str): The code representing the player's position.
        name (str): The name of the position.
        type (str): The type of the position.
        abbreviation (str): The abbreviation of the position.
    """
    code: str
    name: str
    type: str
    abbreviation: str


class Status(BaseModel):
    """
    Represents the status of a player.
    
    Attributes:
        code (str): The code representing the status of the player.
        description (str): A description of the player's status.
    """
    code: str
    description: str


class Home(BaseModel):
    """
    Represents the hometown of a player.
    
    Attributes:
        city (str): The city where the player is from.
        state (str): The state where the player is from.
        country (str): The country where the player is from.
    """
    city: str
    state: str
    country: str


class School(BaseModel):
    """
    Represents the school that a player attended.
    
    Attributes:
        name (str): The name of the school.
        schoolclass (str): The class or grade in the school.
        city (str): The city where the school is located.
        country (str): The country where the school is located.
        state (str): The state where the school is located.
    """
    name: str
    schoolclass: str
    city: str
    country: str
    state: str
