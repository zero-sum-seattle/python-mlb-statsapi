Class: `Mlb`
===================

`get_homerun_derby`
----------

Description: Returns a Gamepace

**Parameters:**

| Name       | Type      | Required | Description                         | Default
| ---------- | --------- | -------- | ----------------------------------- | -------
| `season` | int | Yes      | Insert year to return a directory of pace of game metrics for a given season. | None

**Other Parameters:**

| Name       | Type      | Required | Description                         | Default
| ---------- | --------- | -------- | ----------------------------------- | -------
| `teamIds` | int | No      | Insert a teamIds to return directory of pace of game metrics for a given team. Format '110' or '110,147' | None
| `leagueId` | int | No      | Insert leagueIds to return a directory of pace of game metrics for a given league. Format '103' or '103,104' | None
| `leagueListId` | string | No      | Insert a unique League List Identifier to return a directory of pace of game metrics for a specific league listId. | None
| `sportId` | int | No      | Insert a sportId to return a directory of pace of game metrics for a specific sport. Format '11' or '1,11' | None
| `gameType` | string | No      | Insert gameType(s) a return a directory of pace of game metrics for a specific gameType. For a list of all gameTypes:  | None
| `date` | string | No      | Insert date to return a directory of pace of game metrics for a particular date range. Format: MM/DD/YYYY !startDate must be coupled with endDate! | None
| `endDate` | string | No      | Insert date to return a directory of pace of game metrics for a particular date range. Format: MM/DD/YYYY ! endDate must be coupled with startDate ! | None
| `venueIds` | int | No      | Insert venueId to return a directory of pace of game metrics for a particular venueId. | None
| `orgType` | string | No      | Insert a orgType to return a directory of pace of game metrics based on team, league or sport. Available values : T- TEAM, L- LEAGUE, S- SPORT | None
| `includeChildren` | bool | No      | Insert includeChildren to return a directory of pace of game metrics for all child teams in a given parent sport. | None
| `fields` | string | No      | Comma delimited list of specific fields to be returned. Format: topLevelNode, childNode, attribute | None