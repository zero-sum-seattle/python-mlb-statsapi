from mlbstatsapi.mlbdataadapter import MlbDataAdapter, MlbResult
import logging
from typing import List, Dict
from .mlb import *



class Mlb:
    def __init__(self, hostname: str = 'statsapi.mlb.com', ver: str = 'v1', logger: logging.Logger = None):
        self._mlb_adapter_v1 = MlbDataAdapter(hostname, 'v1', logger)
        self._mlb_adapter_v1_1 = MlbDataAdapter(hostname, 'v1.1', logger)

    def get_people(self) -> List[Person]:
        # TODO Doc string
        mlbdata = self._mlb_adapter_v1.get(endpoint="/sports/1/players") # get all people
        people = [Person(**person) for person in mlbdata.data['people'] if "people" in mlbdata.data]
        return people # return list of people objects

    def get_person(self, playerId) -> List[Person]:
        # TODO Doc string
        mlbdata = self._mlb_adapter_v1.get(endpoint=f"/people/{playerId}") # Get player
        person = [Person(**person) for person in mlbdata.data['people'] if "people" in mlbdata.data ]# Create Person object
        return person # Return

    def get_people_id(self, fullName) -> List[int]:
        # TODO Doc string
        # fullName: Ty France
        mlbdata = self._mlb_adapter_v1.get(endpoint=f"/sports/1/players") # Get All People: players
        playerIds = [] # create empty list
        for person in mlbdata.data['people']:
            if person['fullName'] == fullName: # Match person fullName
                playerIds.append(person['id']) # add to list

        return playerIds

    def get_teams(self) -> List[Team]:
        # TODO Doc string
        mlbdata = self._mlb_adapter_v1.get(endpoint="/teams") # Get all teams
        teams = [Team(**team) for team in mlbdata.data['teams'] if "teams" in mlbdata.data] # create list of all team objects
        return teams # return list of all Team objects

    def get_team(self, teamId) -> List[Team]:
        # TODO Doc string
        mlbdata = self._mlb_adapter_v1.get(endpoint=f"/teams/{teamId}")
        team = [ Team(**team) for team in mlbdata.data['teams'] if "teams" in mlbdata.data] # This is ugly. We shouldn't need to pass the key.
        return team

    def get_team_id(self, teamName) -> List[int]:
        # TODO Doc string
        # teamName: Mariners
        mlbdata = self._mlb_adapter_v1.get(endpoint="/teams") # Get all Teams
        teamIds = [] # create empty list
        for team in mlbdata.data['teams']:
            if team['teamName'] == teamName: # find matching Team Name
                teamIds.append(team['id']) # append match id

        return teamIds

    def get_game(self, gameId) -> Game:
        mlbdata = self._mlb_adapter_v1_1.get(endpoint=f'/game/{gameId}/feed/live') # Get all Teams
        game = Game(gameId, **mlbdata.data)
        return game
