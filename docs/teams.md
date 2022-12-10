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

**Other Parameters:**

| Name       | Type      | Required | Description                         | Default
| ---------- | --------- | -------- | ----------------------------------- | -------
| `sportId`  | string/int| No      | sport id number for team search. | 

`get_team`
----------

Description: Return Team Object from Id

**Parameters:**

| Name       | Type      | Required | Description                         | Default
| ---------- | --------- | -------- | ----------------------------------- | -------
| `team_id`  | string/int| Yes      | unique team id | 

**Other Parameters:**

| Name       | Type      | Required | Description                         | Default
| ---------- | --------- | -------- | ----------------------------------- | -------
| `sportId`  | string/int| No       | Insert a sportId to return a directory of team information for a particular club in a sport. |
| `season`   | string/int| No       | Insert year to return a directory of team information for a particular club in a specific season. |
| `fields`   | string    | No       | Comma delimited list of specific fields to be returned. Format: topLevelNode, childNode, attribute |

`get_teams`
----------

Description: Return all Team Objects from sportId

**Parameters:**


| Name       | Type      | Required | Description                         | Default
| ---------- | --------- | -------- | ----------------------------------- | -------
| `sport_id`  | string/int| Yes      | unique sport id of teams | 1

**Other Parameters:**

| Name       | Type      | Required | Description                         | Default
| ---------- | --------- | -------- | ----------------------------------- | -------
| `sportId`  | string/int| No       | Insert a sportId to return a directory of team information for a particular club in a sport. |
| `season`   | string/int| No       | Insert year to return a directory of team information for a particular club in a specific season. |
| `fields`   | string    | No       | Comma delimited list of specific fields to be returned. Format: topLevelNode, childNode, attribute |
| `leagueIds` | string/int| No      | Insert leagueId to return team information for particular league. |
| `activeStatus` | string | No      | Insert activeStatus to populate a teams based on active/inactive status for a given season. There are three status types: Y, N, B |
| `allStarStatuses` | string    | No       | Insert allStarStatuses to populate a teams based on Allstar status for a given season. There are two status types: Y and N |
| `gameType`   | string    | No       | Comma delimited list of specific fields to be returned. Format: topLevelNode, childNode, attribute |

`get_team_coaches`
----------

Description: Return all Coaches from team_id

**Parameters:**

| Name       | Type      | Required | Description                         | Default
| ---------- | --------- | -------- | ----------------------------------- | -------
| `team_id`  | string/int| Yes      | unique team id of team |

**Other Parameters:**

| Name       | Type      | Required | Description                         | Default
| ---------- | --------- | -------- | ----------------------------------- | -------
| `season`  | string/int | Yes      | Insert year to return a directory of players based on roster status for a particular club in a specific season. |
| `date`  | string | Yes      | unique team id of team |
| `fields`  | string/int| Yes      | Comma delimited list of specific fields to be returned. Format: topLevelNode, childNode, attribute |

`get_team_roster`
----------

Description: Return all Player Objects from team_id

**Parameters:**

| Name       | Type      | Required | Description                         | Default
| ---------- | --------- | -------- | ----------------------------------- | -------
| `team_id`  | string/int| Yes      | unique team id of team |

**Other Parameters:**

| Name       | Type      | Required | Description                         | Default
| ---------- | --------- | -------- | ----------------------------------- | -------
| `team_id`  | string/int| Yes      | unique team id of team |
| `rosterType`  | string | Yes      | Insert teamId to return a directory of players based on roster status for a particular club. rosterType's include 40Man, fullSeason, fullRoster, nonRosterInvitees, active, allTime, depthChart, and gameday. |
| `season`  | string/int | Yes      | Insert year to return a directory of players based on roster status for a particular club in a specific season. |
| `date`  | string | Yes      | unique team id of team |
| `fields`  | string/int| Yes      | Comma delimited list of specific fields to be returned. Format: topLevelNode, childNode, attribute |