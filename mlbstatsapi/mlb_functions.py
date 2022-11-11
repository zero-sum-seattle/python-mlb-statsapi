from typing import Union, List, Dict
import importlib
import inspect


def _transform_mlb_data(mlb_dict, mlb_keys: Union[List[Union[dict, str]], str]) -> dict:
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
    transformed_dict
    """

    if isinstance(mlb_keys, List):   
        for key in mlb_keys:

            if isinstance(key, Dict):      
                for nested_key in key:                       
                    mlb_merge_item = mlb_dict.pop(nested_key)
                    mlb_dict.update(_transform_mlb_data(mlb_merge_item, key[nested_key]))
            else:
                mlb_merge_item = mlb_dict.pop(key)
                mlb_dict.update(**mlb_merge_item)
    else:
        mlb_merge_item = mlb_dict.pop(mlb_keys)
        mlb_dict.update(**mlb_merge_item)

    return mlb_dict


def _return_splits(split_data: dict, stat_type: str, stat_group: str) -> List['Splits']:
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
    splits
    """

    stat_log_type = ['playLog', 'pitchLog']
    splits = []

    stat_module = f"mlbstatsapi.models.stats.{stat_group}"
    stat_module = importlib.import_module(stat_module)

    # if splits is empty return empty list
    if not ('splits' in split_data and split_data['splits']):
        return splits

    for name, obj in inspect.getmembers(stat_module):
        # type_ attribute holds the stat_type of the class
        if inspect.isclass(obj) and (hasattr(obj, '_stat') and stat_type in obj._stat):
            for split in split_data['splits']:

                # if stat_type is in stat_log_type
                # do required dictionary transformation
                if stat_type in stat_log_type:
                    split = _transform_mlb_data(split, [{'stat': 'play'}])

                # if stat is in split merge
                # some splits don't have stat
                if 'stat' in split:
                    split = _transform_mlb_data(split, 'stat')

                splits.append(obj(_type=stat_type, _group=stat_group, **split))

    return splits
