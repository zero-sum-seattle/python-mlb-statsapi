from typing import Union, List, Dict

def _transform_mlbdata(mlb_dict, mlb_keys: Union[List[Union[dict, str]], str]) -> dict:
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
                    mlbmergeitem = mlb_dict.pop(nested_key)
                    mlb_dict.update(_transform_mlbdata(mlbmergeitem, key[nested_key]))            
            else:
                mlbmergeitem = mlb_dict.pop(key)
                mlb_dict.update(**mlbmergeitem)
    else:
        mlbmergeitem = mlb_dict.pop(mlb_keys)
        mlb_dict.update(**mlbmergeitem)

    return mlb_dict