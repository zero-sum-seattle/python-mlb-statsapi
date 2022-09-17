# from .. import mlbStatsAPI
# from parentdirectory import geeks

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import mlbStatsAPI

def print_game_stats(gamePk):
    game = mlbStatsAPI.Game(gamePk)

    print ('\n')
    # print (game._home_team_full, ' @ ', game._away_team_full)

    print ("{} ({})   @   {} ({}) \n".format(game._home_team_full,
                                             game._linescore['teams']['home']['runs'],
                                             game._away_team_full,
                                             game._linescore['teams']['away']['runs']))

    print ("@", game.venue_name, 'in', game.venue_city + ',', game.venue_state)

    print (" ", game.temperature, "degrees and", game.weather_condition, "with winds at", game.wind)

    print ("\n")

    print ("\n")


    # game._currentPlay
    #
    # game._linescore
    #
    # ['defense']['center']['fullName']



    print ("    {:^107}".format(game._linescore['defense']['center']['fullName']))
    print ("    \ {:^103} /".format("Center: " + str(game._linescore['defense']['center']['id'])))
    print ("      \                                                                                                     /")
    print ("        \{:^48} {:^48}/".format(game._linescore['defense']['left']['fullName'], game._linescore['defense']['right']['fullName']))
    print ("          \{:^45}   {:^45}/".format("Left: " + str(game._linescore['defense']['left']['id']), "Right: " + str(game._linescore['defense']['right']['id'])))
    print ("            \                                                                                         /")
    print ("              \                                                                                     /")
    print ("                \                                                                                 /")
    print ("                  \                                                                             /")
    print ("                    \ {:>30}            {:31}/".format(game._linescore['defense']['shortstop']['fullName'], game._linescore['defense']['second']['fullName']))
    print ("                      \ {:>28}            {:29}/".format("Shortstop: " + str(game._linescore['defense']['shortstop']['id']), "Second: " + str(game._linescore['defense']['second']['id'])))
    print ("                        \                              [--]                               /")
    print ("                          {:29}[__]{:>30}".format(game._linescore['defense']['third']['fullName'], game._linescore['defense']['first']['fullName']))
    print ("                          {:31}{:>32}".format("Third: " + str(game._linescore['defense']['third']['id']), "First: " + str(game._linescore['defense']['first']['id'])))
    print ("                              \                                                     /")
    print ("        [ ]                     \ [--]                                       [--] /")
    print ("     [ ]   [ ]                    [__]                                       [__]")
    print ("        [ ]                         \{:^41}/".format((game._linescore['defense']['pitcher']['fullName'])))
    print ("                                      \                 ---                 /")
    print ("     {:^9}                          \{:^33}/".format(game._linescore['inningState']+' '+str(game._linescore['currentInning']),game._currentPlay['matchup']['pitchHand']['code']+"hp "+str(game._linescore['defense']['pitcher']['id'])))
    print ("     ---------                            \                             /")
    print ("     Balls   {}                              \                         /".format(game._linescore['balls']))
    print ("     Strikes {}                                \                     /".format(game._linescore['strikes']))
    print ("     Outs    {}                                  \                 /".format(game._linescore['outs']))
    print ("                                                  \             /")
    print ("                                                    \         /")
    print ("                                                      \ / \ /")

    if game._currentPlay['matchup']['batSide']['code'] == 'L':
        print ("    {:>45}      [   ]                    onDeck:   {}".format(game._linescore['offense']['batter']['fullName'], game._linescore['offense']['onDeck']['fullName']+": "+str(game._linescore['offense']['onDeck']['id'])))
        print ("    {:>45}      [___]                    inHole:   {}".format("Lhb: "+str(game._linescore['offense']['batter']['id']), game._linescore['offense']['inHole']['fullName']+": "+str(game._linescore['offense']['inHole']['id'])))
    else:
        print ("                                                       [   ]      {}".format(game._linescore['offense']['batter']['fullName']))
        print ("                                                       [___]      {}".format("Rhb: "+str(game._linescore['offense']['batter']['id'])))


    print ("")
    print ("")
    print ("                                             {:^30}".format(game._linescore['defense']['catcher']['fullName']))
    print ("                                             {:^30}".format('Catcher: ' + str(game._linescore['defense']['catcher']['id'])))
    print ("")
    print ("")


    print ("     Current Play:")

    for play in game._currentPlay['playEvents']:
        if ('call' in play['details']):
            print ("    ", play['details']['description'])
        else:
            print ("    ", play['details']['event'], play['details']['description'])





    #
    #
    #
    #
    #
    #
    #                                               Nick Senzel
    # \                                             center: 669222                                              /
    #   \                                                                                                     /
    #     \         Jake Fraley                                                  Aristides Aquino           /
    #       \      left: 641584                                                   right: 606157           /
    #         \                                                                                         /
    #           \                                                                                     /
    #             \                                                                                 /
    #               \                                                                             /
    #                 \                  Jose Barrero            Jonathan India                 /
    #                   \             shortstop: 676480          second: 663697               /
    #                     \                              [--]                               /
    #                       Kyle Farmer                  [__]                 Spencer Steer
    #                      third: 571657                                      first: 668715
    #                           \                                                     /
    #     [ ]                     \ [--]                                       [--] /
    #  [ ]   [ ]                    [__]                                       [__]
    #     [ ]                         \                Luis Cessa               /
    #                                   \                 ---                 /
    #   Top 4th                           \           Rhp: 570666           /
    #  ---------                            \                             /
    #  Balls   0                              \                         /
    #  Strikes 0                                \                     /
    #  Outs    0                                  \                 /
    #                                               \             /
    #                                                 \         /
    #                                                   \ / \  /
    #                                 Jack Suwinski      [   ]                    onDeck:   Ke'Bryan Hayes: 663647
    #                                  Lhb: 669261       [___]                    inHole:   Ben Gamel: 592325
    #
    #
    #                                                Austin Romine
    #                                                  c: 519222
    #
    #
    #  Current Play:
    #
    #





def check_if_gameId_in_list_of_dict(list_of_dict, value):
    """Check if given value exists in list of dictionaries """
    for dict in list_of_dict:
        if dict['game_id'] == value:
            return True

    return False

def selectACurrentGame():
    liveGameData = mlbStatsAPI.liveGames()

    if not liveGameData:
        sys.exit("Error:    There are no live games being played at the moment. Please try again when there is a live game! \n")

    liveGames = ""
    liveGames += "\n"
    liveGames += "\n"
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

    liveGames += "\n"
    print (liveGames)

    print ('To get gameStats from a live game')
    gamePk = input("Please select and enter a valid game ID: ")

    if (gamePk.isdigit()):
        gamePk = int(gamePk)
    else:
        sys.exit("Error:    You entered a game Id that contained invalid characters. Please restart and try again! \n")

    if not check_if_gameId_in_list_of_dict(liveGameData, gamePk):
        sys.exit("Error:    You entered a game id that does not exists. Please restart and try again! \n")

    return gamePk


def main():
    gamePk = selectACurrentGame()
    print_game_stats(gamePk)

if __name__ == "__main__":
    main()
