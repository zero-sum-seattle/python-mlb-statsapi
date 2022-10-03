import unittest
from mlbstatsapi.models.stats import Stats
from mlbstatsapi.mlbapi import Mlb


class TestStatCreation(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.mlb = Mlb()
        cls.player = cls.mlb.get_person(664034)[0]
        cls.position_player = cls.mlb.get_person(664034)[0]
        cls.pitcher_player = cls.mlb.get_person(660271)[0]
        cls.catcher_player = cls.mlb.get_person(663728)[0]
        cls.traded_position_player = cls.mlb.get_person(665742)[0]
        cls.team = cls.mlb.get_team(133)[0]

    @classmethod
    def tearDownClass(cls) -> None:
        pass

    def test_player_adapter(self):
        self.assertTrue(hasattr(self.player, "_mlb_adapter"))


    def test_team_adapter_generate_stats_select_type(self):
        self.assertTrue(hasattr(self.team, "_mlb_adapter"))

    def test_player_generate_stats_select_group(self):
        """Pitcher Player is Shohei Ohtani, who is a AL Pitcher and Position player"""
        stat_groups = ["hitting", "pitching"]
        stat_objects = self.pitcher_player.get_stats(stat_groups=stat_groups)
        self.assertEqual(len(stat_objects), 2, "two stat objects should be present")
        for x in range(len(stat_objects)):
            self.assertIsInstance(stat_objects[x], Stats, "Stat objects should be a Stat Object")
            self.assertTrue(hasattr(stat_objects[x], "stat_group"), "Stat objects should have stat_group attr")
            self.assertTrue(hasattr(stat_objects[x], "stat_type"), "Stat objects should have stat_type attr")


    def test_player_generate_stats_select_group_and_type(self):
        """
        Position Player should return six stat_type objects for that stat_group
        
        Only the season and career stat types will return a hitting stat object
        """
        stat_types = ["projected", "projectedRos", "season", "standard", "advanced", "career"]
        stat_groups = ["hitting"]

        stat_objects = self.position_player.get_stats(stat_groups=stat_groups, stat_types=stat_types)

        number_of_stats = len(stat_objects)

        self.assertEqual(number_of_stats, 2, "Two stat objects should be present. season and career")
        for x in range(number_of_stats):
            self.assertTrue(stat_objects[x].stat_type in stat_types, "Stat types returned should be in list")

    def test_player_hitting_season_stats_attrs(self):
        stat_types = ["season"]
        stat_groups = ["hitting"]

        season_hitting_stat = self.traded_position_player.get_stats(stat_groups=stat_groups, stat_types=stat_types)[0]
        for split in season_hitting_stat.splits:
            self.assertIsInstance(split.gamesPlayed, int, "gamesPlayed should be int")
            self.assertIsInstance(split.avg, str, "avg should return a str")

    def test_player_pitching_season_stats_attrs(self):
        stat_types = ["season"]
        stat_groups = ["pitching"]

        season_pitching_stat = self.pitcher_player.get_stats(stat_groups=stat_groups, stat_types=stat_types)[0]
        print(season_pitching_stat.__dict__)
        for split in season_pitching_stat.splits:
            print(split.__dict__)
            self.assertIsInstance(split.strikeOuts, int, "gamesPlayed should be int")
            self.assertIsInstance(split.hitByPitch, int, "hitByPitch should return a int")








