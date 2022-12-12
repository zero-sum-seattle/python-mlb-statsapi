Class: `Mlb`
===================

`get_standings`
----------

Description: Return


**Parameters:**

| Name       | Type      | Required | Description                         | Default
| ---------- | --------- | -------- | ----------------------------------- | -------
| `league_id` | string/int | Yes      | Insert leagueId to return all standings based on a particular standingType for a specific league. |
| `season` | string | Yes      | Insert year to return all standings based on a particular year. |

**Other Parameters:**

| Name       | Type      | Required | Description                         | Default
| ---------- | --------- | -------- | ----------------------------------- | -------
| `standingsTypes` | string | No      | Insert standingType to return all standings based on a particular year. Find standingTypes at https://statsapi.mlb.com/api/v1/standingsTypes |
| `date` | string | Yes      | Insert date to return standing information for on a particular date. Format: MM/DD/YYYY  |
            
            