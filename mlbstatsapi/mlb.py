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
    
class MlbObject:
    """
    A class to represent a base Mlboject.

    ...

    Methods
    -------
    generate_stats(stat_types=[], stat_groups=[]):
        Populate Stat objects for the MlbObject
    """
    # _mlb_adapter = MlbDataAdapter()

    # def get_stats(self, stat_types: List[str] = ["season"], stat_groups: List[str] = ["hitting"]):
    #     statList = [] # Empty List to hold Stats while they are created 
    #     for stat_group in stat_groups:

    #         stat_type_url = ",".join(stat_types)

    #         statdata = self._mlb_adapter.get(endpoint=f"{self.mlb_class}/{self.id}/stats?stats={stat_type_url}&group={stat_group}") # get stats
    #         if "stats" in statdata.data:
    #             statList += [ Stats(**stat) for stat in statdata.data['stats'] ] # Add Stat to List[statList]
        
    #     return statList # Return list of Stat Objects








