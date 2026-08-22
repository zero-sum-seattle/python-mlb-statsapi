# mlbstatsapi/async_mlb.py

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from ._helpers.schedule import build_schedule_params
from ._parsers.divisions import parse_division, parse_divisions
from ._parsers.leagues import parse_league, parse_leagues
from ._parsers.people import parse_person, parse_people
from ._parsers.roster import parse_roster_coaches, parse_roster_players
from ._parsers.schedules import parse_schedule
from ._parsers.seasons import parse_season, parse_seasons
from ._parsers.sports import parse_sport, parse_sports
from ._parsers.teams import parse_team, parse_teams
from .async_mlb_dataadapter import AsyncMlbDataAdapter
from .mlb_dataadapter import DEFAULT_TIMEOUT, TimeoutType
from .models.divisions import Division
from .models.leagues import League
from .models.people import Coach, Person, Player
from .models.schedules import Schedule
from .models.seasons import Season
from .models.sports import Sport
from .models.teams import Team

if TYPE_CHECKING:
    import httpx


class AsyncMlb:
    """Asynchronous client for the MLB Stats API."""

    def __init__(
        self,
        hostname: str = "statsapi.mlb.com",
        logger: logging.Logger | None = None,
        timeout: TimeoutType = DEFAULT_TIMEOUT,
        client: "httpx.AsyncClient | None" = None,
        *,
        strict_http: bool = True,
    ):
        self._logger = logger or logging.getLogger(__name__)

        self._mlb_adapter_v1 = AsyncMlbDataAdapter(
            hostname=hostname,
            ver="v1",
            logger=self._logger,
            timeout=timeout,
            client=client,
            strict_http=strict_http,
        )

    async def aclose(self) -> None:
        """Close library-owned async resources."""
        await self._mlb_adapter_v1.aclose()

    async def __aenter__(self) -> "AsyncMlb":
        return self

    async def __aexit__(
        self,
        exc_type,
        exc,
        traceback,
    ) -> None:
        try:
            await self.aclose()
        except BaseException:
            # Cleanup must not replace an exception or cancellation that
            # already occurred inside the async context.
            if exc is None:
                raise

            self._logger.exception(
                "AsyncMlb cleanup failed while preserving the original exception"
            )

    async def get_team(
        self,
        team_id: int,
        **params,
    ) -> Team | None:
        """
        Returns a team based on teamId.

        Async counterpart of ``Mlb.get_team``.

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
        AsyncMlb.get_teams : Return a list of Teams from sport id.

        Examples
        --------
        >>> async with AsyncMlb() as mlb:
        ...     team = await mlb.get_team(133)
        Team
        """
        mlb_data = await self._mlb_adapter_v1.get(
            endpoint=f"teams/{team_id}",
            ep_params=params,
        )

        if 400 <= mlb_data.status_code <= 499:
            return None

        return parse_team(mlb_data.data)

    async def get_teams(
        self,
        sport_id: int = 1,
        **params,
    ) -> list[Team]:
        """
        return the all Teams

        Async counterpart of ``Mlb.get_teams``.

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
        AsyncMlb.get_team : Return a Team from id

        Examples
        --------
        >>> async with AsyncMlb() as mlb:
        ...     teams = await mlb.get_teams()
        [Team, Team, Team]
        """
        params["sportId"] = sport_id

        mlb_data = await self._mlb_adapter_v1.get(
            endpoint="teams",
            ep_params=params,
        )

        if 400 <= mlb_data.status_code <= 499:
            return []

        return parse_teams(mlb_data.data)

    async def get_team_roster(
        self,
        team_id: int,
        **params,
    ) -> list[Player]:
        """
        return the team player roster

        Async counterpart of ``Mlb.get_team_roster``.

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
        AsyncMlb.get_team : Return a Team from id
        AsyncMlb.get_team_coaches : Return a list of Coaches from team id

        Examples
        --------
        >>> async with AsyncMlb() as mlb:
        ...     roster = await mlb.get_team_roster(133)
        [Player, Player, Player]
        """
        mlb_data = await self._mlb_adapter_v1.get(
            endpoint=f"teams/{team_id}/roster",
            ep_params=params,
        )

        if 400 <= mlb_data.status_code <= 499:
            return []

        return parse_roster_players(mlb_data.data)

    async def get_team_coaches(
        self,
        team_id: int,
        **params,
    ) -> list[Coach]:
        """
        Return a directory of coaches for a particular team.

        Async counterpart of ``Mlb.get_team_coaches``.

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
        AsyncMlb.get_team : Return a Team from id
        AsyncMlb.get_team_roster : Return a list of Players from team id

        Examples
        --------
        >>> async with AsyncMlb() as mlb:
        ...     coaches = await mlb.get_team_coaches(133)
        [Coach, Coach, Coach]
        """
        mlb_data = await self._mlb_adapter_v1.get(
            endpoint=f"teams/{team_id}/coaches",
            ep_params=params,
        )

        if 400 <= mlb_data.status_code <= 499:
            return []

        return parse_roster_coaches(mlb_data.data)

    async def get_person(
        self,
        player_id: int,
        **params,
    ) -> Person | None:
        """
        This endpoint returns statistical data and biographical information
        for a player,coach or umpire based on playerId.

        Async counterpart of ``Mlb.get_person``.

        Parameters
        ----------
        player_id : int
            Insert personId for a specific player, coach or umpire based on
            playerId.

        Returns
        -------
        Person
            Returns a Person

        See Also
        --------
        AsyncMlb.get_people : Return a list of People from sport id.

        Examples
        --------
        >>> async with AsyncMlb() as mlb:
        ...     person = await mlb.get_person(660271)
        Person
        """
        mlb_data = await self._mlb_adapter_v1.get(
            endpoint=f"people/{player_id}",
            ep_params=params,
        )

        if 400 <= mlb_data.status_code <= 499:
            return None

        return parse_person(mlb_data.data)

    async def get_people(
        self,
        sport_id: int = 1,
        **params,
    ) -> list[Person]:
        """
        return the all players for sportid

        Async counterpart of ``Mlb.get_people``, which reads the
        ``sports/{sport_id}/players`` endpoint rather than ``people``.

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
        AsyncMlb.get_person : Return Person from id.

        Examples
        --------
        >>> async with AsyncMlb() as mlb:
        ...     people = await mlb.get_people()
        [Person, Person, Person]
        """
        mlb_data = await self._mlb_adapter_v1.get(
            endpoint=f"sports/{sport_id}/players",
            ep_params=params,
        )

        if 400 <= mlb_data.status_code <= 499:
            return []

        return parse_people(mlb_data.data)


    async def get_schedule(
        self,
        date: str = None,
        start_date: str = None,
        end_date: str = None,
        sport_id: int = 1,
        team_id: int = None,
        **params,
    ) -> Schedule | None:
        """
        return the schedule created from the included params.

        Async counterpart of ``Mlb.get_schedule``.

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

        Examples
        --------
        >>> async with AsyncMlb() as mlb:
        ...     schedule = await mlb.get_schedule(start_date="2021-08-01", end_date="2021-08-11")
        Schedule
        """
        params = build_schedule_params(
            date=date,
            start_date=start_date,
            end_date=end_date,
            sport_id=sport_id,
            team_id=team_id,
            **params,
        )

        if params is None:
            return None

        mlb_data = await self._mlb_adapter_v1.get(
            endpoint="schedule",
            ep_params=params,
        )


        if 400 <= mlb_data.status_code <= 499:
            return None

        return parse_schedule(mlb_data.data)

    async def get_sport(
        self,
        sport_id: int,
        **params,
    ) -> Sport | None:
        """
        return sport object from sport_id

        Async counterpart of ``Mlb.get_sport``.

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
        AsyncMlb.get_sports : return a list of sports

        Examples
        --------
        >>> async with AsyncMlb() as mlb:
        ...     sport = await mlb.get_sport(1)
        Sport
        """
        mlb_data = await self._mlb_adapter_v1.get(
            endpoint=f"sports/{sport_id}",
            ep_params=params,
        )

        if 400 <= mlb_data.status_code <= 499:
            return None

        return parse_sport(mlb_data.data)

    async def get_sports(
        self,
        **params,
    ) -> list[Sport]:
        """
        return all sports

        Async counterpart of ``Mlb.get_sports``.

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
        AsyncMlb.get_sport : return a sport from id

        Examples
        --------
        >>> async with AsyncMlb() as mlb:
        ...     sports = await mlb.get_sports()
        [Sport, Sport, Sport]
        """
        mlb_data = await self._mlb_adapter_v1.get(
            endpoint="sports",
            ep_params=params,
        )

        if 400 <= mlb_data.status_code <= 499:
            return []

        return parse_sports(mlb_data.data)

    async def get_league(
        self,
        league_id: int,
        **params,
    ) -> League | None:
        """
        return league

        Async counterpart of ``Mlb.get_league``.

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
        AsyncMlb.get_leagues : return a list of Leagues

        Examples
        --------
        >>> async with AsyncMlb() as mlb:
        ...     league = await mlb.get_league(103)
        League
        """
        mlb_data = await self._mlb_adapter_v1.get(
            endpoint=f"leagues/{league_id}",
            ep_params=params,
        )

        if 400 <= mlb_data.status_code <= 499:
            return None

        return parse_league(mlb_data.data)

    async def get_leagues(
        self,
        **params,
    ) -> list[League]:
        """
        return all leagues

        Async counterpart of ``Mlb.get_leagues``.

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
        AsyncMlb.get_league : return a League from league id

        Examples
        --------
        >>> async with AsyncMlb() as mlb:
        ...     leagues = await mlb.get_leagues()
        [League, League, League]
        """
        mlb_data = await self._mlb_adapter_v1.get(
            endpoint="leagues",
            ep_params=params,
        )

        if 400 <= mlb_data.status_code <= 499:
            return []

        return parse_leagues(mlb_data.data)

    async def get_division(
        self,
        division_id: int,
        **params,
    ) -> Division | None:
        """
        Returns a division based on divisionId,

        Async counterpart of ``Mlb.get_division``.

        Parameters
        ----------
        division_id : int
            divisionId to return a directory of division(s) for a specific division.

        Returns
        -------
        Division
            returns a Division

        See Also
        --------
        AsyncMlb.get_divisions : return a list of Divisions

        Examples
        --------
        >>> async with AsyncMlb() as mlb:
        ...     division = await mlb.get_division(200)
        Division
        """
        mlb_data = await self._mlb_adapter_v1.get(
            endpoint=f"divisions/{division_id}",
            ep_params=params,
        )

        if 400 <= mlb_data.status_code <= 499:
            return None

        return parse_division(mlb_data.data)

    async def get_divisions(
        self,
        **params,
    ) -> list[Division]:
        """
        return all divisons

        Async counterpart of ``Mlb.get_divisions``.

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
        AsyncMlb.get_division : return a Division from id

        Examples
        --------
        >>> async with AsyncMlb() as mlb:
        ...     divisions = await mlb.get_divisions()
        [Division, Division, Division]
        """
        mlb_data = await self._mlb_adapter_v1.get(
            endpoint="divisions",
            ep_params=params,
        )

        if 400 <= mlb_data.status_code <= 499:
            return []

        return parse_divisions(mlb_data.data)

    async def get_season(
        self,
        season_id: str,
        sport_id: int = 1,
        **params,
    ) -> Season | None:
        """
        return a season object for seasonid and sportid

        Async counterpart of ``Mlb.get_season``.

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
        AsyncMlb.get_seasons : return a list of seasons

        Examples
        --------
        >>> async with AsyncMlb() as mlb:
        ...     season = await mlb.get_season(season_id="2021", sport_id=1)
        Season
        """
        if sport_id is not None:
            params["sportId"] = sport_id

        mlb_data = await self._mlb_adapter_v1.get(
            endpoint=f"seasons/{season_id}",
            ep_params=params,
        )

        if 400 <= mlb_data.status_code <= 499:
            return None

        return parse_season(mlb_data.data)

    async def get_seasons(
        self,
        sport_id: int = 1,
        **params,
    ) -> list[Season]:
        """
        return a season object for sportid

        Async counterpart of ``Mlb.get_seasons``.

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
        AsyncMlb.get_season : return a Season from season id

        Examples
        --------
        >>> async with AsyncMlb() as mlb:
        ...     seasons = await mlb.get_seasons(1)
        [Season, Season, Season, Season]
        """
        if sport_id is not None:
            params["sportId"] = sport_id

        mlb_data = await self._mlb_adapter_v1.get(
            endpoint="seasons/all",
            ep_params=params,
        )

        if 400 <= mlb_data.status_code <= 499:
            return []

        return parse_seasons(mlb_data.data)
