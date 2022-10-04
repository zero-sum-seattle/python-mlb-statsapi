from dataclasses import dataclass

@dataclass
class LinescoreTeamScoreInfo:
    runs: int
    hits: int
    errors: int
    leftOnBase: int
