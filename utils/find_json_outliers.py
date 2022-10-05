import requests
from typing import List, Dict
import json
import os
import sys

def merge_dictionaries(dict1, dict2):
    merged_dictionary = {}

    for key in dict1:
        # print (key)
        merged_dictionary[key] = {"occurs#":0, "dictitems":{}}
        if key in dict2:
            new_count = dict1[key]['occurs#'] + dict2[key]['occurs#']

            if isinstance(dict1[key]['dictitems'], Dict) and isinstance(dict2[key]['dictitems'], Dict):
                merged_dictionary[key]['dictitems'] = merge_dictionaries(dict1[key]['dictitems'], dict2[key]['dictitems'])
            elif isinstance(dict1[key]['dictitems'], Dict):
                merged_dictionary[key]['dictitems'] = dict1[key]['dictitems']
            elif isinstance(dict2[key]['dictitems'], Dict):
                merged_dictionary[key]['dictitems'] = dict2[key]['dictitems']
            else:
                merged_dictionary[key]['dictitems'] = {}
        else:
            new_count = dict1[key]['occurs#']
            merged_dictionary[key]['dictitems'] = dict1[key]['dictitems']

        merged_dictionary[key]['occurs#'] = new_count

    for key in dict2:
        if key not in merged_dictionary:
            merged_dictionary[key] = dict2[key]

    return merged_dictionary


def get_reps(r):

    temp_dict = {}

    if isinstance(r, Dict):
        for key, value in r.items():
            temp_dict[key] = {'occurs#':1, 'dictitems':get_reps(value)}

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

    list_of_endpoints = ["/api/v1/people/664034",
                         "/api/v1/people/668881",
                         "/api/v1/people/668804"
                         ]

    fp = "json_counting.json"

    result_dict = {}

    for end_point in list_of_endpoints:
        if end_point[:7]=='/api/v1':
            url = "https://statsapi.mlb.com" + end_point
            print ("Grabbing and joing ", url)
            endpointData = requests.get(url).json()
            result_dict = merge_dictionaries(get_reps(endpointData), result_dict)
        else:
            print ("bad endpoint Nothing done with:", end_point)

    data = json.dumps(json.loads(json.dumps(result_dict)), indent=4)

    with open(fp, "w+", newline="", encoding="UTF-8") as f:
            f.write(data)

if __name__ == '__main__':
    main()
