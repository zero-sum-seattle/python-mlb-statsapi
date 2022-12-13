Class: `Mlb`
===================

`get_attendance`
----------

Description: Returns attendance data based on teamId, leagueId, or leagueListId. Required Parameters (at least one)

**Parameters:**

| Name       | Type      | Required | Description                         | Default
| ---------- | --------- | -------- | ----------------------------------- | -------
| `team_id ` | Int | Yes      | Insert a teamId to return directory of attendnace for a given team | None
| `league_id ` | Int/List[int] | Yes      | Insert leagueId(s) to return a directory of attendanace for a specific league. Format '103,104' | None
| `league_list_id ` | Str | Yes      | Insert a unique League List Identifier to return a directory of attendanace for a specific league listId. [List of Options](https://github.com/zero-sum-seattle/python-mlb-statsapi/blob/ef5c8bd1d59a30345ab6a70fa0aa6f5910489a9a/mlbstatsapi/mlb_api.py#L1875)| None

**Other Parameters:**

| Name       | Type      | Required | Description                         | Default
| ---------- | --------- | -------- | ----------------------------------- | -------
| `season` | int | No      | Insert year(s) to return a directory of attendance for a given season. Season year number format yyyy | None
| `date` | string | No      | Insert date to return information for attendance on a particular date. Format: MM/DD/YYYY | None
| `gametype` | string | No      | Insert gameType(s) a directory of attendance for a given gameType. For a list of all gameTypes: https://statsapi.mlb.com/api/v1/gameTypes | None