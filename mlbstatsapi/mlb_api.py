import logging
import datetime

from typing import List, Union

from .mlb_dataadapter import MlbDataAdapter
from . import mlb_module

from mlbstatsapi.models.people import Person, Player, Coach
from mlbstatsapi.models.teams import Team
from mlbstatsapi.models.leagues import League
from mlbstatsapi.models.divisions import Division


class Mlb:
    """
    A class used to retrive MLB Stats API objects

    ...

    Attributes
    ----------
    hostname: str
        hostname of statsapi.mlb.com
    logger: logging.Loger
        logger
    """
    def __init__(self, hostname: str = 'statsapi.mlb.com', logger: logging.Logger = None):
        self._mlb_adapter_v1 = MlbDataAdapter(hostname, 'v1', logger)
        self._mlb_adapter_v1_1 = MlbDataAdapter(hostname, 'v1.1', logger)
        self._logger = logger or logging.getLogger(__name__)
        self._logger.setLevel(logging.DEBUG)

    def get_people(self, sport_id: int = 1, **params) -> List[Person]:
        """
        return the all players for sportid

        Parameters
        ----------
        sport_id : int
            Insert a sportId to return player information for a particular 
            sport.

        Other Parameters
        ----------------
        season : str
            Insert year to return player information for a particular season.
        gameType : str
            Insert gameType to return player information for a particular 
            gameType.

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

        mlb_data = self._mlb_adapter_v1.get(endpoint=f'sports/{sport_id}/players', ep_params=params)
        if 400 <= mlb_data.status_code <= 499:
            return []

        people = []

        if 'people' in mlb_data.data and mlb_data.data['people']:
            people = [Person(**person) for person in mlb_data.data['people']]

        return people

    def get_person(self, player_id: int, **params) -> Union[Person, None]:
        """
        This endpoint returns statistical data and biographical information 
        for a player,coach or umpire based on playerId.

        Parameters
        ----------
        person_id : int
            Insert personId for a specific player, coach or umpire based on
            playerId.

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

        mlb_data = self._mlb_adapter_v1.get(endpoint=f'people/{player_id}', ep_params=params)
        if 400 <= mlb_data.status_code <= 499:
            return None

        if 'people' in mlb_data.data and mlb_data.data['people']:
            for person in mlb_data.data['people']:
                return Person(**person)

    def get_people_id(self, fullname: str, sport_id: int = 1, 
                      search_key: str = 'fullName', **params) -> List[int]:
        """
        Returns specific player information based on players fullname

        Parameters
        ----------
        fullname : str
            Person full name
        sport_id : int
            Insert sportId to return player information for particular sport.

        Other Parameters
        ----------------
        season : int
            Insert year to return player information for a particular season.
        gameType : str
            Insert gameType to return player information for a particular 
            gameType. 

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
        # Used to reduce the amount of unneccessary data requested from api
        params['fields'] = 'people,id,fullName'

        mlb_data = self._mlb_adapter_v1.get(endpoint=f'sports/{sport_id}/players', ep_params=params)
        if 400 <= mlb_data.status_code <= 499:
            return []

        player_ids = []

        if 'people' in mlb_data.data and mlb_data.data['people']:
            for person in mlb_data.data['people']:
                try:
                    if person[search_key].lower() == fullname.lower():
                        player_ids.append(person['id'])
                except KeyError:
                    continue

        return player_ids


    def get_teams(self, sport_id: int = 1, **params) -> List[Team]:
        """
        return the all Teams

        Parameters
        ----------
        sport_id : int
            Insert sportId to return team information for a particular sportId

        Other Parameters
        ----------------
        season : str
            Insert year to return team information for a particular season.
        leagueIds : int
            Insert leagueId to return team information for particular league.
        activeStatus : str
            Insert activeStatus to populate a teams based on active/inactive 
            status for a given season. There are three status types: Y, N, B
        allStarStatuses : str
            Insert allStarStatuses to populate a teams based on Allstar status
            for a given season. There are two status types: Y and N
        sportIds : str
            Insert sportId to return team information for a particular sportId
            Usage: '1' or '1,11,12'
        gameType : str
            Insert gameType to return team information for a particular 
            gameType. For a list of all gameTypes: 
            https://statsapi.mlb.com/api/v1/gameTypes
        hydrate : str
            Insert Hydration(s) to return data for any available team 
            hydration. Format "league,venue"
            Available Hydrations:
                previousSchedule
                nextSchedule
                venue
                social
                deviceProperties
                game(promotions)
                game(atBatPromotions)
                game(tickets)
                game(atBatTickets)
                game(sponsorships)
                league
                person
                sport
                division
        fields : str
            Comma delimited list of specific fields to be returned. 
            Format: topLevelNode, childNode, attribute

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
        params['sportId'] = sport_id

        mlb_data = self._mlb_adapter_v1.get(endpoint=f'teams', ep_params=params)
        if 400 <= mlb_data.status_code <= 499:
            return []

        teams = []

        if 'teams' in mlb_data.data and mlb_data.data['teams']:
            teams = [Team(**team) for team in mlb_data.data['teams']]

        return teams

    def get_team(self, team_id: int, **params) -> Union[Team, None]:
        """
        Returns a team based on teamId.

        Parameters
        ----------
        team_id : int
            Insert teamId to return a directory of team information for a 
            particular club.

        Other Parameters
        ----------------
        season : int
            Insert year to return a directory of team information for a 
            particular club in a specific season.
        sportId : int
            Insert a sportId to return a directory of team information for a 
            particular club in a sport.
        hydrate : str
            Insert Hydration(s) to return data for any available team 
            hydration. Format "league,venue"
            Available Hydrations:
                previousSchedule
                nextSchedule
                venue
                social
                deviceProperties
                game(promotions)
                game(atBatPromotions)
                game(tickets)
                game(atBatTickets)
                game(sponsorships)
                league
                person
                sport
                division
        fields : str
            Comma delimited list of specific fields to be returned. 
            Format: topLevelNode, childNode, attribute

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

        mlb_data = self._mlb_adapter_v1.get(endpoint=f'teams/{team_id}', 
                                            ep_params=params)
        if 400 <= mlb_data.status_code <= 499:
            return None

        if 'teams' in mlb_data.data and mlb_data.data['teams']:
            for team in mlb_data.data['teams']:
                return Team(**team)

    def get_team_id(self, team_name: str,
                    search_key: str = 'name', **params) -> List[int]:
        """
        return a team Id

        Parameters
        ----------
        team_name : str
            Teams name

        search_key : str
            search key search json for matching team_name

        Other Parameters
        ----------------
        sportId : int
            sport id number for team search

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
        # Used to reduce the amount of unneccessary data requested from api
        params['fields'] = 'teams,id,name'

        mlb_data = self._mlb_adapter_v1.get(endpoint='teams', ep_params=params)
        if 400 <= mlb_data.status_code <= 499:
            return []

        team_ids = []
    
        if 'teams' in mlb_data.data and mlb_data.data['teams']:
            for team in mlb_data.data['teams']:
                try:
                    if team[search_key].lower() == team_name.lower():
                        team_ids.append(team['id'])
                except (KeyError):
                    continue

        return team_ids

    def get_team_roster(self, team_id: int, **params) -> List[Player]:
        """
        return the team player roster

        Parameters
        ----------
        team_id : int
            teamId to return a directory of players based on roster status for
            a particular club.

        Other Parameters
        ----------------
        rosterType : str
            Insert teamId to return a directory of players based on roster 
            status for a particular club. rosterType's include 40Man, 
            fullSeason, fullRoster, nonRosterInvitees, active, allTime,
            depthChart, gameday, and coach.
        season : str
            Insert year to return a directory of players based on roster 
            status for a particular club in a specific season.
        date : str
            Insert date to return a directory of players based on roster 
            status for a particular club on a specific date.
        hydrate : str
            Insert Hydration(s) to return data for any available team 
            hydration. The hydration for Teams contains "person" which has 
            subhydrations Format "person(subHydration1, subHydrations2)"
            Available Hydrations:
                "person"
                    Hydrations Available Through Person
                    hydrations
                    awards
                    currentTeam
                    team
                    rosterEntries
                    relatives
                    transactions
                    social
                    education
                    stats
                    draft
                    mixedFeed
                    articles
                    video
                    xrefId
        fields : str
            Comma delimited list of specific fields to be returned. 
            Format: topLevelNode, childNode, attribute

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
        >>> mlb.get_team_roster(133, rosterType=40Man, season=2018)
        [Player, Player, Player]
        >>> mlb.get_team_roster(133, date='06/05/2018')
        [Player, Player, Player]
        """

        mlb_data = self._mlb_adapter_v1.get(endpoint=f'teams/{team_id}/roster', ep_params=params)
        if 400 <= mlb_data.status_code <= 499:
            return []

        players = []

        if 'roster' in mlb_data.data and mlb_data.data['roster']:
            for player in mlb_data.data['roster']:
                players.append(Player(**mlb_module.merge_keys(player, ['person'])))

        return players

    def get_team_coaches(self, team_id: int, **params) -> List[Coach]:
        """
        Return a directory of coaches for a particular team.

        Parameters
        ----------
        team_id : int
            Insert teamId to return a directory of coaches for a given team.

        Other Parameters
        ----------------
        season : str
            Insert year to return a directory of players based on roster status for a particular club in a specific season.
        date : str
            Insert date to return a directory of players based on roster status for a particular club on a specific date.   
        fields : str
            Comma delimited list of specific fields to be returned. Format: topLevelNode, childNode, attribute

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
        >>> mlb.get_team_coaches(133, season='2018')
        [Coach, Coach, Coach]
        """

        mlb_data = self._mlb_adapter_v1.get(endpoint=f'teams/{team_id}/coaches', ep_params=params)
        if 400 <= mlb_data.status_code <= 499:
            return []

        coaches = []

        if 'roster' in mlb_data.data and mlb_data.data['roster']:
            for coach in mlb_data.data['roster']:
                coaches.append(Coach(**mlb_module.merge_keys(coach, ['person'])))

        return coaches

    def get_division(self, division_id: int, **params) -> Union[Division, None]:
        """
        Returns a division based on divisionId,

        Parameters
        ----------
        divison_id : int
            divisionId to return a directory of division(s) for a specific division.

        Returns
        -------
        Division
            returns a Division

        See Also
        --------
        Mlb.get_divisions : return a list of Divisions
        Mlb.get_division_id : return a list of matching division ids

        Examples
        --------
        >>> mlb = Mlb()
        >>> mlb.get_division(200)
        Division
        """

        mlb_data = self._mlb_adapter_v1.get(endpoint=f'divisions/{division_id}', ep_params=params)
        if 400 <= mlb_data.status_code <= 499:
            return None

        if 'divisions' in mlb_data.data and mlb_data.data['divisions']:
            for division in mlb_data.data['divisions']:
                return Division(**division)

    def get_divisions(self, **params) -> List[Division]:
        """
        return all divisons

        Other Parameters
        ----------------
        divisionId : str
            Insert divisionId(s) to return a directory of division(s) for a 
            specific division. Format '200,201'
        leagueId : int
            Insert leagueId to return a directory of division(s) for all 
            divisions in a specific league.
        sportId : int
            Insert a sportId to return a directory of division(s) for all 
            divisions in a specific sport.

        Returns
        -------
        list of Divisions
            returns a list of all divisions

        See Also
        --------
        Mlb.get_division : return a Division from id
        Mlb.get_division_id : return a list of matching division ids

        Examples
        --------
        >>> mlb = Mlb()
        >>> mlb.get_divisions()
        [Divison, Division, Division]
        """

        mlb_data = self._mlb_adapter_v1.get(endpoint='divisions', ep_params=params)
        if 400 <= mlb_data.status_code <= 499:
            return []

        divisions = []

        if 'divisions' in mlb_data.data and mlb_data.data['divisions']:
            divisions = [Division(**division) for division in mlb_data.data['divisions']]

        return divisions

    def get_division_id(self, division_name: str, 
                        search_key: str = 'name', **params) -> List[Division]:
        """
        return divsion id

        Parameters
        ----------
        division_name : str
            Division name
        search_key : str
            search key name

        Returns
        -------
        list of ints
            returns a matching list of division ids

        See Also
        --------
        Mlb.get_division : return a Division from id
        Mlb.get_divisions : return a list of Divisions

        Examples
        --------
        >>> mlb = Mlb()
        >>> mlb.get_division_id('American League West')
        [200]
        """

        mlb_data = self._mlb_adapter_v1.get(endpoint='divisions', ep_params=params)
        if 400 <= mlb_data.status_code <= 499:
            return []
        
        division_ids = []

        if 'divisions' in mlb_data.data and mlb_data.data['divisions']:
            for division in mlb_data.data['divisions']:
                try:
                    if division[search_key].lower() == division_name.lower():
                        division_ids.append(division['id'])
                except KeyError:
                    continue

        return division_ids
    
    def get_league(self, league_id: int, **params) -> Union[League, None]:
        """
        return league

        Parameters
        ----------
        league_id : int
            leagueId to return league information for a specific league

        Other Parameters
        ----------------
        fields : str
            Comma delimited list of specific fields to be returned. 
            Format: topLevelNode, childNode, attribute    

        Returns
        -------
        League

        See Also
        --------
        Mlb.get_leagues : return a list of Leagues
        Mlb.get_league_id : return a list of league ids that match name

        Examples
        --------
        >>> mlb = Mlb()
        >>> mlb.get_league(103)
        [League]
        """

        mlb_data = self._mlb_adapter_v1.get(endpoint=f'leagues/{league_id}', ep_params=params)
        if 400 <= mlb_data.status_code <= 499:
            return None

        if 'leagues' in mlb_data.data and mlb_data.data['leagues']:
            for league in mlb_data.data['leagues']:
                return League(**league)

    def get_leagues(self, **params) -> List[League]:
        """
        return all leagues

        Returns
        -------
        list of Leagues

        Other Parameters
        ----------------
        leagueId : str
            leagueId(s) to return league information for specific leagues.
            Format '103,104'
        sportId : int
            Insert sportId to return league information for a specific sport.
            For a list of all sportIds: http://statsapi.mlb.com/api/v1/sports   
        seasons : str
            Insert year(s) to return league information for a specific season. 
            Format '2017,2018'
        fields : str
            Comma delimited list of specific fields to be returned. 
            Format: topLevelNode, childNode, attribute    

        See Also
        --------
        Mlb.get_league : return a League from league id
        Mlb.get_league_id : return a list of league ids that match name

        Examples
        --------
        >>> mlb = Mlb()
        >>> mlb.get_leagues()
        [League, League, League]
        """

        mlb_data = self._mlb_adapter_v1.get(endpoint='leagues', ep_params=params)
        if 400 <= mlb_data.status_code <= 499:
            return []

        leagues = []

        if 'leagues' in mlb_data.data and mlb_data.data['leagues']:
            leagues = [League(**league) for league in mlb_data.data['leagues']]

        return leagues

    def get_league_id(self, league_name: str,
                      search_key: str = 'name', **params) -> List[int]:
        """
        return league id

        Parameters
        ----------
        league_name : str
            League name

        Returns
        -------
        list of ints

        See Also
        --------
        Mlb.get_league : return a League from league id
        Mlb.get_leagues : return a list of Leagues

        Examples
        --------
        >>> mlb = Mlb()
        >>> mlb.get_league_id('American League')
        [103]
        """
        # Used to reduce the amount of unneccessary data requested from api
        params['fields'] = 'leagues,id,name'

        mlb_data = self._mlb_adapter_v1.get(endpoint='leagues', ep_params=params)
        if 400 <= mlb_data.status_code <= 499:
            return []

        league_ids = []

        if 'leagues' in mlb_data.data and mlb_data.data['leagues']:
            for league in mlb_data.data['leagues']:
                try:
                    if league[search_key].lower() == league_name.lower():
                        league_ids.append(league['id'])
                except KeyError:
                    continue
                
        return league_ids