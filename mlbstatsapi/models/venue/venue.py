from dataclasses import dataclass, field


@dataclass
class Venue:
    id: int = field(default=None)
    link: str = field(default=None)
    name: str = field(default=None)