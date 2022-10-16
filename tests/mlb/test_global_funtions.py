from typing import Dict, List
from mlbstatsapi import _transform_mlbdata
import unittest
import json
import os




class TestMlbFuntions(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        # I still feel like there is a better way to do this
        path_to_current_file = os.path.realpath(__file__)
        current_directory = os.path.dirname(path_to_current_file)
        cls.path_to_file = os.path.join(current_directory, "json_data/players.json")

    @classmethod
    def tearDownClass(cls) -> None:
        pass

    def test_merging_one_dict_transform(self):
        """_transform_mlbdata should return the one dictionary merged with the base"""
        
        with open(self.path_to_file, "r", encoding="utf-8-sig") as file:
            read_json = file.read()
            json_object = json.loads(read_json)

            # pass json_object to transform for transformation to all lowercase key 
            transform_dict = _transform_mlbdata(json_object, mlb_keys=['person'])

            # let's make sure we get a dict back
            self.assertEqual(type(transform_dict), dict)

            # let's check if the keys in person got merged
            self.assertIn('id', transform_dict)
            self.assertIn('link', transform_dict)
            self.assertIn('fullname', transform_dict)
            
    def test_merging_two_dict_transform(self):
        """_transform_mlbdata should return two dictionaries merged with the base"""

        with open(self.path_to_file, "r", encoding="utf-8-sig") as file:
            read_json = file.read()
            json_object = json.loads(read_json)

            # pass json_object to transform for transformation to all lowercase key 
            transform_dict = _transform_mlbdata(json_object, mlb_keys=['person', 'status'])

            # let's make sure we get a dict back
            self.assertEqual(type(transform_dict), dict)

            # let's check if the keys in person got merged
            self.assertIn('id', transform_dict)
            self.assertIn('link', transform_dict)
            self.assertIn('fullname', transform_dict)

            # let's check if the keys in person got merged
            self.assertIn('code', transform_dict)
            self.assertIn('description', transform_dict)




