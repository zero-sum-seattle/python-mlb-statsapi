import logging
from typing import List
from mlbstatsapi.models.person import Person
from mlbstatsapi.models.team import Team
from mlbstatsapi.models.sport import Sport
from mlbstatsapi.models.league import League
from .mlbdataadapter import MlbDataAdapter, MlbResult

class Mlb:
    def __init__(self, hostname: str = 'statsapi.mlb.com', ver: str = 'v1', logger: logging.Logger = None):
        self._mlb_adapter_v1 = MlbDataAdapter(hostname, 'v1', logger)
        self._mlb_adapter_v1_1 = MlbDataAdapter(hostname, 'v1.1', logger)

    def get_people(self) -> List[Person]:
        # TODO Doc string
        mlbdata = self._mlb_adapter_v1.get(endpoint="sports/1/players") # get all people
        if 'people' in mlbdata.data:
            people = [ Person(**person) for person in mlbdata.data['people'] ]
        return people # return list of people objects

    def get_person(self, playerId) -> List[Person]:
        # TODO Doc string
        mlbdata = self._mlb_adapter_v1.get(endpoint=f"people/{playerId}") # Get player
        if 'people' in mlbdata.data:
            person = [ Person(**person) for person in mlbdata.data['people'] ]
        return person # Return

    def get_people_id(self, fullName) -> List[int]:
        # TODO Doc string
        # fullName: Ty France
        mlbdata = self._mlb_adapter_v1.get(endpoint=f"sports/1/players") # Get All People: players
        playerIds = [] # create empty list
        for person in mlbdata.data['people']:
            if person['fullName'] == fullName: # Match person fullName
                playerIds.append(person['id']) # add to list

        return playerIds

    def get_teams(self) -> List[Team]:
        # TODO Doc string
        mlbdata = self._mlb_adapter_v1.get(endpoint="teams?sportId=1") # Get all major league teams
        if 'teams' in mlbdata.data:
            teams = [ Team(**team) for team in mlbdata.data['teams']]
        return teams # return list of all Team objects

    def get_team(self, teamId) -> List[Team]:
        # TODO Doc string
        mlbdata = self._mlb_adapter_v1.get(endpoint=f"teams/{teamId}")
        if 'teams' in mlbdata.data:
            teams = [ Team(**team) for team in mlbdata.data['teams']]
        return teams # return list of all Team objects        return team

    def get_team_id(self, teamName) -> List[int]:
        # TODO Doc string
        # teamName: Mariners
        mlbdata = self._mlb_adapter_v1.get(endpoint="teams") # Get all Teams
        teamIds = [] # create empty list
        for team in mlbdata.data['teams']:
            if team['teamName'] == teamName: # find matching Team Name
                teamIds.append(team['id']) # append match id

        return teamIds

    def get_sport(self) -> List[Sport]:
        pass

    def get_league(self) -> List[League]:
        pass

    def get_sports(self) -> List[Sport]:
        pass

    def get_leagues(self) -> List[League]:
        pass