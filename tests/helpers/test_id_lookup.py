from mlbstatsapi._helpers.id_lookup import find_ids_by_key


def test_find_ids_by_key_matches_case_insensitively():
    items = [
        {"id": 133, "name": "Athletics"},
        {"id": 147, "name": "Yankees"},
    ]

    assert find_ids_by_key(items, "name", "athletics") == [133]


def test_find_ids_by_key_returns_every_match():
    items = [
        {"id": 1, "name": "Duplicate"},
        {"id": 2, "name": "Duplicate"},
        {"id": 3, "name": "Other"},
    ]

    assert find_ids_by_key(items, "name", "Duplicate") == [1, 2]


def test_find_ids_by_key_returns_empty_list_for_no_match():
    assert find_ids_by_key([{"id": 1, "name": "Athletics"}], "name", "Yankees") == []
    assert find_ids_by_key([], "name", "Athletics") == []


def test_find_ids_by_key_skips_items_missing_the_search_key_or_id():
    items = [
        {"id": 1},
        {"name": "Athletics"},
        {"id": 2, "name": "Athletics"},
    ]

    assert find_ids_by_key(items, "name", "Athletics") == [2]
