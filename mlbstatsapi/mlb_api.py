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
from mlbstatsapi.models.schedules import Schedule, ScheduleGames
from mlbstatsapi.models.attendances import Attendance
from mlbstatsapi.models.stats import Stat
from mlbstatsapi.models.seasons import Season
from mlbstatsapi.models.drafts import Round
from mlbstatsapi.models.awards import Award
from mlbstatsapi.models.gamepace import Gamepace
from mlbstatsapi.models.homerunderby import Homerunderby
from mlbstatsapi.models.standings import Standings

from .mlb_dataadapter import MlbDataAdapter
# from .exceptions import TheMlbStatsApiException
from . import mlb_module


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

    def get_persons(self, person_ids: Union[str, List[int]], **params) -> List[Person]:
        """
        This endpoint returns statistical data and biographical information 
        for a players,umpires, and coaches based on playerId.

        Parameters
        ----------
        person_ids : str, List[int]
            Insert personId(s) to return biographical information for a 
            specific player. Format '605151,592450' or [605151,592450]

        Other Parameters
        ----------------
        hydrate : str
            Insert hydration(s) to return statistical or biographical data 
            for a specific player(s). 
            Format stats(group=["statGroup1","statGroup2"],
                         type=["statType1","statType2"]).
            Available Hydrations:
                hydrations                
                currentTeam
                team
                rosterEntries
                relatives
                transactions
                social
                education                
                draft
                mixedFeed
                articles
                videos
                xrefId
        fields : str
            Comma delimited list of specific fields to be returned. 
            Format: topLevelNode, childNode, attribute

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
        params['personIds'] = person_ids

        mlb_data = self._mlb_adapter_v1.get(endpoint=f'people', ep_params=params)
        if 400 <= mlb_data.status_code <= 499:
            return []

        person_list = []

        if 'people' in mlb_data.data and mlb_data.data['people']:
            for person in mlb_data.data['people']:
                person_list.append(Person(**person))

        return person_list

    def get_people_id(self, fullname: str, sport_id: int = 1, 
                      search_key: str = 'fullname', **params) -> List[int]:
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

    def get_schedule(self, 
                    date: str = None, 
                    start_date: str = None, 
                    end_date: str = None, 
                    sport_id: int = 1, 
                    team_id: int = None, **params) -> Union[Schedule, None]:
        """
        return the schedule created from the included params.

        Calling get_schedule without startDate or endDate results in a schedule returned
        for todays date. Calling with startDate and endDate as the same date returns a
        schedule for just that desired date. Different results in the schedule for multiple
        days.

        Parameters
        ----------
        date : str
            Date
        start_date : str "yyyy-mm-dd"
            Start date
        end_date : str "yyyy-mm-dd"
            End date
        sport_id : int
            sport id of schedule defaults to 1
        team_id : int
            get schedule for team with team_id

        Other Parameters
        ----------------
        leagueId : int,str
            Insert leagueId to return all schedules based on a particular 
            scheduleType for a specific league. Usage: 1 or '1,11
        gamePks : int,str
            Insert gamePks to return all schedules based on a particular 
            scheduleType for specific games. Usage: 531493 or '531493,531497'
        venueIds : int
            Insert venueId to return all schedules based on a particular 
            scheduleType for a specific venueId.
        gameTypes : str
            Insert gameTypes to return schedule information for all games in 
            particular gameTypes. For a list of all gameTypes: 
            https://statsapi.mlb.com/api/v1/gameTypes
        
        scheduleType : str
            Insert one or mutliple of the three available scheduleTypes to 
            return data for a particular schedule. Format "games,events,xref"
        eventTypes : str
            Insert one or mutliple of the three available eventTypes to 
            return data for a particular schedule. Format "primary,secondary"
            There are two different schedule eventTypes:
                primary- returns calendar/schedule pages.
                secondary returns ticket pages.
        hydrate : str
            Insert Hydration(s) to return data for any available schedule 
            hydration. The hydrations for schedule contain "venue" and "team" 
            which have subhydrations.
            Format "team(subHydration1, subHydrations2)"
            Available Hydrations:
                tickets
                game(content)
                game(content(all))
                game(content(media(all)))
                game(content(editorial(all)))
                game(content(highlights(all)))
                game(content(editorial(preview)))
                game(content(editorial(recap)))
                game(content(editorial(articles)))
                game(content(editorial(wrap)))
                game(content(media(epg)))
                game(content(media(milestones)))
                game(content(highlights(scoreboard)))
                game(content(highlights(scoreboardPreview)))
                game(content(highlights(highlights)))
                game(content(highlights(gamecenter)))
                game(content(highlights(milestone)))
                game(content(highlights(live)))
                game(content(media(featured)))
                game(content(summary))
                game(content(gamenotes))
                game(tickets)
                game(atBatTickets)
                game(promotions)
                game(atBatPromotions)
                game(sponsorships)
                lineup
                linescore
                linescore(matchup)
                linescore(runners)
                linescore(defense)
                decisions
                scoringplays
                broadcasts
                broadcasts(all)
                radioBroadcasts
                metadata
                game(seriesSummary)
                seriesStatus
                event(performers)
                event(promotions)
                event(timezone)
                event(tickets)
                event(venue)
                event(designations)
                event(game)
                event(status)
                weather
                officials
                probablePitcher
                venue                    
                    relatedVenues
                    parentVenues
                    residentVenues
                    relatedVenues(venue)
                    parentVenues(venue)
                    residentVenues(venue)
                    location
                    social
                    relatedApplications
                    timezone
                    menu
                    metadata
                    performers
                    images
                    schedule
                    nextSchedule
                    previousSchedule
                    ticketManagement
                    xrefId
                team                                    
                    previousSchedule
                    nextSchedule
                    venue
                    springVenue
                    social
                    deviceProperties
                    game(promotions)
                    game(promotions)
                    game(atBatPromotions)
                    game(tickets)
                    game(atBatTickets)
                    game(sponsorships)
                    league
                    videos
                    person
                    sport
                    standings
                    division
                    xref


        Returns
        -------
        Schedule
            returns the Schedule for the dates

        See Also
        --------
        Mlb.get_scheduled_games_by_date : return a list of scheduledgames


        Examples
        --------
        >>> mlb = Mlb()
        >>> mlb.get_schedule(start_date="2021-08-01", end_date="2021-08-11")
        Schedule

        """
        
        if start_date and end_date:
            params['startDate'] = start_date
            params['endDate'] = end_date
        elif date and not (start_date or end_date):
            params['date'] = date
        else:
            return None


        if team_id:
            params['teamId'] = team_id
    
        params['sportId'] = sport_id

        mlb_data = self._mlb_adapter_v1.get(endpoint='schedule', ep_params=params)
        if 400 <= mlb_data.status_code <= 499:
            return None

        # if mlb_data is not empty, and 'dates' key is in mlb_data.data and mlb_data.data['dates]
        # can sometimes be an empty list when there are no scheduled game for the date(s).
        # Only check for existance 'dates' key for this reason.

        if 'dates' in mlb_data.data and mlb_data.data['dates']:
            return Schedule(**mlb_data.data)

    def get_scheduled_games_by_date(self, date: str = None,
                                    start_date: str = None, 
                                    end_date: str = None,
                                    sport_id: int = 1, 
                                    **params) -> List[ScheduleGames]:
        """
        return game ids for a specific date and game status

        Parameters
        ----------
        date : str 
            start date, 'yyyy-mm-dd'
        start_date : str "yyyy-mm-dd"
            Start date
        end_date : str
            end date, 'yyyy-mm-dd'
        spord_id : int
            spord id of schedule defaults to 1

        Other Parameters
        ----------------
        leagueId : int,str
            Insert leagueId to return all schedules based on a particular 
            scheduleType for a specific league. Usage: 1 or '1,11
        gamePks : int,str
            Insert gamePks to return all schedules based on a particular 
            scheduleType for specific games. Usage: 531493 or '531493,531497'
        venueIds : int
            Insert venueId to return all schedules based on a particular 
            scheduleType for a specific venueId.
        gameTypes : str
            Insert gameTypes to return schedule information for all games in 
            particular gameTypes. For a list of all gameTypes: 
            https://statsapi.mlb.com/api/v1/gameTypes

        Returns
        -------
        list of ScheduleGames 
            returns a list of matching game ids

        See Also
        --------
        Mlb.get_game_play_by_play : return play by play data for a game
        Mlb.get_game_line_score : return a linescore for a game
        Mlb.get_todays_game_ids : return a list of game ids for today
        Mlb.get_game : return a specific game from game id

        Examples
        --------
        >>> mlb = Mlb()
        >>> mlb.get_game_ids()
        """
        if start_date and end_date:
            params['startDate'] = start_date
            params['endDate'] = end_date
        elif date and not (start_date or end_date):
            params['date'] = date
        else:
            return None

        params['sportId'] = sport_id

        games = []

        mlb_data = self._mlb_adapter_v1.get(endpoint='schedule', ep_params=params)
        if 400 <= mlb_data.status_code <= 499:
            return []

        if 'dates' in mlb_data.data and mlb_data.data['dates']:
            for date in mlb_data.data['dates']:
               for game in date['games']:
                   games.append(ScheduleGames(**game))

        return games

    def get_game(self, game_id: int, **params) -> Union[Game, None]:
        """
        Return the game for a specific game id
        Gumbo Live Feed for a specific gamePk.

        Parameters
        ----------
        game_id : int
            Insert gamePk to return the GUMBO live feed for a specific game.
            
        Other Parameters
        ----------------
        timecode : str
            Use this parameter to return a snapshot of the data at the 
            specified time. Format: YYYYMMDD_HHMMSS.
            Return timecodes from timecodes endpoint 
            https://statsapi.mlb.com/api/v1.1/game/534196/feed/live/timestamps
        hydrate : str
            Insert hydration(s) to return putout credits or defensive 
            positioning data for all plays in a particular game. 
            Format 'credits,alignment,flags'
            Available Hydrations:
                credits
                alignment
                flags
                officials
        fields : str
            Comma delimited list of specific fields to be returned. 
            Format: topLevelNode, childNode, attribute

            !!! To use this we would need to make almost every !!!
            !!!    data class attr optonal? Do we want this?   !!!

        Returns
        -------
        Game

        See Also
        --------
        Mlb.get_game_play_by_play : return play by play data for a game
        Mlb.get_game_line_score : return a linescore for a game
        Mlb.get_game_box_score : return a boxscore for a game

        Examples
        --------
        >>> mlb = Mlb()
        >>> mlb.get_game(662242)
        Game
        """

        mlb_data = self._mlb_adapter_v1_1.get(endpoint=f'game/{game_id}/feed/live', ep_params=params)
        if 400 <= mlb_data.status_code <= 499:
            return None

        if 'gamepk' in mlb_data.data and mlb_data.data['gamepk'] == game_id:
            return Game(**mlb_data.data)

    def get_game_play_by_play(self, game_id: int, **params) -> Union[Plays, None]:
        """
        return the playbyplay of a game for a specific game id

        Parameters
        ----------
        game_id : int
            Game id number

        Other Parameters
        ----------------
        timecode : int
            Use this parameter to return a snapshot of the data at the 
            specified time. Format: YYYYMMDD_HHMMSS
        fields :
            Comma delimited list of specific fields to be returned. 
            Format: topLevelNode, childNode, attribute

            !!! To use this we would need to make almost every !!!
            !!!    data class attr optonal? Do we want this?   !!!

        Returns
        -------
        Plays

        See Also
        --------
        Mlb.get_game_line_score : return a linescore for a game
        Mlb.get_game_box_score : return a boxscore for a game
        Mlb.get_game : return a specific game from game id

        Examples
        --------
        >>> mlb = Mlb()
        >>> mlb.get_game_play_by_play(662242)
        Plays
        """

        mlb_data = self._mlb_adapter_v1.get(endpoint=f'game/{game_id}/playByPlay', ep_params=params)
        if 400 <= mlb_data.status_code <= 499:
            return None

        if 'allplays' in mlb_data.data and mlb_data.data['allplays']:
            return Plays(**mlb_data.data)

    def get_game_line_score(self, game_id: int, **params) -> Union[Linescore, None]:
        """
        return the Linescore of a game for a specific game id

        Parameters
        ----------
        game_id : int
            Game id number

        Other Parameters
        ----------------
        timecode : int
            Use this parameter to return a snapshot of the data at the 
            specified time. Format: YYYYMMDD_HHMMSS
        fields :
            Comma delimited list of specific fields to be returned. 
            Format: topLevelNode, childNode, attribute

            !!! To use this we would need to make almost every !!!
            !!!    data class attr optonal? Do we want this?   !!!

        Returns
        -------
        Linescore

        See Also
        --------
        Mlb.get_game_play_by_play : return play by play data for a game
        Mlb.get_game_box_score : return a boxscore for a game
        Mlb.get_game : return a specific game from game id

        Examples
        --------
        >>> mlb = Mlb()
        >>> mlb.get_game_line_scrore(662242)
        Linescore
        """

        mlb_data = self._mlb_adapter_v1.get(endpoint=f'game/{game_id}/linescore', ep_params=params)

        if 'teams' in mlb_data.data and mlb_data.data['teams']:
            return Linescore(**mlb_data.data)

    def get_game_box_score(self, game_id: int, **params) -> Union[BoxScore, None]:
        """
        return the boxscore of a game for a specific game id

        Parameters
        ----------
        game_id : int
            Game id number

        Other Parameters
        ----------------
        timecode : int
            Use this parameter to return a snapshot of the data at the 
            specified time. Format: YYYYMMDD_HHMMSS
        fields :
            Comma delimited list of specific fields to be returned. 
            Format: topLevelNode, childNode, attribute

            !!! To use this we would need to make almost every !!!
            !!!    data class attr optonal? Do we want this?   !!!

        Returns
        -------
        BoxScore

        See Also
        --------
        Mlb.get_game_play_by_play : return play by play data for a game
        Mlb.get_game_line_score : return a linescore for a game
        Mlb.get_game : return a specific game from game id

        Examples
        --------
        >>> mlb = Mlb()
        >>> mlb.get_game_box_score(662242)
        BoxScore
        """

        mlb_data = self._mlb_adapter_v1.get(endpoint=f'game/{game_id}/boxscore', ep_params=params)
        if 400 <= mlb_data.status_code <= 499:
            return None

        if 'teams' in mlb_data.data and mlb_data.data['teams']:
            return BoxScore(**mlb_data.data)


    def get_game_ids(self, date: str = None,
                     start_date: str = None,
                     end_date: str = None,
                     sport_id: int = 1,
                    **params) -> List[int]:
        """
        return game ids for a specific date and game status

        Parameters
        ----------
        date : str 
            date, 'yyyy-mm-dd'
        start_date : str
            start date, 'yyyy-mm-dd'
        end_date : str
            end date, 'yyyy-mm-dd'
        spord_id : int
            spord id of schedule defaults to 1

        Returns
        -------
        list of ints
            returns a list of matching game ids

        See Also
        --------
        Mlb.get_game_play_by_play : return play by play data for a game
        Mlb.get_game_line_score : return a linescore for a game
        Mlb.get_todays_game_ids : return a list of game ids for today
        Mlb.get_game : return a specific game from game id

        Examples
        --------
        >>> mlb = Mlb()
        >>> mlb.get_game_ids()
        """
        if start_date and end_date:
            params['startDate'] = start_date
            params['endDate'] = end_date
        elif date and not (start_date or end_date):
            params['date'] = date
        else:
            return None

        params['sportId'] = sport_id

        mlb_data = self._mlb_adapter_v1.get(endpoint='schedule', ep_params=params)
        if 400 <= mlb_data.status_code <= 499:
            return []

        game_ids = []

        if 'dates' in mlb_data.data and mlb_data.data['dates']:
            for date in mlb_data.data['dates']:
               for game in date['games']:
                   game_ids.append(game.gamepk)

        return game_ids

    def get_gamepace(self, season: str, sport_id=1, **params) -> Union[Gamepace, None]:
        """
        Get pace of game metrics for specific sport, league or team.

        Parameters
        ----------
        season : int
            Insert year to return a directory of pace of game metrics for a 
            given season.
        
        Other Parameters
        ----------------
        teamIds : int
            Insert a teamIds to return directory of pace of game metrics for 
            a given team. Format '110' or '110,147'
        leagueId : int
            Insert leagueIds to return a directory of pace of game metrics 
            for a given league. Format '103' or '103,104'
        leagueListId : str
            Insert a unique League List Identifier to return a directory of 
            pace of game metrics for a specific league listId.
            Available values : milb_full, milb_short, milb_complex, milb_all,
                milb_all_nomex, milb_all_domestic, milb_noncomp, 
                milb_noncomp_nomex, milb_domcomp, milb_intcomp, win_noabl, 
                win_caribbean, win_all, abl, mlb, mlb_hist, mlb_milb, 
                mlb_milb_hist, mlb_milb_win, baseball_all
        sportId : int
            Insert a sportId to return a directory of pace of game metrics 
            for a specific sport. Format '11' or '1,11'
        gameType : str
            Insert gameType(s) a return a directory of pace of game metrics 
            for a specific gameType. For a list of all gameTypes: 
            https://statsapi.mlb.com/api/v1/gameTypes
        date : str
            Insert date to return a directory of pace of game metrics for a 
            particular date range. Format: MM/DD/YYYY
            !!! startDate must be coupled with endDate !!!
        endDate : str
            Insert date to return a directory of pace of game metrics for a 
            particular date range. Format: MM/DD/YYYY
            !!! endDate must be coupled with startDate !!!
        venueIds : id
            Insert venueId to return a directory of pace of game metrics for 
            a particular venueId.
        orgType : str
            Insert a orgType to return a directory of pace of game metrics 
            based on team, league or sport.
            Available values : T- TEAM, L- LEAGUE, S- SPORT
        includeChildren : bool
            Insert includeChildren to return a directory of pace of game 
            metrics for all child teams in a given parent sport.
        fields : str
            Comma delimited list of specific fields to be returned. 
            Format: topLevelNode, childNode, attribute
        """
        params['sportId'] = sport_id

        mlb_data = self._mlb_adapter_v1.get(endpoint=f'gamePace?season={season}', ep_params=params)
        if 400 <= mlb_data.status_code <= 499:
            return None

        if ('teams' in mlb_data.data and mlb_data.data['teams']
            or 'leagues' in mlb_data.data and mlb_data.data['leagues']
            or 'sports' in mlb_data.data and mlb_data.data['sports']):

            return Gamepace(**mlb_data.data)

    def get_venue(self, venue_id: int, **params) -> Union[Venue, None]:
        """
        returns venue directorial information for all available venues in the Stats API.

        Parameters
        ----------
        venue_id : int
            venueId to return venue directorial information based venueId.

        Other Parameters
        ----------------
        fields : str
            Comma delimited list of specific fields to be returned. 

        Returns
        -------
        Venue

        See Also
        --------
        Mlb.get_venues : return a list of Venues
        Mlb.get_venue_id : return a list of venue ids that match name

        Examples
        --------
        >>> mlb = Mlb()
        >>> mlb.get_venue(31)
        Venue
        """
        params['hydrate'] = ['location', 'fieldInfo', 'timezone']

        mlb_data = self._mlb_adapter_v1.get(endpoint=f'venues/{venue_id}', ep_params=params)
        if 400 <= mlb_data.status_code <= 499:
            return []

        if 'venues' in mlb_data.data and mlb_data.data['venues']:
            for venue in mlb_data.data['venues']:
                return Venue(**venue)

    def get_venues(self, **params) -> List[Venue]:
        """
        return all venues

        Returns
        -------
        list of Venues
            returns a list of Venues

        Other Parameters
        ----------------
        venueIds : int, List[int]
            Insert venueId to return venue directorial information based 
            venueId.
        sportIds : int, List[int]
            Insert sportIds to return venue directorial information based a 
            given sport(s). For a list of all sports: 
            https://statsapi.mlb.com/api/v1/sports
        season : int
            Insert year to return venue directorial information for a given 
            season.        
        fields : str
            Comma delimited list of specific fields to be returned. 
            Format: topLevelNode, childNode, attribute

        See Also
        --------
        Mlb.get_venue : return a Venue
        Mlb.get_venue_id : return a list of venue ids that match name

        Examples
        --------
        >>> mlb = Mlb()
        >>> mlb.get_venues()
        [Venue, Venue, Venue]
        """
        params['hydrate'] = ['location', 'fieldInfo', 'timezone']

        mlb_data = self._mlb_adapter_v1.get(endpoint='venues', ep_params=params)
        if 400 <= mlb_data.status_code <= 499:
            return []

        venues = []

        if 'venues' in mlb_data.data and mlb_data.data['venues']:
            venues = [Venue(**venue) for venue in mlb_data.data['venues']]

        return venues

    def get_venue_id(self, venue_name: str,
                     search_key: str = 'name', **params) -> List[int]:
        """
        return venue id

        Parameters
        ----------
        venue_name : str
            venue name

        Returns
        -------
        list of ints
            returns a list of matching venue ints

        See Also
        --------
        Mlb.get_venue : return a Venue
        Mlb.get_venues : return a list of Venues

        Examples
        --------
        >>> mlb = Mlb()
        >>> mlb.get_venue_id('PNC Park')
        [31]
        """
        mlb_data = self._mlb_adapter_v1.get(endpoint='venues', ep_params=params)
        if 400 <= mlb_data.status_code <= 499:
            return []

        venue_ids = []

        if 'venues' in mlb_data.data and mlb_data.data['venues']:
            for venue in mlb_data.data['venues']:
                try:
                    if venue[search_key].lower() == venue_name.lower():
                        venue_ids.append(venue['id'])
                except KeyError:
                    continue
        return venue_ids

    def get_sport(self, sport_id: int, **params) -> Union[Sport, None]:
        """
        return sport object from sport_id

        Parameters
        ----------
        sport_id : int
            Insert a sportId to return a directory of sport(s).
            For a list of all sportIds: http://statsapi.mlb.com/api/v1/sports

        Other Parameters
        ----------------
        fields : str
            Comma delimited list of specific fields to be returned. 
            Format: topLevelNode, childNode, attribute

        Returns
        -------
        Sport

        See Also
        --------
        Mlb.get_sports : return a list of sports
        Mlb.get_sport_id : return a list of matching sport ids from name
        Mlb.get_sport : return a sport from id

        Examples
        --------
        >>> mlb = Mlb()
        >>> mlb.get_sport(1)
        Sport
        """

        mlb_data = self._mlb_adapter_v1.get(endpoint=f'sports/{sport_id}', ep_params=params)
        if 400 <= mlb_data.status_code <= 499:
            return None

        if 'sports' in mlb_data.data and mlb_data.data['sports']:
            for sport in mlb_data.data['sports']:
                return Sport(**sport)

    def get_sports(self, **params) -> List[Sport]:
        """
        return all sports

        Returns
        -------
        list of Sports
            returns a list of sport objects

        Other Parameters
        ----------------
        fields : str
            Comma delimited list of specific fields to be returned. 
            Format: topLevelNode, childNode, attribute

        See Also
        --------
        Mlb.get_sport_id : return a list of matching sport ids from name
        Mlb.get_sport : return a sport from id

        Examples
        --------
        >>> mlb = Mlb()
        >>> mlb.get_sports()
        [Sport, Sport, Sport]
        """

        mlb_data = self._mlb_adapter_v1.get(endpoint='sports', ep_params=params)
        if 400 <= mlb_data.status_code <= 499:
            return []

        sports = []

        if 'sports' in mlb_data.data and mlb_data.data['sports']:
            sports = [Sport(**sport) for sport in mlb_data.data['sports']]

        return sports

    def get_sport_id(self, sport_name: str,
                     search_key: str = 'name', **params) -> List[int]:
        """
        return sport id 

        Parameters
        ----------
        sport_name : str
            Sport name
        search_key : str
            search key name 

        Returns
        -------
        list of ints
            returns a list of sport ids

        See Also
        --------
        Mlb.get_sports : return a list of sports
        Mlb.get_sport : return a sport from id

        Examples
        --------
        >>> mlb = Mlb()
        >>> mlb.get_sport_id("Major League Baseball")
        [1]
        """

        mlb_data = self._mlb_adapter_v1.get(endpoint='sports', ep_params=params)
        if 400 <= mlb_data.status_code <= 499:
            return []

        sport_ids = []

        if 'sports' in mlb_data.data and mlb_data.data['sports']:
            for sport in mlb_data.data['sports']:
                try:
                    if sport[search_key].lower() == sport_name.lower():
                        sport_ids.append(sport['id'])
                except KeyError:
                    continue

        return sport_ids

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

    def get_season(self, season_id: str, sport_id: int = 1, **params) -> Season:
        """
        return a season object for seasonid and sportid

        Parameters
        ----------
        sport_id : int
            Insert a sportId to return a directory of seasons for a specific sport.
        season_id : str
            Insert year to return season information for a particular season.
        
        Other Parameters
        ----------------
        withGameTypeDates : bool, optional
            Insert a withGameTypeDates to return season information for all gameTypes.
        fields : str
            Comma delimited list of specific fields to be returned. 
            Format: topLevelNode, childNode, attribute
        
        Returns
        -------
        Season
            returns a season object

        See Also
        --------
        Mlb.get_all_seasons : return a list of seasons

        Examples
        --------
        >>> mlb = Mlb()
        >>> mlb.get_season(season_id="2021", sport_id=1)
        Season
        """
        if sport_id is not None:
            params['sportId'] = sport_id
            
        mlb_data = self._mlb_adapter_v1.get(endpoint=f'seasons/{season_id}', ep_params=params)
        if 400 <= mlb_data.status_code <= 499:
            return None

        if 'seasons' in mlb_data.data and mlb_data.data['seasons']:
            for season in mlb_data.data['seasons']:
                return Season(**season)

    def get_seasons(self, sport_id: int = 1, **params) -> List[Season]:
        """
        return a season object for sportid

        Parameters
        ----------
        sport_id : int
            Insert a sportId to return a directory of seasons for a specific 
            sport.

        Other Parameters
        ----------------
        divisionId : int, optional
            Insert divisionId to return a directory of seasons for a specific 
            division.
        leagueId : int, optional
            Insert leagueId to return a directory of seasons in a specific 
            league.
        withGameTypeDates : bool, optional
            Insert a withGameTypeDates to return season information for all 
            gameTypes.
        fields : str
            Comma delimited list of specific fields to be returned. 
            Format: topLevelNode, childNode, attribute
            
        Returns
        -------
        Season
            returns a season object

        See Also
        --------
        Mlb.get_current_season : return a current Season

        Examples
        --------
        >>> mlb = Mlb()
        >>> mlb.get_all_seasons(1)
        [Season, Season, Season, Season]
        >>> mlb = Mlb()
        >>> mlb.get_all_seasons(leagueId=104)
        [Season, Season, Season, Season]
        >>> mlb = Mlb()
        >>> mlb.get_all_seasons(leagueId=103, withGameTypeDates=True)
        [Season, Season, Season, Season]
        """
        if sport_id is not None:
            params['sportId'] = sport_id

        mlb_data = self._mlb_adapter_v1.get(endpoint='seasons/all', ep_params=params)
        if 400 <= mlb_data.status_code <= 499:
            return []

        season_list = []

        if 'seasons' in mlb_data.data and mlb_data.data['seasons']:
            for season in mlb_data.data['seasons']:
                season_list.append(Season(**season))
        
        return season_list

    def get_standings(self, league_id: int, season: str, **params):
        """
        return a list of standings for league_id and season

        Parameters
        ----------
        league_id : str
            Insert leagueId to return all standings based on a particular 
            standingType for a specific league.
        season : str
            Insert year to return all standings based on a particular year.

        Other Parameters
        ----------------
        standingsTypes : str
            Insert standingType to return all standings based on a particular 
            year.
            Description of all standingTypes:
                regularSeason - Regular Season Standings
                wildCard - Wild card standings
                divisionLeaders - Division Leader standings
                wildCardWithLeaders - Wild card standings with Division 
                Leaders firstHalf - First half standings. Only valid for 
                                    leagues with a split season 
                                    (Mexican League).
                secondHalf - Second half standings. Only valid for leagues 
                             with a split season (Mexican League).
                springTraining - Spring Training Standings
                postseason - Postseason Standings
                byDivision - Standings by Division
                byConference - Standings by Conference
                byLeague - Standings by League  
            Find standingTypes at https://statsapi.mlb.com/api/v1/standingsTypes
        date : str
            Insert date to return standing information for on a particular 
            date. Format: MM/DD/YYYY
        hydrate : str
            Insert Hydration(s) to return data for any available standings 
            hydration. Format "team,league"
            Available Hydrations:
                team
                league
                division
                sport
                conference
                record(conference)
                record(division)
        fields : str
            Comma delimited list of specific fields to be returned. Format: topLevelNode, childNode, attribute

        Returns
        -------
        list of Standings
            returns a list of Standings
        See Also
        --------

        Examples
        --------
        """
        if league_id is not None:
            params['leagueId'] = league_id

        if season is not None:
            params['season'] = season

        mlb_data = self._mlb_adapter_v1.get(endpoint=f'standings', ep_params=params)
        if 400 <= mlb_data.status_code <= 499:
            return []
        
        standings_list = []

        if 'records' in mlb_data.data and mlb_data.data['records']:
            for standing in mlb_data.data['records']:
                standings_list.append(Standings(**standing))
        
        return standings_list


    def get_attendance(self, team_id: int = None, league_id: int = None,
                       league_list_id: str = None, 
                       **params) -> Union[Attendance, None]:
        """
        returns attendance data based on teamId, leagueId, or leagueListId.

        Required Parameters (at least one)
        ----------
        team_id : int
            Insert a teamId to return directory of attendnace for a given team
        league_id : int
            Insert leagueId(s) to return a directory of attendanace for a 
            specific league. Format '103,104'
        league_list_id : str
            Insert a unique League List Identifier to return a directory of 
            attendanace for a specific league listId.
            Available values : milb_full, milb_short, milb_complex, milb_all, 
            milb_all_nomex, milb_all_domestic, milb_noncomp, 
            milb_noncomp_nomex, milb_domcomp, milb_intcomp, win_noabl, 
            win_caribbean, win_all, abl, mlb, mlb_hist, mlb_milb, 
            mlb_milb_hist, mlb_milb_win, baseball_all

        Parameters
        ----------
        season : int
            Insert year(s) to return a directory of attendance for a given 
            season. Season year number format yyyy
        date : str 'yyyy-mm-dd'
            Insert date to return information for attendance on a particular 
            date. Format: MM/DD/YYYY
        gametype : str
            Insert gameType(s) a directory of attendance for a given gameType.
            For a list of all gameTypes: 
            https://statsapi.mlb.com/api/v1/gameTypes
    
        Returns
        -------
        Attendance

        See Also
        --------
        Mlb.get_leagues : return a list of Leagues
        Mlb.get_venues : return a list of Venues

        Examples
        --------
        >>> mlb = Mlb()
        >>> mlb.get_attendance(team_id=133, {'season': 2022})
        Attendance
        """
        required_args = {'teamId': team_id, 'leagueId': league_id, 'leagueListId': league_list_id}

        if not any(required_args):
            return

        # let's create a list of the args passed
        # this will filter out None
        for arg_name, arg_value in required_args.items():
            if arg_value:
                params[arg_name] = arg_value

        mlb_data = self._mlb_adapter_v1.get('attendance', ep_params=params)
        if 400 <= mlb_data.status_code <= 499:
            return None

        if 'records' in mlb_data.data and mlb_data.data['records']:
            return Attendance(**mlb_data.data)

    def get_draft(self, year_id: int, **params) -> List[Round]:
        """
        return a draft object for year_id

        Parameters
        ----------
        year_id : int
            Insert a year_id to return a directory of seasons for a specific sport.

        Other Parameters
        ----------------
        round : str
            Insert a round to return biographical and financial data for a specific round in a Rule 4 draft.
        name : str
            Insert the first letter of a draftees last name to return their Rule 4 biographical and financial data.
        school : str
            Insert the first letter of a draftees school to return their Rule 4 biographical and financial data.
        state : str
            Insert state to return a list of Rule 4 draftees from that given state
        country : str
            Insert state to return a list of Rule 4 draftees from that given state
        position : str
            Insert the position to return Rule 4 biographical and financial data for a players drafted at that position.    
        teamId : int
            Insert teamId to return Rule 4 biographical and financial data for all picks made by a specific team.
        playerId : int
            Insert MLB playerId to return a player's Rule 4 biographical and financial data a specific Rule 4 draft.
        bisPlayerId : int
            Insert bisPlayerId to return a player's Rule 4 biographical and financial data a specific Rule 4 draft.

        Returns
        -------
        list of DraftPicks
            returns a list of DraftPicks
            
        See Also
        --------

        Examples
        --------
        """
        mlb_data = self._mlb_adapter_v1.get(endpoint=f'draft/{year_id}', ep_params=params)
        if 400 <= mlb_data.status_code <= 499:
            return []

        round_list = []

        if 'drafts' in mlb_data.data and mlb_data.data['drafts']:
            if mlb_data.data['drafts']['rounds']:
                for round in mlb_data.data['drafts']['rounds']:
                    round_list.append(Round(**round))
        return round_list

    def get_awards(self, award_id: str, **params) -> List[Award]:
        """
        return a list of awards for award_id

        Parameters
        ----------
        award_id : str
            Insert a awardId to return a directory of players for a given award.

        Other Parameters
        ----------------
        sportId : int
            Insert a sportId to return a directory of players for a given award in a specific sport.
        leagueId : int, List[int]
            Insert leagueId(s) to return a directory of players for a given award in a specific league. Format '103,104'
        season : int, List[int]
            Insert year(s) to return a directory of players for a given award in a given season. Format '2016,2017'

        Returns
        -------
        list of Awards
            returns a list of awards
        See Also
        --------

        Examples
        --------
        """

        mlb_data = self._mlb_adapter_v1.get(endpoint=f'awards/{award_id}/recipients?', ep_params=params)
        if 400 <= mlb_data.status_code <= 499:
            return []
        
        awards_list = []

        if 'awards' in mlb_data.data and mlb_data.data['awards']:
            for award in mlb_data.data['awards']:
                awards_list.append(Award(**award))
        
        return awards_list

    def get_homerun_derby(self, game_id, **params) -> Union[Homerunderby, None]:
        """
        The homerun derby endpoint on the Stats API allows for users to 
        request information from the MLB database pertaining to the 
        homerun derby. This is endpoint contains Statcast trajectory, 
        launchSpeed, launchAngle, & hit coordinates data. Also a timeRemaning 
        string is added to track the progress of the derby in real time.

        Parameters
        ----------
        game_id : int
            Insert gamePk to return HomerunDerby data for a specific gamepk.

        Other Parameters
        ----------------
        fields : str
            Format: Comma delimited list of specific fields to be returned. Format: topLevelNode, childNode, attribute

        Returns
        -------
        Homerunderby object

        See Also
        --------

        Examples
        --------
        """
        mlb_data = self._mlb_adapter_v1.get(endpoint=f'homeRunDerby/{game_id}', ep_params=params)
        if 400 <= mlb_data.status_code <= 499:
            None
        
        if 'status' in mlb_data.data and mlb_data.data['status']:
            return Homerunderby(**mlb_data.data)


    def get_team_stats(self, team_id: int, stats: list, groups: list, **params) -> dict:
        """
        returns a split stat data for a team

        Parameters
        ----------
        team_id : int
            the team id 
        stats : list
            list of stat types. List of statTypes can be found at https://statsapi.mlb.com/api/v1/statTypes
        groups : list
            list of stat grous. List of statGroups can be found at https://statsapi.mlb.com/api/v1/statGroups

        Other Parameters
        ----------------
        season : str
            Insert year to return team stats for a particular season, season=2018

        Returns
        -------
        dict 
            returns a dict of stats

        See Also
        --------
        Mlb.get_player_stats : Get stats for a player
        Mlb.get_stats : Get stats
        Mlb.get_player_stats : Get player stats


        Examples
        --------
        >>> mlb = Mlb()
        >>> stats = ['season', 'seasonAdvanced']
        >>> groups = ['pitching']
        >>> mlb.get_team_stats(133, stats, groups)
        {'pitching': {'season': [PitchingSeason], 'seasonadvanced': [PitchingSeasonAdvanced] }}
        """
        params['stats'] = stats
        params['group'] = groups

        mlb_data = self._mlb_adapter_v1.get(endpoint=f'teams/{team_id}/stats', ep_params=params)
        if 400 <= mlb_data.status_code <= 499:
            return {}

        if 'stats' in mlb_data.data and mlb_data.data['stats']:
            splits = mlb_module.create_split_data(mlb_data.data['stats'])
        else:
            return {}
            
        return splits

    def get_players_stats_for_game(self, person_id: int, game_id: int, **params) -> dict:
        """
        Insert personId and gamePk to view stats for individual player based on a specific game.
         
         Fielding, Hitting, & Pitching gameLog Statistics as well as vsPlayer stats.

        Parameters
        ----------
        person_id : int
            the team id 
        game_id : list
            list of stat types

        Returns
        -------
        dict 
            returns a dict of stats

        See Also
        --------
        Mlb.get_team_stats : Get team stats
        Mlb.get_player_stats : Get stats for a player
        Mlb.get_stats : Get stats

        Examples
        --------
        >>> mlb = Mlb()
        >>> player_id = 663728
        >>> game_id = 715757
        >>> stats = mlb.get_player_stats_for_game(person_id=person_id, game_id=game_id)
        >>> print(stats['stats']['gamelog'])
        >>> print(stats['hitting']['playlog'])
        """
        mlb_data = self._mlb_adapter_v1.get(endpoint=f'people/{person_id}/stats/game/{game_id}')
        if 400 <= mlb_data.status_code <= 499:
            return {}

        if 'stats' in mlb_data.data and mlb_data.data['stats']:
            splits = mlb_module.create_split_data(mlb_data.data['stats'])
        else:
            return {}
            
        return splits
        
    def get_player_stats(self, person_id: int, stats: list, groups: list, **params) -> dict:
        """
        returns stat data for a team

        Parameters
        ----------
        person_id : int
            the person id
        stats : list
            list of stat types. List of statTypes can be found at https://statsapi.mlb.com/api/v1/statTypes
        groups : list
            list of stat grous. List of statGroups can be found at https://statsapi.mlb.com/api/v1/statGroups

        Other Parameters
        ----------------
        season : str
            Insert year to return team stats for a particular season, season=2018
        eventType : str
            Notes for individual events for playLog, playlog can be filered by individual events.
            List of eventTypes can be found at https://statsapi.mlb.com/api/v1/eventTypes

        Returns
        -------
        dict
            returns a dict of stats

        See Also
        --------
        Mlb.get_stats : Get stats
        Mlb.get_team_stats : Get team stats
        Mlb.get_players_stats_for_game : Get player stats for a game

        Examples
        --------
        >>> mlb = Mlb()
        >>> stats = ['season', 'seasonAdvanced']
        >>> groups = ['hitting']
        >>> mlb.get_player_stats(647351, stats, groups)
        {'hitting': {'season': [HittingSeason], 'seasonadvanced': [HittingSeasonAdvanced] }}
        """
        params['stats'] = stats
        params['group'] = groups

        mlb_data = self._mlb_adapter_v1.get(endpoint=f'people/{person_id}/stats', ep_params=params)
        if 400 <= mlb_data.status_code <= 499:
            return {}

        if 'stats' in mlb_data.data and mlb_data.data['stats']:
            splits = mlb_module.create_split_data(mlb_data.data['stats'])
        else:
            return {}

        return splits

    def get_stats(self, stats: list, groups: list, **params: dict) -> dict:
        """
        return a stat dictionary

        Parameters
        ----------
        params : dict
            dict of params to pass
        stats : list
            list of stat types. List of statTypes can be found at https://statsapi.mlb.com/api/v1/statTypes
        groups : list
            list of stat grous. List of statGroups can be found at https://statsapi.mlb.com/api/v1/statGroups

        Other Parameters
        ----------------
        season : str
            Insert year to return team stats for a particular season, season=2018
        teamId : int
            Insert teamId to return statistics for a given team. Default to "Qualified" playerPool.
            For a list of all teamIds : Mlb.get_leagues()
        leagueId : int
            Insert leagueId to return statistics for a given league. Default to "Qualified" playerPool
            For a list of all leagueIds : Mlb.get_leagues()
        gameType : str
            Insert gameType to return statistics for a given sport or league based on gameType. Default to "Qualified" playerPool
            Find available gameType at https://statsapi.mlb.com/api/v1/gameTypes
        sportIds : int
            Insert sportId to return statistics for a given sport.
            For a list of all sportIds : Mlb.get_sports()

        Returns
        -------
        splits : dict

        See Also
        --------
        Mlb.get_team_stats : Get team stats
        Mlb.get_player_stats : Get player stats
        Mlb.get_players_stats_for_game : Get player stats for a game

        Examples
        --------
        >>> mlb = Mlb()
        >>> mlb.get_stats()
        """
        params['stats'] = stats
        params['group'] = groups

        mlb_data = self._mlb_adapter_v1.get(endpoint='stats', ep_params=params)
        if 400 <= mlb_data.status_code <= 499:
            return {}

        if 'stats' in mlb_data.data and mlb_data.data['stats']:
            splits = mlb_module.create_split_data(mlb_data)
        else:
            return {}
            
        return splits



