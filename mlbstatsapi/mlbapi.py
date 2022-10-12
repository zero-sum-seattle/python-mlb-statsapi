import logging
import datetime 
from typing import List, Union
from mlbstatsapi.models.people import Person, Player, Coach
from mlbstatsapi.models.teams import Team
from mlbstatsapi.models.sports import Sport
from mlbstatsapi.models.leagues import League
from mlbstatsapi.models.game import Game
from mlbstatsapi.models.venues import Venue
from mlbstatsapi.models.divisions import Division
from mlbstatsapi.models.schedules import Schedule
from mlbstatsapi.models.attendances import Attendance
from .mlbdataadapter import TheMlbStatsApiException
from .mlbdataadapter import MlbDataAdapter, MlbResult


class Mlb:
    def __init__(self, hostname: str = 'statsapi.mlb.com', ver: str = 'v1', logger: logging.Logger = None):
        self._mlb_adapter_v1 = MlbDataAdapter(hostname, 'v1', logger)
        self._mlb_adapter_v1_1 = MlbDataAdapter(hostname, 'v1.1', logger)

    def get_people(self) -> List[Person]:
        """
        return the all players 

        Returns
        -------
        List[Person]
        """       
        mlbdata = self._mlb_adapter_v1.get(endpoint="sports/1/players") # get all people
        
        if mlbdata.data and ('people' in mlbdata.data and mlbdata.data['people']):
            people = [ Person(**person) for person in mlbdata.data['people'] ]
        
        return people # return list of people objects

    def get_person(self, playerId) -> Union[Person, None]:
        """
        return a person

        Parameters
        ----------
        playerId : int
            Person id 

        Returns
        -------
        Person
        """       
        mlbdata = self._mlb_adapter_v1.get(endpoint=f"people/{playerId}") # Get player
        
        if mlbdata.data and ('people' in mlbdata.data and mlbdata.data['people']):
            for person in mlbdata.data['people']:
                return Person(**person)

    def get_people_id(self, fullName) -> List[int]:
        """
        return a person Id

        Parameters
        ----------
        fullName : str
            Person full name

        Returns
        -------
        List[int]
        """        
        mlbdata = self._mlb_adapter_v1.get(endpoint=f"sports/1/players") # Get All People: players
        playerIds = [] # create empty list

        for person in mlbdata.data['people']:
            if person['fullName'] == fullName: # Match person fullName
                playerIds.append(person['id']) # add to list

        return playerIds

    def get_teams(self) -> List[Team]:
        """
        return the all Teams 

        Returns
        -------
        List[Team]
        """         
        mlbdata = self._mlb_adapter_v1.get(endpoint="teams?sportId=1") # Get all major league teams
        
        if mlbdata.data and ('teams' in mlbdata.data and mlbdata.data['teams']):
            teams = [ Team(**team) for team in mlbdata.data['teams']]

        return teams # return list of all Team objects

    def get_team(self, teamId) -> Union[Team, None]:
        """
        return the Team

        Parameters
        ----------
        teamId : int
            Team id 

        Returns
        -------
        Team
        """       
        mlbdata = self._mlb_adapter_v1.get(endpoint=f"teams/{teamId}")
        
        if mlbdata.data and ('teams' in mlbdata.data and mlbdata.data['teams']):
            for team in mlbdata.data['teams']:
                return Team(**team) 

    def get_team_id(self, teamName) -> List[int]:
        """
        return a team Id

        Parameters
        ----------
        teamName : str
            Teams name

        Returns
        -------
        List[ints]
        """       
        mlbdata = self._mlb_adapter_v1.get(endpoint="teams") # Get all Teams
        teamIds = [] # create empty list
        
        if mlbdata.data and ('teams' in mlbdata.data and mlbdata.data['teams']):
            for team in mlbdata.data['teams']:
                if team['teamName'] == teamName: # find matching Team Name
                    teamIds.append(team['id']) # append match id
        
        return teamIds

    def get_team_roster(self, teamId) -> List[Player]:
        """
        return the team player roster

        Parameters
        ----------
        teamId : int
            Team id 

        Returns
        -------
        List[Player]
        """
        mlbdata = self._mlb_adapter_v1.get(endpoint=f"teams/{teamId}/roster")
        players = []
        # if mlbdata is not empty, and 'roster' key is in mlbdata.data and mlbdata.data['roster] is not empty list
        if mlbdata.data and ('roster' in mlbdata.data and mlbdata.data['roster']):
            # for player in mlbdata.data['roster']
            for player in mlbdata.data['roster']:
                # remove person key and return value to person
                person = player.pop('person')
                # create Player, and unpack player and person
                players.append(Player(**{**player, **person}))
    
        return players

    def get_team_coaches(self, teamId) -> List[Coach]:
        """
        return the team coach roster

        Parameters
        ----------
        teamId : int
            Team id 

        Returns
        -------
        List[Coach]
        """       
        mlbdata = self._mlb_adapter_v1.get(endpoint=f"teams/{teamId}/coaches")
        coaches = []

        # if mlbdata is not empty, and 'roster' key is in mlbdata.data and mlbdata.data['roster] is not empty list
        if mlbdata.data and ('roster' in mlbdata.data and mlbdata.data['roster']):
            # for player in mlbdata.data['roster']
            for coach in mlbdata.data['roster']:
                # remove person key and return value to person
                person = coach.pop('person')
                # create Player, and unpack player and person
                coaches.append(Coach(**{**coach, **person}))

        return coaches

    def get_schedule(self, startDate = datetime.date.today().strftime("%Y-%m-%d"), 
                     endDate = datetime.date.today().strftime("%Y-%m-%d")) -> Schedule:
        # TODO Doc string
        mlbdata = self._mlb_adapter_v1.get(endpoint=f"schedule?sportId=1&startDate={startDate}&endDate={endDate}") # Get schedule
        return Schedule(**mlbdata.data)

    def get_schedule_today(self) -> Schedule:
        # TODO Doc string
        return self.get_schedule()

    def get_schedule_date(self, date) -> Schedule:
        # TODO Doc string
        return self.get_schedule(startDate = date, endDate = date)

    def get_schedule_date_range(self, startDate, endDate) -> Schedule: 
        # TODO Doc string
        return self.get_schedule(startDate = startDate, endDate = endDate)

    def get_game(self, gameId) -> Game:
        # TODO Doc string
        mlbdata = self._mlb_adapter_v1_1.get(endpoint=f'game/{gameId}/feed/live') # Get game
        
        if mlbdata.data and ('gamePk' in mlbdata.data and mlbdata.data['gamePk'] != gameId): # If game id eccepted but not valid
            raise TheMlbStatsApiException("Bad JSON in response")
        
        return Game(**mlbdata.data)

    def get_todays_games(self) -> List[int]:
        # TODO Doc string
        todaysGames = self.get_schedule_today()
        todaysGamesIds = []
        
        if todaysGames.dates and len(todaysGames.dates) == 1:
            if todaysGames.dates[0].date == datetime.date.today().strftime("%Y-%m-%d"):
                if todaysGames.dates[0].games:
                    for game in todaysGames.dates[0].games:
                        todaysGamesIds.append(game.gamePk) # Append game Ids
        
        return todaysGamesIds

    def get_venue(self, venueId) -> Union[Venue, None]:
        """
        return venue

        Returns
        -------
        Venue
        """             
        mlbdata = self._mlb_adapter_v1.get(endpoint=f'venues/{venueId}?hydrate=location,fieldInfo,timezone')
        
        if mlbdata.data and ('venue' in mlbdata.data and mlbdata.data['venues']):
            for venue in mlbdata.data['venues']:
                return Venue(**venue)

    def get_venues(self) -> List[Venue]:
        """
        return all venues

        Returns
        -------
        List[Venue]
        """             
        mlbdata = self._mlb_adapter_v1.get(endpoint="venues") # Get All venuess
        
        if mlbdata.data and ('venue' in mlbdata.data and mlbdata.data['venues']):
            venues = [ Venue(**venue) for venue in mlbdata.data['venues']]
        
        return venues # return list of all Venue objects

    def get_venue_id(self, venueName) -> List[int]:
        """
        return venue id

        Parameters
        ----------
        venueName : str
            venue name 

        Returns
        -------
        List[int]
        """        
        mlbdata = self._mlb_adapter_v1.get(endpoint=f"venues") # Get All Venues
        venueIds = [] # create empty list
        
        if mlbdata.data and ('venue' in mlbdata.data and mlbdata.data['venues']):
            for venue in mlbdata.data['venues']:
                if venue['name'].lower() == venueName.lower(): # Match venue name
                    venueIds.append(venue['id']) # add to list
        
        return venueIds

    def get_sport(self, sportId) -> Union[Sport, None]:
        """
        return sport

        Returns
        -------
        Sport
        """             
        mlbdata = self._mlb_adapter_v1.get(endpoint=f'sports/{sportId}')

        if mlbdata.data and ('sports' in mlbdata.data and mlbdata.data['sports']):
            for sport in mlbdata.data['sports']:
                return Sport(**sport)

    def get_sports(self) -> List[Sport]:
        """
        return all sports

        Returns
        -------
        List[Sport]
        """          
        mlbdata = self._mlb_adapter_v1.get(endpoint="sports") # Get All sports
        
        if mlbdata.data and ('sports' in mlbdata.data and mlbdata.data['sports']):
            sports = [ Sport(**sport) for sport in mlbdata.data['sports']]
        
        return sports # return list of all Sport objects

    def get_sport_id(self, sportName) -> List[int]:
        """
        return Sport id

        Parameters
        ----------
        sportName : str
            Sport name 

        Returns
        -------
        List[int]
        """          
        mlbdata = self._mlb_adapter_v1.get(endpoint=f"sports") # Get All Sports
        sportIds = [] # create empty list

        if mlbdata.data and ('sports' in mlbdata.data and mlbdata.data['sports']):
            for sport in mlbdata.data['sports']:
                if sport['name'].lower() == sportName.lower(): # Match sport name
                    sportIds.append(sport['id']) # add to list

        return sportIds

    def get_league(self, leagueId) -> Union[League, None]:
        """
        return divison

        Returns
        -------
        League
        """   
        mlbdata = self._mlb_adapter_v1.get(endpoint=f'league/{leagueId}')


        if mlbdata.data and ('leagues' in mlbdata.data and mlbdata.data['leagues']):
            for league in mlbdata.data['leagues']:
                return League(**league)

    def get_leagues(self) -> List[League]:
        """
        return all leagues

        Returns
        -------
        List[League]
        """           
        mlbdata = self._mlb_adapter_v1.get(endpoint="league") # Get All sports
        
        if mlbdata.data and ('leagues' in mlbdata.data and mlbdata.data['leagues']):
            leagues = [ League(**league) for league in mlbdata.data['leagues']]
        
        return leagues # return list of all Sport objects

    def get_league_id(self, leagueName) -> List[League]:
        """
        return league id

        Parameters
        ----------
        leagueName : str
            League name 

        Returns
        -------
        List[int]
        """            
        mlbdata = self._mlb_adapter_v1.get(endpoint=f"league") # Get All divisions
        leagueIds = [] # create empty list

        if mlbdata.data and ('leagues' in mlbdata.data and mlbdata.data['leagues']):
            for league in mlbdata.data['leagues']:
                if league['name'].lower() == leagueName.lower(): # Match division name
                    leagueIds.append(league['id']) # add to list
        
        return leagueIds

    def get_division(self, divisionId) -> Union[Division, None]:
        """
        return the Division

        Parameters
        ----------
        divisonId : int
            Division id 

        Returns
        -------
        Division
        """   
        mlbdata = self._mlb_adapter_v1.get(endpoint=f'divisions/{divisionId}')
        
        if mlbdata.data and ('divisons' in mlbdata.data and mlbdata.data['divisions']):
            for division in mlbdata.data['divisions']:
                return Division(**division)

    def get_divisions(self) -> List[Division]:
        """
        return all divisons

        Returns
        -------
        List[Division]
        """   
        mlbdata = self._mlb_adapter_v1.get(endpoint="divisions") # Get All divisions
        
        if mlbdata.data and ('divisons' in mlbdata.data and mlbdata.data['divisions']):
            divisions = [ Division(**division) for division in mlbdata.data['divisions']]
        
        return divisions # return list of all Division objects

    def get_division_id(self, divisionName) -> List[Division]:
        """
        return divsion id

        Parameters
        ----------
        divisonName : str
            Division name 

        Returns
        -------
        List[int]
        """           
        mlbdata = self._mlb_adapter_v1.get(endpoint=f"divisions") # Get All divisions
        divisionIds = [] # create empty list
        
        if mlbdata.data and ('divisons' in mlbdata.data and mlbdata.data['divisions']):
            for division in mlbdata.data['divisions']:
                if division['name'].lower() == divisionName.lower(): # Match division name
                    divisionIds.append(division['id']) # add to list

        return divisionIds

    def get_attendance(self, teamId=None, leagueId=None, season=None, date=None,
                            leagueListId=None, gameType=None, fields=None) -> Attendance:
        # TODO Doc string
        if not any([teamId, leagueId, leagueListId]):
            raise TheMlbStatsApiException("""Need at least one of the following while
                                            calling get_attendance: teamId, leagueId, 
                                            leagueListId""")

        endpoint = f'attendance?'
        if teamId: endpoint += f'teamId={teamId}'
        if leagueId: endpoint += f'{leagueId}' if endpoint==f'attendance?' else f'&leagueId={leagueId}'
        if leagueListId: endpoint += f'{leagueListId}' if endpoint==f'attendance?' else f'&leagueListId={leagueListId}'
        if season: endpoint += f'&season={season}' 
        if date: endpoint += f'&date={date}'
        if gameType: endpoint += f'&gameType={gameType}'
        if fields: endpoint += f'&fields={fields}'
        
        mlbdata = self._mlb_adapter_v1.get(endpoint)
        if not mlbdata.data['records']:
            raise TheMlbStatsApiException("Bad JSON in response")
        return Attendance(**mlbdata.data)

    def get_object(self, object):
        # TODO Doc string
        get_func = getattr(self, 'get_'+str(object.__class__.__name__).lower())
        return get_func(object.id)
