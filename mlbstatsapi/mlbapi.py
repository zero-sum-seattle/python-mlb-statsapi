import logging
from typing import List
from mlbstatsapi.models.people import Person
from mlbstatsapi.models.teams import Team
from mlbstatsapi.models.sports import Sport
from mlbstatsapi.models.leagues import League
from mlbstatsapi.models.game import Game
from mlbstatsapi.models.venues import Venue
from .mlbdataadapter import TheMlbStatsApiException
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

    def get_game(self, gameId) -> Game:
        # TODO Doc string
        mlbdata = self._mlb_adapter_v1_1.get(endpoint=f'game/{gameId}/feed/live') # Get game
        if (mlbdata.data['gamePk'] != gameId): # If game id eccepted but not valid
            raise TheMlbStatsApiException("Bad JSON in response")

        return Game(**mlbdata.data)

    def get_venue(self, venueId) -> Venue:
        # TODO Doc string
        mlbdata = self._mlb_adapter_v1.get(endpoint=f'venues/{venueId}?hydrate=location,fieldInfo,timezone')
        if (mlbdata.data['venues'][0]['id'] != venueId):
            raise TheMlbStatsApiException("Bad JSON in response")

        return Venue(**mlbdata.data['venues'][0])

    def get_venue_id(self, venueName) -> List[int]:
        # TODO Doc string
        mlbdata = self._mlb_adapter_v1.get(endpoint=f"venues") # Get All Venues
        venueIds = [] # create empty list
        for venue in mlbdata.data['venues']:
            if venue['name'].lower() == venueName.lower(): # Match venue name
                venueIds.append(venue['id']) # add to list

        return venueIds

    def get_sport(self, sportId) -> Sport:
        mlbdata = self._mlb_adapter_v1.get(endpoint=f'sports/{sportId}')
        if (mlbdata.data['sports'][0]['id'] != sportId):
            raise TheMlbStatsApiException("Bad JSON in response")

        return Sport(**mlbdata.data['sports'][0])

    def get_sports(self) -> List[Sport]:
        # TODO Doc string
        mlbdata = self._mlb_adapter_v1.get(endpoint="sports") # Get All sports
        if 'sports' in mlbdata.data:
            sports = [ Sport(**sport) for sport in mlbdata.data['sports']]
        return sports # return list of all Sport objects

    def get_sport_id(self, sportName) -> List[int]:
        # TODO Doc string
        mlbdata = self._mlb_adapter_v1.get(endpoint=f"sports") # Get All Sports
        sportIds = [] # create empty list
        for sport in mlbdata.data['sports']:
            if sport['name'].lower() == sportName.lower(): # Match sport name
                sportIds.append(sport['id']) # add to list

        return sportIds


    def get_league(self) -> List[League]:
        pass

    # def get_sports(self) -> List[Sport]:
    #     pass

    def get_leagues(self) -> List[League]:
        pass
