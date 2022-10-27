import logging
import datetime
import inspect
import importlib
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
from mlbstatsapi.models.stats import Stats

from .mlbdataadapter import TheMlbStatsApiException
from .mlbdataadapter import MlbDataAdapter

from .mlb import _transform_mlbdata


class Mlb:
    def __init__(self, hostname: str = 'statsapi.mlb.com', ver: str = 'v1', logger: logging.Logger = None):
        self._mlb_adapter_v1 = MlbDataAdapter(hostname, 'v1', logger)
        self._mlb_adapter_v1_1 = MlbDataAdapter(hostname, 'v1.1', logger)
        self._logger = logger or logging.getLogger(__name__)
        self._logger.setLevel(logging.DEBUG) 

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

    def get_person(self, playerid) -> Union[Person, None]:
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
        mlbdata = self._mlb_adapter_v1.get(endpoint=f"people/{playerid}") # Get player
        
        if ('people' in mlbdata.data and mlbdata.data['people']):
            for person in mlbdata.data['people']:
                return Person(**person)

    def get_people_id(self, fullname) -> List[int]:
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
                if person['fullname'].lower() == fullname.lower(): # Match person fullName
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

    def get_team(self, teamid) -> Union[Team, None]:
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
        mlbdata = self._mlb_adapter_v1.get(endpoint=f"teams/{teamid}")

        if ('teams' in mlbdata.data and mlbdata.data['teams']):
            for team in mlbdata.data['teams']:
                return Team(**team) 

    def get_team_id(self, teamname) -> List[int]:
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
                if team['teamname'].lower() == teamname.lower(): # find matching Team Name
                    teamIds.append(team['id']) # append match id
        
        return teamIds

    def get_team_roster(self, teamid) -> List[Player]:
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
        mlbdata = self._mlb_adapter_v1.get(endpoint=f"teams/{teamid}/roster")
        players = []

        if ('roster' in mlbdata.data and mlbdata.data['roster']):
            for player in mlbdata.data['roster']:
                players.append(Player(**_transform_mlbdata(player, ['person'])))

        return players

    def get_team_coaches(self, teamid) -> List[Coach]:
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
        mlbdata = self._mlb_adapter_v1.get(endpoint=f"teams/{teamid}/coaches")
        coaches = []

        if ('roster' in mlbdata.data and mlbdata.data['roster']):
            for coach in mlbdata.data['roster']:               
                coaches.append(Coach(**_transform_mlbdata(coach, ['person'])))

        return coaches

    def get_schedule(self, startdate = datetime.date.today().strftime("%Y-%m-%d"), 
                     enddate = datetime.date.today().strftime("%Y-%m-%d")) -> Union[Schedule, None]:
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
        mlbdata = self._mlb_adapter_v1.get(endpoint=f"schedule?sportId=1&startDate={startdate}&endDate={enddate}") # Get schedule

        # if mlbdata is not empty, and 'dates' key is in mlbdata.data and mlbdata.data['dates] can sometimes be an empty list
        # when there are no scheduled game for the date(s). Only check for existance 'dates' key for this reason.
        if ('dates' in mlbdata.data):
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
        return self.get_schedule(startdate = date, enddate = date)

    def get_schedule_date_range(self, startdate, enddate) -> Union[Schedule, None]: 
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
        return self.get_schedule(startdate = startdate, enddate = enddate)

    def get_game(self, gameid) -> Union[Game, None]:
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
        mlbdata = self._mlb_adapter_v1_1.get(endpoint=f'game/{gameid}/feed/live') # Get game
        
        if ('gamepk' in mlbdata.data and mlbdata.data['gamepk'] == gameid):
            return Game(**mlbdata.data)

    def get_game_playByPlay(self, gameid) -> Union[Plays, None]:
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
        mlbdata = self._mlb_adapter_v1.get(endpoint=f'game/{gameid}/playByPlay') # Get games boxscore
        if ('allplays' in mlbdata.data and mlbdata.data['allplays']): # if teams in mlbdata
            return Plays(**mlbdata.data)

    def get_game_linescore(self, gameid) -> Union[Linescore, None]:
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
        mlbdata = self._mlb_adapter_v1.get(endpoint=f'game/{gameid}/linescore') # Get games boxscore
        if ('teams' in mlbdata.data and mlbdata.data['teams']): # if teams in mlbdata
            return Linescore(**mlbdata.data)

    def get_game_boxscore(self, gameid) -> Union[BoxScore, None]:
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
        mlbdata = self._mlb_adapter_v1.get(endpoint=f'game/{gameid}/boxscore') # Get games boxscore
        if ('teams' in mlbdata.data and mlbdata.data['teams']): # if teams in mlbdata
            return BoxScore(**mlbdata.data)

    def get_game_ids(self, date, abstractgamestate=None) -> List[int]:
        """
        return game ids for a specific date and game status

        Parameters
        ----------
        date : str 'yyyy-mm-dd'
            Date
        abstractgamestate : str
            Game status type to search for, abstractgamestate

        Returns
        -------
        List[int]
        """  
        scheduledgames = self.get_schedule(date, date)
        gamesids = []
        
        # If get_schedule_today is successful and returns a schedule object
        if scheduledgames:
            # If only one date is in dates. Zero would mean no games today. 
            if scheduledgames.dates and len(scheduledgames.dates) == 1:
                # If the single date is todays date
                if scheduledgames.dates[0].date == date:
                    # If todays date has games. A date could have no games and events.
                    if scheduledgames.dates[0].games:
                        # Collect all the game Id's for todays games
                        for game in scheduledgames.dates[0].games:
                            # If abstractGameState param provided only get games that match
                            if not abstractgamestate or (game.status.abstractgamestate == abstractgamestate):
                                gamesids.append(game.gamepk) # Append game Ids
            
            return gamesids

    def get_todays_game_ids(self, abstractgamestate=None) -> List[int]:
        """
        return game ids for todays date

        Parameters
        ----------
        abstractgamestate : str
            Game status type to search for, abstractgamestate

        Returns
        -------
        List[int]
        """  
        todaysdate = datetime.date.today()
        todaysgames = self.get_game_ids(todaysdate.strftime("%Y-%m-%d"), abstractgamestate)
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

    def get_venue(self, venueid) -> Union[Venue, None]:
        """
        return venue

        Parameters
        ----------
        venueid : int

        Returns
        -------
        Venue
        """             
        mlbdata = self._mlb_adapter_v1.get(endpoint=f'venues/{venueid}?hydrate=location,fieldInfo,timezone')
        
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

    def get_venue_id(self, venuename) -> List[int]:
        """
        return venue id

        Parameters
        ----------
        venuename : str
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
                if venue['name'].lower() == venuename.lower():
                    venueIds.append(venue['id']) # add to list

        return venueIds

    def get_sport(self, sportid) -> Union[Sport, None]:
        """
        return sport

        Parameters
        ----------
        sportId : int 


        Returns
        -------
        Sport
        """             
        mlbdata = self._mlb_adapter_v1.get(endpoint=f'sports/{sportid}')

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

    def get_sport_id(self, sportname) -> List[int]:
        """
        return Sport id

        Parameters
        ----------
        sportname : str
            Sport name 

        Returns
        -------
        List[int]
        """          
        mlbdata = self._mlb_adapter_v1.get(endpoint=f"sports") # Get All Sports
        sportIds = [] # create empty list

        if ('sports' in mlbdata.data and mlbdata.data['sports']):
            for sport in mlbdata.data['sports']:
                if sport['name'].lower() == sportname.lower(): # Match sport name
                    sportIds.append(sport['id']) # add to list

        return sportIds

    def get_league(self, leagueid) -> Union[League, None]:
        """
        return league

        Returns
        -------
        League
        """   
        mlbdata = self._mlb_adapter_v1.get(endpoint=f'league/{leagueid}')

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

    def get_league_id(self, leaguename) -> List[League]:
        """
        return league id

        Parameters
        ----------
        leaguename : str
            League name 

        Returns
        -------
        List[int]
        """            
        mlbdata = self._mlb_adapter_v1.get(endpoint=f"league") # Get All divisions
        leagueIds = [] # create empty list

        if ('leagues' in mlbdata.data and mlbdata.data['leagues']):
            for league in mlbdata.data['leagues']:
                if league['name'].lower() == leaguename.lower(): # Match division name
                    leagueIds.append(league['id']) # add to list
        
        return leagueIds

    def get_division(self, divisionid) -> Union[Division, None]:
        """
        return the Division

        Parameters
        ----------
        divisonid : int
            Division id 

        Returns
        -------
        Division
        """   
        mlbdata = self._mlb_adapter_v1.get(endpoint=f'divisions/{divisionid}')
        
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

    def get_division_id(self, divisionname) -> List[Division]:
        """
        return divsion id

        Parameters
        ----------
        divisonname : str
            Division name 

        Returns
        -------
        List[int]
        """           
        mlbdata = self._mlb_adapter_v1.get(endpoint=f"divisions") # Get All divisions
        divisionIds = [] # create empty list
        
        if ('divisions' in mlbdata.data and mlbdata.data['divisions']):
            for division in mlbdata.data['divisions']:
                if division['name'].lower() == divisionname.lower(): # Match division name
                    divisionIds.append(division['id']) # add to list

        return divisionIds

    def get_attendance(self, teamid=None, leagueid=None, season=None, date=None,
                            leaguelistid=None, gametype=None, fields=None) -> Union[Attendance, None]:
        """
        return attendance

        Required Parameters (atleast one)
        ----------
        teamid : int
            Team id number
        leagueid : int
            League id number
        leaguelistid : int
            Not sure 

        Parameters
        ----------
        season : int
            Season year number format yyyy
        date : str 'yyyy-mm-dd'
            Date
        gametype : str
            Game type
        fields : ?

        Returns
        -------
        Attendance
        """   
        if not any([teamid, leagueid, leaguelistid]):
            return

        endpoint = f'attendance?'
        if teamid: endpoint += f'teamId={teamid}'
        if leagueid: endpoint += f'{leagueid}' if endpoint==f'attendance?' else f'&leagueId={leagueid}'
        if leaguelistid: endpoint += f'{leaguelistid}' if endpoint==f'attendance?' else f'&leagueListId={leaguelistid}'
        if season: endpoint += f'&season={season}' 
        if date: endpoint += f'&date={date}'
        if gametype: endpoint += f'&gameType={gametype}'
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

    def get_stats(self, object : Union[object, dict], params : dict) -> List[Stats]:
        """
        return a split object 

        Parameters
        ----------
        object : mlb object
            mlb object or dict e.g Team, Player, Person
        params : dict
            dict of params to pass e.g { 'stats': [ "seasonAdvanced", "season" ], 'group': 'hitting' }

        Returns
        -------
        Stats
        """  
        mlbdata = self._mlb_adapter_v1.get(endpoint=f"{object.mlb_class}/{object.id}/stats", ep_params=params) # Get All divisions        
        splits = [] 
        stat_log_type = [ 'playLog', 'pitchLog' ]


        if ('stats' in mlbdata.data and mlbdata.data['stats']):
            for stats in mlbdata.data['stats']:
                # set stat_group and stat_type
                # default to stats if no group present
                stat_group = stats['group']['displayname'] if 'group' in stats else "stats"
                stat_type = stats['type']['displayname'] if 'type' in stats else None

                # convert string base on stat_group to module name
                stat_module = f"mlbstatsapi.models.stats.{stat_group}"
                stat_module = importlib.import_module(stat_module)

                # if splits is in stats and splits not empty
                if ('splits' in stats and stats['splits']):

                    # loop through classes found in stat_module 
                    for name, obj in inspect.getmembers(stat_module):

                        # if obj has _type attr and stat_type matches class var
                        if inspect.isclass(obj) and (hasattr(obj, 'type_') and stat_type in obj.type_):

                            # loop through json in splits
                            for stat in stats['splits']:
                                if 'stat' in stat:
                                    if stat_type in stat_log_type: # check for log stat type
                                        stat = _transform_mlbdata(stat, [{'stat':'play'}])
                                        #self._logger.error(msg=(stat)) # log error JSON

                                    else:

                                        stat = _transform_mlbdata(stat, 'stat')
                                
                                # log error JSON
                                #self._logger.error(msg=(stat_type, stat_group, obj, name)) 
                                # create object from stat
                                splits.append(obj(stat_type=stat_type, stat_group=stat_group, **stat))

            # return splits
            return splits
