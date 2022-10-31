#!/usr/bin/env python3


from argparse import ArgumentParser
import code
from math import e
from warnings import resetwarnings
import requests
import time 
import json

def data_http_return():
    ver = f"v1"
    hostname = f"statsapi.mlb.com"
    short_url = f"https://{hostname}/api/{ver}/"

    # pitcher? "position": "664034", "pitcher": "660271", 
    type_object = { "catcher": "663728", "al_team":"133" } # need to check if sports, league etc have stats
    groups = [ 
    # "hitting",
    # "pitching",
    # "fielding",
    "catching",
    # "running",
    # "game",
    # "team",
    # "streak" 
    ]
    stattypes = [ "projected",
    "projectedRos",
    "yearByYear",
    "yearByYearAdvanced",
    "yearByYearPlayoffs",
    "season",
    "standard",
    "advanced",
    "career",
    "careerRegularSeason",
    "careerAdvanced",
    "seasonAdvanced",
    "careerStatSplits",
    "careerPlayoffs",
    "gameLog",
    "playLog",
    "pitchLog",
    "metricLog",
    "metricAverages",
    "pitchArsenal",
    "outsAboveAverage",
    "expectedStatistics",
    "sabermetrics",
    "sprayChart",
    "tracking",
    "vsPlayer",
    "vsPlayerTotal",
    "vsPlayer5Y",
    "vsTeam",
    "vsTeam5Y",
    "vsTeamTotal",
    "lastXGames",
    "byDateRange",
    "byDateRangeAdvanced"
    "byMonth",
    "byMonthPlayoffs",
    "byDayOfWeek",
    "byDayOfWeekPlayoffs",
    "homeAndAway",
    "homeAndAwayPlayoffs",
    "winLoss",
    "winLossPlayoffs"
    "rankings",
    "rankingsByYear",
    "statsSingleSeason",
    "statsSingleSeasonAdvanced",
    "hotColdZones",
    "availableStats",
    "opponentsFaced",
    "gameTypeStats",
    "firstYearStats",
    "lastYearStats",
    "statSplits",
    "statSplitsAdvanced",
    "atGameStart",
    "vsOpponents" ]

    with open("./endpoint_information.json",'w', encoding = 'utf-8') as f:
        f.write("[")
        for position, id in type_object.items():
            for group in groups:
                for stat_type in stattypes:


                    match position:
                        case "position":
                            mlb_class = "people"
                        case "pitcher":
                            mlb_class = "people"
                        case "catcher":
                            mlb_class = "people"
                        case "al_team":
                            mlb_class = "teams"
                        case "nl_team":
                            mlb_class = "teams"
                        case _:
                            mlb_class = position
    

                    statusdict = {} # stats?stats=hotColdZones&group=hitting
                    stats_url = f"{mlb_class}/{id}/stats?stats={stat_type}&group={group}"
                    full_url = short_url + stats_url

                    statusdict.update({'object_class': mlb_class})
                    statusdict.update({'endpoint': full_url})
                    statusdict.update({'group': group})
                    statusdict.update({'stat_type': stat_type})


                    try:
                        response = requests.get(url=full_url) # mlbstats API only uses get calls
                        response.raise_for_status()
                        statusdict.update({'http_status_code': response.status_code})
                        if response.status_code <= 200 and response.status_code <= 299:
                            data = response.json()
                            statusdict.update({'data': response.json()})
                            statusdict.update({'reason': "success"})
                        time.sleep(.2)


                    except Exception as e:
                        print(e)
                        statusdict.update({'http_status_code': response.status_code})
                        statusdict.update({'reason': response.reason})
                        statusdict.update({'data': response.json()})
                        time.sleep(.2)

                    json.dump(statusdict, f, indent=4, sort_keys=True)
                    f.write(",\n")
        f.write("]")

def parse_data_function(http_error):
    with open("./endpoint_information.json",'r', encoding = 'utf-8') as f:
        file = json.load(f)
        for dic in file:
            if dic['http_status_code'] == http_error:
                if dic['object_class'] == "league":
                    break
                print(dic['http_status_code'])
                print(dic['endpoint'])
                print(dic['stat_type'])
                print(dic['object_class'])
                print(dic['group'])
                print("--------------------")


def main():
    data_http_return()

if __name__ == '__main__':
    main()