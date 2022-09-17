from datetime import datetime
import requests

def lookup_player(firstName, lastName, season=None):
    """Get data about players based on full name. """

    if not season:
        season = datetime.now().year

    fields = "people,id,fullName,firstName,lastName,primaryNumber,currentTeam,id,primaryPosition,code,abbreviation,useName,boxscoreName,nickName,mlbDebutDate,nameFirstLast,firstLastName,lastFirstName,lastInitName,initLastName,fullFMLName,fullLFMName"

    lookupUrl = f'https://statsapi.mlb.com/api/v1/sports/1/players?fields={fields}&season={season}'

    r = requests.get(lookupUrl).json()

    players = []
    for player in r["people"]:
        if (player['firstName'].lower() == firstName.lower() or player['useName'].lower() == firstName.lower()):
            if player['lastName'].lower() == lastName.lower():
                players.append(player)

    return players

def liveGames():
    """Returns a python dict containing game data for games currently in progress"""

    r = requests.get("https://statsapi.mlb.com/api/v1/schedule?sportId=1").json()


    live_games = []
    if r.get("totalItems") == 0:
        return live_games  # TODO: ValueError('No games to parse from schedule object.') instead?
    else:
        for date in r.get("dates"):
            for game in date.get("games"):
                if game["status"]["detailedState"] == "In Progress":
                    game_info = {
                        "game_id": game["gamePk"],
                        "game_datetime": game["gameDate"],
                        "game_date": date["date"],
                        "game_type": game["gameType"],
                        "status": game["status"]["detailedState"],
                        "away_name": game["teams"]["away"]["team"]["name"],
                        "home_name": game["teams"]["home"]["team"]["name"],
                        "away_id": game["teams"]["away"]["team"]["id"],
                        "home_id": game["teams"]["home"]["team"]["id"],
                        "away_score": game["teams"]["away"].get("score", "0"),
                        "home_score": game["teams"]["home"].get("score", "0"),
                        "current_inning": game.get("linescore", {}).get(
                            "currentInning", ""
                        ),
                        "inning_state": game.get("linescore", {}).get("inningState", ""),
                        "venue_id": game.get("venue", {}).get("id"),
                        "venue_name": game.get("venue", {}).get("name"),
                    }


                    live_games.append(game_info)

        return live_games


def todaysGames():
    """ """

    r = requests.get("https://statsapi.mlb.com/api/v1/schedule?sportId=1").json()

    games = []

    if r.get("totalItems") == 0:
        return games  # TODO: ValueError('No games to parse from schedule object.') instead?
    else:
        for date in r.get("dates"):
            for game in date.get("games"):
                game_info = {
                    "game_id": game["gamePk"],
                    "game_datetime": game["gameDate"],
                    "game_date": date["date"],
                    "game_type": game["gameType"],
                    "status": game["status"]["detailedState"],
                    "away_name": game["teams"]["away"]["team"]["name"],
                    "home_name": game["teams"]["home"]["team"]["name"],
                    "away_id": game["teams"]["away"]["team"]["id"],
                    "home_id": game["teams"]["home"]["team"]["id"],
                    "away_score": game["teams"]["away"].get("score", "0"),
                    "home_score": game["teams"]["home"].get("score", "0"),
                    "current_inning": game.get("linescore", {}).get(
                        "currentInning", ""
                    ),
                    "inning_state": game.get("linescore", {}).get("inningState", ""),
                    "venue_id": game.get("venue", {}).get("id"),
                    "venue_name": game.get("venue", {}).get("name"),
                }


                games.append(game_info)

        return games
