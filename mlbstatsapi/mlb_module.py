from typing import Union, List, Dict
import importlib
import inspect

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