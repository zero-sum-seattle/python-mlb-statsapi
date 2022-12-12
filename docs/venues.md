Class: `Mlb`
===================

`get_venue`
----------

Description: Returns venue directorial information for all available venues in the Stats API.

**Parameters:**

| Name       | Type      | Required | Description                         | Default
| ---------- | --------- | -------- | ----------------------------------- | -------
| `venue_id`  | string/int | Yes      | venueId to return venue directorial information based venueId. |


**Other Parameters:**

| Name       | Type      | Required | Description                         | Default
| ---------- | --------- | -------- | ----------------------------------- | -------
| `fields`   | string | Yes       | Comma delimited list of specific fields to be returned. Format: topLevelNode, childNode, attribute | 

`get_venues`
----------

Description: Return all venues

**Other Parameters:**

| Name       | Type      | Required | Description                         | Default
| ---------- | --------- | -------- | ----------------------------------- | -------
| `venueIds`   | int/list | No | Insert venueId to return venue directorial information based venueId. | 
| `sportIds`   | string/int | No | Insert sportIds to return venue directorial information based a given sport(s). For a list of all sports: https://statsapi.mlb.com/api/v1/sports | 
| `season`   | string/int | No | Insert year to return venue directorial information for a given season.  | 
| `fields`   | string | No | Comma delimited list of specific fields to be returned. Format: topLevelNode, childNode, attribute | 

`get_venue_id`
----------

Description: Return venue id

**Parameters:**

| Name       | Type      | Required | Description                         | Default
| ---------- | --------- | -------- | ----------------------------------- | -------
| `venue_name`  | string/int | Yes      | venue name. |
| `search_key`  | string/int | No      | venue name. | name