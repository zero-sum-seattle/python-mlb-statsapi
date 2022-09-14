import requests

class person:

    def __init__(self, personId):

        game_url = f'https://statsapi.mlb.com/api/v1/people/{personId}'
        # params = {'hydrate':'venue,flags,preState',
        #           'timecode':timecode}
        params = {}

        prsn = requests.get(game_url,params=params).json()['people']
        self._raw_person_data = prsn


        self.fullName = prsn['fullName']
        self.firstName = prsn['firstName']
        self.lastName = prsn['lastName']
        self.primaryNumber = prsn['primaryNumber']
        self.birthDate = prsn['birthDate']
        self.currentAge = prsn['currentAge']

        # self.birthCity = prsn['birthCity']
        # self.birthStateProvince = prsn['birthStateProvince']
        # self.birthCountry = prsn['birthCountry']

        self.height = prse['height']
        self.weight = prse['weight']
        self.active = prse['active']

        primaryPosition = prse['primaryPosition']
        self.primaryPosition_name = primaryPosition['name']
        self.primaryPosition_type = primaryPosition['type']

        self.useName = prse['useName']
        self.boxscoreName = prse['boxscoreName']
        self.nickName = prse['nickName']
        self.gender = prse['gender']

        # self.nameMatrilineal = prse['nameMatrilineal']

        self.isPlayer = prse['isPlayer']

        self.isVerified = prse['isVerified']
        self.mlbDebutDate = prse['mlbDebutDate']

        self.batSide_code = prse['batSide']['code']
        self.batSide_description = prse['batSide']['description']

        self.pitchHand_code = prse['pitchHand']['code']
        self.pitchHand_description = prse['pitchHand']['description']


        # self.nameFirstLast = prse['nameFirstLast']
        self.nameTitle = prse['nameTitle']
        self.nameSlug = prse['nameSlug']

        # self.firstLastName = prse['firstLastName']
        # self.lastFirstName = prse['lastFirstName']
        # self.lastInitName = prse['lastInitName']
        # self.initLastName = prse['initLastName']
        # self.fullFMLName = prse['fullFMLName']
        # self.fullLFMName = prse['fullLFMName']


        self.strikeZoneTop = prse['strikeZoneTop']
        self.strikeZoneBottom = prse['strikeZoneBottom']
