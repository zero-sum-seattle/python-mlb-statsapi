# mlbstatsapi/async_mlb.py

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from ._parsers.people import parse_person, parse_people
from ._parsers.schedules import parse_schedule, build_schedule_params
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
        **params,
    ) -> list[Team]:
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
        person_ids: Union[str, List[int]],
        **params,
    ) -> list[Person]:

        params['personIds'] = person_ids

        mlb_data = await self._mlb_adapter_v1.get(
            endpoint="people",
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
