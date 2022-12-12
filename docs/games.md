Class: `Mlb`
===================

`get_game`
----------

Description: Returns a Game

**Parameters:**

| Name       | Type      | Required | Description                         | Default
| ---------- | --------- | -------- | ----------------------------------- | -------
| `game_id` | string/int | Yes      | Game id number |

**Other Parameters:**

| Name       | Type      | Required | Description                         | Default
| ---------- | --------- | -------- | ----------------------------------- | -------
| `timecode` | string | No      | Use this parameter to return a snapshot of the data at the specified time. Format: YYYYMMDD_HHMMSS |
| `fields` | string | No      | Comma delimited list of specific fields to be returned. Format: topLevelNode, childNode, attribute |

`get_game_play_by_play`
----------

Description: Return the playbyplay of a game for a specific game id

**Parameters:**

| Name       | Type      | Required | Description                         | Default
| ---------- | --------- | -------- | ----------------------------------- | -------
| `game_id` | string/int | Yes      | Game id number |

**Other Parameters:**

| Name       | Type      | Required | Description                         | Default
| ---------- | --------- | -------- | ----------------------------------- | -------
| `timecode` | string | No      | Use this parameter to return a snapshot of the data at the specified time. Format: YYYYMMDD_HHMMSS |
| `fields` | string | No      | Comma delimited list of specific fields to be returned. Format: topLevelNode, childNode, attribute |

`get_game_line_score`
----------

Description: Return the Linescore of a game for a specific game id

**Parameters:**

| Name       | Type      | Required | Description                         | Default
| ---------- | --------- | -------- | ----------------------------------- | -------
| `game_id` | string/int | Yes      | Game id number |

**Other Parameters:**

| Name       | Type      | Required | Description                         | Default
| ---------- | --------- | -------- | ----------------------------------- | -------
| `timecode` | string | No      | Use this parameter to return a snapshot of the data at the specified time. Format: YYYYMMDD_HHMMSS |
| `fields` | string | No      | Comma delimited list of specific fields to be returned. Format: topLevelNode, childNode, attribute |


`get_game_box_score`
----------

Description: Return the boxscore of a game for a specific game id

**Parameters:**

| Name       | Type      | Required | Description                         | Default
| ---------- | --------- | -------- | ----------------------------------- | -------
| `game_id` | string/int | Yes      | Game id number |

**Other Parameters:**

| Name       | Type      | Required | Description                         | Default
| ---------- | --------- | -------- | ----------------------------------- | -------
| `timecode` | string | No      | Use this parameter to return a snapshot of the data at the specified time. Format: YYYYMMDD_HHMMSS |
| `fields` | string | No      | Comma delimited list of specific fields to be returned. Format: topLevelNode, childNode, attribute |

`get_game_ids`
----------

Description: Return game ids for a specific date and game status

**Parameters:**

| Name       | Type      | Required | Description                         | Default
| ---------- | --------- | -------- | ----------------------------------- | -------
| `date` | string | Yes      | date 'yyyy-mm-dd' |
| `start_date` | string | Yes      | start date 'yyyy-mm-dd' |
| `end_date` | string | Yes      | end date 'yyyy-mm-dd' |
| `spord_id` | string | Yes      | spord id of schedule | 1

`get_scheduled_games_by_date`
----------

Description: Return the list games for by date

**Parameters:**

| Name       | Type      | Required | Description                         | Default
| ---------- | --------- | -------- | ----------------------------------- | -------
| `date` | string | Yes      | date 'yyyy-mm-dd' |
| `start_date` | string | Yes      | start date 'yyyy-mm-dd' |
| `end_date` | string | Yes      | end date 'yyyy-mm-dd' |
| `spord_id` | string | Yes      | spord id of schedule | 1

**Other Parameters:**

| Name       | Type      | Required | Description                         | Default
| ---------- | --------- | -------- | ----------------------------------- | -------
| `leagueId` | string | No      |  Insert leagueId to return all schedules based on a particular scheduleType for a specific league.  |
| `gamePks` | string | No      | Insert gamePks to return all schedules based on a particular scheduleType for specific games. |
| `venueIds` | string | No      | Insert venueId to return all schedules based on a particular scheduleType for a specific venueId. |
| `gameTypes` | string | No      | Insert gameTypes to return schedule information for all games in particular gameTypes. For a list of all gameTypes: https://statsapi.mlb.com/api/v1/gameTypes |



