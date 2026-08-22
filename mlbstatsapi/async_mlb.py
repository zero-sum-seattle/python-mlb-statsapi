# mlbstatsapi/async_mlb.py

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from ._helpers.schedule import build_schedule_params
from ._parsers.attendance import parse_attendance
from ._parsers.awards import parse_awards
from ._parsers.divisions import parse_division, parse_divisions
from ._parsers.draft import parse_draft
from ._parsers.leagues import parse_league, parse_leagues
from ._parsers.people import parse_person, parse_people
from ._parsers.roster import parse_roster_coaches, parse_roster_players
from ._parsers.schedules import parse_schedule
from ._parsers.seasons import parse_season, parse_seasons
from ._parsers.sports import parse_sport, parse_sports
from ._parsers.standings import parse_standings
from ._parsers.teams import parse_team, parse_teams
from ._parsers.venues import parse_venue, parse_venues
from .async_mlb_dataadapter import AsyncMlbDataAdapter
from .mlb_dataadapter import DEFAULT_TIMEOUT, TimeoutType
from .models.attendances import Attendance
from .models.awards import Award
from .models.divisions import Division
from .models.drafts import Round
from .models.leagues import League
from .models.people import Coach, Person, Player
from .models.schedules import Schedule
from .models.seasons import Season
from .models.sports import Sport
from .models.standings import Standings
from .models.teams import Team
from .models.venues import Venue

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

    async def get_venue(
        self,
        venue_id: int,
        **params,
    ) -> Venue | None:
        """
        returns venue directorial information for all available venues in the Stats API.

        Async counterpart of ``Mlb.get_venue``.

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
        AsyncMlb.get_venues : return a list of Venues

        Examples
        --------
        >>> async with AsyncMlb() as mlb:
        ...     venue = await mlb.get_venue(31)
        Venue
        """
        params["hydrate"] = ["location", "fieldInfo", "timezone"]

        mlb_data = await self._mlb_adapter_v1.get(
            endpoint=f"venues/{venue_id}",
            ep_params=params,
        )

        if 400 <= mlb_data.status_code <= 499:
            # Documented quirk: this returns [] rather than None here, unlike
            # every other single-resource endpoint, matching Mlb.get_venue.
            # See docs/public-api.md.
            return []

        return parse_venue(mlb_data.data)

    async def get_venues(
        self,
        **params,
    ) -> list[Venue]:
        """
        return all venues

        Async counterpart of ``Mlb.get_venues``.

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
        AsyncMlb.get_venue : return a Venue

        Examples
        --------
        >>> async with AsyncMlb() as mlb:
        ...     venues = await mlb.get_venues()
        [Venue, Venue, Venue]
        """
        params["hydrate"] = ["location", "fieldInfo", "timezone"]

        mlb_data = await self._mlb_adapter_v1.get(
            endpoint="venues",
            ep_params=params,
        )

        if 400 <= mlb_data.status_code <= 499:
            return []

        return parse_venues(mlb_data.data)

    async def get_standings(
        self,
        league_id: int,
        season: str,
        **params,
    ) -> list[Standings]:
        """
        return a list of standings for league_id and season

        Async counterpart of ``Mlb.get_standings``.

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

        Examples
        --------
        >>> async with AsyncMlb() as mlb:
        ...     standings = await mlb.get_standings(103, "2022")
        [Standings, Standings, Standings]
        """
        if league_id is not None:
            params["leagueId"] = league_id

        if season is not None:
            params["season"] = season

        mlb_data = await self._mlb_adapter_v1.get(
            endpoint="standings",
            ep_params=params,
        )

        if 400 <= mlb_data.status_code <= 499:
            return []

        return parse_standings(mlb_data.data)

    async def get_attendance(
        self,
        team_id: int = None,
        league_id: int = None,
        league_list_id: str = None,
        **params,
    ) -> Attendance | None:
        """
        returns attendance data based on teamId, leagueId, or leagueListId.

        Async counterpart of ``Mlb.get_attendance``.

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
        AsyncMlb.get_leagues : return a list of Leagues
        AsyncMlb.get_venues : return a list of Venues

        Examples
        --------
        >>> async with AsyncMlb() as mlb:
        ...     attendance = await mlb.get_attendance(team_id=133, season=2022)
        Attendance
        """
        required_args = {"teamId": team_id, "leagueId": league_id, "leagueListId": league_list_id}

        if not any(required_args.values()):
            return None

        for arg_name, arg_value in required_args.items():
            if arg_value:
                params[arg_name] = arg_value

        mlb_data = await self._mlb_adapter_v1.get(
            endpoint="attendance",
            ep_params=params,
        )

        if 400 <= mlb_data.status_code <= 499:
            return None

        return parse_attendance(mlb_data.data)

    async def get_draft(
        self,
        year_id: int,
        **params,
    ) -> list[Round]:
        """
        return a draft object for year_id

        Async counterpart of ``Mlb.get_draft``.

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

        Examples
        --------
        >>> async with AsyncMlb() as mlb:
        ...     rounds = await mlb.get_draft(2019)
        [Round, Round, Round]
        """
        mlb_data = await self._mlb_adapter_v1.get(
            endpoint=f"draft/{year_id}",
            ep_params=params,
        )

        if 400 <= mlb_data.status_code <= 499:
            return []

        return parse_draft(mlb_data.data)

    async def get_awards(
        self,
        award_id: str,
        **params,
    ) -> list[Award]:
        """
        return a list of awards for award_id

        Async counterpart of ``Mlb.get_awards``.

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

        Examples
        --------
        >>> async with AsyncMlb() as mlb:
        ...     awards = await mlb.get_awards("ALMVP")
        [Award, Award, Award]
        """
        mlb_data = await self._mlb_adapter_v1.get(
            endpoint=f"awards/{award_id}/recipients?",
            ep_params=params,
        )

        if 400 <= mlb_data.status_code <= 499:
            return []

        return parse_awards(mlb_data.data)
