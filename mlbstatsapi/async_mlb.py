# mlbstatsapi/async_mlb.py

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from ._helpers.schedule import build_schedule_params
from ._parsers.people import parse_person, parse_people
from ._parsers.schedules import parse_schedule
from ._parsers.teams import parse_team, parse_teams
from .async_mlb_dataadapter import AsyncMlbDataAdapter
from .mlb_dataadapter import DEFAULT_TIMEOUT, TimeoutType
from .models.people import Person
from .models.schedules import Schedule
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
        """Return every Team for a sport id.

        Async counterpart of ``Mlb.get_teams``; see that method for the
        supported keyword parameters.
        """
        params["sportId"] = sport_id

        mlb_data = await self._mlb_adapter_v1.get(
            endpoint="teams",
            ep_params=params,
        )

        if 400 <= mlb_data.status_code <= 499:
            return []

        return parse_teams(mlb_data.data)

    async def get_person(
        self,
        player_id: int,
        **params,
    ) -> Person | None:
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
        """Return every player for a sport id.

        Async counterpart of ``Mlb.get_people``, which reads the
        ``sports/{sport_id}/players`` endpoint rather than ``people``.
        """
        mlb_data = await self._mlb_adapter_v1.get(
            endpoint=f"sports/{sport_id}/players",
            ep_params=params,
        )

        if 400 <= mlb_data.status_code <= 499:
            return []

        return parse_people(mlb_data.data)

    async def get_persons(
        self,
        person_ids: str | list[int],
        **params,
    ) -> list[Person]:
        """Return a Person for each requested person id.

        Async counterpart of ``Mlb.get_persons``; ``person_ids`` accepts the
        same ``'605151,592450'`` or ``[605151, 592450]`` forms.
        """
        params["personIds"] = person_ids

        mlb_data = await self._mlb_adapter_v1.get(
            endpoint="people",
            ep_params=params,
        )

        if 400 <= mlb_data.status_code <= 499:
            return []

        return parse_people(mlb_data.data)

    async def get_people_id(
        self,
        fullname: str,
        sport_id: int = 1,
        search_key: str = "fullName",
        **params,
    ) -> list[int]:
        """Return the person ids whose ``search_key`` matches ``fullname``.

        Async counterpart of ``Mlb.get_people_id``; matching is
        case-insensitive and people missing ``search_key`` are skipped.
        """
        # Used to reduce the amount of unneccessary data requested from api
        params["fields"] = "people,id,fullName"

        mlb_data = await self._mlb_adapter_v1.get(
            endpoint=f"sports/{sport_id}/players",
            ep_params=params,
        )

        if 400 <= mlb_data.status_code <= 499:
            return []

        player_ids = []

        if "people" in mlb_data.data and mlb_data.data["people"]:
            for person in mlb_data.data["people"]:
                try:
                    if person[search_key].lower() == fullname.lower():
                        player_ids.append(person["id"])
                except KeyError:
                    continue

        return player_ids

    async def get_team_id(
        self,
        team_name: str,
        search_key: str = "name",
        **params,
    ) -> list[int]:
        """Return the team ids whose ``search_key`` matches ``team_name``.

        Async counterpart of ``Mlb.get_team_id``; matching is
        case-insensitive and teams missing ``search_key`` are skipped.
        """
        # Used to reduce the amount of unneccessary data requested from api
        params["fields"] = "teams,id,name"

        mlb_data = await self._mlb_adapter_v1.get(
            endpoint="teams",
            ep_params=params,
        )

        if 400 <= mlb_data.status_code <= 499:
            return []

        team_ids = []

        if "teams" in mlb_data.data and mlb_data.data["teams"]:
            for team in mlb_data.data["teams"]:
                try:
                    if team[search_key].lower() == team_name.lower():
                        team_ids.append(team["id"])
                except KeyError:
                    continue

        return team_ids

    async def get_schedule(
        self,
        date: str = None,
        start_date: str = None,
        end_date: str = None,
        sport_id: int = 1,
        team_id: int = None,
        **params,
    ) -> Schedule | None:

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
