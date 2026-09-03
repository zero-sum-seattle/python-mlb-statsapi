"""Normalization helper for MLB Stats API's non-numeric sentinel strings.

The live API represents "not applicable" rate/ratio stats (e.g. a caught
stealing percentage when nobody has attempted a steal) with placeholder
strings instead of omitting the field or returning null. These are the only
two sentinel values observed so far; any other non-numeric string is left
alone so Pydantic's float coercion raises a ValidationError instead of
silently discarding unexpected malformed input.
"""

MLB_FLOAT_SENTINELS = {".---", "-.--"}


def normalize_mlb_float_sentinel(value):
    if isinstance(value, str) and value in MLB_FLOAT_SENTINELS:
        return None
    return value
