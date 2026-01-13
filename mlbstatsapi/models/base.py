from pydantic import BaseModel, ConfigDict


def to_camel_case(value: str) -> str:
    parts = value.split("_")
    if not parts:
        return value
    return parts[0] + "".join(part[:1].upper() + part[1:] for part in parts[1:])


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
    )
