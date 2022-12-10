Class: `Mlb`
===================

`get_people_id`
----------

Description: Return Person Id(s) from fullname

**Parameters:**

| Name       | Type      | Required | Description                         | Default
| ---------- | --------- | -------- | ----------------------------------- | -------
| `sport_id`  | string/int| Yes      | Insert a sportId to return player information for a particular sport. For a list of all sportIds: http://statsapi.mlb.com/api/v1/sports | 1
| `fullname`   | string| Yes       | Search fullname | 
| `search_key` | string| No     | Search key | 'fullname'

**Other Parameters:**

| Name       | Type      | Required | Description                         | Default
| ---------- | --------- | -------- | ----------------------------------- | -------
| `season`  | string/int| Yes      | Insert year to return player information for a particular season. | 
| `gameType`   | string| Yes       | Insert gameType to return player information for a particular gameType. Find available game types at https://statsapi.mlb.com/api/v1/gameTypes | 

`get_person`
----------

Description: Return Person Object from Id

**Parameters:**


| Name       | Type      | Required | Description                         | Default
| ---------- | --------- | -------- | ----------------------------------- | -------
| `player_id`  | string/int| Yes      | unique person id | 

`get_people`
----------

Description: Return Person Object from Id

**Parameters:**


| Name       | Type      | Required | Description                         | Default
| ---------- | --------- | -------- | ----------------------------------- | -------
| `sport_id`  | string/int| Yes      | Insert a sportId to return player information for a particular sport. For a list of all sportIds: http://statsapi.mlb.com/api/v1/sports | 1