from typing import List, Dict

class Stats():
    # Stats don't have an ID
    def __init__(self, playerId=None, teamId=None) -> None:
        self.playerId = playerId # this needs to be OR
        self.teamId = teamId # this needs to be OR


class StatsSeason(Stats):
    def __init__(self, stats) -> None:
        self.stats = stats


class StatsGroupHitting(object):
    def __init__(self) -> None:
        pass












    # "gamesPlayed" : 149,
    # "groundOuts" : 1316,
    # "airOuts" : 1275,
    # "runs" : 519,
    # "doubles" : 230,
    # "triples" : 12,
    # "homeRuns" : 126,
    # "strikeOuts" : 1289,
    # "baseOnBalls" : 394,
    # "intentionalWalks" : 6,
    # "hits" : 1055,
    # "hitByPitch" : 57,
    # "avg" : ".216",
    # "atBats" : 4884,
    # "obp" : ".281",
    # "slg" : ".345",
    # "ops" : ".626",
    # "caughtStealing" : 21,
    # "stolenBases" : 72,
    # "stolenBasePercentage" : ".774",
    # "groundIntoDoublePlay" : 103,
    # "numberOfPitches" : 20803,
    # "plateAppearances" : 5388,
    # "totalBases" : 1687,
    # "rbi" : 489,
    # "leftOnBase" : 888,
    # "sacBunts" : 20,
    # "sacFlies" : 31,
    # "babip" : ".265",
    # "groundOutsToAirouts" : "1.03",
    # "catchersInterference" : 2,
    # "atBatsPerHomeRun" : "38.76"

        # self.__regular = MlbDataWrapper(
        #     career=career_regular, season=season_regular, yearByYear=yearByYear_regular
        # )
        # self.__advanced = MlbDataWrapper(
        #     career=career_advanced, season=season_advanced, yearByYear=yearByYear_advanced
        # )

        # self.__career = MlbDataWrapper(regular=career_regular, advanced=career_advanced)
        # self.__season = MlbDataWrapper(regular=season_regular, advanced=season_advanced)
        # self.__yearByYear = MlbDataWrapper(regular=yearByYear_regular, advanced=yearByYear_advanced)

        # self.__sabermetrics = sabermetrics
        # self.__expectedStatistics = expectedStatistics

    # @property
    # def season(self):
    #     return self.__season

    # @property
    # def career(self):
    #     return self.__career

    # @property
    # def yearByYear(self):
    #     return self.__yearByYear

    # @property
    # def regular(self):
    #     return self.__regular

    # @property
    # def standard(self):
    #     return self.__regular

    # @property
    # def advanced(self):
    #     return self.__advanced

    # @property
    # def sabermetrics(self):
    #     return self.__sabermetrics

    # @property
    # def expectedStatistics(self):
    #     return self.__expectedStatistics


# class PlayerStats(MlbDataWrapper):
#     def __init__(
#         self,
#         season_hitting = None,
#         season_pitching = None,
#         season_fielding = None,
#         seasonAdvanced_hitting = None,
#         seasonAdvanced_pitching = None,
#         seasonAdvanced_fielding = None,
#         career_hitting = None,
#         career_pitching = None,
#         career_fielding = None,
#         careerAdvanced_hitting = None,
#         careerAdvanced_pitching = None,
#         careerAdvanced_fielding = None,
#         yearByYear_hitting = None,
#         yearByYear_pitching = None,
#         yearByYear_fielding = None,
#         yearByYearAdvanced_hitting = None,
#         yearByYearAdvanced_pitching = None,
#         yearByYearAdvanced_fielding = None,
#         sabermetrics_hitting = None,
#         sabermetrics_pitching = None,
#         sabermetrics_fielding = None,
#         expectedStatistics_hitting = None,
#         expectedStatistics_pitching = None,
#         expectedStatistics_fielding = None,
#         sprayChart = None,
#         hotColdZones = None
#     ):
#         super().__init__(
#             **{
#                 "season_hitting" : season_hitting,
#                 "season_pitching" : season_pitching,
#                 "season_fielding" : season_fielding,
#                 "seasonAdvanced_hitting" : seasonAdvanced_hitting,
#                 "seasonAdvanced_pitching" : seasonAdvanced_pitching,
#                 "seasonAdvanced_fielding" : seasonAdvanced_fielding,
#                 "career_hitting" : career_hitting,
#                 "career_pitching" : career_pitching,
#                 "career_fielding" : career_fielding,
#                 "careerAdvanced_hitting" : careerAdvanced_hitting,
#                 "careerAdvanced_pitching" : careerAdvanced_pitching,
#                 "careerAdvanced_fielding" : careerAdvanced_fielding,
#                 "yearByYear_hitting" : yearByYear_hitting,
#                 "yearByYear_pitching" : yearByYear_pitching,
#                 "yearByYear_fielding" : yearByYear_fielding,
#                 "yearByYearAdvanced_hitting" : yearByYearAdvanced_hitting,
#                 "yearByYearAdvanced_pitching" : yearByYearAdvanced_pitching,
#                 "yearByYearAdvanced_fielding" : yearByYearAdvanced_fielding,
#                 "sabermetrics_hitting" : sabermetrics_hitting,
#                 "sabermetrics_pitching" : sabermetrics_pitching,
#                 "sabermetrics_fielding" : sabermetrics_fielding,
#                 "expectedStatistics_hitting" : expectedStatistics_hitting,
#                 "expectedStatistics_pitching" : expectedStatistics_pitching,
#                 "expectedStatistics_fielding" : expectedStatistics_fielding,
#                 "sprayChart" : sprayChart,
#                 "hotColdZones" : hotColdZones
#             }
#         )

#         self.__hitting = StatGroup(
#             season_regular=season_hitting,
#             season_advanced=seasonAdvanced_hitting,
#             career_regular=career_hitting,
#             career_advanced=careerAdvanced_hitting,
#             yearByYear_regular=yearByYear_hitting,
#             yearByYear_advanced=yearByYearAdvanced_hitting,
#             sabermetrics=sabermetrics_hitting,
#             expectedStatistics=expectedStatistics_hitting,
#         )
#         self.__pitching = StatGroup(
#             season_regular=season_pitching,
#             season_advanced=seasonAdvanced_pitching,
#             career_regular=career_pitching,
#             career_advanced=careerAdvanced_pitching,
#             yearByYear_regular=yearByYear_pitching,
#             yearByYear_advanced=yearByYearAdvanced_pitching,
#             sabermetrics=sabermetrics_pitching,
#             expectedStatistics=expectedStatistics_pitching,
#         )
#         self.__fielding = StatGroup(
#             season_regular=season_fielding,
#             career_regular=career_fielding,
#             yearByYear_regular=yearByYear_fielding,
#         )
#         self.__sprayChart = sprayChart
#         self.__hotColdZones = hotColdZones

#     @property
#     def hitting(self):
#         """Player's hitting stats (regular or advanced)"""
#         return self.__hitting

#     @property
#     def pitching(self):
#         """Player's pitching stats (regular or advanced)"""
#         return self.__pitching

#     @property
#     def fielding(self):
#         """Player's fielding stats"""
#         return self.__fielding

#     @property
#     def sprayChart(self):
#         """Player's sprayChart stats"""
#         return self.__sprayChart

#     @property
#     def hotColdZones(self):
#         """Player's hotColdZones stats"""
#         return self.__hotColdZones


# class StatGroup(MlbDataWrapper):
#     def __init__(
#         self,
#         career_regular = None,
#         career_advanced = None,
#         season_regular = None,
#         season_advanced = None,
#         yearByYear_regular = None,
#         yearByYear_advanced = None,
#         sabermetrics = None,
#         expectedStatistics = None,
#     ):

#         self.__regular = MlbDataWrapper(
#             career=career_regular, season=season_regular, yearByYear=yearByYear_regular
#         )
#         self.__advanced = MlbDataWrapper(
#             career=career_advanced, season=season_advanced, yearByYear=yearByYear_advanced
#         )

#         self.__career = MlbDataWrapper(regular=career_regular, advanced=career_advanced)
#         self.__season = MlbDataWrapper(regular=season_regular, advanced=season_advanced)
#         self.__yearByYear = MlbDataWrapper(regular=yearByYear_regular, advanced=yearByYear_advanced)

#         self.__sabermetrics = sabermetrics
#         self.__expectedStatistics = expectedStatistics

#     @property
#     def season(self):
#         return self.__season

#     @property
#     def career(self):
#         return self.__career

#     @property
#     def yearByYear(self):
#         return self.__yearByYear

#     @property
#     def regular(self):
#         return self.__regular

#     @property
#     def standard(self):
#         return self.__regular

#     @property
#     def advanced(self):
#         return self.__advanced

#     @property
#     def sabermetrics(self):
#         return self.__sabermetrics

#     @property
#     def expectedStatistics(self):
#         return self.__expectedStatistics


# class PlayerStats(MlbDataWrapper):
#     def __init__(
#         self,
#         season_hitting = None,
#         season_pitching = None,
#         season_fielding = None,
#         seasonAdvanced_hitting = None,
#         seasonAdvanced_pitching = None,
#         seasonAdvanced_fielding = None,
#         career_hitting = None,
#         career_pitching = None,
#         career_fielding = None,
#         careerAdvanced_hitting = None,
#         careerAdvanced_pitching = None,
#         careerAdvanced_fielding = None,
#         yearByYear_hitting = None,
#         yearByYear_pitching = None,
#         yearByYear_fielding = None,
#         yearByYearAdvanced_hitting = None,
#         yearByYearAdvanced_pitching = None,
#         yearByYearAdvanced_fielding = None,
#         sabermetrics_hitting = None,
#         sabermetrics_pitching = None,
#         sabermetrics_fielding = None,
#         expectedStatistics_hitting = None,
#         expectedStatistics_pitching = None,
#         expectedStatistics_fielding = None,
#         sprayChart = None,
#         hotColdZones = None
#     ):
#         super().__init__(
#             **{
#                 "season_hitting" : season_hitting,
#                 "season_pitching" : season_pitching,
#                 "season_fielding" : season_fielding,
#                 "seasonAdvanced_hitting" : seasonAdvanced_hitting,
#                 "seasonAdvanced_pitching" : seasonAdvanced_pitching,
#                 "seasonAdvanced_fielding" : seasonAdvanced_fielding,
#                 "career_hitting" : career_hitting,
#                 "career_pitching" : career_pitching,
#                 "career_fielding" : career_fielding,
#                 "careerAdvanced_hitting" : careerAdvanced_hitting,
#                 "careerAdvanced_pitching" : careerAdvanced_pitching,
#                 "careerAdvanced_fielding" : careerAdvanced_fielding,
#                 "yearByYear_hitting" : yearByYear_hitting,
#                 "yearByYear_pitching" : yearByYear_pitching,
#                 "yearByYear_fielding" : yearByYear_fielding,
#                 "yearByYearAdvanced_hitting" : yearByYearAdvanced_hitting,
#                 "yearByYearAdvanced_pitching" : yearByYearAdvanced_pitching,
#                 "yearByYearAdvanced_fielding" : yearByYearAdvanced_fielding,
#                 "sabermetrics_hitting" : sabermetrics_hitting,
#                 "sabermetrics_pitching" : sabermetrics_pitching,
#                 "sabermetrics_fielding" : sabermetrics_fielding,
#                 "expectedStatistics_hitting" : expectedStatistics_hitting,
#                 "expectedStatistics_pitching" : expectedStatistics_pitching,
#                 "expectedStatistics_fielding" : expectedStatistics_fielding,
#                 "sprayChart" : sprayChart,
#                 "hotColdZones" : hotColdZones
#             }
#         )

#         self.__hitting = StatGroup(
#             season_regular=season_hitting,
#             season_advanced=seasonAdvanced_hitting,
#             career_regular=career_hitting,
#             career_advanced=careerAdvanced_hitting,
#             yearByYear_regular=yearByYear_hitting,
#             yearByYear_advanced=yearByYearAdvanced_hitting,
#             sabermetrics=sabermetrics_hitting,
#             expectedStatistics=expectedStatistics_hitting,
#         )
#         self.__pitching = StatGroup(
#             season_regular=season_pitching,
#             season_advanced=seasonAdvanced_pitching,
#             career_regular=career_pitching,
#             career_advanced=careerAdvanced_pitching,
#             yearByYear_regular=yearByYear_pitching,
#             yearByYear_advanced=yearByYearAdvanced_pitching,
#             sabermetrics=sabermetrics_pitching,
#             expectedStatistics=expectedStatistics_pitching,
#         )
#         self.__fielding = StatGroup(
#             season_regular=season_fielding,
#             career_regular=career_fielding,
#             yearByYear_regular=yearByYear_fielding,
#         )
#         self.__sprayChart = sprayChart
#         self.__hotColdZones = hotColdZones

#     @property
#     def hitting(self):
#         """Player's hitting stats (regular or advanced)"""
#         return self.__hitting

#     @property
#     def pitching(self):
#         """Player's pitching stats (regular or advanced)"""
#         return self.__pitching

#     @property
#     def fielding(self):
#         """Player's fielding stats"""
#         return self.__fielding

#     @property
#     def sprayChart(self):
#         """Player's sprayChart stats"""
#         return self.__sprayChart

#     @property
#     def hotColdZones(self):
#         """Player's hotColdZones stats"""
#         return self.__hotColdZones