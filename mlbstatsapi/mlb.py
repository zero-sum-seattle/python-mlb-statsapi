from typing import List

def _transform_mlbdata(mlb_dict, mlb_keys: List[str]):
    """
    change keys to all lowercase, and merge requested dictionarys return MlbResult

    Parameters
    ----------
    mlb_dict : dict
        mlb_dict is a dictionary that requires transformation

    mlb_keys : list
        list of key names you want to nest 

    Returns
    -------
    transformed_dict
    """ 
    for key in mlb_keys:
        mlbmergeitem = mlb_dict.pop(key)
        mlb_dict.update(**mlbmergeitem)

    return mlb_dict









