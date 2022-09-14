import requests

class Person:

    def __init__(self, personId):

        game_url = f'https://statsapi.mlb.com/api/v1/people/{personId}'
        # params = {'hydrate':'venue,flags,preState',
        #           'timecode':timecode}
        params = {}

        prsn = requests.get(game_url,params=params).json()['people'][0]
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

        self.height = prsn['height']
        self.weight = prsn['weight']
        self.active = prsn['active']

        primaryPosition = prsn['primaryPosition']
        self.primaryPosition_name = primaryPosition['name']
        self.primaryPosition_type = primaryPosition['type']

        self.useName = prsn['useName']
        self.boxscoreName = prsn['boxscoreName']
        self.nickName = prsn['nickName']
        self.gender = prsn['gender']

        # self.nameMatrilineal = prsn['nameMatrilineal']

        self.isPlayer = prsn['isPlayer']

        self.isVerified = prsn['isVerified']
        self.mlbDebutDate = prsn['mlbDebutDate']

        self.batSide_code = prsn['batSide']['code']
        self.batSide_description = prsn['batSide']['description']

        self.pitchHand_code = prsn['pitchHand']['code']
        self.pitchHand_description = prsn['pitchHand']['description']


        # self.nameFirstLast = prsn['nameFirstLast']
        self.nameTitle = prsn['nameTitle']
        self.nameSlug = prsn['nameSlug']

        # self.firstLastName = prsn['firstLastName']
        # self.lastFirstName = prsn['lastFirstName']
        # self.lastInitName = prsn['lastInitName']
        # self.initLastName = prsn['initLastName']
        # self.fullFMLName = prsn['fullFMLName']
        # self.fullLFMName = prsn['fullLFMName']


        self.strikeZoneTop = prsn['strikeZoneTop']
        self.strikeZoneBottom = prsn['strikeZoneBottom']
