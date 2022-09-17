import requests


class Game():

    def __init__(self,game_pk, timecode=None):

        if timecode == '':
            timecode = None
        if timecode is not None and timecode.find('_') == -1:
            timecode = parse(timecode).strftime(r'%Y%m%d_%H%M%S')


        self._game_pk = game_pk


        game_url = f'https://statsapi.mlb.com/api/v1.1/game/{game_pk}/feed/live?'
        # params = {'hydrate':'venue,flags,preState',
        #           'timecode':timecode}
        params = {'timecode':timecode}

        gm = requests.get(game_url,params=params).json()
        self._raw_game_data = gm

        self.meta = gm['metaData']
        gameData = gm['gameData']
        liveData = gm['liveData']

        # GAME gameData
        self._linescore = liveData['linescore']
        self._boxscore = liveData['boxscore']
        self._flags = gameData['flags']

        self.gameType = gameData['game']['type']
        self.doubleHeader = gameData['game']['doubleHeader']
        self.gameNumber = gameData['game']['gameNumber']

        datetime = gameData['datetime']
        self.game_dateTime = datetime['dateTime']
        self.game_date = datetime['officialDate']
        self.gameDate = self.game_date
        self.daynight = datetime['dayNight']
        self.game_time = datetime['time']

        status = gameData['status']
        self.gameState = status['abstractGameState']
        self.detailedGameState = status['detailedState']

        venue = gameData['venue']
        self.venue_id = venue['id']
        self.venue_name = venue['name']
        self.venue_city = venue['location']['city']
        self.venue_state = venue['location']['state']
        self.field_info = venue['fieldInfo']

        weather = gameData['weather']
        self.weather_condition = weather['condition']
        self.temperature = weather['temp']
        self.wind = weather['wind']

        gameInfo = gameData['gameInfo']
        self.attendance = gameData.get('gameInfo', {}).get('attendance', '-')
        self.gameDuration = gameData.get('gameInfo', {}).get('gameDurationMinutes', '-')


        # Game Team data
        away = gameData['teams']['away']
        _away_score_data = self._linescore['teams']['away']
        self._away_info = away
        self.away_id = away['id']
        # self.away_fullName =
        # self.away_clubName =
        # self.away_abbrv =
        # self.away_runs =
        # self.away_hits =
        # self.away_errs =

        self._away_team_full = away['name']
        self._away_team = away['clubName']
        self._away_team_abbrv = away['abbreviation']

        home = gameData['teams']['home']
        _home_score_data = self._linescore['teams']['home']
        self._home_info = home
        self.home_id = home['id']
        # self.away_fullName =
        # self.away_clubName =
        # self.away_abbrv =
        # self.away_runs =
        # self.away_hits =
        # self.away_errs =


        self._home_team_full = home['name']
        self._home_team = home['clubName']
        self._home_team_abbrv = home['abbreviation']





        # Game liveData
        self._allPlays = liveData['plays']['allPlays']
        self._currentPlay = liveData['plays']['currentPlay']






        # def print_game_plays():
