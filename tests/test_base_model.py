from pydantic import Field

from mlbstatsapi.models import MLBBaseModel


class Sample(MLBBaseModel):
    id: int
    full_name: str = Field(alias="fullName")


def test_ignore_extra_fields():
    obj = Sample(id=1, full_name="Test", extra_field="ignored")
    assert obj.id == 1
    assert obj.full_name == "Test"
    # Extra fields should be ignored and not set as attributes
    assert not hasattr(obj, "extra_field")


def test_populate_by_name_alias():
    # populate_by_name allows alias population when present
    obj = Sample(id=1, fullName="Alias Name")  # type: ignore[arg-type]
    assert obj.full_name == "Alias Name"
