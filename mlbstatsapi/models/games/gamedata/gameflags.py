from dataclasses import dataclass

@dataclass
class GameFlags:
    noHitter:               bool
    perfectGame:            bool
    awayTeamNoHitter:       bool
    awayTeamPerfectGame:    bool
    homeTeamNoHitter:       bool
    homeTeamPerfectGame:    bool
