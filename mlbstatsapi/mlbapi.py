import logging
import datetime 
from typing import List, Union
from mlbstatsapi.models.people import Person
from mlbstatsapi.models.teams import Team, Roster
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
        if mlbdata and mlbdata.data['people']:
            people = [ Person(**person) for person in mlbdata.data['people'] ]
        return people # return list of people objects

    def get_person(self, playerId) -> Union[Person, None]:
        # TODO Doc string
        mlbdata = self._mlb_adapter_v1.get(endpoint=f"people/{playerId}") # Get player
        if mlbdata and mlbdata.data['people']:
            for person in mlbdata.data['people']:
                return Person(**person)

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
        if mlbdata and mlbdata.data['teams']:
            teams = [ Team(**team) for team in mlbdata.data['teams']]
        return teams # return list of all Team objects

    def get_team(self, teamId) -> Union[Team, None]:
        # TODO Doc string
        mlbdata = self._mlb_adapter_v1.get(endpoint=f"teams/{teamId}")
        if mlbdata and mlbdata.data['teams']:
            for team in mlbdata.data['teams']:
                return Team(**team) 

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

    def get_todays_games(self) -> List[int]:
        todaysGames = self.get_schedule_today()
        todaysGamesIds = []
        if todaysGames.dates and len(todaysGames.dates) == 1:
            if todaysGames.dates[0].date == datetime.date.today().strftime("%Y-%m-%d"):
                if todaysGames.dates[0].games:
                    for game in todaysGames.dates[0].games:
                        todaysGamesIds.append(game.gamePk) # Append game Ids
        return todaysGamesIds

    def get_venue(self, venueId) -> Union[Venue, None]:
        # TODO Doc string
        mlbdata = self._mlb_adapter_v1.get(endpoint=f'venues/{venueId}?hydrate=location,fieldInfo,timezone')
        if mlbdata and mlbdata.data['venues']:
            for venue in mlbdata.data['venues']:
                return Venue(**venue)

    def get_venues(self) -> List[Venue]:
        # TODO Doc string
        mlbdata = self._mlb_adapter_v1.get(endpoint="venues") # Get All venuess
        if mlbdata and mlbdata.data['venues']:
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

    def get_sport(self, sportId) -> Union[Sport, None]:
        # TODO Doc string
        mlbdata = self._mlb_adapter_v1.get(endpoint=f'sports/{sportId}')
        if mlbdata and mlbdata.data['sports']:
            for sport in mlbdata.data['sports']:
                return Sport(**sport)

    def get_sports(self) -> List[Sport]:
        # TODO Doc string
        mlbdata = self._mlb_adapter_v1.get(endpoint="sports") # Get All sports
        if mlbdata and mlbdata.data['sports']:
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

    def get_league(self, leagueId) -> Union[League, None]:
        # TODO Doc string
        mlbdata = self._mlb_adapter_v1.get(endpoint=f'league/{leagueId}')
        if mlbdata and mlbdata.data['leagues']:
            for league in mlbdata.data['leagues']:
                return League(**league)

    def get_leagues(self) -> List[League]:
        # TODO Doc string
        mlbdata = self._mlb_adapter_v1.get(endpoint="league") # Get All sports
        if mlbdata and mlbdata.data['leagues']:
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

    def get_division(self, divisionId) -> Union[Division, None]:
        mlbdata = self._mlb_adapter_v1.get(endpoint=f'divisions/{divisionId}')
        if mlbdata and mlbdata.data['divisions']:
            for division in mlbdata.data['divisions']:
                return Division(**division)

    def get_divisions(self) -> List[Division]:
        mlbdata = self._mlb_adapter_v1.get(endpoint="divisions") # Get All divisions
        if mlbdata and mlbdata.data['divisions']:
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