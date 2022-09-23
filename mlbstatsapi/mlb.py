from cmath import log
import requests
from typing import List, Dict
from .exceptions import TheMlbStatsApiException
from .person import Person
from .team import Team
import logging


class MlbDataAdapter:
    """Adapter for calling the mlb statsapi endpoint"""

    def __init__(self, hostname: str, ver: str = 'v1', logger: logging.Logger = None):
        self.url = f"https://{hostname}/api/{ver}/" # we'll figure out the v1.1 endpoint later
        self._logger = logger or logging.getLogger(__name__)


    def get(self, endpoint: str, data: Dict = None) -> List[Dict]:
        full_url = self.url + endpoint # pass endpoint from inhertited classes
        logline_pre = f"url={full_url}"
        logline_post = f" ,".join((logline_pre, "success={}, status_code={}, message={}"))
        try: 
            self._logger.debug(logline_post)
            response = requests.get(url=full_url) # mlbstats API only uses get calls

        except requests.exceptions.RequestException as e: # catch a response error
            self._logger.error(msg=(str(e))) # log error 
            raise TheMlbStatsApiException("Request failed") from e

        try:
            data = response.json()
        except (ValueError, requests.JSONDecodeError) as e: # catch a JSON error
            self._logger.error(msg=(str(e))) # log error JSON 
            raise TheMlbStatsApiException("Bad JSON in response") from e
        if response.status_code <= 200 and response.status_code <= 299: # catch HTTP errors
            self._logger.debug(msg=logline_post.format("success", response.status_code, response.reason)) # log success 
            return MlbResult(response.status_code, message=response.reason, data=data) # return result

        raise TheMlbStatsApiException(f"{response.status_code}: {response.reason}") # raise exception 


class Mlb(MlbDataAdapter):
    def __init__(self, hostname: str = 'statsapi.mlb.com', ver: str = 'v1', logger: logging.Logger = None):
        self._mlb_adapter = MlbDataAdapter(hostname, ver, logger)

    def get_people(self) -> Person:
        # TODO Doc string
        mlbdata = self._mlb_adapter.get(endpoint="/sports/1/players") # get all people
        people = [Person(**person) for person in mlbdata.data['people'] if "people" in mlbdata.data]
        return people # return list of people objects
    
    def get_person(self, playerId) -> Person:
        # TODO Doc string
        mlbdata = self._mlb_adapter.get(endpoint=f"/people/{playerId}") # Get player 
        person = Person(**mlbdata.data['people']) # Create Person object
        return person # Return

    def get_people_id(self, fullName) -> List:
        # TODO Doc string
        # fullName: Ty France
        mlbdata = self._mlb_adapter.get(endpoint=f"/sports/1/players") # Get All People: players
        playerIds = [] # create empty list
        for person in mlbdata.data['people']:
            if person['fullName'] == fullName: # Match person fullName
                playerIds.append(person['id']) # add to list
        
        return playerIds
        
    def get_teams(self) -> Team:
        # TODO Doc string
        mlbdata = self._mlb_adapter.get(endpoint="/teams") # Get all teams
        teams = [Team(**team) for team in mlbdata.data['teams'] if "teams" in mlbdata.data] # create list of all team objects
        return teams # return list of all Team objects

    def get_team(self, teamId) -> Team:
        # TODO Doc string
        mlbdata = self._mlb_adaper.get(endpoint=f"/team/{teamId}")
        team = Team(**mlbdata.data['teams']) # This is ugly. We shouldn't need to pass the key.
        return team

    def get_team_id(self, teamName) -> List:
        # TODO Doc string
        # teamName: Mariners
        mlbdata = self._mlb_adapter.get(endpoint="/teams") # Get all Teams
        teamIds = [] # create empty list
        for team in mlbdata.data['teams']:
            if team['teamName'] == teamName: # find matching Team Name
                teamIds.append(team['id']) # append match id
        
        return teamIds


class MlbResult:
    def __init__(self, status_code: int, message: str, data: List[Dict]):
        self.status_code = int(status_code)
        self.message = str(message)
        self.data = data if data else []