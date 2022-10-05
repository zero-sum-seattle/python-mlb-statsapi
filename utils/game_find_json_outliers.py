import requests
import pprint
from typing import List, Dict
import json
import os


def merge_dictionaries(dict1, dict2):
    merged_dictionary = {}

    for key in dict1:
        # print (key)
        merged_dictionary[key] = {}
        if key in dict2:
            new_count = dict1[key]['#occurs#'] + dict2[key]['#occurs#']

            if isinstance(dict1[key]['dictitems'], Dict) and isinstance(dict2[key]['dictitems'], Dict):
                merged_dictionary[key]['dictitems'] = merge_dictionaries(dict1[key]['dictitems'], dict2[key]['dictitems'])
            elif isinstance(dict1[key]['dictitems'], Dict):
                merged_dictionary[key]['dictitems'] = dict1[key]['dictitems']
            elif isinstance(dict2[key]['dictitems'], Dict):
                merged_dictionary[key]['dictitems'] = dict2[key]['dictitems']
            else:
                merged_dictionary[key]['dictitems'] = {}
        else:
            new_count = dict1[key]['#occurs#']
            merged_dictionary[key]['dictitems'] = dict1[key]['dictitems']

        merged_dictionary[key]['#occurs#'] = new_count

    for key in dict2:
        if key not in merged_dictionary:
            merged_dictionary[key] = dict2[key]

    return merged_dictionary


def get_reps(r):

    temp_dict = {}

    if isinstance(r, Dict):
        for key, value in r.items():
            temp_dict[key] = {'#occurs#':1, 'dictitems':get_reps(value)}

        return temp_dict

    elif isinstance(r, List):

        list_temp_dict = {}

        for item in r:
            if isinstance(item, Dict):
                list_temp_dict = merge_dictionaries(get_reps(item), list_temp_dict)

        return list_temp_dict

    else:
        return r


def main():


    list_of_game_pks = [662242]

    print ("Adding gamepk: 662242 With progress: Final")

    r = requests.get("https://statsapi.mlb.com/api/v1/schedule?sportId=1").json()

    live_games = []
    if r.get("totalItems") != 0:
        for date in r.get("dates"):
            for game in date.get("games"):
                print ("Adding gamepk: ", game["gamePk"], "With progress:", game["status"]["detailedState"])
                list_of_game_pks.append(game["gamePk"])


    print ()

    fp = "games_json_counting.json"

    result_dict = {}

    for game in list_of_game_pks:
        r = requests.get(f"https://statsapi.mlb.com/api/v1.1/game/{game}/feed/live").json()
        print ("merging in game:", game)
        result_dict = merge_dictionaries(get_reps(r), result_dict)


    data = json.dumps(json.loads(json.dumps(result_dict)), indent=4)


    with open(fp, "w+", newline="", encoding="UTF-8") as f:
            f.write(data)






if __name__ == '__main__':
    main()
