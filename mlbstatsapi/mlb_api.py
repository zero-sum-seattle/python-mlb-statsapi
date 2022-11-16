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
from mlbstatsapi.models.stats import Splits

from .mlb_dataadapter import MlbDataAdapter
from . import mlb_module


class Mlb:
    """
    A class used to retrive MLB Stats API objects

    ...

    Attributes
    ----------
    hostname: str
        hostname of statsapi.mlb.com
    ver: str
        api version
    logger: logging.Loger
        logger
    """
    def __init__(self, hostname: str = 'statsapi.mlb.com', ver: str = 'v1', logger: logging.Logger = None):
        self._mlb_adapter_v1 = MlbDataAdapter(hostname, 'v1', logger)
        self._mlb_adapter_v1_1 = MlbDataAdapter(hostname, 'v1.1', logger)
        self._logger = logger or logging.getLogger(__name__)
        self._logger.setLevel(logging.DEBUG)

    def get_people(self, sport_id: int = 1) -> List[Person]:
        """
        return the all players for sportid

        Parameters
        ----------
        sport_id : int
            sportid for players defaults to 1

        Returns
        -------
        list
            Returns a list of People

        See Also
        --------
        Mlb.get_person : Return Person from id.
        Mlb.get_people_id : Return person id from name.

        Examples
        --------
        >>> mlb = Mlb()
        >>> mlb.get_people()
        [Person, Person, Person]
        """

        mlb_data = self._mlb_adapter_v1.get(endpoint=f'sports/{sport_id}/players')
        people = []

        if 'people' in mlb_data.data and mlb_data.data['people']:
            people = [Person(**person) for person in mlb_data.data['people']]

        return people

    def get_person(self, player_id) -> Union[Person, None]:
        """
        return a person

        Parameters
        ----------
        player_id : int
            Person id

        Returns
        -------
        Person
            Returns a Person

        See Also
        --------
        Mlb.get_people : Return a list of People from sport id.
        Mlb.get_people_id : Return person id from name.

        Examples
        --------
        >>> mlb = Mlb()
        >>> mlb.get_person(660271)
        Person
        """

        mlb_data = self._mlb_adapter_v1.get(endpoint=f'people/{player_id}')

        if 'people' in mlb_data.data and mlb_data.data['people']:
            for person in mlb_data.data['people']:
                return Person(**person)

    def get_people_id(self, fullname, sport_id: int = 1) -> List[int]:
        """
        return a person Id

        Parameters
        ----------
        fullname : str
            Person full name
        sport_id : int
            sportid for players defaults to 1

        Returns
        -------
        list of int
            Returns a list of person ids

        See Also
        --------
        Mlb.get_people : Return a list of People from sport id.
        Mlb.get_person : Return Person from id.

        Examples
        --------
        >>> mlb = Mlb()
        >>> mlb.get_people_id("Ty France")
        [664034]
        """

        mlb_data = self._mlb_adapter_v1.get(endpoint=f'sports/{sport_id}/players')
        player_ids = []

        if 'people' in mlb_data.data and mlb_data.data['people']:
            for person in mlb_data.data['people']:
                if person['fullname'].lower() == fullname.lower():
                    player_ids.append(person['id'])

        return player_ids

    def get_teams(self, sport_id: int = 1) -> List[Team]:
        """
        return the all Teams

        Parameters
        ----------
        sport_id : int
            sport_id for teams defaults to 1

        Returns
        -------
        list of Teams
            returns a list of teams

        See Also
        --------
        Mlb.get_team : Return a Team from id
        Mlb.get_team_id : Return a list of Teams from sport id.
        Mlb.get_team_coaches : Return a list of Coaches from team id
        Mlb.get_team_roster : Return a list of Players from team id

        Examples
        --------
        >>> mlb = Mlb()
        >>> mlb.get_teams()
        [Team, Team, Team]
        """

        params = {'sportId': sport_id}
        mlb_data = self._mlb_adapter_v1.get(endpoint=f'teams', ep_params=params)
        teams = []

        if 'teams' in mlb_data.data and mlb_data.data['teams']:
            teams = [Team(**team) for team in mlb_data.data['teams']]

        return teams

    def get_team(self, team_id) -> Union[Team, None]:
        """
        return the Team

        Parameters
        ----------
        team_id : int
            Team id

        Returns
        -------
        Team
            returns a Team from team id

        See Also
        --------
        Mlb.get_teams : Return a list of Teams from sport id.
        Mlb.get_team_id : Return a list of team ids from name.
        Mlb.get_team_coaches : Return a list of Coaches from team id
        Mlb.get_team_roster : Return a list of Players from team id

        Examples
        --------
        >>> mlb = Mlb()
        >>> mlb.get_team(133)
        Team
        """

        mlb_data = self._mlb_adapter_v1.get(endpoint=f'teams/{team_id}')

        if 'teams' in mlb_data.data and mlb_data.data['teams']:
            for team in mlb_data.data['teams']:
                return Team(**team)

    def get_team_id(self, team_name) -> List[int]:
        """
        return a team Id

        Parameters
        ----------
        team_name : str
            Teams name

        Returns
        -------
        list of ints
            returns a list of matching team ids

        See Also
        --------
        Mlb.get_teams : Return a list of Teams from sport id.
        Mlb.get_team : Return a Team from id
        Mlb.get_team_coaches : Return a list of Coaches from team id
        Mlb.get_team_roster : Return a list of Players from team id

        Examples
        --------
        >>> mlb = Mlb()
        >>> mlb.get_team_id("Oakland Athletics")
        [133]
        """

        mlb_data = self._mlb_adapter_v1.get(endpoint='teams')
        team_ids = []

        if 'teams' in mlb_data.data and mlb_data.data['teams']:
            for team in mlb_data.data['teams']:
                if team['teamname'].lower() == team_name.lower():
                    team_ids.append(team['id'])

        return team_ids

    def get_team_roster(self, team_id) -> List[Player]:
        """
        return the team player roster

        Parameters
        ----------
        team_id : int
            Team id 

        Returns
        -------
        list of players

        See Also
        --------
        Mlb.get_teams : Return a list of Teams from sport id.
        Mlb.get_team : Return a Team from id
        Mlb.get_team_coaches : Return a list of Coaches from team id

        Examples
        --------
        >>> mlb = Mlb()
        >>> mlb.get_team_roster(133)
        [Player, Player, Player]
        """

        mlb_data = self._mlb_adapter_v1.get(endpoint=f'teams/{team_id}/roster')
        players = []

        if 'roster' in mlb_data.data and mlb_data.data['roster']:
            for player in mlb_data.data['roster']:
                players.append(Player(**mlb_module.merge_keys(player, ['person'])))

        return players

    def get_team_coaches(self, team_id) -> List[Coach]:
        """
        return the team coach roster

        Parameters
        ----------
        team_id : int
            Team id 

        Returns
        -------
        list of Coaches
            returns a list of Coaches

        See Also
        --------
        Mlb.get_teams : Return a list of Teams from sport id.
        Mlb.get_team : Return a Team from id
        Mlb.get_team_roster : Return a list of Players from team id
        
        Examples
        --------
        >>> mlb = Mlb()
        >>> mlb.get_team_coaches(133)
        [Coach, Coach, Coach]
        """

        mlb_data = self._mlb_adapter_v1.get(endpoint=f'teams/{team_id}/coaches')
        coaches = []

        if 'roster' in mlb_data.data and mlb_data.data['roster']:
            for coach in mlb_data.data['roster']:
                coaches.append(Coach(**mlb_module.merge_keys(coach, ['person'])))

        return coaches

    def get_schedule(self, start_date: str = None, end_date: str = None, sport_id: int = 1) -> Union[Schedule, None]:
        """
        return the schedule created from the included params.

        Calling get_schedule without startDate or endDate results in a schedule returned
        for todays date. Calling with startDate and endDate as the same date returns a
        schedule for just that desired date. Different results in the schedule for multiple
        days.

        Parameters
        ----------
        start_date : str "yyyy-mm-dd"
            Start date
        end_date : str "yyyy-mm-dd"
            End date
        spord_id : int
            spord id of schedule defaults to 1

        Returns
        -------
        Schedule
            returns the Schedule for the date

        See Also
        --------
        Mlb.get_schedule_today : Return schedule for today
        Mlb.get_schedule_date : Return schedule for date
        Mlb.get_schedule_date_range : Return schedule between date

        Examples
        --------
        >>> mlb = Mlb()
        >>> mlb.get_schedule(start_date="2021-08-01", end_date="2021-08-11")
        Schedule

        """

        # default to today if not set
        start_date = datetime.date.today().strftime("%Y-%m-%d") if start_date is None else start_date
        end_date = datetime.date.today().strftime("%Y-%m-%d") if end_date is None else end_date

        params = {'sportId': sport_id, 'startDate': start_date, 'endDate': end_date}

        mlb_data = self._mlb_adapter_v1.get(endpoint='schedule', ep_params=params)

        # if mlb_data is not empty, and 'dates' key is in mlb_data.data and mlb_data.data['dates]
        # can sometimes be an empty list when there are no scheduled game for the date(s).
        # Only check for existance 'dates' key for this reason.

        if 'dates' in mlb_data.data and mlb_data.data['dates']:
            return Schedule(**mlb_data.data)

    def get_schedule_today(self, sport_id: int = 1) -> Union[Schedule, None]:        
        """
        return the schedule for today

        Parameters
        ----------
        spord_id : int
            sport id of the schedule

        Returns
        -------
        Schedule
            returns todays schedule

        See Also
        --------
        Mlb.get_schedule : Return schedule for dates
        Mlb.get_schedule_date : Return schedule for date
        Mlb.get_schedule_date_range : Return schedule between date
        
        Examples
        --------
        >>> mlb = Mlb()
        >>> mlb.get_schedule_today()
        Schedule
        """

        return self.get_schedule(sport_id=sport_id)

    def get_schedule_date(self, date, sport_id: int = 1) -> Union[Schedule, None]:
        """
        return the schedule for a specific date

        Parameters
        ----------
        date : str "yyyy-mm-dd"
            Date
        sport_id : int
            sport id of the schedule

        Returns
        -------
        Schedule
            returns the schedule for given date

        See Also
        --------
        Mlb.get_schedule : Return schedule for dates
        Mlb.get_schedule_today : Return schedule for today
        Mlb.get_schedule_date_range : Return schedule between date
        
        Examples
        --------
        >>> mlb = Mlb()
        >>> mlb.get_schedule_date("2022-07-03")
        Schedule
        """

        return self.get_schedule(start_date=date, end_date=date, sport_id=sport_id)

    def get_schedule_date_range(self, start_date: str, end_date: str, sport_id: int = 1) -> Union[Schedule, None]:
        """
        return the schedule for a range of dates

        Parameters
        ----------
        start_date : str "yyyy-mm-dd"
            Start date
        end_date : str "yyyy-mm-dd"
            End date
        sport_id : int
            sport id of the schedule

        Returns
        -------
        Schedule

        See Also
        --------
        Mlb.get_schedule : Return schedule for dates
        Mlb.get_schedule_today : Return schedule for today
        Mlb.get_schedule_date : Return schedule for date

        Examples
        --------
        >>> mlb = Mlb()
        >>> mlb.get_schedule_date_range(start_date="2021-08-01", end_date="2021-08-11")
        """

        return self.get_schedule(start_date=start_date, end_date=end_date, sport_id=sport_id)

    def get_game(self, game_id) -> Union[Game, None]:
        """
        return the game for a specific game id

        Parameters
        ----------
        game_id : int
            Game id number

        Returns
        -------
        Game

        See Also
        --------

        Examples
        --------
        >>> mlb = Mlb()
        """

        mlb_data = self._mlb_adapter_v1_1.get(endpoint=f'game/{game_id}/feed/live')

        if 'gamepk' in mlb_data.data and mlb_data.data['gamepk'] == game_id:
            return Game(**mlb_data.data)

    def get_game_play_by_play(self, game_id) -> Union[Plays, None]:
        """
        return the playbyplay of a game for a specific game id

        Parameters
        ----------
        game_id : int
            Game id number

        Returns
        -------
        Plays

        See Also
        --------

        Examples
        --------
        >>> mlb = Mlb()
        """

        mlb_data = self._mlb_adapter_v1.get(endpoint=f'game/{game_id}/playByPlay')

        if 'allplays' in mlb_data.data and mlb_data.data['allplays']:
            return Plays(**mlb_data.data)

    def get_game_line_score(self, game_id) -> Union[Linescore, None]:
        """
        return the Linescore of a game for a specific game id

        Parameters
        ----------
        game_id : int
            Game id number

        Returns
        -------
        Linescore

        See Also
        --------

        Examples
        --------
        >>> mlb = Mlb()
        """

        mlb_data = self._mlb_adapter_v1.get(endpoint=f'game/{game_id}/linescore')

        if 'teams' in mlb_data.data and mlb_data.data['teams']:
            return Linescore(**mlb_data.data)

    def get_game_box_score(self, game_id) -> Union[BoxScore, None]:
        """
        return the boxscore of a game for a specific game id

        Parameters
        ----------
        game_id : int
            Game id number

        Returns
        -------
        BoxScore

        See Also
        --------

        Examples
        --------
        >>> mlb = Mlb()
        """

        mlb_data = self._mlb_adapter_v1.get(endpoint=f'game/{game_id}/boxscore')

        if 'teams' in mlb_data.data and mlb_data.data['teams']:
            return BoxScore(**mlb_data.data)

    def get_game_ids(self, date: str, abstract_game_state: str = None) -> List[int]:
        """
        return game ids for a specific date and game status

        Parameters
        ----------
        date : str 'yyyy-mm-dd'
            Date
        abstract_game_state : str
            Game status type to search for, abstract_game_state

        Returns
        -------
        List[int]

        See Also
        --------

        Examples
        --------
        >>> mlb = Mlb()
        """

        scheduled_games = self.get_schedule(date, date)
        games_ids = []

        # TODO Can we clean up this logic? lol my attempt isn't much better, it's still confusing
        # If get_schedule_today is successful and returns a schedule object
        if not scheduled_games:
            return games_ids
            # If only one date is in dates. Zero would mean no games today. 
        if scheduled_games.dates and len(scheduled_games.dates) == 1:
            # If the single date is todays date
            if not scheduled_games.dates[0].date == date:
                return games_ids
                # If todays date has games. A date could have no games and events.
            if not scheduled_games.dates[0].games:
                return games_ids
                # Collect all the game Id's for todays games
            for game in scheduled_games.dates[0].games:
                # If abstractGameState param provided only get games that match
                if not abstract_game_state or (game.status.abstractgamestate == abstract_game_state):
                    games_ids.append(game.gamepk)

        return games_ids

    def get_todays_game_ids(self, abstract_game_state: str = None) -> List[int]:
        """
        return game ids for todays date

        Parameters
        ----------
        abstract_game_state : str
            Game status type to search for, abstract_game_state

        Returns
        -------
        List[int]

        See Also
        --------

        Examples
        --------
        >>> mlb = Mlb()
        """

        todays_date = datetime.date.today()
        todays_games = self.get_game_ids(todays_date.strftime("%Y-%m-%d"), abstract_game_state)
        return todays_games

    def get_tomorrows_game_ids(self) -> List[int]:
        """
        return game ids for tomorrows date

        Returns
        -------
        List[int]

        See Also
        --------

        Examples
        --------
        >>> mlb = Mlb()
        """

        tomorrows_date = datetime.date.today() + datetime.timedelta(days=1)
        tomorrows_games = self.get_game_ids(tomorrows_date.strftime("%Y-%m-%d"))
        return tomorrows_games

    def get_yesterdays_game_ids(self) -> List[int]:
        """
        return game ids for yesterdays date

        Returns
        -------
        List[int]

        See Also
        --------

        Examples
        --------
        >>> mlb = Mlb()
        """

        yesterdays_date = datetime.date.today() - datetime.timedelta(days=1)
        yesterdays_games = self.get_game_ids(yesterdays_date.strftime("%Y-%m-%d"))
        return yesterdays_games

    def get_venue(self, venue_id) -> Union[Venue, None]:
        """
        return venue

        Parameters
        ----------
        venue_id : int

        Returns
        -------
        Venue

        See Also
        --------

        Examples
        --------
        >>> mlb = Mlb()
        """

        params = {'hydrate': ['location', 'fieldInfo', 'timezone']}
        mlb_data = self._mlb_adapter_v1.get(endpoint=f'venues/{venue_id}', ep_params=params)
        
        if 'venues' in mlb_data.data and mlb_data.data['venues']:
            for venue in mlb_data.data['venues']:

                return Venue(**venue)

    def get_venues(self) -> List[Venue]:
        """
        return all venues

        Returns
        -------
        List[Venue]

        See Also
        --------

        Examples
        --------
        >>> mlb = Mlb()
        """

        mlb_data = self._mlb_adapter_v1.get(endpoint='venues')
        venues = []

        if 'venues' in mlb_data.data and mlb_data.data['venues']:
            venues = [Venue(**venue) for venue in mlb_data.data['venues']]

        return venues

    def get_venue_id(self, venue_name: str) -> List[int]:
        """
        return venue id

        Parameters
        ----------
        venue_name : str
            venue name

        Returns
        -------
        List[int]

        See Also
        --------

        Examples
        --------
        >>> mlb = Mlb()
        """

        mlb_data = self._mlb_adapter_v1.get(endpoint='venues')
        venue_ids = []

        if 'venues' in mlb_data.data and mlb_data.data['venues']:
            for venue in mlb_data.data['venues']:

                if venue['name'].lower() == venue_name.lower():
                    venue_ids.append(venue['id'])

        return venue_ids

    def get_sport(self, sport_id: int) -> Union[Sport, None]:
        """
        return sport object from sportid

        Parameters
        ----------
        sport_id : int

        Returns
        -------
        Sport

        See Also
        --------

        Examples
        --------
        >>> mlb = Mlb()
        """

        mlb_data = self._mlb_adapter_v1.get(endpoint=f'sports/{sport_id}')

        if 'sports' in mlb_data.data and mlb_data.data['sports']:
            for sport in mlb_data.data['sports']:

                return Sport(**sport)

    def get_sports(self) -> List[Sport]:
        """
        return all sports

        Returns
        -------
        List[Sport]

        See Also
        --------

        Examples
        --------
        >>> mlb = Mlb()
        """

        mlb_data = self._mlb_adapter_v1.get(endpoint='sports')
        sports = []

        if 'sports' in mlb_data.data and mlb_data.data['sports']:
            sports = [Sport(**sport) for sport in mlb_data.data['sports']]

        return sports

    def get_sport_id(self, sport_name: str) -> List[int]:
        """
        return sport id 

        Parameters
        ----------
        sport_name : str
            Sport name

        Returns
        -------
        List[int]

        See Also
        --------

        Examples
        --------
        >>> mlb = Mlb()
        """

        mlb_data = self._mlb_adapter_v1.get(endpoint='sports')
        sport_ids = []

        if 'sports' in mlb_data.data and mlb_data.data['sports']:
            for sport in mlb_data.data['sports']:

                if sport['name'].lower() == sport_name.lower():
                    sport_ids.append(sport['id'])

        return sport_ids

    def get_league(self, league_id) -> Union[League, None]:
        """
        return league

        Returns
        -------
        League

        See Also
        --------

        Examples
        --------
        >>> mlb = Mlb()
        """

        mlb_data = self._mlb_adapter_v1.get(endpoint=f'league/{league_id}')

        if 'leagues' in mlb_data.data and mlb_data.data['leagues']:
            for league in mlb_data.data['leagues']:

                return League(**league)

    def get_leagues(self) -> List[League]:
        """
        return all leagues

        Returns
        -------
        List[League]

        See Also
        --------

        Examples
        --------
        >>> mlb = Mlb()
        """

        mlb_data = self._mlb_adapter_v1.get(endpoint='league')
        leagues = []

        if 'leagues' in mlb_data.data and mlb_data.data['leagues']:
            leagues = [League(**league) for league in mlb_data.data['leagues']]

        return leagues

    def get_league_id(self, league_name) -> List[League]:
        """
        return league id

        Parameters
        ----------
        league_name : str
            League name

        Returns
        -------
        List[int]

        See Also
        --------

        Examples
        --------
        >>> mlb = Mlb()
        """

        mlb_data = self._mlb_adapter_v1.get(endpoint='league')
        league_ids = []

        if 'leagues' in mlb_data.data and mlb_data.data['leagues']:
            for league in mlb_data.data['leagues']:

                if league['name'].lower() == league_name.lower():
                    league_ids.append(league['id'])

        return league_ids

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

        See Also
        --------

        Examples
        --------
        >>> mlb = Mlb()
        """

        mlb_data = self._mlb_adapter_v1.get(endpoint=f'divisions/{divisionid}')

        if 'divisions' in mlb_data.data and mlb_data.data['divisions']:
            for division in mlb_data.data['divisions']:

                return Division(**division)

    def get_divisions(self) -> List[Division]:
        """
        return all divisons

        Returns
        -------
        List[Division]

        See Also
        --------

        Examples
        --------
        >>> mlb = Mlb()
        """

        mlb_data = self._mlb_adapter_v1.get(endpoint='divisions')
        divisions = []

        if 'divisions' in mlb_data.data and mlb_data.data['divisions']:
            divisions = [Division(**division) for division in mlb_data.data['divisions']]

        return divisions

    def get_division_id(self, division_name) -> List[Division]:
        """
        return divsion id

        Parameters
        ----------
        division_name : str
            Division name

        Returns
        -------
        List[int]

        See Also
        --------

        Examples
        --------
        >>> mlb = Mlb()
        """

        mlb_data = self._mlb_adapter_v1.get(endpoint='divisions')
        division_ids = []

        if 'divisions' in mlb_data.data and mlb_data.data['divisions']:
            for division in mlb_data.data['divisions']:

                if division['name'].lower() == division_name.lower():
                    division_ids.append(division['id'])

        return division_ids

    def get_attendance(self, team_id: int = None, league_id: int = None,
                       league_list_id: int = None, params: dict = {}) -> Union[Attendance, None]:
        """
        return attendance

        Required Parameters (at least one)
        ----------
        team_id : int
            Team id number
        league_id : int
            League id number
        league_list_id : int
            Not sure

        Parameters
        ----------
        season : int
            Season year number format yyyy
        date : str 'yyyy-mm-dd'
            Date
        gametype : str
            Game type
        Returns
        -------
        Attendance

        See Also
        --------

        Examples
        --------
        >>> mlb = Mlb()
        """
        required_args = {'teamId': team_id, 'leagueId': league_id, 'leagueListId': league_list_id}

        # I like this
        if not any(required_args):
            return

        # let's create a list of the args passed
        # this will filter out None
        for arg_name, arg_value in required_args.items():
            if arg_value:
                params[arg_name] = arg_value

        mlb_data = self._mlb_adapter_v1.get('attendance', ep_params=params)

        if 'records' in mlb_data.data and mlb_data.data['records']:
            return Attendance(**mlb_data.data)

    def get_object(self, mlb_object):
        """
        return a hydrated object

        Parameters
        ----------
        mlb_object : class
            Object to be hydrated. Can by dry or one that just needs updating

        Returns
        -------
        object


        See Also
        --------

        Examples
        --------
        >>> mlb = Mlb()
        """

        get_func = getattr(self, 'get_'+str(mlb_object.__class__.__name__).lower())
        hydrated_object = get_func(mlb_object.id)

        # If problem with hydrating object, return the old dry object
        if hydrated_object:
            return hydrated_object
        else:
            return mlb_object

    def get_team_stats(self, team_id: int, params: dict):
        """
        returns a split stat data for a team

        Parameters
        ----------
        params: dict
            dict of params to pass
        
        Returns
        -------
        splits: dict

        See Also
        --------

        Examples
        --------
        >>> mlb = Mlb()
        """
        mlb_data = self._mlb_adapter_v1.get(endpoint=f'teams/{team_id}/stats', ep_params=params)
        if 400 <= mlb_data.status_code <= 499:
            return {}

        groups = mlb_module.build_group_list(params)

        splits = mlb_module.create_split_data(mlb_data, groups)

        return splits

    def get_player_stats(self, person_id: int, params: dict):
        """
        returns a split stat data for a team

        Parameters
        ----------
        params: dict
            dict of params to pass

        Returns
        -------
        splits: dict

        See Also
        --------

        Examples
        --------
        >>> mlb = Mlb()
        """
        mlb_data = self._mlb_adapter_v1.get(endpoint=f'people/{person_id}/stats', ep_params=params)
        if 400 <= mlb_data.status_code <= 499:
            return {}
        # use the param groups to build a set of groups
        groups = mlb_module.build_group_list(params)

        splits = mlb_module.create_split_data(mlb_data, groups)

        return splits

    def get_stats(self, params: dict) -> Union['Splits', dict]:
        """
        return a split object

        Parameters
        ----------
        params: dict
            dict of params to pass

        Returns
        -------
        splits: dict

        See Also
        --------

        Examples
        --------
        >>> mlb = Mlb()
        """
        mlb_data = self._mlb_adapter_v1.get(endpoint='stats', ep_params=params)
        if 400 <= mlb_data.status_code <= 499:
            return {}

        groups = mlb_module.build_group_list(params)

        splits = mlb_module.create_split_data(mlb_data, groups)

        return splits
