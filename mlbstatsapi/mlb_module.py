from typing import Union, List, Dict
import importlib
import inspect

from mlbstatsapi.models.stats import Stat


def merge_keys(mlb_dict, mlb_keys: Union[List[Union[dict, str]], str]) -> dict:
    """
    A recursive function that merges requested nested dicts inside mlb_dict into mlb_dict base.
    
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

def return_splits(split_data: dict, stat_type: str, stat_group: str) -> List['Split']:
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
                if 'stat' in split and split['stat']:
                    splits.append(obj(**split))

    return splits

def get_split_count(stat: dict) -> int:
    """
    function that returns split count from stats

    Parameters
    ----------
    stat: dict
        dict of stats

    Returns
    -------
    int
        returns number of splits
    """



def create_split_data(stat_data: dict) -> dict:
    """
    function that loops through stat information, creates splits, and return stat dict

    Parameters
    ----------
    stat_data: dict
        dict of params to pass

    Returns
    -------
    dict
        returns a dict of stats
    """
    stats = {}

    for stat in stat_data:
        # get type and group of stat
        stat_type, stat_group, total_splits = get_stat_attributes(stat)

        if 'splits' in stat and stat['splits']:
            split_data = return_splits(stat['splits'], stat_type, stat_group)
            stat_object = Stat(group=stat_group, type=stat_type,
                        totalsplits=total_splits, splits=split_data)
        else:
            continue
    
        if stat_group not in stats:
            stats[stat_group] = {}
    
        stats[stat_group][stat_type.lower()] = stat_object

    return stats

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
        stat_type = 'gameLog'

    # default to stats if no group returned
    if 'group' in stats and 'displayname' in stats['group']:
        stat_group = stats['group']['displayname']
    else:
        # if stat_type is None return None
        if stat_type:
            stat_group = 'stats'
        else: 
            stat_group = None
    
    if 'totalsplits' in stats:
        total_splits = stats['totalsplits']
    else:
        total_splits = len(stats['splits'])

    return (stat_type, stat_group, total_splits)


