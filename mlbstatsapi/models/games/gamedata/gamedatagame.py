from dataclasses import dataclass

@dataclass
class GameDataGame:
    pk: int
    type: str
    doubleHeader: str
    id: str
    gamedayType: str
    tiebreaker: str
    gameNumber: int
    calendarEventID: str
    season: str
    seasonDisplay: str

    @property
    def id(self):
        return self.pk
