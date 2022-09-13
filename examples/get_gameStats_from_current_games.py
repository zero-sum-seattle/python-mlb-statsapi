# from .. import mlbStatsAPI
# from parentdirectory import geeks

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import mlbStatsAPI


def check_if_gameId_in_list_of_dict(list_of_dict, value):
    """Check if given value exists in list of dictionaries """
    for dict in list_of_dict:
        if value in dict['game_id']:
            return True

    return False

def print_game_stats(gamePk):
    game = mlbStatsAPI.Game(gamePk)

    print (game._home_team_full, ' vs ', game._away_team_full)


def selectACurrentGame():
    liveGameData = mlbStatsAPI.liveGames_data()

    if not liveGameData:
        sys.exit("There are no live games being played at the moment. Please try again when there is a live game!")

    liveGames = ""
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

    print (liveGames)

    gamePk = input("Please enter a valid game ID: ")

    if not check_if_gameId_in_list_of_dict(liveGameData, gamePk):
        sys.exit("You entered a game id that does not exists. Please restart and try again!")

    return gamePk


def main():
    gamePk = selectACurrentGame()
    print_game_stats(gamePk)

if __name__ == "__main__":
    main()
