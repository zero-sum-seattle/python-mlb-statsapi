from mlbstatsapi.models.data import CodeDesc, PlayDetails


def test_codedesc_accepts_missing_code():
    """
    Regression test for #342.

    Game 777961 returns a play event whose details.type has a description of
    "Unknown" and no code. Validation used to fail because code was required.
    """
    code_desc = CodeDesc(description="Unknown")

    assert code_desc.code is None
    assert code_desc.description == "Unknown"


def test_play_details_accepts_type_without_code():
    """The missing code must not break parsing of the enclosing play details."""
    details = PlayDetails.model_validate(
        {"description": "Status Change - Pre-Game", "type": {"description": "Unknown"}}
    )

    assert details.type is not None
    assert details.type.code is None
    assert details.type.description == "Unknown"


def test_codedesc_still_populates_code_when_present():
    """Making code optional must not stop a present code from populating the field."""
    code_desc = CodeDesc.model_validate({"code": "R", "description": "Right"})

    assert code_desc.code == "R"
    assert code_desc.description == "Right"
