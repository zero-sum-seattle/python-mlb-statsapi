Class: `Mlb`
===================

`get_season`
----------

Description: Returns a Season

**Parameters:**

| Name       | Type      | Required | Description                         | Default
| ---------- | --------- | -------- | ----------------------------------- | -------
| `season_id` | string/int | Yes      | Insert year to return season information for a particular season. |
| `sport_id` | string/int | No      | Insert a sportId to return a directory of seasons for a specific sport. | 1


**Other Parameters:**

| Name       | Type      | Required | Description                         | Default
| ---------- | --------- | -------- | ----------------------------------- | -------
| `withGameTypeDates` | bool | No      | Insert a withGameTypeDates to return season information for all gameTypes. |
| `fields` | string/int | No      | Comma delimited list of specific fields to be returned. Format: topLevelNode, childNode, attribute  | 


`get_seasons`
----------

Description: Return a list of Seasons

**Parameters:**

| Name       | Type      | Required | Description                         | Default
| ---------- | --------- | -------- | ----------------------------------- | -------
| `sport_id` | string/int | Yes      | Insert a sportId to return a directory of seasons for a specific sport. | 1

**Other Parameters:**

| Name       | Type      | Required | Description                         | Default
| ---------- | --------- | -------- | ----------------------------------- | -------
| `divisionId` | string/int | No      | Insert divisionId to return a directory of seasons for a specific division. |
| `leagueId` | string/int | No      |  Insert leagueId to return a directory of seasons in a specific league. |
| `withGameTypeDates` | bool | No      | Insert a withGameTypeDates to return season information for all gameTypes. |
| `fields` | string/int | No      | Comma delimited list of specific fields to be returned. Format: topLevelNode, childNode, attribute |

            