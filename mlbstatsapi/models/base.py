from pydantic import BaseModel, ConfigDict, BeforeValidator
from typing import Annotated
def to_camel_case(value: str) -> str:
    parts = value.split("_")
    if not parts:
        return value
    return parts[0] + "".join(part[:1].upper() + part[1:] for part in parts[1:])


def float_or_none(v)-> float | None:
    try:
        f = float(v)
        return f
    except (TypeError, ValueError):
        return None

OptionalFloat = Annotated[float | None, BeforeValidator(float_or_none)]

class MLBBaseModel(BaseModel):
    """Common base for all MLB Stats API models.

    - Pydantic v2
    - Ignores unknown fields to remain resilient to API changes
    - populate_by_name allows alias-based population when needed
    """
    model_config = ConfigDict(
        extra="ignore",
        alias_generator=to_camel_case,
        populate_by_name=True,
        # MLB's API occasionally returns numbers for fields that are logically strings
        # (e.g. liveData.plays.*.playEvents.*.base can be 1/2/3).
        # Enable coercion to be resilient to these inconsistencies.
        coerce_numbers_to_str=True,
    )
