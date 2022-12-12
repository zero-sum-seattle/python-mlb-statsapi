from typing import Union, List, Dict
import importlib
import inspect


def merge_keys(mlb_dict, mlb_keys: Union[List[Union[dict, str]], str]) -> dict:
    """
    merge requested nested dicts inside mlb_dict into mlb_dict base.
    Parameters
    ----------
    mlb_dict : dict
        mlb_dict is a dictionary that requires transformation

    mlb_keys : str, list[str], list[dict[str, dict]]
        key names you want to nest

    Returns
    -------
    dict
        returns a dict that has been transformed
    """

    if isinstance(mlb_keys, List):
        for key in mlb_keys:

            if isinstance(key, Dict):
                for nested_key in key:
                    mlb_merge_item = mlb_dict.pop(nested_key)
                    mlb_dict.update(merge_keys(mlb_merge_item, key[nested_key]))
            else:
                mlb_merge_item = mlb_dict.pop(key)
                mlb_dict.update(**mlb_merge_item)
    else:
        mlb_merge_item = mlb_dict.pop(mlb_keys)
        mlb_dict.update(**mlb_merge_item)

    return mlb_dict

def return_splits_no_groups(split_data: dict):
    """
    function that loops through split information

    Parameters
    ----------
    split_data : dict
        dict of params to pass
    Returns
    -------
    dict
        returns a dict of stats
    """

    splits = []
    
    for split in split_data:
        if split['stat']:
            if 'group' in split:
                stat_group = split['group']
        else: # if no stat skip
            continue

        # get stat_module file to build a stat object
        stat_type = 'gameLog'
        stat_module = f"mlbstatsapi.models.stats.{stat_group}"
        stat_module = importlib.import_module(stat_module)

        # match stat object to stat_group
        for name, obj in inspect.getmembers(stat_module, predicate=inspect.isclass):
            if hasattr(obj, '_stat') and stat_group in obj._stat:
                splits.append(obj(**split))

    return splits

def return_splits(split_data: dict, stat_type: str, stat_group: str) -> List['Splits']:
    """
    The split objects are built using the group name and split data. The stat group name is used to source the correct
    stat group classes.

    stat group: hitting will load the classes in hitting.py and use the _type parameter to locate the correct class.

    Parameters
    ----------
    split_data : dict
        split data
    stat_type : str
        type of stat
    stat_group : str
        group of stat

    Returns
    -------
    list
        returns a list of stat objects
    """

    splits = []

    stat_module = f"mlbstatsapi.models.stats.{stat_group}"
    stat_module = importlib.import_module(stat_module)
    
    for name, obj in inspect.getmembers(stat_module, predicate=inspect.isclass):
        if hasattr(obj, '_stat') and stat_type in obj._stat:
            for split in split_data:
                splits.append(obj(type=stat_type, group=stat_group, **split))

    return splits


def create_split_data(stat_data: dict, param_groups: list):
    """
    function that loops through stat information
    Parameters
    ----------
    params: dict
        dict of params to pass
    Returns
    -------
    dict
        returns a dict of stats
    """
    stat_splits = {}

    for stat in stat_data:
        stat_type, stat_group = get_stat_attributes(stat)

        # if stat_type is None and stat_group is None
        # we are assumming this is a call to the game player stats
        # endpoint. Build gamelog stats
        # URL: https://statsapi.mlb.com/api/v1/people/664034/stats/game/715757
        if stat_type is None and stat_group is None:
            split = return_splits_no_groups(stat['splits'])

            stat_group = 'stats'
            stat_type = 'gameLog'

            if stat_group not in stat_splits:
                    stat_splits[stat_group] = {}   
            stat_splits[stat_group][stat_type.lower()] = split
            
            continue

        # build stat classes that have stat groups and stat types set
        for group in param_groups:
            if stat_group == group:
                # checking if we need to init stat group key
                if stat_group not in stat_splits:
                    stat_splits[stat_group] = {}        
                    # get splits from stats
                if 'splits' in stat and stat['splits']:
                    split = return_splits(stat['splits'], stat_type, stat_group)
                    stat_splits[stat_group][stat_type.lower()] = split

    return stat_splits


def build_group_list(params) -> List[str]:
    """
    return groups with stats key
    Parameters
    ----------
    params : dict
        params is a dictionary of params sent to requests

    Returns
    -------
    list
        returns a list of stat groups
    """
    no_group_types = ('hotColdZones', 'sprayChart', 'pitchArsenal')

    if params['group'] is list:
        group_list = params['group'].copy()
    else:
        group_list = list(params['group'])

    for _type in no_group_types:
        if _type in params['stats']:
            group_list.append('stats')
            break

    return group_list


def get_stat_attributes(stats) -> str:
    """
    return stat type
    Parameters
    ----------
    stats : dict
        stat data 

    Returns
    -------
    (stat_type, stat_group)
    """
    if 'type' in stats and 'displayname' in stats['type']:
        stat_type = stats['type']['displayname']
    else:
        stat_type = None

    # default to stats if no group returned
    if 'group' in stats and 'displayname' in stats['group']:
        stat_group = stats['group']['displayname']
    else:
        # if stat_type is None return None
        if stat_type:
            stat_group = 'stats'
        else: 
            stat_group = None

    return (stat_type, stat_group)


