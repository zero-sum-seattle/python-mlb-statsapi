import pytest

from mlbstatsapi.models.game.livedata.linescore.attributes import LinescoreOffense
from mlbstatsapi.models.game.livedata.plays.play.attributes import PlayReviewDetails
from mlbstatsapi.models.game.livedata.plays.play.playevent.playevent import PlayEvent
from mlbstatsapi.models.game.livedata.plays.playbyinning.attributes import HitCoordinates
from mlbstatsapi.models.game.livedata.plays.play.playrunner.attributes import RunnerMovement


# These gamepk IDs are taken from a user-submitted error log where the MLB API payload
# was rejected by Pydantic validation. The underlying issues are schema inconsistencies
# in MLB's API responses (int where str expected, dict where str expected, null where bool expected).

GAMEPKS_BASE_INT = [
    776160, 776165, 776219, 776252, 776286, 776320, 776336, 776351, 776386, 776420,
    776498, 776659, 776759, 776770, 776903, 776937, 777091, 777135, 777191, 777265,
    777305, 777445, 777488, 777514, 777555, 777570, 777650, 777722,
    # Additional gamepks reported later (same base=int issue)
    744814, 744819, 744824, 744826, 744832, 744836, 744837, 744838,
    745146, 745542, 745796, 745799,
    747000, 747080, 747170,
]

GAMEPKS_ISOUT_NULL = [
    776320, 776545,
    # Additional gamepks reported later (same isOut=null issue)
    744832, 744836,
]

GAMEPKS_UMPIRE_DICT = [
    776221, 776367, 776420, 776525, 776650, 776850, 776903,
    # Additional gamepks reported later (same umpire=dict issue)
    744831, 747000,
]

GAMEPKS_ADDITIONAL_REVIEWS_LIST = [
    776259, 776386, 777213, 777544, 777555,
    # Additional gamepks reported later (same additionalReviews=list issue)
    747000,
]

GAMEPKS_LINESCORE_OFFENSE_RUNNER_DICT = [
    776784, 777091,
    # Additional gamepks reported later (same offense.*=person dict issue)
    744814, 747080,
]

GAMEPKS_HIT_COORDS_NULL = [
    778077,
]


@pytest.mark.parametrize("gamepk", GAMEPKS_BASE_INT)
def test_gamepk_play_event_base_coerces_int_to_str(gamepk: int):
    # path in log: liveData.plays.*.playEvents.*.base is int
    evt = PlayEvent(details={}, index=0, isPitch=True, type="pitch", base=1)
    assert evt.base == "1"


@pytest.mark.parametrize("gamepk", GAMEPKS_ISOUT_NULL)
def test_gamepk_runner_movement_is_out_coerces_null_to_false(gamepk: int):
    # path in log: liveData.plays.*.runners.*.movement.isOut is null
    mv = RunnerMovement(isOut=None)
    assert mv.is_out is False


@pytest.mark.parametrize("gamepk", GAMEPKS_UMPIRE_DICT)
def test_gamepk_play_event_umpire_accepts_person_object(gamepk: int):
    # path in log: liveData.plays.*.playEvents.*.umpire is a dict {id, link}
    evt = PlayEvent(
        details={},
        index=0,
        isPitch=True,
        type="pitch",
        umpire={"id": 484499, "link": "/api/v1/people/484499"},
    )
    assert evt.umpire is not None


@pytest.mark.parametrize("gamepk", GAMEPKS_ADDITIONAL_REVIEWS_LIST)
def test_gamepk_review_details_additional_reviews_accepts_list(gamepk: int):
    # path in log: liveData.plays.allPlays.*.reviewDetails.additionalReviews is a list
    rd = PlayReviewDetails(
        isOverturned=False,
        inProgress=False,
        reviewType="NA",
        additionalReviews=[{"isOverturned": False, "reviewType": "NA", "challengeTeamId": 120}],
    )
    assert isinstance(rd.additional_reviews, list)


@pytest.mark.parametrize("gamepk", GAMEPKS_LINESCORE_OFFENSE_RUNNER_DICT)
def test_gamepk_linescore_offense_baserunners_accept_person_object(gamepk: int):
    # path in log: liveData.linescore.offense.first/second/third is a dict person object
    offense = LinescoreOffense(
        team={"id": 120, "link": "/api/v1/teams/120"},
        first={"id": 682928, "fullName": "Runner One", "link": "/api/v1/people/682928"},
        second=None,
        third=None,
    )
    assert offense.first is not None


@pytest.mark.parametrize("gamepk", GAMEPKS_HIT_COORDS_NULL)
def test_gamepk_hit_coordinates_accept_null_x_y(gamepk: int):
    coords = HitCoordinates(x=None, y=None)
    assert coords.x is None
    assert coords.y is None


