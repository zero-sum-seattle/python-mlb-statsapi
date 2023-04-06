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
