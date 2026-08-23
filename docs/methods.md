# Method Reference

This page contains the method reference that previously lived in the README.

For detailed return-object and model documentation, follow the linked Wiki pages. For the stable 1.x public API contract and current async endpoint coverage, see [public-api.md](public-api.md).

## People, Person, Players, Coaches

[Wiki: People](https://github.com/zero-sum-seattle/python-mlb-statsapi/wiki/Data-Types:-People)

* `Mlb.get_people_id(self, fullname: str, sport_id: int = 1, search_key: str = 'fullname', **params)` - Return Person Id(s) from fullname
* `Mlb.get_person(self, player_id: int, **params)` - Return Person Object from Id
* `Mlb.get_people(self, sport_id: int = 1, **params)` - Return all Players from Sport

## Draft

[Wiki: Draft](https://github.com/zero-sum-seattle/python-mlb-statsapi/wiki/Data-Types:-Draft(round))

* `Mlb.get_draft(self, year_id: int, **params)` - Return a draft for a given year

## Awards

[Wiki: Award](https://github.com/zero-sum-seattle/python-mlb-statsapi/wiki/Data-Types:-Award)

* `Mlb.get_awards(self, award_id: int, **params)` - Return award recipients for a given award

## Teams

[Wiki: Team](https://github.com/zero-sum-seattle/python-mlb-statsapi/wiki/Data-Types:-Team)

* `Mlb.get_team_id(self, team_name: str, search_key: str = 'name', **params)` - Return Team Id(s) from name
* `Mlb.get_team(self, team_id: int, **params)` - Return Team Object from Team Id
* `Mlb.get_teams(self, sport_id: int = 1, **params)` - Return all Teams for Sport
* `Mlb.get_team_coaches(self, team_id: int, **params)` - Return coaching roster for team for current or specified season
* `Mlb.get_team_roster(self, team_id: int, **params)` - Return player roster for team for current or specified season

## Stats

[Wiki: Stats](https://github.com/zero-sum-seattle/python-mlb-statsapi/wiki/Data-Types:-Stats)

* `Mlb.get_player_stats(self, person_id: int, stats: list, groups: list, **params)` - Return stats by player id, stat type and groups
* `Mlb.get_team_stats(self, team_id: int, stats: list, groups: list, **params)` - Return stats by team id, stat types and groups
* `Mlb.get_stats(self, stats: list, groups: list, **params: dict)` - Return stats by stat type and group args
* `Mlb.get_players_stats_for_game(self, person_id: int, game_id: int, **params)` - Return player stats for a game

## Gamepace

[Wiki: Gamepace](https://github.com/zero-sum-seattle/python-mlb-statsapi/wiki/Data-Types:-Gamepace)

* `Mlb.get_gamepace(self, season: str, sport_id=1, **params)` - Return pace of game metrics for specific sport, league or team.

## Venues

[Wiki: Venue](https://github.com/zero-sum-seattle/python-mlb-statsapi/wiki/Data-Types:-Venue)

* `Mlb.get_venue_id(self, venue_name: str, search_key: str = 'name', **params)` - Return Venue Id(s)
* `Mlb.get_venue(self, venue_id: int, **params)` - Return Venue Object from venue Id
* `Mlb.get_venues(self, **params)` - Return all Venues

## Sports

[Wiki: Sport](https://github.com/zero-sum-seattle/python-mlb-statsapi/wiki/Data-Types:-Sport)

* `Mlb.get_sport(self, sport_id: int, **params)` - Return a Sport object from Id
* `Mlb.get_sports(self, **params)` - Return all Sports
* `Mlb.get_sport_id(self, sport_name: str, search_key: str = 'name', **params)` - Return Sport Id from name

## Schedules

[Wiki: Schedule](https://github.com/zero-sum-seattle/python-mlb-statsapi/wiki/Data-Types:-Schedule)

* `Mlb.get_schedule(self, date: str, start_date: str, end_date: str, sport_id: int, team_id: int, **params)` - Return a Schedule
* `Mlb.get_schedule(self, date: str = None, start_date: str = None, end_date: str = None, sport_id: int = 1, team_id: int = None, **params)` - Return a Schedule from dates
* `Mlb.get_scheduled_games_by_date(self, date: str = None, start_date: str = None, end_date: str = None, sport_id: int = 1, **params)` - Return game ids from dates

## Divisions

[Wiki: Division](https://github.com/zero-sum-seattle/python-mlb-statsapi/wiki/Data-Types:-Division)

* `Mlb.get_division(self, division_id: int, **params)` - Return a Division
* `Mlb.get_divisions(self, **params)` - Return all Divisions
* `Mlb.get_division_id(self, division_name: str, search_key: str = 'name', **params)` - Return Division Id(s) from name

## Leagues

[Wiki: League](https://github.com/zero-sum-seattle/python-mlb-statsapi/wiki/Data-Types:-League)

* `Mlb.get_league(self, league_id: int, **params)` - Return a League from Id
* `Mlb.get_leagues(self, **params)` - Return all Leagues
* `Mlb.get_league_id(self, league_name: str, search_key: str = 'name', **params)` - Return League Id(s)

## Seasons

[Wiki: Season](https://github.com/zero-sum-seattle/python-mlb-statsapi/wiki/Data-Types:-Season)

* `Mlb.get_season(self, season_id: str, sport_id: int = None, **params)` - Return a season
* `Mlb.get_seasons(self, sportid: int = None, **params)` - Return all seasons

## Standings

[Wiki: Standings](https://github.com/zero-sum-seattle/python-mlb-statsapi/wiki/Data-Types:-Standings)

* `Mlb.get_standings(self, league_id: int, season: str, **params)` - Return standings

## Games

[Wiki: Game](https://github.com/zero-sum-seattle/python-mlb-statsapi/wiki/Data-Types:-Game)

* `Mlb.get_game(self, game_id: int, **params)` - Return the Game for a specific Game Id
* `Mlb.get_game_play_by_play(self, game_id: int, **params)` - Return Play by play data for a game
* `Mlb.get_game_line_score(self, game_id: int, **params)` - Return a Linescore for a game
* `Mlb.get_game_box_score(self, game_id: int, **params)` - Return a Boxscore for a game
