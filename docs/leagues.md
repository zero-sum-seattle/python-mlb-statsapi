Class: `Mlb`
===================

`get_league`
----------

Description: Returns 

**Parameters:**

| Name       | Type      | Required | Description                         | Default
| ---------- | --------- | -------- | ----------------------------------- | -------
| `league_id` | string | Yes      | leagueId to return league information for a specific league |

**Other Parameters:**

| Name       | Type      | Required | Description                         | Default
| ---------- | --------- | -------- | ----------------------------------- | -------
| `fields` | string | No      | Comma delimited list of specific fields to be returned. Format: topLevelNode, childNode, attribute|

`get_leagues`
----------

Description: Return all leagues

**Other Parameters:**

| Name       | Type      | Required | Description                         | Default
| ---------- | --------- | -------- | ----------------------------------- | -------
| `leagueId` | string | No      | leagueId(s) to return league information for specific leagues. Format '103,104'|
| `sportId` | string | No      | Insert sportId to return league information for a specific sport. For a list of all sportIds: http://statsapi.mlb.com/api/v1/sports|
| `seasons` | string | No      | Insert year(s) to return league information for a specific season. |
| `fields` | string | No      | Comma delimited list of specific fields to be returned. Format: topLevelNode, childNode, attribute |

`get_league_id`
----------

Description: Return league id


**Parameters:**

| Name       | Type      | Required | Description                         | Default
| ---------- | --------- | -------- | ----------------------------------- | -------
| `league_name` | string | Yes      | League name |
