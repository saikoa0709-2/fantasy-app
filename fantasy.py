"""This is for local usage for now"""
from yahoo_oauth import OAuth2
import yahoo_fantasy_api as yfa
import csv


# global var
skip_stat_id_set = {'9004003','9007006'}

# connect to yahoo api
sc = OAuth2(None, None, from_file='oauth2.json')

# get game object
gm = yfa.Game(sc, 'nba')
leagues = gm.league_ids()

# get the league object
lg = gm.to_league('428.l.117327')

# get the team key for logged in users
teamkey = lg.team_key()
all_teams = lg.teams()
all_keys = all_teams.keys()

# get the team object
my_team = lg.to_team(teamkey)

# get team roster
my_roster = my_team.roster()


def get_matchups_scores_by_week(week=None):
    matchups_result = [["Week", "Name", "FG%", "FT%", "3PTM", "PTS", "REB", "AST", "ST", "BLK", "TO"]]
    
    # get matchups data for a given week, defaults to current week.
    if week == None:
        week = lg.current_week()-1
    matchups_obj = lg.matchups(week)
    matchups_contents = matchups_obj["fantasy_content"]["league"]
    matchups_scoreboards = matchups_contents[1]["scoreboard"]["0"]["matchups"] # matchups_scoreboards={'0': data of first match, '1': data of second match, ..., 'count':6}

    # delete the 'count' from the matchups_scoreboards
    del matchups_scoreboards['count']

    # iterate matchups_scoreboards to get the data of each match
    for matchups_data in matchups_scoreboards.values():
        matchup_data = matchups_data["matchup"]
        matchup_teams_data = matchup_data["0"]["teams"]  # matchup_teams_data={'0': data of first team, '1': data of second team,'count':2}

        # delete the 'count' from the matchup_teams_data
        del matchup_teams_data['count']
        
        for team_data in matchup_teams_data.values():
            team_result = []
            team_data = team_data["team"]
            team_name = team_data[0][2]['name']
            # print(team_name)
            team_result.append(week)
            team_result.append(team_name)
            team_stats = team_data[1]["team_stats"]['stats']
            
            # iterate team_stats to get the data of each cat
            for team_stat in team_stats:
                team_stat_id = team_stat['stat']['stat_id']
                cat_val = team_stat['stat']['value']
                
                # skip FGM/A & FTM/A
                if team_stat_id in skip_stat_id_set:
                    continue
                team_result.append(cat_val)
                # print(cat_val)
            matchups_result.append(team_result)
    
    with open('matchups.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(matchups_result)


# get final matchups scores for a given week, default to the latest finished week.
get_matchups_scores_by_week()

'''
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
'''