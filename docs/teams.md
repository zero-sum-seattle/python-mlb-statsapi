Class: `Mlb`
===================

`get_team_id`
----------

Description: Return Team Id(s) from team_name

**Parameters:**


| Name       | Type      | Required | Description                         | Default
| ---------- | --------- | -------- | ----------------------------------- | -------
| `team_name`   | string| Yes       | Search team name | 
| `search_key` | string| No     | Search key | 'name'

`get_team`
----------

Description: Return Team Object from Id

**Parameters:**


| Name       | Type      | Required | Description                         | Default
| ---------- | --------- | -------- | ----------------------------------- | -------
| `team_id`  | string/int| Yes      | unique team id | 

`get_teams`
----------

Description: Return all Team Objects from sportId

**Parameters:**


| Name       | Type      | Required | Description                         | Default
| ---------- | --------- | -------- | ----------------------------------- | -------
| `sport_id`  | string/int| Yes      | unique sport id of teams | 1

`get_team_coaches`
----------

Description: Return all Coaches from team_id

**Parameters:**


| Name       | Type      | Required | Description                         | Default
| ---------- | --------- | -------- | ----------------------------------- | -------
| `team_id`  | string/int| Yes      | unique team id of team |

`get_team_roster`
----------

Description: Return all Player Objects from team_id

**Parameters:**


| Name       | Type      | Required | Description                         | Default
| ---------- | --------- | -------- | ----------------------------------- | -------
| `team_id`  | string/int| Yes      | unique team id of team |