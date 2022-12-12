Class: `Mlb`
===================

`get_schedule`
----------

Description: Returns a schedule object

**Parameters:**

| Name       | Type      | Required | Description                         | Default
| ---------- | --------- | -------- | ----------------------------------- | -------
| `date` | string | Yes      | Date |
| `start_date` | string | Yes      | Start date "yyyy-mm-dd" |
| `end_date` | string | Yes      | End date "yyyy-mm-dd" |
| `sport_id` | string/int | Yes      | Sport ID of schedule | 1
| `team_id` | string/int | No      | Team ID of schedule |

**Other Parameters:**

| Name       | Type      | Required | Description                         | Default
| ---------- | --------- | -------- | ----------------------------------- | -------
| `leagueId` | string | Yes      | Insert leagueId to return all schedules based on a particular scheduleType for a specific league |
| `gamePks` | string | Yes      | Insert gamePks to return all schedules based on a particular scheduleType for specific games. |
| `venueIds` | string | Yes      | Insert venueId to return all schedules based on a particular scheduleType for a specific venueId. |
| `gameTypes` | string | Yes      | Insert gameTypes to return schedule information for all games in particular gameTypes. For a list of all gameTypes: https://statsapi.mlb.com/api/v1/gameTypes |

