import logging
import datetime

from typing import List, Union

from .mlb_dataadapter import MlbDataAdapter

from mlbstatsapi.models.people import Person


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
