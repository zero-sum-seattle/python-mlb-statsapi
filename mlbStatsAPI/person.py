import requests
from . import objects as objs

class Person:

    def __init__(self, personId):

        group = "[hitting,pitching,fielding,catching,running]"

        type = "[season,seasonAdvanced,career,careerAdvanced,yearByYear,yearByYearAdvanced,sabermetrics,expectedStatistics,sprayChart,hotColdZones]"

        person_url = f'https://statsapi.mlb.com/api/v1/people/{personId}?'

        params = {
            "hydrate": "stats(group="
            + group
            + ",type="
            + type
            + ")"
        }

        prsn = requests.get(person_url,params=params).json()['people'][0]
        # self._raw_person_data = prsn

        self.personId = personId
        self.primaryPosition = prsn.get('primaryPosition',{})

        self.fullName = prsn['fullName']
        self.firstName = prsn['firstName']
        self.middleName = prsn.get('middleName','')
        self.lastName = prsn['lastName']
        self.pronunciation = prsn.get('pronunciation','')
        self.useName = prsn['useName']
        self.boxscoreName = prsn['boxscoreName']
        self.nickName = prsn.get('nickName','')
        self.primaryNumber = prsn['primaryNumber']
        self.currentAge = prsn['currentAge']

        self.birthDate = prsn.get('birthDate','')
        self.birthCity = prsn.get('birthCity','')
        self.birthStateProvince = prsn.get('birthStateProvince','')
        self.birthCountry = prsn.get('birthCountry','')

        self.deathDate = prsn.get('deathDate',''),
        self.deathCity = prsn.get('deathCity',''),
        self.deathState =  prsn.get('deathStateProvince',''),
        self.deathCountry =  prsn.get('deathCountry',''),

        self.height = prsn['height']
        self.weight = prsn['weight']
        self.bats = prsn['batSide']['code']
        self.throws = prsn['pitchHand']['code']
        self.strikeZoneTop = prsn['strikeZoneTop']
        self.strikeZoneBottom = prsn['strikeZoneBottom']

        self.active = prsn['active']
        self.mlbDebutDate = prsn['mlbDebutDate']



        # Stats
        stat_dict = {
            "season_hitting":[],
            "season_pitching":[],
            "season_fielding":[],

            "seasonAdvanced_hitting":[],
            "seasonAdvanced_pitching":[],

            "career_hitting":[],
            "career_pitching":[],
            "career_fielding":[],

            "careerAdvanced_hitting":[],
            "careerAdvanced_pitching":[],

            "yearByYear_hitting":[],
            "yearByYear_pitching":[],
            "yearByYear_fielding":[],

            "yearByYearAdvanced_hitting":[],
            "yearByYearAdvanced_pitching":[],

            "sabermetrics_hitting":[],
            "sabermetrics_pitching":[],
            "expectedStatistics_hitting":[],
            "expectedStatistics_pitching":[],
            "sprayChart":[],

            "hotColdZones":[]
        }

        for stat_item in prsn['stats']:
            statType = stat_item.get("type",{}).get("displayName")
            statGroup = stat_item.get("group",{}).get("displayName")
            splits = stat_item.get("splits",[{}])

            if statType == "season" or statType == "career":
                data = []
                for s in splits:
                    stats = s.get("stat")

                    team = s.get("team",{})
                    league = s.get("league",{})
                    game_type = s.get("gameType")

                    tm_mlbam = team.get("id","")
                    tm_name = team.get("name","")
                    lg_mlbam = league.get("id","")
                    lg_name = league.get("name","")

                    stats["game_type"] = game_type

                    if statGroup == 'fielding':
                        stats["position"] = s.get("position",{}).get("abbreviation")

                    stats["tm_mlbam"] = tm_mlbam
                    stats["tm_name"] = tm_name
                    stats["lg_mlbam"] = lg_mlbam
                    stats["lg_name"] = lg_name

                    data.append(stats)
                stat_dict[statType+'_'+statGroup] = stats

            if ((statType == "seasonAdvanced" or statType == "careerAdvanced") and (statGroup == "hitting" or statGroup == "pitching")):
                data = []
                for s in splits:
                    # s = splits[0]
                    stats = s.get("stat")

                    team = s.get("team",{})
                    league = s.get("league",{})
                    game_type = s.get("gameType")

                    tm_mlbam = team.get("id","")
                    tm_name = team.get("name","")
                    lg_mlbam = league.get("id","")
                    lg_name = league.get("name","")

                    stats["game_type"] = game_type
                    stats["tm_mlbam"] = tm_mlbam
                    stats["tm_name"] = tm_name
                    stats["lg_mlbam"] = lg_mlbam
                    stats["lg_name"] = lg_name

                    data.append(stats)
                # df = pd.DataFrame(data=data).rename(columns=c.STATDICT)#[c.WO_SEASON+c.COLS_HIT]
                stat_dict[statType+'_'+"hitting"] = stats

            if statType == "yearByYear":
                data = []
                for s in splits:
                    stats = s.get("stat")

                    team = s.get("team",{})
                    league = s.get("league",{})
                    game_type = s.get("gameType")

                    tm_mlbam = team.get("id","")
                    tm_name = team.get("name","")
                    lg_mlbam = league.get("id","")
                    lg_name = league.get("name","")

                    stats["game_type"] = game_type
                    stats["season"] = s.get("season","")

                    if statGroup == 'fielding':
                        stats["position"] = s.get("position",{}).get("abbreviation")

                    stats["tm_mlbam"] = tm_mlbam
                    stats["tm_name"] = tm_name
                    stats["lg_mlbam"] = lg_mlbam
                    stats["lg_name"] = lg_name

                    data.append(stats)
                stat_dict["yearByYear"+'_'+statGroup] = stats

            if statType == "yearByYearAdvanced" and (statGroup == "hitting" or statGroup == "pitching"):
                data = []
                for s in splits:
                    stats = s.get("stat")

                    team = s.get("team",{})
                    league = s.get("league",{})
                    game_type = s.get("gameType")

                    tm_mlbam = team.get("id","")
                    tm_name = team.get("name","")
                    lg_mlbam = league.get("id","")
                    lg_name = league.get("name","")

                    stats["game_type"] = game_type
                    stats["season"] = s.get("season","")
                    stats["tm_mlbam"] = tm_mlbam
                    stats["tm_name"] = tm_name
                    stats["lg_mlbam"] = lg_mlbam
                    stats["lg_name"] = lg_name

                    data.append(stats)
                stat_dict["yearByYearAdvanced"+'_'+statGroup] = stats

            if statType == "sabermetrics" and (statGroup == "hitting" or statGroup == "pitching"):
                data = []
                for s in splits:
                    stats = s.get("stat")

                    team = s.get("team",{})
                    league = s.get("league",{})
                    game_type = s.get("gameType")

                    tm_mlbam = team.get("id","")
                    tm_name = team.get("name","")
                    lg_mlbam = league.get("id","")
                    lg_name = league.get("name","")

                    stats["game_type"] = game_type
                    stats["tm_mlbam"] = tm_mlbam
                    stats["tm_name"] = tm_name
                    stats["lg_mlbam"] = lg_mlbam
                    stats["lg_name"] = lg_name

                    data.append(stats)
                stat_dict["sabermetrics"+'_'+statGroup] = stats

            if statType == "expectedStatistics" and (statGroup == "hitting" or statGroup == "pitching"):
                data = []
                for s in splits:
                    stats = s.get("stat")

                    team = s.get("team",{})
                    league = s.get("league",{})
                    game_type = s.get("gameType")

                    tm_mlbam = team.get("id","")
                    tm_name = team.get("name","")
                    lg_mlbam = league.get("id","")
                    lg_name = league.get("name","")

                    stats["game_type"] = game_type
                    stats["primaryPosition"] = s.get("primaryPosition",{}).get("abbreviation")
                    stats["tm_mlbam"] = tm_mlbam
                    stats["tm_name"] = tm_name
                    stats["lg_mlbam"] = lg_mlbam
                    stats["lg_name"] = lg_name

                    data.append(stats)
                stat_dict["expectedStatistics"+'_'+statGroup] = stats

            if statType == "sprayChart":
                data = []
                for s in splits:
                    stats = s.get("stat")

                    game_type = s.get("gameType")

                    stats["game_type"] = game_type

                    data.append(stats)
                stat_dict["sprayChart"] = stats

            if statType == "hotColdZones":
                data = []
                for s in splits:
                    stats = s.get("stat")

                    name = s.get("name",{})

                    stats["name"] = name

                    data.append(stats)
                stat_dict["hotColdZones"] = stats





        self._stats = objs.PlayerStats(
            season_hitting = stat_dict["season_hitting"],
            season_pitching = stat_dict["season_pitching"],
            season_fielding = stat_dict["season_fielding"],
            seasonAdvanced_hitting = stat_dict["seasonAdvanced_hitting"],
            seasonAdvanced_pitching = stat_dict["seasonAdvanced_pitching"],
            # seasonAdvanced_fielding = stat_dict[,
            career_hitting = stat_dict["career_hitting"],
            career_pitching = stat_dict["career_pitching"],
            career_fielding = stat_dict["career_fielding"],
            careerAdvanced_hitting = stat_dict["careerAdvanced_hitting"],
            careerAdvanced_pitching = stat_dict["careerAdvanced_pitching"],
            # careerAdvanced_fielding = None,
            yearByYear_hitting = stat_dict["yearByYear_hitting"],
            yearByYear_pitching = stat_dict["yearByYear_pitching"],
            yearByYear_fielding = stat_dict["yearByYear_fielding"],
            yearByYearAdvanced_hitting = stat_dict["yearByYearAdvanced_hitting"],
            yearByYearAdvanced_pitching = stat_dict["yearByYearAdvanced_pitching"],
            # yearByYearAdvanced_fielding = stat_dict[""],
            sabermetrics_hitting = stat_dict["sabermetrics_hitting"],
            sabermetrics_pitching = stat_dict["sabermetrics_pitching"],
            # sabermetrics_fielding = stat_dict[""],
            expectedStatistics_hitting = stat_dict["expectedStatistics_hitting"],
            expectedStatistics_pitching = stat_dict["expectedStatistics_pitching"],
            # expectedStatistics_fielding = stat_dict[""],
            sprayChart = stat_dict["sprayChart"],
            hotColdZones = stat_dict["hotColdZones"],
        )





    @property
    def stats(self):
        """Player stats
        """
        return self._stats
