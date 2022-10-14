import logging
import datetime 
from typing import List, Union
from mlbstatsapi.models.people import Person, Player, Coach
from mlbstatsapi.models.teams import Team
from mlbstatsapi.models.sports import Sport
from mlbstatsapi.models.leagues import League
from mlbstatsapi.models.game import Game, Plays, Linescore, BoxScore
from mlbstatsapi.models.venues import Venue
from mlbstatsapi.models.divisions import Division
from mlbstatsapi.models.schedules import Schedule
from mlbstatsapi.models.attendances import Attendance
from .mlbdataadapter import TheMlbStatsApiException
from .mlbdataadapter import MlbDataAdapter

from .mlb import _transform_mlbdata


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
        
        if ('people' in mlbdata.data and mlbdata.data['people']):
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
        
        if ('people' in mlbdata.data and mlbdata.data['people']):
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

        # if mlbdata is not empty, and 'people' key is in mlbdata.data and mlbdata.data['people'] is not empty list
        if ('people' in mlbdata.data and mlbdata.data['people']): 
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
        
        if ('teams' in mlbdata.data and mlbdata.data['teams']):
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

        if ('teams' in mlbdata.data and mlbdata.data['teams']):
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
        
        if ('teams' in mlbdata.data and mlbdata.data['teams']):
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

        if ('roster' in mlbdata.data and mlbdata.data['roster']):
            for player in mlbdata.data['roster']:
                players.append(Player(**_transform_mlbdata(player, ['person'])))

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

        if ('roster' in mlbdata.data and mlbdata.data['roster']):
            for coach in mlbdata.data['roster']:               
                coaches.append(Coach(**_transform_mlbdata(coach, ['person'])))

        return coaches

    def get_schedule(self, startDate = datetime.date.today().strftime("%Y-%m-%d"), 
                     endDate = datetime.date.today().strftime("%Y-%m-%d")) -> Union[Schedule, None]:
        """
        return the schedule created from the included params.

        Calling get_schedule without startDate or endDate results in a schedule returned
        for todays date. Calling with startDate and endDate as the same date returns a
        schedule for just that desired date. Different results in the schedule for multiple
        days.

        Parameters
        ----------
        startDate : str "yyyy-mm-dd"
            Start date
        endDate : str "yyyy-mm-dd"
            End date

        Returns
        -------
        Schedule
        """     
        mlbdata = self._mlb_adapter_v1.get(endpoint=f"schedule?sportId=1&startDate={startDate}&endDate={endDate}") # Get schedule

        # if mlbdata is not empty, and 'dates' key is in mlbdata.data and mlbdata.data['dates] is not empty list
        if ('dates' in mlbdata.data and mlbdata.data['dates']):
            return Schedule(**mlbdata.data)

    def get_schedule_today(self) -> Union[Schedule, None]:        
        """
        return the schedule for today

        Returns
        -------
        Schedule
        """    
        return self.get_schedule()

    def get_schedule_date(self, date) -> Union[Schedule, None]:
        """
        return the schedule for a specific date

        Parameters
        ----------
        date : str "yyyy-mm-dd"
            Date

        Returns
        -------
        Schedule
        """  
        return self.get_schedule(startDate = date, endDate = date)

    def get_schedule_date_range(self, startDate, endDate) -> Union[Schedule, None]: 
        """
        return the schedule for a range of dates

        Parameters
        ----------
        startDate : str "yyyy-mm-dd"
            Start date
        endDate : str "yyyy-mm-dd"
            End date

        Returns
        -------
        Schedule
        """  
        return self.get_schedule(startDate = startDate, endDate = endDate)

    def get_game(self, gameId) -> Union[Game, None]:
        """
        return the game for a specific game id

        Parameters
        ----------
        gameId : int
            Game id number

        Returns
        -------
        Game
        """  
        mlbdata = self._mlb_adapter_v1_1.get(endpoint=f'game/{gameId}/feed/live') # Get game
        
        if ('gamePk' in mlbdata.data and mlbdata.data['gamePk'] == gameId):
            return Game(**mlbdata.data)

    def get_game_playByPlay(self, gameId) -> Union[Plays, None]:
        """
        return the playbyplay of a game for a specific game id

        Parameters
        ----------
        gameId : int
            Game id number

        Returns
        -------
        Plays
        """  
        mlbdata = self._mlb_adapter_v1.get(endpoint=f'game/{gameId}/playByPlay') # Get games boxscore
        if ('allPlays' in mlbdata.data and mlbdata.data['allPlays']): # if teams in mlbdata
            return Plays(**mlbdata.data)

    def get_game_linescore(self, gameId) -> Union[Linescore, None]:
        """
        return the Linescore of a game for a specific game id

        Parameters
        ----------
        gameId : int
            Game id number

        Returns
        -------
        Linescore
        """  
        mlbdata = self._mlb_adapter_v1.get(endpoint=f'game/{gameId}/linescore') # Get games boxscore
        if ('teams' in mlbdata.data and mlbdata.data['teams']): # if teams in mlbdata
            return Linescore(**mlbdata.data)

    def get_game_boxscore(self, gameId) -> Union[BoxScore, None]:
        """
        return the boxscore of a game for a specific game id

        Parameters
        ----------
        gameId : int
            Game id number

        Returns
        -------
        BoxScore
        """  
        mlbdata = self._mlb_adapter_v1.get(endpoint=f'game/{gameId}/boxscore') # Get games boxscore
        if ('teams' in mlbdata.data and mlbdata.data['teams']): # if teams in mlbdata
            return BoxScore(**mlbdata.data)

    def get_game_ids(self, date, abstractGameState=None) -> List[int]:
        """
        return game ids for a specific date and game status

        Parameters
        ----------
        date : str 'yyyy-mm-dd'
            Date
        abstractGameState : str
            Game status type to search for, abstractGameState

        Returns
        -------
        List[int]
        """  
        scheduledGames = self.get_schedule(date, date)
        gamesIds = []
        
        # If get_schedule_today is successful and returns a schedule object
        if scheduledGames:
            # If only one date is in dates. Zero would mean no games today. 
            if scheduledGames.dates and len(scheduledGames.dates) == 1:
                # If the single date is todays date
                if scheduledGames.dates[0].date == date:
                    # If todays date has games. A date could have no games and events.
                    if scheduledGames.dates[0].games:
                        # Collect all the game Id's for todays games
                        for game in scheduledGames.dates[0].games:
                            # If abstractGameState param provided only get games that match
                            if not abstractGameState or (game.status.abstractGameState == abstractGameState):
                                gamesIds.append(game.gamePk) # Append game Ids
            
            return gamesIds

    def get_todays_game_ids(self, abstractGameState=None) -> List[int]:
        """
        return game ids for todays date

        Parameters
        ----------
        abstractGameState : str
            Game status type to search for, abstractGameState

        Returns
        -------
        List[int]
        """  
        todaysdate = datetime.date.today()
        todaysgames = self.get_game_ids(todaysdate.strftime("%Y-%m-%d"), abstractGameState)
        return todaysgames

    def get_tomorrows_game_ids(self) -> List[int]:
        """
        return game ids for tomorrows date

        Returns
        -------
        List[int]
        """  
        tomorrowsdate = datetime.date.today() + datetime.timedelta(days=1)
        tomorrowsgames = self.get_game_ids(tomorrowsdate.strftime("%Y-%m-%d"))
        return tomorrowsgames

    def get_yesterdays_game_ids(self) -> List[int]:
        """
        return game ids for yesterdays date

        Returns
        -------
        List[int]
        """  
        yesterdaysdate = datetime.date.today() - datetime.timedelta(days=1)
        yesterdaysgames = self.get_game_ids(yesterdaysdate.strftime("%Y-%m-%d"))
        return yesterdaysgames

    def get_venue(self, venueId) -> Union[Venue, None]:
        """
        return venue

        Parameters
        ----------
        venueId : int

        Returns
        -------
        Venue
        """             
        mlbdata = self._mlb_adapter_v1.get(endpoint=f'venues/{venueId}?hydrate=location,fieldInfo,timezone')
        
        if ('venues' in mlbdata.data and mlbdata.data['venues']):
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
        venues = []
        
        if ('venues' in mlbdata.data and mlbdata.data['venues']):
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
        venueIds = [] 
        
        if ('venues' in mlbdata.data and mlbdata.data['venues']):
            for venue in mlbdata.data['venues']:
                # Match venue name
                if venue['name'].lower() == venueName.lower():
                    venueIds.append(venue['id']) # add to list

        return venueIds

    def get_sport(self, sportId) -> Union[Sport, None]:
        """
        return sport

        Parameters
        ----------
        sportId : int 


        Returns
        -------
        Sport
        """             
        mlbdata = self._mlb_adapter_v1.get(endpoint=f'sports/{sportId}')

        if ('sports' in mlbdata.data and mlbdata.data['sports']):
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
        
        if ('sports' in mlbdata.data and mlbdata.data['sports']):
            sports = [ Sport(**sport) for sport in mlbdata.data['sports'] ]

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

        if ('sports' in mlbdata.data and mlbdata.data['sports']):
            for sport in mlbdata.data['sports']:
                if sport['name'].lower() == sportName.lower(): # Match sport name
                    sportIds.append(sport['id']) # add to list

        return sportIds

    def get_league(self, leagueId) -> Union[League, None]:
        """
        return league

        Returns
        -------
        League
        """   
        mlbdata = self._mlb_adapter_v1.get(endpoint=f'league/{leagueId}')

        if ('leagues' in mlbdata.data and mlbdata.data['leagues']):
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
        leagues = []
        
        if ('leagues' in mlbdata.data and mlbdata.data['leagues']):
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

        if ('leagues' in mlbdata.data and mlbdata.data['leagues']):
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
        
        if ('divisions' in mlbdata.data and mlbdata.data['divisions']):
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
        divisions = []
        
        if ('divisions' in mlbdata.data and mlbdata.data['divisions']):
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
        
        if ('divisions' in mlbdata.data and mlbdata.data['divisions']):
            for division in mlbdata.data['divisions']:
                if division['name'].lower() == divisionName.lower(): # Match division name
                    divisionIds.append(division['id']) # add to list

        return divisionIds

    def get_attendance(self, teamId=None, leagueId=None, season=None, date=None,
                            leagueListId=None, gameType=None, fields=None) -> Union[Attendance, None]:
        """
        return attendance

        Required Parameters (atleast one)
        ----------
        teamId : int
            Team id number
        leagueId : int
            League id number
        leagueListId : int
            Not sure 

        Parameters
        ----------
        season : int
            Season year number format yyyy
        date : str 'yyyy-mm-dd'
            Date
        gameType : str
            Game type
        fields : ?

        Returns
        -------
        Attendance
        """   
        if not any([teamId, leagueId, leagueListId]):
            return

        endpoint = f'attendance?'
        if teamId: endpoint += f'teamId={teamId}'
        if leagueId: endpoint += f'{leagueId}' if endpoint==f'attendance?' else f'&leagueId={leagueId}'
        if leagueListId: endpoint += f'{leagueListId}' if endpoint==f'attendance?' else f'&leagueListId={leagueListId}'
        if season: endpoint += f'&season={season}' 
        if date: endpoint += f'&date={date}'
        if gameType: endpoint += f'&gameType={gameType}'
        if fields: endpoint += f'&fields={fields}'
        
        mlbdata = self._mlb_adapter_v1.get(endpoint)

        if ('records' in mlbdata.data and mlbdata.data['records']):   
            return Attendance(**mlbdata.data)

    def get_object(self, object):
        """
        return a hydrated object

        Parameters
        ----------
        object : class
            Object to be hydrated. Can by dry or one that just needs updating
        Returns
        -------
        object
        """   
        get_func = getattr(self, 'get_'+str(object.__class__.__name__).lower())
        hydratedobject = get_func(object.id)
        # If problem with hydrating object, return the old dry object
        return hydratedobject if hydratedobject else object
