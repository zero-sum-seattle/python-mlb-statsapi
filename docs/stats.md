Class: `Mlb`
===================

`get_team_stats`
----------

Description: Returns stats for a team

**Parameters:**

| Name       | Type      | Required | Description                         | Default
| ---------- | --------- | -------- | ----------------------------------- | -------
| `team_id` | string/int | Yes      | description |
| `stats` | list | Yes      | Insert statType to return statistics for a players for a given sportId. Find available stat types at https://statsapi.mlb.com/api/v1/statTypes |
| `groups` | list | Yes      | Insert statGroup to return statistics for a given player based on group. Find available stat types at https://statsapi.mlb.com/api/v1/statGroup |


**Other Parameters:**

| Name       | Type      | Required | Description                         | Default
| ---------- | --------- | -------- | ----------------------------------- | -------
| `season` | string | No      | Insert year to return team stats for a particular season. |
| `sportIds` | string | No      | Insert sportId to return team stats for a particular sportId. |
| `gameType` | string | No      | Insert gameType to return team stats for a particular gameType. |


`get_players_stats_for_game`
----------

Description: Return game stats for a player

**Parameters:**

| Name       | Type      | Required | Description                         | Default
| ---------- | --------- | -------- | ----------------------------------- | -------
| `person_id` | string/int | Yes      | person id for the stats |
| `game_id` | string/int | Yes      | game id for the stats |

`get_player_stats`
----------

Description: Return stats for a player

**Parameters:**

| Name       | Type      | Required | Description                         | Default
| ---------- | --------- | -------- | ----------------------------------- | -------
| `person_id` | string | Yes      | person id for the stats |
| `stats` | list | Yes      | Insert statType to return statistics for a players for a given sportId. Find available stat types at https://statsapi.mlb.com/api/v1/statTypes |
| `groups` | list | Yes      | Insert statGroup to return statistics for a given player based on group. Find available stat types at https://statsapi.mlb.com/api/v1/statGroup |


**Other Parameters:**

| Name       | Type      | Required | Description                         | Default
| ---------- | --------- | -------- | ----------------------------------- | -------
| `season` | string | No      | Insert year to return player stats for a particular season. |
| `sportIds` | string | No      | Insert sportId to return player stats for a particular sportId. |
| `gameType` | string | No      | Insert gameType to return player stats for a particular gameType. |

`get_stats`
----------

Return standard statistics.

**Parameters:**

| Name       | Type      | Required | Description                         | Default
| ---------- | --------- | -------- | ----------------------------------- | -------
| `stats` | list | Yes      | Insert statType to return statistics for a players for a given sportId. Find available stat types at https://statsapi.mlb.com/api/v1/statTypes |
| `groups` | list | Yes      | Insert statGroup to return statistics for a given player based on group. Find available stat types at https://statsapi.mlb.com/api/v1/statGroup |


**Other Parameters:**

| Name       | Type      | Required | Description                         | Default
| ---------- | --------- | -------- | ----------------------------------- | -------
| `season` | string | No      | Insert year to return player stats for a particular season. |
| `sportIds` | string | No      | Insert sportId to return player stats for a particular sportId. |
| `gameType` | string | No      | Insert gameType to return player stats for a particular gameType. |
| `playerPool` | string | No      | There are 4 different types of playerPools to return statistics for a particular playerPool across a sport. e.g All, Qualified, Rookies|
| `position` | string | No      | Insert position to return statistics for a given position. Default to "Qualified" playerPool. Find available positions at https://statsapi.mlb.com/api/v1/positions |
| `teamId` | string | No      | Insert teamId to return statistics for a given team. Default to "Qualified" playerPool. |
| `leagueId` | string | No      | Insert leagueId to return statistics for a given team. Default to "Qualified" playerPool. |


