from unittest.mock import patch

from mlbstatsapi import Mlb, MlbResult


GAME_PK = 831508


def _empty_schedule_result() -> MlbResult:
    """Return a valid empty schedule response without calling the MLB API."""
    return MlbResult(
        status_code=200,
        message="OK",
        data={"dates": []},
    )


def test_get_scheduled_games_by_date_allows_gamepk_without_date():
    """
    Regression test for #245.

    A gamePk is a valid selector for the MLB schedule endpoint and should not
    require a date. The current bug returns None before the adapter is called.

    This test verifies that a gamePk-only request reaches the adapter and that
    the expected parameters are passed through without adding date parameters.
    """
    with Mlb() as mlb:
        # Replace the real HTTP call with a deterministic fake response.
        with patch.object(
            mlb._mlb_adapter_v1,
            "get",
            return_value=_empty_schedule_result(),
        ) as adapter_get:
            mlb.get_scheduled_games_by_date(gamePks=GAME_PK)

    # The important regression check: the method must not return before
    # attempting the schedule request.
    adapter_get.assert_called_once()

    call = adapter_get.call_args

    # Verify that the correct MLB endpoint would have been requested.
    assert call.kwargs["endpoint"] == "schedule"

    params = call.kwargs["ep_params"]

    # gamePks should be preserved as a valid schedule selector.
    assert params["gamePks"] == GAME_PK

    # sportId is still expected to use its existing default.
    assert params["sportId"] == 1

    # A gamePk-only lookup should not invent any date constraints.
    assert "date" not in params
    assert "startDate" not in params
    assert "endDate" not in params


def test_get_schedule_allows_gamepk_without_date():
    """
    Verify that get_schedule() has the same gamePk-only behavior.

    While #245 was reported against get_scheduled_games_by_date(), get_schedule()
    contains the same early date validation and can fail for the same reason.
    """
    with Mlb() as mlb:
        # Prevent a real network request while recording how the adapter is used.
        with patch.object(
            mlb._mlb_adapter_v1,
            "get",
            return_value=_empty_schedule_result(),
        ) as adapter_get:
            mlb.get_schedule(gamePks=GAME_PK)

    # gamePks alone should be enough for execution to reach the adapter.
    adapter_get.assert_called_once()

    call = adapter_get.call_args

    assert call.kwargs["endpoint"] == "schedule"

    params = call.kwargs["ep_params"]

    # Preserve the caller's gamePk filter and the normal sportId default.
    assert params["gamePks"] == GAME_PK
    assert params["sportId"] == 1

    # No date parameters should be required for a gamePk-specific lookup.
    assert "date" not in params
    assert "startDate" not in params
    assert "endDate" not in params