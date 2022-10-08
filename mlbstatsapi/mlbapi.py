import logging
import datetime 
from typing import List
from mlbstatsapi.models.people import Person
from mlbstatsapi.models.teams import Team
from mlbstatsapi.models.sports import Sport
from mlbstatsapi.models.leagues import League
from mlbstatsapi.models.game import Game
from mlbstatsapi.models.venues import Venue
from mlbstatsapi.models.divisions import Division
from mlbstatsapi.models.schedules import Schedule
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

    def get_schedule(self, startDate = datetime.date.today().strftime("%Y-%m-%d"), 
                           endDate = datetime.date.today().strftime("%Y-%m-%d")) -> Schedule:
        mlbdata = self._mlb_adapter_v1.get(endpoint=f"schedule?sportId=1&startDate={startDate}&endDate={endDate}") # Get schedule
        return Schedule(**mlbdata.data)

    def get_schedule_today(self) -> Schedule:
        return self.get_schedule()

    def get_schedule_date(self, date) -> Schedule:
        return self.get_schedule(startDate = date, endDate = date)

    def get_schedule_date_range(self, startDate, endDate) -> Schedule: 
        return self.get_schedule(startDate = startDate, endDate = endDate)

    def get_game(self, gameId) -> Game:
        # TODO Doc string
        mlbdata = self._mlb_adapter_v1_1.get(endpoint=f'game/{gameId}/feed/live') # Get game
        if (mlbdata.data['gamePk'] != gameId): # If game id eccepted but not valid
            raise TheMlbStatsApiException("Bad JSON in response")
        return Game(**mlbdata.data)

    def get_todays_games(self) -> list[int]:
        todaysGames = self.get_schedule_today()
        todaysGamesIds = []
        if todaysGames.dates and len(todaysGames.dates) == 1:
            if todaysGames.dates[0].date == datetime.date.today().strftime("%Y-%m-%d"):
                if todaysGames.dates[0].games:
                    for game in todaysGames.dates[0].games:
                        todaysGamesIds.append(game.gamePk) # Append game Ids
        return todaysGamesIds

    def get_venue(self, venueId) -> Venue:
        # TODO Doc string
        mlbdata = self._mlb_adapter_v1.get(endpoint=f'venues/{venueId}?hydrate=location,fieldInfo,timezone')
        if (mlbdata.data['venues'][0]['id'] != venueId):
            raise TheMlbStatsApiException("Bad JSON in response")
        return Venue(**mlbdata.data['venues'][0])

    def get_venues(self) -> List[Venue]:
        # TODO Doc string
        mlbdata = self._mlb_adapter_v1.get(endpoint="venues") # Get All venuess
        if 'venues' in mlbdata.data:
            venues = [ Venue(**venue) for venue in mlbdata.data['venues']]
        return venues # return list of all Venue objects

    def get_venue_id(self, venueName) -> List[int]:
        # TODO Doc string
        mlbdata = self._mlb_adapter_v1.get(endpoint=f"venues") # Get All Venues
        venueIds = [] # create empty list
        if 'venues' in mlbdata.data:
            for venue in mlbdata.data['venues']:
                if venue['name'].lower() == venueName.lower(): # Match venue name
                    venueIds.append(venue['id']) # add to list
        return venueIds

    def get_sport(self, sportId) -> Sport:
        # TODO Doc string
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

    def get_league(self, leagueId) -> League:
        # TODO Doc string
        mlbdata = self._mlb_adapter_v1.get(endpoint=f'league/{leagueId}')
        if (mlbdata.data['leagues'][0]['id'] != leagueId):
            raise TheMlbStatsApiException("Bad JSON in response")
        return League(**mlbdata.data['leagues'][0])

    def get_leagues(self) -> List[League]:
        # TODO Doc string
        mlbdata = self._mlb_adapter_v1.get(endpoint="league") # Get All sports
        if 'leagues' in mlbdata.data:
            leagues = [ League(**league) for league in mlbdata.data['leagues']]
        return leagues # return list of all Sport objects

    def get_league_id(self, leagueName) -> List[League]:
        # TODO Doc string
        mlbdata = self._mlb_adapter_v1.get(endpoint=f"league") # Get All divisions
        leagueIds = [] # create empty list
        for league in mlbdata.data['leagues']:
            if league['name'].lower() == leagueName.lower(): # Match division name
                leagueIds.append(league['id']) # add to list
        return leagueIds

    def get_division(self, divisionId) -> Division:
        mlbdata = self._mlb_adapter_v1.get(endpoint=f'divisions/{divisionId}')
        if (mlbdata.data['divisions'][0]['id'] != divisionId):
            raise TheMlbStatsApiException("Bad JSON in response")
        return Division(**mlbdata.data['divisions'][0])

    def get_divisions(self) -> List[Division]:
        mlbdata = self._mlb_adapter_v1.get(endpoint="divisions") # Get All divisions
        if 'divisions' in mlbdata.data:
            divisions = [ Division(**division) for division in mlbdata.data['divisions']]
        return divisions # return list of all Division objects

    def get_division_id(self, divisionName) -> List[Division]:
        # TODO Doc string
        mlbdata = self._mlb_adapter_v1.get(endpoint=f"divisions") # Get All divisions
        divisionIds = [] # create empty list
        for division in mlbdata.data['divisions']:
            if division['name'].lower() == divisionName.lower(): # Match division name
                divisionIds.append(division['id']) # add to list
        return divisionIds