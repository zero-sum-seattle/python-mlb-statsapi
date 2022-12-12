Class: `Mlb`
===================

`get_sport`
----------
Description: Returns sport object from sport_id

**Parameters:**

| Name       | Type      | Required | Description                         | Default
| ---------- | --------- | -------- | ----------------------------------- | -------
| `sport_id` | string/int | Yes      | description |

**Other Parameters:**

| Name       | Type      | Required | Description                         | Default
| ---------- | --------- | -------- | ----------------------------------- | -------
| `fields` | string | No      | Comma delimited list of specific fields to be returned. Format: topLevelNode, childNode, attribute |

`get_sports`
----------

Description: Return all sports


**Other Parameters:**

| Name       | Type      | Required | Description                         | Default
| ---------- | --------- | -------- | ----------------------------------- | -------
| `fields` | string | No      | Comma delimited list of specific fields to be returned. Format: topLevelNode, childNode, attribute |

`get_sport_id`
----------
Description: Return sport id 


**Parameters:**

| Name       | Type      | Required | Description                         | Default
| ---------- | --------- | -------- | ----------------------------------- | -------
| `sport_name` | string | Yes      | Sport name |
| `search_key` | string | No      | Search key name | 'name'


