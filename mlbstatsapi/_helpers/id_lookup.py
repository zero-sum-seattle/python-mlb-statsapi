def find_ids_by_key(items: list[dict], search_key: str, value: str) -> list[int]:
    """Return the ids of items whose ``search_key`` value case-insensitively matches ``value``.

    Shared by every ``Mlb``/``AsyncMlb`` ``get_*_id`` name-lookup helper. An
    item missing ``search_key`` or ``id`` is silently skipped, matching the
    historical per-endpoint behavior.
    """
    ids = []
    for item in items:
        try:
            if item[search_key].lower() == value.lower():
                ids.append(item["id"])
        except KeyError:
            continue
    return ids
