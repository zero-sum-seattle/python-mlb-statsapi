import unittest
from mlbstatsapi.models.venues import Venue
from mlbstatsapi import Mlb
from pydantic import ValidationError


class TestVenue(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.mlb = Mlb()
        cls.venue = cls.mlb.get_venue(31)

    @classmethod
    def tearDownClass(cls) -> None:
        pass

    def test_venue_instance_type_error(self):
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
        self.assertTrue(hasattr(self.venue, "fieldinfo"))
        self.assertTrue(hasattr(self.venue, "active"))
