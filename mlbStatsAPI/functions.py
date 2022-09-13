import requests

def liveGames_print():
    """Get a formatted list of live games."""

    liveGames = ""

    liveGameData = liveGames_data()

    liveGames += "  gameId    game_date     state    inning      Teams \n"
    liveGames += "----------------------------------------------------------------------------------------------------------------------------\n"

    for gameData in liveGameData:
        liveGames += "{:^10}{:^14}{:^10}{:^5}        {} ({})   @   {} ({}) \n".format(
            gameData["game_id"],
            gameData["game_date"],
            gameData["inning_state"],
            gameData["current_inning"],
            gameData["away_name"],
            gameData["away_score"],
            gameData["home_name"],
            gameData["home_score"]
        )

    return liveGames

def liveGames_data():
    """Returns a python dict containing game data for games currently in progress"""

    params = {}

    params.update(
        {
            "sportId": str(1),
            "hydrate": "linescore",
        }
    )

    # r = statsapi.get("schedule", params)


    # c.BASE = 'https://statsapi.mlb.com/api'

    url = 'https://statsapi.mlb.com/api/v1' + "/schedule?"
    #
    # params = {
    #     "sportId":1,
    #     "hydrate": "linescore",
    # }

    r = requests.get(url,params=params).json()


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
