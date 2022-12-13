Class: `Mlb`
===================

`get_team_stats`
----------

Description: Returns stats for a team

**Parameters:**

| Name       | Type      | Required | Description                         | Default
| ---------- | --------- | -------- | ----------------------------------- | -------
| `team_id` | string/int | Yes      | description |
| `stats` | list | Yes      | Insert statType to return statistics for a players for a given sportId. Find available stat types at https://statsapi.mlb.com/api/v1/statTypes |
| `groups` | list | Yes      | Insert statGroup to return statistics for a given player based on group. Find available stat types at https://statsapi.mlb.com/api/v1/statGroup |


**Other Parameters:**

| Name       | Type      | Required | Description                         | Default
| ---------- | --------- | -------- | ----------------------------------- | -------
| `season` | string | No      | Insert year to return team stats for a particular season. |
| `sportIds` | string | No      | Insert sportId to return team stats for a particular sportId. |
| `gameType` | string | No      | Insert gameType to return team stats for a particular gameType. |
| `opposingTeamId` | string | No      | Insert team id to return stats against a team. Used with vsTeam stat type. |
| `opposingPlayerId` | string | No      | Insert person id to return player stats for against a player. Used with vsPlayer stat type. |


`get_players_stats_for_game`
----------

Description: Return game stats for a player

**Parameters:**

| Name       | Type      | Required | Description                         | Default
| ---------- | --------- | -------- | ----------------------------------- | -------
| `person_id` | string/int | Yes      | person id for the stats |
| `game_id` | string/int | Yes      | game id for the stats |

`get_player_stats`
----------

Description: Return stats for a player

**Parameters:**

| Name       | Type      | Required | Description                         | Default
| ---------- | --------- | -------- | ----------------------------------- | -------
| `person_id` | string | Yes      | person id for the stats |
| `stats` | list | Yes      | Insert statType to return statistics for a players for a given sportId. Find available stat types at https://statsapi.mlb.com/api/v1/statTypes |
| `groups` | list | Yes      | Insert statGroup to return statistics for a given player based on group. Find available stat types at https://statsapi.mlb.com/api/v1/statGroup |


**Other Parameters:**

| Name       | Type      | Required | Description                         | Default
| ---------- | --------- | -------- | ----------------------------------- | -------
| `season` | string | No      | Insert year to return player stats for a particular season. |
| `sportIds` | string | No      | Insert sportId to return player stats for a particular sportId. |
| `gameType` | string | No      | Insert gameType to return player stats for a particular gameType. |
| `opposingTeamId` | string | No      | Insert team id to return stats against a team. Used with vsTeam stat type. |
| `opposingPlayerId` | string | No      | Insert person id to return player stats for against a player. Used with vsPlayer stat type. |

`get_stats`
----------

Return standard statistics.

**Parameters:**

| Name       | Type      | Required | Description                         | Default
| ---------- | --------- | -------- | ----------------------------------- | -------
| `stats` | list | Yes      | Insert statType to return statistics for a players for a given sportId. Find available stat types at https://statsapi.mlb.com/api/v1/statTypes |
| `groups` | list | Yes      | Insert statGroup to return statistics for a given player based on group. Find available stat types at https://statsapi.mlb.com/api/v1/statGroup |


**Other Parameters:**

| Name       | Type      | Required | Description                         | Default
| ---------- | --------- | -------- | ----------------------------------- | -------
| `season` | string | No      | Insert year to return player stats for a particular season. |
| `sportIds` | string | No      | Insert sportId to return player stats for a particular sportId. |
| `gameType` | string | No      | Insert gameType to return player stats for a particular gameType. |
| `playerPool` | string | No      | There are 4 different types of playerPools to return statistics for a particular playerPool across a sport. e.g All, Qualified, Rookies|
| `position` | string | No      | Insert position to return statistics for a given position. Default to "Qualified" playerPool. Find available positions at https://statsapi.mlb.com/api/v1/positions |
| `teamId` | string | No      | Insert teamId to return statistics for a given team. Default to "Qualified" playerPool. |
| `leagueId` | string | No      | Insert leagueId to return statistics for a given team. Default to "Qualified" playerPool. |
| `opposingTeamId` | string | No      | Insert team id to return stats against a team. Used with vsTeam stat type. |
| `opposingPlayerId` | string | No      | Insert person id to return player stats for against a player. Used with vsPlayer stat type. |

`Stats`
-----------

Stat types.

**Stats:**

| Name       | Type      | Required | Description                         | Default
| ---------- | --------- | -------- | ----------------------------------- | -------
| `season` | string | No      | A season stat, supports stat groups hitting, pitching, fielding, and catching. Requires use of season param.|
| `seasonAdvanced` | string | No      | A seasonAdvanced stat, supports stat groups hitting, pitching, fielding, and catching. |
| `career` | string | No      |  A career stat, supports stat groups hitting, pitching, fielding, and catching. |
| `careerAdvanced` | string | No      | A career advanced stat, supports stat groups hitting, pitching, fielding, and catching. |
| `winLoss` | string | No      | A winLoss stat, supports stat groups hitting, pitching. |
| `winLossPlayoffs` | string | No      | A winloss playoff stat, supports stat groups hitting, pitching. |
| `homeAndAway` | string | No      |  A homeandaway stat, supports stat groups hitting, pitching. |
| `homeAndAwayPlayoffs` | string | No      | A winLoss stat, supports stat groups hitting, pitching. |
| `careerRegularSeason` | string | No      | A homeandaway playoffs stat, supports stat groups hitting, pitching. |
| `careerPlayoffs` | string | No      |  A career playoff stat, supports stat groups hitting, pitching. |
| `statsSingleSeason` | string | No      | A season stat, supports stat groups hitting, pitching, fielding, and catching. |
| `yearByYear` | string | No      | A yearbyyear stat, supports stat groups hitting, pitching, fielding, and catching. |
| `yearByYearPlayoffs` | string | No      | A yearByYearPlayoffs stat, supports stat groups hitting, pitching, fielding, and catching. |
| `opponentsFaced` | string | No      | A opponentsFaced stat, supports stat groups hitting, pitching. |
| `sabermetrics` | string | No      | A sabermetrics stat, supports stat groups hitting, pitching. |
| `gameLog` | string | No      | A gameLog stat, supports stat groups hitting, pitching. |
| `pitchLog` | string | No      | A pitchLog stat, supports stat groups hitting, pitching. |
| `playLog` | string | No      | A playLog stat, supports stat groups hitting, pitching. |
| `vsPlayer` | string | No      | A playLog stat, supports stat groups hitting, pitching. Requires use of opposingPlayerId param. |

`Groups`
-----------

Stat Groups.

**Groups:**

| Name       | Type      | Required | Description                         | Default
| ---------- | --------- | -------- | ----------------------------------- | -------
| `hitting` | string | No      | hitting stat group |
| `pitching` | string | No      | pitching stat group |
| `fielding` | string | No      | fielding stat group |
| `catching` | string | No      | catching stat group |
