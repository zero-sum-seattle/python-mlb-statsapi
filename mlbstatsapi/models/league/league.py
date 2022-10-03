from dataclasses import dataclass



@dataclass
class League:
    id: int
    name: str
    link: str
    abbreviation: str = None