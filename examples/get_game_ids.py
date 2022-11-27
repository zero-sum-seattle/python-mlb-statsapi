# imports
import mlbstatsapi


mlb = mlbstatsapi.Mlb()


# get schedule for 13th of october
schedule = mlb.get_schedule(date='2022-10-13')


# pull out scheduled games
scheduled_games = schedule.dates

# create empty list and set team
game_ids = []
team = "Seattle Mariners"

# loop through each scheduled_games for games
for date in scheduled_games.dates:
	for game in date.games:
        
		# let's get the mariners games
		if game.teams.home.name == team:
			game_ids.append(game.gamepk)
			continue

		if game.teams.away.name == team:
			game_ids.append(game.gamepk)
			continue

print(game_ids)