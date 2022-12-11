Class: `Mlb`
===================

`get_draft`
----------

Description: Returns a draft object for year_id

**Parameters:**

| Name       | Type      | Required | Description                         | Default
| ---------- | --------- | -------- | ----------------------------------- | -------
| `year_id` | string/int | Yes      | Insert a year_id to return a directory of seasons for a specific sport. |

**Other Parameters:**

| Name       | Type      | Required | Description                         | Default
| ---------- | --------- | -------- | ----------------------------------- | -------
| `round` | string | No      | Insert a round to return biographical and financial data for a specific round in a Rule 4 draft. |
| `name` | string | No      | Insert the first letter of a draftees last name to return their Rule 4 biographical and financial data. |
| `school` | string | No      | Insert the first letter of a draftees school to return their Rule 4 biographical and financial data. |
| `state` | string | No      | Insert state to return a list of Rule 4 draftees from that given state. |
| `country` | string | No      | Insert state to return a list of Rule 4 draftees from that given country. |
| `position` | string | No      | Insert the position to return Rule 4 biographical and financial data for a players drafted at that position. |
| `teamId` | string/int | No      | Insert teamId to return Rule 4 biographical and financial data for all picks made by a specific team. |
| `playerId` | string/int | No      | Insert MLB playerId to return a player's Rule 4 biographical and financial data a specific Rule 4 draft. |
| `bisPlayerId` | string/int | No      | Insert bisPlayerId to return a player's Rule 4 biographical and financial data a specific Rule 4 draft. |