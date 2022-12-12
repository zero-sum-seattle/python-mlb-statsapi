Class: `Mlb`
===================

`get_awards`
----------

Description: Return a list of awards

**Parameters:**

| Name       | Type      | Required | Description                         | Default
| ---------- | --------- | -------- | ----------------------------------- | -------
| `award_id` | string | Yes      | Insert a awardId to return a directory of players for a given award. |

**Other Parameters:**

| Name       | Type      | Required | Description                         | Default
| ---------- | --------- | -------- | ----------------------------------- | -------
| `sportId` | string/int | No      | Insert a sportId to return a directory of players for a given award in a specific sport. |
| `leagueId` | string/int | No      | Insert leagueId(s) to return a directory of players for a given award in a specific league. Format '103,104' |
| `season` | string/int | No      | Insert year(s) to return a directory of players for a given award in a given season. Format '2016,2017' |

            