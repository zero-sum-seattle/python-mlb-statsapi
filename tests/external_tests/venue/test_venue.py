import unittest
from unittest.mock import patch

from pydantic import ValidationError
from mlbstatsapi.models.venues import Venue
from mlbstatsapi import Mlb
from mlbstatsapi.mlb_dataadapter import MlbResult


class TestVenue(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.mlb = Mlb()
        cls.venue = cls.mlb.get_venue(31)

    @classmethod
    def tearDownClass(cls) -> None:
        pass

    def test_venue_instance_type_error(self):
        """Pydantic raises ValidationError when required fields are missing."""
        with self.assertRaises(ValidationError):
            venue = Venue()

    def test_venue_instance_position_arguments(self):
        self.assertEqual(self.venue.id, 31)
        self.assertEqual(self.venue.link, "/api/v1/venues/31")
        self.assertEqual(self.venue.name, "PNC Park")
        self.assertEqual(self.venue.active, True)

    def test_venue_attributes(self):
        self.assertIsInstance(self.venue, Venue)
        self.assertTrue(hasattr(self.venue, "id"))
        self.assertTrue(hasattr(self.venue, "link"))
        self.assertTrue(hasattr(self.venue, "name"))
        self.assertTrue(hasattr(self.venue, "location"))
        self.assertTrue(hasattr(self.venue, "timezone"))
        self.assertTrue(hasattr(self.venue, "field_info"))
        self.assertTrue(hasattr(self.venue, "active"))

    def test_venue_hydrated_attributes_are_populated(self):
        """get_venue requests location, fieldInfo and timezone, so they must arrive.

        hasattr passes on any pydantic model whether or not the value came through,
        which is why the hydrate parameter could be sent in a form MLB ignored without
        any test noticing.
        """
        self.assertIsNotNone(self.venue.location)
        self.assertIsNotNone(self.venue.timezone)
        self.assertIsNotNone(self.venue.field_info)
        self.assertEqual(self.venue.location.city, "Pittsburgh")
        self.assertEqual(self.venue.timezone.id, "America/New_York")

    def test_venue_hydrate_is_sent_as_one_comma_delimited_value(self):
        """A list becomes repeated hydrate params, which MLB answers without hydrating."""
        captured = {}

        def capture(endpoint, ep_params=None, data=None):
            captured.update(ep_params or {})
            return MlbResult(200, "OK", {})

        with patch.object(self.mlb._mlb_adapter_v1, "get", side_effect=capture):
            self.mlb.get_venue(31)
            self.assertEqual(captured["hydrate"], "location,fieldInfo,timezone")

            captured.clear()
            self.mlb.get_venues()
            self.assertEqual(captured["hydrate"], "location,fieldInfo,timezone")
