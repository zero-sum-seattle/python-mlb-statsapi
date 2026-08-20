import asyncio
from unittest.mock import AsyncMock, patch

import pytest

from mlbstatsapi.async_mlb import AsyncMlb


def run_async(coro):
    return asyncio.run(coro)


def test_async_mlb_context_manager_returns_self():
    async def scenario():
        mlb = AsyncMlb()

        async with mlb as entered:
            assert entered is mlb

    run_async(scenario())


def test_async_mlb_aclose_delegates_to_adapter():
    async def scenario():
        mlb = AsyncMlb()

        mlb._mlb_adapter_v1.aclose = AsyncMock()

        await mlb.aclose()

        mlb._mlb_adapter_v1.aclose.assert_awaited_once()

    run_async(scenario())


def test_async_mlb_context_manager_closes_on_normal_exit():
    async def scenario():
        mlb = AsyncMlb()

        mlb._mlb_adapter_v1.aclose = AsyncMock()

        async with mlb:
            pass

        mlb._mlb_adapter_v1.aclose.assert_awaited_once()

    run_async(scenario())


def test_async_mlb_context_manager_closes_when_body_raises():
    async def scenario():
        mlb = AsyncMlb()

        mlb._mlb_adapter_v1.aclose = AsyncMock()

        with pytest.raises(ValueError, match="boom"):
            async with mlb:
                raise ValueError("boom")

        mlb._mlb_adapter_v1.aclose.assert_awaited_once()

    run_async(scenario())


def test_async_mlb_preserves_original_exception_if_cleanup_fails():
    async def scenario():
        mlb = AsyncMlb()

        mlb._mlb_adapter_v1.aclose = AsyncMock(
            side_effect=RuntimeError("cleanup failed")
        )

        with pytest.raises(ValueError, match="original"):
            async with mlb:
                raise ValueError("original")

    run_async(scenario())


def test_async_mlb_cleanup_failure_raises_when_no_original_exception():
    async def scenario():
        mlb = AsyncMlb()

        mlb._mlb_adapter_v1.aclose = AsyncMock(
            side_effect=RuntimeError("cleanup failed")
        )

        with pytest.raises(RuntimeError, match="cleanup failed"):
            async with mlb:
                pass

    run_async(scenario())


def test_async_mlb_preserves_cancellation_during_cleanup():
    async def scenario():
        mlb = AsyncMlb()

        mlb._mlb_adapter_v1.aclose = AsyncMock()

        async def worker():
            async with mlb:
                await asyncio.sleep(60)

        task = asyncio.create_task(worker())

        await asyncio.sleep(0)
        task.cancel()

        with pytest.raises(asyncio.CancelledError):
            await task

        mlb._mlb_adapter_v1.aclose.assert_awaited_once()

    run_async(scenario())
