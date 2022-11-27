# import mlbstatsapi
import mlbstatsapi

# creat instance of Mlb
mlb = mlbstatsapi.Mlb()

# set date
date = '2022-10-13'

# get schedule for 13th of october
schedule = mlb.get_schedule(date=date)

# pull out scheduled games
scheduled_games = schedule.dates

# create empty list and set team
game_ids = []
team = "Seattle Mariners"

# loop through each scheduled_games for games
for date in scheduled_games:
	for game in date.games:
        
		# let's get the mariners games
		if game.teams.home.team.name == team:
			game_ids.append(game.gamepk)
			continue

		if game.teams.away.team.name == team:
			game_ids.append(game.gamepk)
			continue


# set person fullname
player_full_name = 'Ty France'

# get player id for ty france
ty_france = mlb.get_people_id(player_full_name)

game_stats = []
# print matching person id
if len(ty_france) == 1:
	player_id = ty_france[0]
	
	for game_id in game_ids:
		stats = mlb.get_players_stats_for_game(person_id=player_id, game_id=game_id)
		game_stats.append(stats)

print(game_stats)