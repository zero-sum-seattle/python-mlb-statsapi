"""Offline regression tests for MlbResult.

These tests protect MlbResult constructor behavior for version 0.8.0,
including independent data dictionaries and caller-owned dictionary safety.
"""

from mlbstatsapi import MlbResult


def test_stores_status_message_and_data():
    result = MlbResult(200, "OK", {"sports": [{"id": 1}]})

    assert result.status_code == 200
    assert result.message == "OK"
    assert result.data == {"sports": [{"id": 1}]}


def test_converts_status_code_to_int():
    result = MlbResult("200", "OK", {"value": True})

    assert result.status_code == 200
    assert isinstance(result.status_code, int)


def test_converts_message_to_str():
    result = MlbResult(200, 123, {"value": True})

    assert result.message == "123"
    assert isinstance(result.message, str)


def test_type_coercion_for_status_and_message():
    result = MlbResult("200", 123, {"value": True})

    assert result.status_code == 200
    assert result.message == "123"
    assert result.data == {"value": True}


def test_removes_copyright_from_result_data():
    result = MlbResult(
        200,
        "OK",
        {
            "copyright": "Copyright 2026 MLB Advanced Media, L.P.",
            "sports": [{"id": 1, "name": "Major League Baseball"}],
        },
    )

    assert "copyright" not in result.data
    assert result.data == {"sports": [{"id": 1, "name": "Major League Baseball"}]}


def test_accepts_omitted_data_argument():
    result = MlbResult(200, "OK")

    assert result.status_code == 200
    assert result.message == "OK"
    assert result.data == {}


def test_accepts_explicitly_supplied_dictionary():
    payload = {"teams": [{"id": 133}]}
    result = MlbResult(200, "OK", payload)

    assert result.data == {"teams": [{"id": 133}]}


def test_each_instance_gets_independent_data_dict():
    first = MlbResult(200, "OK")
    second = MlbResult(200, "OK")

    first.data["changed"] = True

    assert second.data == {}
    assert first.data is not second.data


def test_does_not_mutate_caller_owned_dictionary():
    payload = {
        "copyright": "MLB",
        "sports": [],
    }

    result = MlbResult(200, "OK", payload)

    assert payload == {
        "copyright": "MLB",
        "sports": [],
    }
    assert result.data == {
        "sports": [],
    }
