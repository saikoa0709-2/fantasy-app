"""This is for local usage for now"""
from yahoo_oauth import OAuth2
import yahoo_fantasy_api as yfa
import csv

#connect to yahoo api
sc = OAuth2(None, None, from_file='oauth2.json')


#get game object
gm = yfa.Game(sc, 'nba')

leagues = gm.league_ids()

print(leagues)

#get the league object
lg = gm.to_league('428.l.117327')

#get the team key
teamkey = lg.team_key()


all_teams = lg.teams()
# print(all_teams)
all_keys = all_teams.keys()

#get the team object
my_team = lg.to_team(teamkey)

#get team roster
my_roster = my_team.roster()

def update_dict(player_dict, player_stats):
  player_stat = player_stats[0] 
#   print(player_stat)
  if (player_stat['FG%'] == '-'):
    return 0
  player_dict['FG%'] = player_dict['FG%'] + player_stat['FG%']
  player_dict['FT%'] = player_dict['FT%'] + player_stat['FT%']
  player_dict['3PTM'] = player_dict['3PTM'] + player_stat['3PTM']
  player_dict['PTS'] = player_dict['PTS'] + player_stat['PTS']
  player_dict['REB'] = player_dict['REB'] + player_stat['REB']
  player_dict['AST'] = player_dict['AST'] + player_stat['AST']
  player_dict['ST'] = player_dict['ST'] + player_stat['ST']
  player_dict['BLK'] = player_dict['BLK'] + player_stat['BLK']
  player_dict['TO'] = player_dict['TO'] + player_stat['TO']

  return 1


# Export team stats to CSV 
all_team_stats = []
i = 1
for key in all_keys:
  team_object = lg.to_team(key)
  team = all_teams.get(key)
  team_name = team['name']
  print("Team %s %s" % (i, team_name))
  i = i + 1
  roster = team_object.roster()
  players = []
  player_dict = {'FG%': 0, 'FT%': 0, '3PTM':0, 'PTS':0, 'REB':0, 'AST':0, 'ST':0, 'BLK':0, 'TO':0}
  total_player = 0
  for player in roster:
    players.append(player['name'])
    player_id = player['player_id']
    player_stats = lg.player_stats([player_id], 'average_season', season=2022)
    total_player += update_dict(player_dict, player_stats)
    # print(player_stats)
    print(total_player)
  for key, value in player_dict.items():
    player_dict[key] = round(value/total_player, 3)
#   print(players)
#   print(player_dict)
  player_dict['Team'] = team_name
  all_team_stats.append(player_dict)

field_names = ['Team', 'FG%', 'FT%', '3PTM', 'PTS', 'REB', 'AST', 'ST', 'BLK', 'TO']
with open('team_stats.csv', 'w') as csvfile:
  writer = csv.DictWriter(csvfile, fieldnames = field_names)
  writer.writeheader()
  writer.writerows(all_team_stats)



  
