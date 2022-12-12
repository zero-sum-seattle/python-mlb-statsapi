Class: `Mlb`
===================

`get_division`
----------

Description: Returns a Division

**Parameters:**

| Name       | Type      | Required | Description                         | Default
| ---------- | --------- | -------- | ----------------------------------- | -------
| `divison_id` | string/int | Yes      | divisionId to return a directory of division(s) for a specific division. |


`get_divisions`
----------

Description: Return all divisons

**Other Parameters:**

| Name       | Type      | Required | Description                         | Default
| ---------- | --------int- | -------- | ----------------------------------- | -------
| `divisionId` | string | No      | Insert divisionId(s) to return a directory of division(s) for a specific division. Format '200,201' |
| `leagueId` | string/int | No      | Insert leagueId to return a directory of division(s) for all divisions in a specific league. |
| `sportId` | string/int | No      | Insert a sportId to return a directory of division(s) for all divisions in a specific sport. |

`get_division_id`
----------

Description: Return division ids

**Parameters:**

| Name       | Type      | Required | Description                         | Default
| ---------- | --------- | -------- | ----------------------------------- | -------
| `division_name` | string | Yes      | Division name |

**Other Parameters:**

| Name       | Type      | Required | Description                         | Default
| ---------- | --------- | -------- | ----------------------------------- | -------
| `search_key` | string | No      | description | 'name'
