from typing import Union, Dict, List, Any
from dataclasses import dataclass

from playRunners_models.runnersMovement import RunnersMovement
from playRunners_models.runnersDetails import RunnersDetails
from playRunners_models.runnersCredits import RunnersCredits

@dataclass
class PlayRunners:
    movement:   Union[RunnersMovement, Dict[str, Any]]
    details:    Union[RunnersDetails, Dict[str, Any]]
    credits:    Union[List[RunnersCredits], List[Dict[str, Any]]]

    def __post_init__(self):
        self.movement = RunnersMovement(**movement)
        self.details = PRunnersDetails(**details)
        self.credits = [RunnersCredits(**credit) for credit in credits]
