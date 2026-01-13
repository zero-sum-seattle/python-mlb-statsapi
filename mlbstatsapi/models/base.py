from pydantic import BaseModel, ConfigDict


class MLBBaseModel(BaseModel):
    """Common base for all MLB Stats API models.

    - Pydantic v2
    - Ignores unknown fields to remain resilient to API changes
    - populate_by_name allows alias-based population when needed
    """

    model_config = ConfigDict(
        extra="ignore",
        populate_by_name=True,
    )
