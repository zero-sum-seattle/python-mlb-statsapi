import requests
from . import objects as objs
from dataclasses import dataclass, asdict

class MlbDataWrapper:
    """### Data wrapper
    Namespace/subscriptable object for retrieving nested data
    """

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def __getitem__(self, __name: str):
        return getattr(self, __name)

    def __call__(self, _attr):
        return getattr(self, _attr)

class StatGroup(MlbDataWrapper):
    def __init__(
        self,
        career_regular = None,
        career_advanced = None,
        season_regular = None,
        season_advanced = None,
        yearByYear_regular = None,
        yearByYear_advanced = None,
        sabermetrics = None,
        expectedStatistics = None,
    ):

        self.__regular = MlbDataWrapper(
            career=career_regular, season=season_regular, yearByYear=yearByYear_regular
        )
        self.__advanced = MlbDataWrapper(
            career=career_advanced, season=season_advanced, yearByYear=yearByYear_advanced
        )

        self.__career = MlbDataWrapper(regular=career_regular, advanced=career_advanced)
        self.__season = MlbDataWrapper(regular=season_regular, advanced=season_advanced)
        self.__yearByYear = MlbDataWrapper(regular=yearByYear_regular, advanced=yearByYear_advanced)

        self.__sabermetrics = sabermetrics
        self.__expectedStatistics = expectedStatistics

    @property
    def season(self):
        return self.__season

    @property
    def career(self):
        return self.__career

    @property
    def yearByYear(self):
        return self.__yearByYear

    @property
    def regular(self):
        return self.__regular

    @property
    def standard(self):
        return self.__regular

    @property
    def advanced(self):
        return self.__advanced

    @property
    def sabermetrics(self):
        return self.__sabermetrics

    @property
    def expectedStatistics(self):
        return self.__expectedStatistics


class PlayerStats(MlbDataWrapper):
    def __init__(
        self,
        season_hitting = None,
        season_pitching = None,
        season_fielding = None,
        seasonAdvanced_hitting = None,
        seasonAdvanced_pitching = None,
        seasonAdvanced_fielding = None,
        career_hitting = None,
        career_pitching = None,
        career_fielding = None,
        careerAdvanced_hitting = None,
        careerAdvanced_pitching = None,
        careerAdvanced_fielding = None,
        yearByYear_hitting = None,
        yearByYear_pitching = None,
        yearByYear_fielding = None,
        yearByYearAdvanced_hitting = None,
        yearByYearAdvanced_pitching = None,
        yearByYearAdvanced_fielding = None,
        sabermetrics_hitting = None,
        sabermetrics_pitching = None,
        sabermetrics_fielding = None,
        expectedStatistics_hitting = None,
        expectedStatistics_pitching = None,
        expectedStatistics_fielding = None,
        sprayChart = None,
        hotColdZones = None
    ):
        super().__init__(
            **{
                "season_hitting" : season_hitting,
                "season_pitching" : season_pitching,
                "season_fielding" : season_fielding,
                "seasonAdvanced_hitting" : seasonAdvanced_hitting,
                "seasonAdvanced_pitching" : seasonAdvanced_pitching,
                "seasonAdvanced_fielding" : seasonAdvanced_fielding,
                "career_hitting" : career_hitting,
                "career_pitching" : career_pitching,
                "career_fielding" : career_fielding,
                "careerAdvanced_hitting" : careerAdvanced_hitting,
                "careerAdvanced_pitching" : careerAdvanced_pitching,
                "careerAdvanced_fielding" : careerAdvanced_fielding,
                "yearByYear_hitting" : yearByYear_hitting,
                "yearByYear_pitching" : yearByYear_pitching,
                "yearByYear_fielding" : yearByYear_fielding,
                "yearByYearAdvanced_hitting" : yearByYearAdvanced_hitting,
                "yearByYearAdvanced_pitching" : yearByYearAdvanced_pitching,
                "yearByYearAdvanced_fielding" : yearByYearAdvanced_fielding,
                "sabermetrics_hitting" : sabermetrics_hitting,
                "sabermetrics_pitching" : sabermetrics_pitching,
                "sabermetrics_fielding" : sabermetrics_fielding,
                "expectedStatistics_hitting" : expectedStatistics_hitting,
                "expectedStatistics_pitching" : expectedStatistics_pitching,
                "expectedStatistics_fielding" : expectedStatistics_fielding,
                "sprayChart" : sprayChart,
                "hotColdZones" : hotColdZones
            }
        )

        self.__hitting = StatGroup(
            season_regular=season_hitting,
            season_advanced=seasonAdvanced_hitting,
            career_regular=career_hitting,
            career_advanced=careerAdvanced_hitting,
            yearByYear_regular=yearByYear_hitting,
            yearByYear_advanced=yearByYearAdvanced_hitting,
            sabermetrics=sabermetrics_hitting,
            expectedStatistics=expectedStatistics_hitting,
        )
        self.__pitching = StatGroup(
            season_regular=season_pitching,
            season_advanced=seasonAdvanced_pitching,
            career_regular=career_pitching,
            career_advanced=careerAdvanced_pitching,
            yearByYear_regular=yearByYear_pitching,
            yearByYear_advanced=yearByYearAdvanced_pitching,
            sabermetrics=sabermetrics_pitching,
            expectedStatistics=expectedStatistics_pitching,
        )
        self.__fielding = StatGroup(
            season_regular=season_fielding,
            career_regular=career_fielding,
            yearByYear_regular=yearByYear_fielding,
        )
        self.__sprayChart = sprayChart
        self.__hotColdZones = hotColdZones

    @property
    def hitting(self):
        """Player's hitting stats (regular or advanced)"""
        return self.__hitting

    @property
    def pitching(self):
        """Player's pitching stats (regular or advanced)"""
        return self.__pitching

    @property
    def fielding(self):
        """Player's fielding stats"""
        return self.__fielding

    @property
    def sprayChart(self):
        """Player's sprayChart stats"""
        return self.__sprayChart

    @property
    def hotColdZones(self):
        """Player's hotColdZones stats"""
        return self.__hotColdZones


@dataclass(frozen=True)
class PersonName:
    __slots__ = ['personId','full','first','middle','last','boxscore','use','nick','pronunciation']
    personId: int
    full: str
    first: str
    middle: str
    last: str
    boxscore: str
    use: str
    nick: str
    pronunciation: str

    def __str__(self) -> str:
        return str(self.full)

    def __repr__(self) -> str:
        return str(self.full)

    @property
    def id(self):
        return self.personId

    def asdict(self):
        return asdict(self)

@dataclass(frozen=True)
class Position:
    __slots__ = ['code','name','type','abbreviation']
    code: str
    name: str
    type: str
    abbreviation: str

    @property
    def abbrv(self):
        return self.abbreviation

    def __str__(self):
        return str(self.abbreviation)

    def __repr__(self):
        return f'<{self.abbreviation}, {self.name}>'

    def asdict(self):
        return asdict(self)

@dataclass(frozen=True)
class StrikeZone:
    __slots__ = ['top','bottom']
    top: int
    bottom: int

    def asdict(self):
        return asdict(self)


class Person:

    def __init__(self, personId):

        group = "[hitting,pitching,fielding]"

        type = "[season,seasonAdvanced,career,careerAdvanced,yearByYear,yearByYearAdvanced,sabermetrics,expectedStatistics,sprayChart,hotColdZones]"

        person_url = f'https://statsapi.mlb.com/api/v1/people/{personId}?hydrate=stats(group={group},type={type})'

        prsn = requests.get(person_url).json()['people'][0]
        # self._raw_person_data = prsn

        self._playerId = personId
        primaryPosition = prsn.get('primaryPosition',{})

        self._name = PersonName (
            personId=personId,
            full=prsn['fullName'],
            first=prsn["firstName"],
            middle=prsn.get('middleName',''),
            last=prsn["lastName"],
            boxscore=prsn['boxscoreName'],
            use=prsn.get('useName',''),
            nick=prsn.get('nickName',''),
            pronunciation=prsn.get('pronunciation','')
        )

        self._position = Position(
            primaryPosition.get('code','-'),
            primaryPosition.get('name','-'),
            primaryPosition.get('type','-'),
            primaryPosition.get('abbreviation','-')
        )


        self._primaryNumber = prsn['primaryNumber']
        self._currentAge = prsn['currentAge']

        self.birthDate = prsn.get('birthDate','')
        self.birthCity = prsn.get('birthCity','')
        self.birthStateProvince = prsn.get('birthStateProvince','')
        self.birthCountry = prsn.get('birthCountry','')

        self.deathDate = prsn.get('deathDate',''),
        self.deathCity = prsn.get('deathCity',''),
        self.deathState =  prsn.get('deathStateProvince',''),
        self.deathCountry =  prsn.get('deathCountry',''),

        self._height = prsn['height']
        self._weight = prsn['weight']
        self._bats = prsn['batSide']['code']
        self._throws = prsn['pitchHand']['code']

        self._strikeZone = StrikeZone (
            prsn['strikeZoneTop'],
            prsn['strikeZoneBottom']
        )

        self._active = prsn['active']
        self._draftYear = prsn.get('draftYear','')
        self._mlbDebutDate = prsn['mlbDebutDate']



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
    def playerId(self) -> int:
        """Player Mlb Advanced Media official ID number"""
        return self._playerId

    @property
    def name(self) -> PersonName:
        """Name variations for player"""
        return self._name

    @property
    def number(self) -> int:
        """Players jersey number"""
        return self._primaryNumber

    @property
    def age(self) -> int:
        """Players age"""
        return self._currentAge

    @property
    def height(self) -> int:
        """Players height"""
        return self._height

    @property
    def weight(self) -> int:
        """Players weight"""
        return self._weight

    @property
    def position(self) -> Position:
        """
        Keys/Attributes:
        ----------------
        - 'code'            : int (3)
        - 'name'            : str ('First Base')
        - 'type'            : str ('Infielder')
        - 'abbreviation'    : str ('1B')
        """
        return self._position;

    @property
    def bats(self) -> str:
        """Code for for player's batting side ('R','L','S')"""
        return self._bats

    @property
    def throws(self) -> str:
        """Code for for player's throwing arm ('R','L','S')"""
        return self._throws

    @property
    def stikeZone(self) -> StrikeZone:
        """
        Keys/Attributes:
        ----------------
        - 'top'     : int (3.59)
        - 'bottom'  : int (1.76)
        """
        return self._strikeZone

    @property
    def active(self) -> bool:
        """If the player is active or not"""
        return self._active

    @property
    def draftYear(self) -> int:
        """The year the player was drafted in"""
        return self._draftYear

    @property
    def mlbDebutDate(self) -> str:
        """Debut date as a string"""
        return self._mlbDebutDate


    @property
    def stats(self):
        """Player stats

        Stats Groups
        ------------
        - hitting
        - pitching
        - fielding
        - sprayChart
        - hotColdZones

        hitting,
        pitching,
        fielding stat Categories
        ----------------
        - season.regular
        - season.advanced
        - career.regular
        - career.advanced
        - yearByYear.regular
        - yearByYear.advanced
        - sabermetrics
        - expectedStatistics


        Notes:

        Stats returned will always be in side a list. This is due to a number of things.
        First is the case of a player changing clubs mid season. This results in three
        splits returned from hitting.season.regular. One is the over all and the other two
        are for each club the player was with. Another example is yearbyyear where the
        splits are each year. For these reasons all stats returned will be nestled in
        a list.

        """
        return self._stats
