from typing import Dict, List
from unittest.mock import patch
import unittest


from mlbstatsapi.models.people import Person

from mlbstatsapi import Mlb
from mlbstatsapi import MlbResult
from mlbstatsapi import TheMlbStatsApiException

class TestMlbDataApi(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.mlb = Mlb()
        pass

    @classmethod
    def tearDownClass(cls) -> None:
        pass

    def test_mlb_adapter_200(self):
        mlbdata = self.mlb._mlb_adapter_v1.get("/divisions")
        self.assertIsInstance(mlbdata, MlbResult)
        self.assertEqual(mlbdata.status_code, 200)
        self.assertIsInstance(mlbdata.data, Dict)

    def test_mlb_adapter_500(self):
        """mlb should raise a exception when adapter returns a 500"""
        with self.assertRaises(TheMlbStatsApiException):
            self.mlb._mlb_adapter_v1.get(endpoint="teams/133/stats?stats=vsPlayer&group=catching")

    def test_mlb_adapter_400(self):
        """mlb should return a MlbResult object with a empty data, and a status code"""
        # invalid endpoint 
        mlbdata = self.mlb._mlb_adapter_v1.get(endpoint="teams/19990")

        # result.status_code should be 404
        self.assertEqual(mlbdata.status_code, 404)

        # result.data should be None
        self.assertEqual(mlbdata.data, {})


class TestMlbGetPeople(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.mlb = Mlb()
        pass

    @classmethod
    def tearDownClass(cls) -> None:
        pass

    def test_mlbdataapi_get_people(self):
        """mlb get_people should return a list of all sport 1 people"""
        mlbdata = self.mlb.get_people()
        self.assertIsInstance(mlbdata, List)
        self.assertIsInstance(mlbdata[0], Person)

    def test_mlbdataapi_get_people_with_sportid(self):
        """mlb get_people should return a list of all sport 1 people"""
        mlbdata = self.mlb.get_people(sport_id=11)
        self.assertIsInstance(mlbdata, List)
        self.assertIsInstance(mlbdata[0], Person)

    def test_mlb_get_person(self):
        """mlb get_person should return a Person object"""
        person = self.mlb.get_person('664034')
        self.assertIsInstance(person, Person)
        self.assertEqual(person.id, 664034)

    def test_mlb_failed_get_person(self):
        """mlb get_person should return None for invalid id"""
        person = self.mlb.get_person('664')
        self.assertIsNone(person)

    def test_mlb_get_person_id(self):
        """mlb get_person_id should return a person id"""
        id = self.mlb.get_people_id('Ty France')
        self.assertEqual(id, [664034])

    def test_mlb_get_person_id_with_sportid(self):
        """mlb get_person_id should return a person id"""
        id = self.mlb.get_people_id('Fernando Abad', sport_id=11)
        self.assertEqual(id, [472551])

    def test_mlb_get_invalid_person_id(self):
        """mlb get_person_id should return empty list for invalid name"""
        id = self.mlb.get_people_id('Joe Blow')
        self.assertEqual(id, [])