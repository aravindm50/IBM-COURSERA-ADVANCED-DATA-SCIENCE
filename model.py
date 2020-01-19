#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# In[2]:


import warnings
warnings.filterwarnings("ignore")


# In[3]:


import os
import sys


# In[4]:


data_path = "/home/griffonuser/DS_Practise/Capstone/ipl_csv"


# In[5]:


from os import listdir

def find_csv_filenames( path_to_dir, suffix=".csv" ):
    filenames = listdir(path_to_dir)
    return [ filename for filename in filenames if filename.endswith( suffix ) ]


# In[6]:


all_matches_files = find_csv_filenames(data_path)


# In[7]:


def is_non_zero_file(fpath):  
    return os.path.isfile(fpath) and os.path.getsize(fpath) > 0


# In[8]:


def extract_match_information(file_path, file_name):
    path = file_path + "/" + file_name
    if is_non_zero_file(path):
        trans  = pd.read_csv(path, error_bad_lines=False, skiprows=1, header=None, warn_bad_lines=False)
        trans1 = trans.set_index(1).T
        trans2 = trans1[trans1['season']!= 'info'].reset_index(drop=True)
        d = {'tv_umpire':['tv_umpire_1','tv_umpire_2'],'team':['home_team','away_team'], 'umpire':['umpire_1','umpire_2','umpire_3'], 'date':['date_1','date_2','date_3','date_4','date_5'],'match_number':['match_number_1','match_number_2'],'player_of_match':['player_of_match_1','player_of_match_2'],'reserve_umpire':['reserve_umpire_1','reserve_umpire_2']}
        trans3 = trans2.loc[:,~trans2.columns.isin(['index',1])]
        trans4 = trans3.rename(columns=lambda c: d[c].pop(0) if c in d.keys() else c).reset_index(drop=True)
        return trans4


# In[ ]:


match_information = pd.DataFrame(columns = ['file','home_team','away_team','gender','season','date_1','date_2','method','competition','match_number','venue','city','toss_winner','toss_decision','player_of_match','umpire_1','umpire_2','reserve_umpire','tv_umpire','match_referee','winner','winner_runs','winner_wickets'])
for file in all_matches_files:
    if is_non_zero_file(data_path + "/" + file):
        data = extract_match_information(data_path,file)
        length = len(data.columns)
        data['file'] = file
        data['length'] = length
        match_information = pd.concat([match_information,data])
match_information = match_information.reset_index()
match_information = match_information.sort_values(['date_1', 'match_number'], ascending=[1,1]).reset_index()
match_information = match_information.loc[:,~match_information.columns.isin(['index','level_0'])]


# In[ ]:


match_information = match_information.fillna(0)


# In[ ]:


match_information.to_csv("/home/griffonuser/DS_Practise/Capstone/match_information.csv", index=False)


# In[10]:


match_information = pd.read_csv("/home/griffonuser/DS_Practise/Capstone/match_information.csv")


# In[11]:


def team_information(file_path,file_name,row):
    path = file_path + "/" + file_name
    match_data = pd.read_csv(path, error_bad_lines = False, skiprows = row, header= None, names = ['type','innings','ball','team_batting','batsman_on_strike','batsman_non_strike','bowler','runs_scored','extras','way_out','batsman_out'])
    match_data = match_data.fillna(0.0)
    match_data['count_ball'] = match_data.groupby((match_data['innings'] != match_data['innings'].shift(1)).cumsum()).cumcount()+1
    match_data['file'] = file_name
    return match_data


# In[12]:


def get_row_of_data(match_information,file_name):
    length = match_information.loc[match_information['file'] == file_name]["length"]
    return int(length)+1


# In[13]:


def match_info(match_data):
    match_info = pd.DataFrame()
    match_info['ball_in_first_innings'] = [(match_data['innings'] == 1).sum()]
    match_info['ball_in_second_innings'] = [(match_data['innings'] == 2).sum()]
    match_info['extra_first'] = [match_data[match_data['innings'] == 1]['extras'].sum()]
    match_info['extra_second'] = [match_data[match_data['innings'] == 2]['extras'].sum()]
    match_info['runs_scored_first'] = [match_data[match_data['innings'] == 1]['runs_scored'].sum()]
    match_info['runs_scored_second'] = [match_data[match_data['innings'] == 2]['runs_scored'].sum()]
    match_info['wicket_first'] = [len(match_data[match_data['innings'] == 1][match_data['way_out'] != 0]['way_out'])]
    match_info['wicket_second'] = [len(match_data[match_data['innings'] == 2][match_data['way_out'] != 0]['way_out'])]
    match_info['first_6'] = [match_data[match_data['innings'] == 1][match_data['count_ball'] <= 36]['runs_scored'].sum()]
    match_info['second_6'] = [match_data[match_data['innings'] == 2][match_data['count_ball'] <= 36]['runs_scored'].sum()]
    match_info['first_15'] = [match_data[match_data['innings'] == 1][match_data['count_ball'] > 90]['runs_scored'].sum()]
    match_info['second_15'] = [match_data[match_data['innings'] == 2][match_data['count_ball'] > 90]['runs_scored'].sum()]
    match_info['first_middle'] = [match_data[match_data['innings'] == 1][match_data['count_ball'] <= 90][match_data['count_ball'] > 36]['runs_scored'].sum()]
    match_info['second_middle'] = [match_data[match_data['innings'] == 2][match_data['count_ball'] <= 90][match_data['count_ball'] > 36]['runs_scored'].sum()]
    match_info['file'] = match_data['file']
    match_info['total_first'] = match_info['runs_scored_first'] + match_info['extra_first']
    match_info['total_second'] = match_info['runs_scored_second'] + match_info['extra_second']
    return match_info


# In[14]:


match_stats = pd.DataFrame(columns = ['ball_in_first_innings', 'ball_in_second_innings', 'total_first','total_second','extra_first',
       'extra_second', 'runs_scored_first', 'runs_scored_second',
       'wicket_first', 'wicket_second', 'first_6', 'second_6', 'first_15',
       'second_15', 'first_middle', 'second_middle', 'file', 'away_team',
       'city', 'competition', 'date_1', 'date_2', 'eliminator', 'gender',
       'home_team', 'length', 'match_number', 'match_referee', 'method',
       'neutralvenue', 'outcome', 'player_of_match', 'reserve_umpire',
       'season', 'toss_decision', 'toss_winner', 'tv_umpire', 'umpire_1',
       'umpire_2', 'venue', 'winner', 'winner_runs', 'winner_wickets'].sort())
for file in all_matches_files:
    if is_non_zero_file(data_path + "/" + file):
        match_data = team_information(data_path,file,get_row_of_data(match_information,file))
        match_in = match_info(match_data)
        match_data1 = pd.merge(match_in, match_information, on=['file'])
        match_stats = pd.concat([match_stats,match_data1])
        


# In[15]:


match_stats = match_stats.sort_values(by=['date_1','match_number'], ascending=[1,1])
match_stats.to_csv("/home/griffonuser/DS_Practise/Capstone/complete_match_info.csv", index = False)


# In[16]:


all_matches_path = "/home/griffonuser/DS_Practise/Capstone/all_csv"
all_matches = find_csv_filenames(all_matches_path)


# In[ ]:


import warnings
warnings.filterwarnings("ignore")
ipl_player_stats_list = get_player_list(match_information,data_path)


# In[ ]:


ipl_player_stats_list = ipl_player_stats_list.fillna(0)
ipl_player_stats_list.to_csv("/home/griffonuser/DS_Practise/Capstone/ipl_player_info.csv", index = False)


# In[18]:


ipl_stats_list = pd.read_csv("/home/griffonuser/DS_Practise/Capstone/complete_match_info.csv")


# In[19]:


bat_first = pd.DataFrame(columns = ['bat_first'])
for idx in ipl_stats_list.index:
    if (ipl_stats_list.home_team[idx] == ipl_stats_list.toss_winner[idx] and ipl_stats_list.toss_decision[idx] == "bat") or (ipl_stats_list.home_team[idx] != ipl_stats_list.toss_winner[idx] and ipl_stats_list.toss_decision[idx] == "field"):
        bat_first.loc[idx] = [ipl_stats_list.home_team[idx]]
    elif (ipl_stats_list.home_team[idx] != ipl_stats_list.toss_winner[idx] and ipl_stats_list.toss_decision[idx] == "bat") or (ipl_stats_list.home_team[idx] == ipl_stats_list.toss_winner[idx] and ipl_stats_list.toss_decision[idx] == "field"):
        bat_first.loc[idx] = [ipl_stats_list.away_team[idx]]


# In[20]:


ipl_stats_list = ipl_stats_list.join(bat_first)


# In[21]:


import seaborn as sns


# In[357]:


plt.figure(figsize=(12,10))
ax = sns.barplot(x=ipl_stats_list['city'][ipl_stats_list['city'] != "0"], y=ipl_stats_list['total_first'],palette=sns.cubehelix_palette(len(ipl_stats_list['city'].unique())), order= np.sort(ipl_stats_list['city'][ipl_stats_list['city'] != "0"].unique()))
# Place the region names at a 90-degree angleipl_stats_list
plt.xticks(rotation= 90)
plt.xlabel('City')
plt.ylabel('Average first Innings score')
plt.title('City Wise First Innings Score')
plt.show()


# In[358]:


plt.figure(figsize=(12,10))
sns.barplot(x=ipl_stats_list['city'][ipl_stats_list['city'] != "0"], y=ipl_stats_list['total_second'],palette=sns.cubehelix_palette(len(ipl_stats_list['city'].unique())), order= np.sort(ipl_stats_list['city'][ipl_stats_list['city'] != "0"].unique()))
# Place the region names at a 90-degree angleipl_stats_list
plt.xticks(rotation= 90)
plt.xlabel('City')
plt.ylabel('Average Second Innings score')
plt.title('City Wise Second Innings Score')
plt.show()


# In[359]:


plt.figure(figsize=(12,10))
sns.barplot(x=ipl_stats_list['winner'][ipl_stats_list['winner'] == ipl_stats_list['bat_first']], y=ipl_stats_list['total_first'],palette=sns.cubehelix_palette(len(ipl_stats_list['winner'].unique())), order= np.sort(ipl_stats_list['winner'][ipl_stats_list['winner'] != "0"].unique()))
# Place the region names at a 90-degree angle
plt.xticks(rotation= 90)
plt.xlabel('Winning Team')
plt.ylabel('Average Batting First score when winning')
plt.title('Team Wise First Innings Score when winning and batting first')
plt.show()


# In[360]:


plt.figure(figsize=(12,10))
sns.barplot(x=ipl_stats_list['winner'][ipl_stats_list['winner'] != ipl_stats_list['bat_first']], y=ipl_stats_list['total_first'],palette=sns.cubehelix_palette(len(ipl_stats_list['winner'].unique())), order= np.sort(ipl_stats_list['winner'][ipl_stats_list['winner'] != "0"].unique()))
# Place the region names at a 90-degree angle
plt.xticks(rotation= 90)
plt.xlabel('Winning Team')
plt.ylabel('Average Batting First score when Chasing and Winning')
plt.title('First Innings Score when Chasing and Winning')
plt.show()


# In[361]:


plt.figure(figsize=(12,10))
sns.barplot(x=ipl_stats_list['winner'][ipl_stats_list['toss_decision'] != "bat"], y=ipl_stats_list['total_first'],palette=sns.cubehelix_palette(len(ipl_stats_list['winner'].unique())), order= np.sort(ipl_stats_list['winner'].unique()))
# Place the region names at a 90-degree angle
plt.xticks(rotation= 90)
plt.xlabel('Winning Team')
plt.ylabel('Average Batting First score when Winning and deciding to field')
plt.title('First Innings Score when Winning match and the toss and deciding to field')
plt.show()


# In[362]:


plt.figure(figsize=(12,10))
sns.barplot(x=ipl_stats_list['winner'][ipl_stats_list['toss_decision'] == "bat"], y=ipl_stats_list['total_first'],palette=sns.cubehelix_palette(len(ipl_stats_list['winner'].unique())), order= np.sort(ipl_stats_list['winner'].unique()))
# Place the region names at a 90-degree angle
plt.xticks(rotation= 90)
plt.xlabel('Winning Team')
plt.ylabel('Average Batting First score when Winning and deciding to bat')
plt.title('First Innings Score when Winning match and the toss and deciding to bat')
plt.show()


# In[363]:


plt.figure(figsize=(12,10))
sns.barplot(x=ipl_stats_list['winner'][ipl_stats_list['winner'] == ipl_stats_list['bat_first']], y=ipl_stats_list['first_6'],palette=sns.cubehelix_palette(len(ipl_stats_list['winner'].unique())), order= np.sort(ipl_stats_list['winner'][ipl_stats_list['winner'] != "0"].unique()))
# Place the region names at a 90-degree angle
plt.xticks(rotation= 90)
plt.xlabel('Winning Team')
plt.ylabel('Average score during first 6 overs')
plt.title('Winning team batting first and scoring in the first 6 overs')
plt.show()


# In[364]:


plt.figure(figsize=(12,10))
sns.barplot(x=ipl_stats_list['winner'][ipl_stats_list['winner'] == ipl_stats_list['bat_first']], y=ipl_stats_list['first_15'],palette=sns.cubehelix_palette(len(ipl_stats_list['winner'].unique())), order= np.sort(ipl_stats_list['winner'][ipl_stats_list['winner'] != "0"].unique()))
# Place the region names at a 90-degree angle
plt.xticks(rotation= 90)
plt.xlabel('Winning Team')
plt.ylabel('Average score during last 5 overs')
plt.title('Winning team batting first and scoring in the last 5 overs')
plt.show()


# In[365]:


plt.figure(figsize=(12,10))
sns.barplot(x=ipl_stats_list['winner'][ipl_stats_list['winner'] != ipl_stats_list['bat_first']], y=ipl_stats_list['second_6'],palette=sns.cubehelix_palette(len(ipl_stats_list['winner'].unique())), order= np.sort(ipl_stats_list['winner'][ipl_stats_list['winner'] != "0"].unique()))
# Place the region names at a 90-degree angle
plt.xticks(rotation= 90)
plt.xlabel('Winning Team')
plt.ylabel('Average score during 6 overs')
plt.title('Winning team batting second and scoring in the first 6 overs')
plt.show()


# In[366]:


plt.figure(figsize=(12,10))
sns.barplot(x=ipl_stats_list['winner'][ipl_stats_list['winner'] != ipl_stats_list['bat_first']], y=ipl_stats_list['second_15'],palette=sns.cubehelix_palette(len(ipl_stats_list['winner'].unique())), order= np.sort(ipl_stats_list['winner'][ipl_stats_list['winner'] != "0"].unique()))
# Place the region names at a 90-degree angle
plt.xticks(rotation= 90)
plt.xlabel('Winning Team')
plt.ylabel('Average score during last 5 overs')
plt.title('Winning team batting second and scoring in the last 5 overs')
plt.show()


# In[27]:


ipl_players_stats = pd.read_csv("/home/griffonuser/DS_Practise/Capstone/ipl_player_info.csv")


# In[24]:


ipl_players_stats['batting_strikerate'] = round(100 * ipl_players_stats['runs_scored'].replace([np.inf, -np.inf], np.nan).fillna(0) / ipl_players_stats['ball_faced'],2).replace([np.inf, -np.inf], np.nan).fillna(0)

ipl_players_stats['bowling_strikerate']= round(100 * ipl_players_stats['wickets_taken'].replace([np.inf, -np.inf], np.nan).fillna(0) / ipl_players_stats['balls_bowled'],2).replace([np.inf, -np.inf], np.nan).fillna(0)

ipl_players_stats['economy_rate'] = round(6 * ipl_players_stats['runs_given'].replace([np.inf, -np.inf], np.nan).fillna(0) / ipl_players_stats['balls_bowled'],2).replace([np.inf, -np.inf], np.nan).fillna(0)

ipl_players_stats['matches'] = ipl_players_stats['matches'].replace([np.inf, -np.inf], np.nan).fillna(0).astype('int')

ipl_players_stats['not_outs'] = ipl_players_stats['not_outs'].replace([np.inf, -np.inf], np.nan).fillna(0).astype('int')

ipl_players_stats['outs'] = ipl_players_stats.apply(lambda x: x['matches'] - x['not_outs'], axis=1)

ipl_players_stats['batting_average'] = round(ipl_players_stats['runs_scored'] / ipl_players_stats['outs'],2).replace([np.inf, -np.inf], np.nan).fillna(0)

ipl_players_stats['bowling_average'] = round(ipl_players_stats['balls_bowled'] / ipl_players_stats['wickets_taken'],2).replace([np.inf, -np.inf], np.nan).fillna(0)

ipl_players_stats = ipl_players_stats.fillna(0)
ipl_players_stats.to_csv("/home/griffonuser/DS_Practise/Capstone/ipl_player_info.csv", index = False)


# In[ ]:


ipl_players_stats


# In[367]:


top_players_bat = ipl_players_stats.sort_values(['runs_scored'], ascending =[0]).head(20)
plt.figure(figsize=(12,10))
sns.barplot(x=top_players_bat['player_name'], y=top_players_bat['runs_scored'],palette=sns.cubehelix_palette(len(top_players_bat['player_name'].unique())))
# Place the region names at a 90-degree angle
plt.xticks(rotation= 90)
plt.xlabel('Player')
plt.ylabel('Total runs scored in IPL')
plt.title('Top Players by the runs scored in IPL')
plt.show()


# In[368]:


top_players_wicket_takers = ipl_players_stats.sort_values(['wickets_taken'], ascending =[0]).head(20)
plt.figure(figsize=(12,10))
sns.barplot(x=top_players_wicket_takers['player_name'], y=top_players_wicket_takers['wickets_taken'],palette=sns.cubehelix_palette(len(top_players_wicket_takers['player_name'].unique())))
# Place the region names at a 90-degree angle
plt.xticks(rotation= 90)
plt.xlabel('Player')
plt.ylabel('Total runs scored in IPL')
plt.title('Top Players by the Wickets taken in IPL')
plt.show()


# In[369]:


top_players_bat_strikerate = ipl_players_stats.assign(f = 100 * ipl_players_stats['runs_scored'][ipl_players_stats['runs_scored'] > 1500] / ipl_players_stats['ball_faced'][ipl_players_stats['runs_scored'] > 1500]).sort_values(['f'], ascending = [0]).head(20)
plt.figure(figsize=(12,10))
g = sns.barplot(x=top_players_bat_strikerate['player_name'], y=top_players_bat_strikerate['f'],palette=sns.cubehelix_palette(len(top_players_bat_strikerate['player_name'].unique())))
# Place the region names at a 90-degree angle
plt.xticks(rotation= 90)
plt.xlabel('Player')
plt.ylabel('Batting Strikerate in IPL')
plt.title('Top Players by the Batting Strikerate taken in IPL with minimum 1500 runs scored')
plt.show()


# In[ ]:


ipl_players_stats


# In[370]:


top_players_six_hitters_100 = ipl_players_stats.assign(f = 100 * ipl_players_stats['6s'][ipl_players_stats['runs_scored'] > 1500] / ipl_players_stats['ball_faced'][ipl_players_stats['runs_scored'] > 1500]).sort_values(['f'], ascending = [0]).head(20)
plt.figure(figsize=(12,10))
g = sns.barplot(x=top_players_six_hitters_100['player_name'], y=top_players_six_hitters_100['f'],palette=sns.cubehelix_palette(len(top_players_six_hitters_100['player_name'].unique())))
# Place the region names at a 90-degree angle
plt.xticks(rotation= 90)
plt.xlabel('Player')
plt.ylabel('Number of 6s per 100 balls in IPL')
plt.title('Top Players by the Number of 6s per 100 balls in IPL with minimum 1500 runs scored')
plt.show()


# In[ ]:


top_players_six_hitters = ipl_players_stats.assign(f = ipl_players_stats['6s']).sort_values(['f'], ascending = [0]).head(20)
plt.figure(figsize=(12,10))
g = sns.barplot(x=top_players_six_hitters['player_name'], y=top_players_six_hitters['f'],palette=sns.cubehelix_palette(len(top_players_six_hitters['player_name'].unique())))
# Place the region names at a 90-degree angle
plt.xticks(rotation= 90)
plt.xlabel('Player')
plt.ylabel('Number of 6s in IPL')
plt.title('Top Players by the Number of 6s in IPL')
plt.show()


# In[ ]:


top_players_four_hitters = ipl_players_stats.assign(f = ipl_players_stats['4s']).sort_values(['f'], ascending = [0]).head(20)
plt.figure(figsize=(12,10))
g = sns.barplot(x=top_players_four_hitters['player_name'], y=top_players_four_hitters['f'],palette=sns.cubehelix_palette(len(top_players_four_hitters['player_name'].unique())))
# Place the region names at a 90-degree angle
plt.xticks(rotation= 90)
plt.xlabel('Player')
plt.ylabel('Number of 4s in IPL')
plt.title('Top Players by the Number of 4s in IPL')
plt.show()


# In[371]:


top_players_2s = ipl_players_stats.assign(f = ipl_players_stats['2s']).sort_values(['f'], ascending = [0]).head(20)
plt.figure(figsize=(12,10))
g = sns.barplot(x=top_players_2s['player_name'], y=top_players_2s['f'],palette=sns.cubehelix_palette(len(top_players_2s['player_name'].unique())))
# Place the region names at a 90-degree angle
plt.xticks(rotation= 90)
plt.xlabel('Player')
plt.ylabel('Number of 2s in IPL')
plt.title('Top Players showing running between the wickets')
plt.show()


# In[373]:


top_players_bowling_strikerate = ipl_players_stats.assign(f = 100 * ipl_players_stats['wickets_taken'][ipl_players_stats['wickets_taken'] > 50]/ ipl_players_stats['balls_bowled'][ipl_players_stats['wickets_taken'] > 50]).sort_values(['f'], ascending = [0]).head(20)
plt.figure(figsize=(12,10))
g = sns.barplot(x=top_players_bowling_strikerate['player_name'], y=top_players_bowling_strikerate['f'],palette=sns.cubehelix_palette(len(top_players_bowling_strikerate['player_name'].unique())))
# Place the region names at a 90-degree angle
plt.xticks(rotation= 90)
plt.xlabel('Player')
plt.ylabel('Number of Wickets taken per 100 balls bowled in IPL')
plt.title('Top Players by the Bowling Srtrikerate in IPL with minimum 50 wickets')
plt.show()


# In[372]:


top_players_economy = ipl_players_stats.assign(f = 6 * ipl_players_stats['runs_given'][ipl_players_stats['balls_bowled'] >= 120] / ipl_players_stats['balls_bowled'][ipl_players_stats['balls_bowled'] >= 120]  ).sort_values(['f'], ascending = [1]).head(30)
plt.figure(figsize=(12,10))
g = sns.barplot(x=top_players_economy['player_name'], y=top_players_economy['f'],palette=sns.cubehelix_palette(len(top_players_economy['player_name'].unique())))
# Place the region names at a 90-degree angle
plt.xticks(rotation= 90)
plt.xlabel('Player')
plt.ylabel('Economy in IPL minimum 20 matches')
plt.title('Top Players by the lowest economy in IPL minimum 20 matches')
plt.show()


# # Assumptions

# ## 1. Top players for respective stats are desired more by the teams and hence are weighted more.
# 
# ## 2.  Batsman are given more weightage than bowlers since T20 tournaments involve more run scoring.
# 
# ## 3. If a player does not play in two consecutive tournaments then he is considered as retired player and will not be part of the auction.
# 
# ## 4. As the information of retired players is not available, it is assumed that players retired in the current year are still part of the auction.
# 
# ## 5. New Players who entered the cricket circuit recently are not considered for future auction since data is not available for the new players.
# 

# In[28]:


def get_current_players(match_information, file_path):
    player_list = pd.DataFrame(columns = ['player_name'])
    for idx in match_information.index:
        if match_information.date_1[idx] > "2018/01/01":
            path = file_path + "/" + match_information['file'][idx]
            row = int(match_information['length'][idx])
            match_data = pd.read_csv(path, error_bad_lines = False, skiprows = row + 1, header= None, names = ['type','innings','ball','team_batting','batsman_on_strike','batsman_non_strike','bowler','runs_scored','extras','way_out','batsman_out'])
            match_data = match_data.fillna(0.0)
            all_players = match_data.batsman_on_strike.append(match_data.batsman_non_strike).append(match_data.bowler)
            for player in all_players.unique():
                if player not in player_list['player_name'].unique():
                    temp = pd.DataFrame()
                    temp['player_name'] = [player]
                    player_list = pd.concat([player_list,temp],ignore_index=True,axis=0)
                else:
                    pass
    return player_list


# In[29]:


current_players = get_current_players(match_information,data_path).sort_values(['player_name'], ascending = [1]).reset_index(drop=True)


# In[30]:


def get_top_current_players_batting(current_players, ipl_player_stats):
    current_ipl_player_stats = pd.DataFrame(columns = ipl_player_stats.columns)
    for player in current_players.player_name:
        temp =  ipl_player_stats[ipl_player_stats['player_name'] == player]
        current_ipl_player_stats = pd.concat([current_ipl_player_stats,temp],ignore_index=True,axis=0)
        current_ipl_player_stats = current_ipl_player_stats[current_ipl_player_stats['batting_strikerate'] >= 100.00][current_ipl_player_stats['batting_average'] >= 20.0]
    return current_ipl_player_stats


# In[31]:


import warnings
warnings.filterwarnings("ignore")

top_current_batsman = get_top_current_players_batting(current_players, ipl_players_stats)


# In[32]:


def get_top_current_players_bowling(current_players, ipl_player_stats):
    current_ipl_player_stats = pd.DataFrame(columns = ipl_player_stats.columns)
    for player in current_players.player_name:
        temp =  ipl_player_stats[ipl_player_stats['player_name'] == player]
        current_ipl_player_stats = pd.concat([current_ipl_player_stats,temp],ignore_index=True,axis=0)
        current_ipl_player_stats = current_ipl_player_stats[current_ipl_player_stats['economy_rate'] <= 9.0][current_ipl_player_stats['wickets_taken'] >= 10][current_ipl_player_stats['bowling_average'] <= 35.0]
    return current_ipl_player_stats


# In[33]:


import warnings
warnings.filterwarnings("ignore")
top_current_bowler = get_top_current_players_bowling(current_players,ipl_players_stats)


# In[34]:


def get_top_current_players_allrounder(current_players, ipl_player_stats):
    current_ipl_player_stats = pd.DataFrame(columns = ipl_player_stats.columns)
    for player in current_players.player_name:
        temp =  ipl_player_stats[ipl_player_stats['player_name'] == player]
        current_ipl_player_stats = pd.concat([current_ipl_player_stats,temp],ignore_index=True,axis=0)
        current_ipl_player_stats = current_ipl_player_stats[current_ipl_player_stats['economy_rate'] <= 10.0][current_ipl_player_stats['wickets_taken'] >= 10][current_ipl_player_stats['batting_strikerate'] >= 100.00][current_ipl_player_stats['batting_average'] >= 20.0][current_ipl_player_stats['bowling_average'] <= 35.0]
    return current_ipl_player_stats


# In[35]:


import warnings
warnings.filterwarnings("ignore")
top_current_allrounder = get_top_current_players_allrounder(current_players,ipl_players_stats)


# In[36]:


not_top = list(set(current_players.player_name.values) - set(top_current_batsman.player_name) - set(top_current_bowler.player_name) - set(top_current_allrounder.player_name))


# In[37]:


not_top_players = ipl_players_stats[ipl_players_stats['player_name'].isin(not_top)]


# In[38]:


not_top_players = not_top_players.reset_index()


# In[39]:


ipl_player_points = pd.read_csv("/home/griffonuser/DS_Practise/Capstone/ipl_points.csv")


# In[40]:


current_players_points = ipl_player_points[ipl_player_points['player_ipl_name'].isin(current_players['player_name'])].reset_index().drop('index',axis = 1)


# In[41]:


current_players_points = current_players_points.rename(columns={'player_ipl_name':'player_name'})


# In[42]:


not_list =ipl_player_points[~ipl_player_points['player_ipl_name'].isin(current_players['player_name'])]


# In[ ]:


current_players_points


# In[43]:


no_point = current_players[~current_players['player_name'].isin(current_players_points['player_name'])].reset_index().drop('index',axis = 1)


# In[44]:


current_player_stats = ipl_players_stats[ipl_players_stats['player_name'].isin(current_players_points['player_name'])].reset_index().drop('index', axis = 1)


# In[45]:


current_player_stats = pd.merge(current_player_stats,current_players_points,on=['player_name'])


# In[46]:


def current_player_season_wise(match_information,file_path):
    player_list = pd.DataFrame(columns = ['player_name','season','runs_scored','ball_faced','4s', '6s','2s','not_outs','','balls_bowled','balls_bowled_15','balls_bowled_6','balls_bowled_middle','wickets_taken','runs_given','runs_given_middle','runs_given_15','runs_given_6','boundaries_given','extras_given','matches','runs_last_5','runs_first_6','runs_middle','boundaries_last_5','boundaries_first_6','economy_first_6','economy_last_5','economy_middle','wickets_first_6','wickets_last_5'])
    all_seasons = match_information['season'].unique()
    for season in all_seasons:
        print(season)
        for idx in match_information.index:
            if match_information['date_1'][idx].split('/',1)[0] == str(season):
                path = file_path + "/" + match_information['file'][idx]
                print(path)
                row = int(match_information['length'][idx])
                match_data = pd.read_csv(path, error_bad_lines = False, skiprows = row + 1, header= None, names = ['type','innings','ball','team_batting','batsman_on_strike','batsman_non_strike','bowler','runs_scored','extras','way_out','batsman_out'])
                match_data = match_data.fillna(0.0)
                all_players = match_data.batsman_on_strike.append(match_data.batsman_non_strike).append(match_data.bowler)
                for player in all_players.unique():
                    season_player = player_list[player_list['player_name'] == player]['season'].unique()
                    if player not in player_list['player_name'].unique() or (player in player_list['player_name'].unique() and str(season) not in season_player):
                        temp = pd.DataFrame()
                        temp['player_name'] = [player]

                        temp['season'] = [match_information['date_1'][idx].split('/',1)[0]]

                        temp['runs_scored'] = [match_data[match_data['batsman_on_strike'] == player]['runs_scored'].sum()]

                        temp['ball_faced'] = [len(match_data[match_data['batsman_on_strike'] == player][match_data['extras'] == 0].index)]

                        temp['4s'] = [len(match_data[match_data['batsman_on_strike'] == player][match_data['runs_scored'] == 4].index)]

                        temp['6s'] = [len(match_data[match_data['batsman_on_strike'] == player][match_data['runs_scored'] == 6].index)]

                        temp['2s'] = [len(match_data[match_data['batsman_on_strike'] == player][match_data['runs_scored'] == 2].index)]

                        if len(match_data[match_data['batsman_out'] == player].index) == 0:
                            temp['not_outs'] = [1]
                        elif len(match_data[match_data['batsman_out'] == player].index) == 1:
                            temp['not_outs'] = [0]

                        temp['balls_bowled'] = [len(match_data[match_data['bowler'] == player].index) - len(match_data[match_data['bowler'] == player][match_data['extras'] != 0].index)]

                        temp['wickets_taken'] = [len(match_data[match_data['bowler'] == player][match_data['way_out'] != 0.0][match_data['way_out'] != "run out"].index)]

                        temp['extras_given'] = [len(match_data[match_data['bowler'] == player][match_data['extras'] != 0].index)]

                        temp['runs_given'] = [match_data[match_data['bowler'] == player][match_data['extras'] != 0]['extras'].sum() + match_data[match_data['bowler'] == player][match_data['runs_scored'] != 0]['runs_scored'].sum()]

                        temp['boundaries_given'] = [len(match_data[match_data['bowler'] == player][match_data['runs_scored'] == 4].index) + len(match_data[match_data['bowler'] == player][match_data['runs_scored'] == 6].index)]

                        temp['matches'] = [1]

                        temp['runs_last_5'] = [match_data[match_data['batsman_on_strike'] == player][match_data['ball']>=15.0]['runs_scored'].sum()]

                        temp['runs_middle'] = [match_data[match_data['batsman_on_strike'] == player][match_data['ball']<15.0][match_data['ball']>=6.0]['runs_scored'].sum()]

                        temp['runs_first_6'] = [match_data[match_data['batsman_on_strike'] == player][match_data['ball'] < 6.0]['runs_scored'].sum()]

                        balls_bowled_15 = len(match_data[match_data['bowler'] == player][match_data['ball'] >= 15.0].index) - len(match_data[match_data['bowler'] == player][match_data['ball'] >= 15.0][match_data['extras'] != 0].index)

                        balls_bowled_6 = len(match_data[match_data['bowler'] == player][match_data['ball'] < 6.0].index) - len(match_data[match_data['bowler'] == player][match_data['ball'] < 6.0][match_data['extras'] != 0].index)

                        balls_bowled_middle = len(match_data[match_data['bowler'] == player][match_data['ball'] >= 6.0][match_data['ball'] < 15.0].index) - len(match_data[match_data['bowler'] == player][match_data['ball'] >= 6.0][match_data['ball'] < 15.0][match_data['extras'] != 0].index)

                        temp['balls_bowled_15'] = [balls_bowled_15]

                        temp['balls_bowled_6'] = [balls_bowled_6]

                        temp['balls_bowled_middle'] = [balls_bowled_middle]

                        runs_given_15 = match_data[match_data['bowler'] == player][match_data['ball'] >= 15.0][match_data['extras'] != 0]['extras'].sum() + match_data[match_data['bowler'] == player][match_data['ball'] >= 15.0][match_data['runs_scored'] != 0]['runs_scored'].sum()

                        runs_given_6 = match_data[match_data['bowler'] == player][match_data['ball'] < 6.0][match_data['extras'] != 0]['extras'].sum() + match_data[match_data['bowler'] == player][match_data['ball'] < 6.0][match_data['runs_scored'] != 0]['runs_scored'].sum()

                        runs_given_middle = match_data[match_data['bowler'] == player][match_data['ball'] >= 6.0][match_data['ball'] < 15.0][match_data['extras'] != 0]['extras'].sum() + match_data[match_data['bowler'] == player][match_data['ball'] >= 6.0][match_data['ball'] < 15.0][match_data['runs_scored'] != 0]['runs_scored'].sum()

                        temp['runs_given_15'] = runs_given_15

                        temp['runs_given_middle'] = runs_given_middle

                        temp['runs_given_6'] = runs_given_6

                        temp['boundaries_last_5'] = [len(match_data[match_data['batsman_on_strike'] == player][match_data['ball'] >= 15.0][match_data['runs_scored'] == 4].index) + len(match_data[match_data['batsman_on_strike'] == player][match_data['ball'] >= 15.0][match_data['runs_scored'] == 6].index)]

                        temp['boundaries_first_6'] = [len(match_data[match_data['batsman_on_strike'] == player][match_data['ball'] < 6.0][match_data['runs_scored'] == 4].index) + len(match_data[match_data['batsman_on_strike'] == player][match_data['ball'] < 6.0][match_data['runs_scored'] == 6].index)]

                        temp['economy_first_6'] = [round(runs_given_6 * 6/ balls_bowled_6,2) ] 

                        temp['economy_last_5'] = [round(runs_given_15 * 6 / balls_bowled_15,2)]

                        temp['economy_middle'] = [round(runs_given_middle * 6 / balls_bowled_middle,2)]

                        temp['wickets_first_6'] = [len(match_data[match_data['bowler'] == player][match_data['ball'] < 6.0][match_data['way_out'] != 0.0][match_data['way_out'] != "run out"].index)]

                        temp['wickets_last_5'] = [len(match_data[match_data['bowler'] == player][match_data['ball'] >= 15.0][match_data['way_out'] != 0.0][match_data['way_out'] != "run out"].index)]

                        player_list = pd.concat([player_list,temp],ignore_index=True,axis=0)             


                    elif (player in player_list['player_name'].unique() and str(season) in season_player):
                        
                        #print("2nd condition")

                        player_list.loc[(player_list['player_name'] == player) & (player_list['season'] == str(season)),'runs_scored'] = player_list[player_list['player_name'] == player][player_list['season'] == str(season)]['runs_scored'].values[0] + match_data[match_data['batsman_on_strike'] == player]['runs_scored'].sum()

                        player_list.loc[(player_list['player_name'] == player) & (player_list['season'] == str(season)),'ball_faced'] = player_list[player_list['player_name'] == player][player_list['season'] == str(season)]['ball_faced'].values[0] + len(match_data[match_data['batsman_on_strike'] == player].index)

                        player_list.loc[(player_list['player_name'] == player) & (player_list['season'] == str(season)),'4s'] = player_list[player_list['player_name'] == player][player_list['season'] == str(season)]['4s'].values[0] + len(match_data[match_data['batsman_on_strike'] == player][match_data['runs_scored'] == 4].index)

                        player_list.loc[(player_list['player_name'] == player) & (player_list['season'] == str(season)),'6s'] = player_list[player_list['player_name'] == player][player_list['season'] == str(season)]['6s'].values[0] + len(match_data[match_data['batsman_on_strike'] == player][match_data['runs_scored'] == 6].index)

                        player_list.loc[(player_list['player_name'] == player) & (player_list['season'] == str(season)),'matches'] = player_list.loc[(player_list['player_name'] == player) & (player_list['season'] == str(season)),'matches'].values[0] + 1

                        player_list.loc[(player_list['player_name'] == player) & (player_list['season'] == str(season)),'2s'] = player_list[player_list['player_name'] == player][player_list['season'] == str(season)]['2s'].values[0] + len(match_data[match_data['batsman_on_strike'] == player][match_data['runs_scored'] == 2].index)

                        if len(match_data[match_data['batsman_out'] != 0.0]) > 0:
                            if len(match_data[match_data['batsman_out'] == player].index) == 0:
                                player_list.loc[(player_list['player_name'] == player) & (player_list['season'] == str(season)),'not_outs'] = player_list[player_list['player_name'] == player][player_list['season'] == str(season)]['not_outs'].values[0] + 1
                            elif len(match_data[match_data['batsman_out'] == player].index) == 1:
                                player_list.loc[(player_list['player_name'] == player) & (player_list['season'] == str(season)),'not_outs'] = player_list[player_list['player_name'] == player][player_list['season'] == str(season)]['not_outs'].values[0]

                        player_list.loc[(player_list['player_name'] == player) & (player_list['season'] == str(season)),'balls_bowled'] = player_list[player_list['player_name'] == player][player_list['season'] == str(season)]['balls_bowled'].values[0] + len(match_data[match_data['bowler'] == player].index) - len(match_data[match_data['bowler'] == player][match_data['extras'] != 0].index)

                        if len(match_data[match_data['way_out'] != 0.0]) > 0:
                            player_list.loc[(player_list['player_name'] == player) & (player_list['season'] == str(season)),'wickets_taken'] = player_list[player_list['player_name'] == player][player_list['season'] == str(season)]['wickets_taken'].values[0] + len(match_data[match_data['bowler'] == player][match_data['way_out'] != 0.0][match_data['way_out'] != "run out"].index)

                        #balls_bowled_15_old = player_list[player_list['player_name'] == player][player_list['balls_bowled_15'] != 0]['balls_bowled_15'].values[0]

                        #balls_bowled_6_old = player_list[player_list['player_name'] == player][player_list['balls_bowled_6'] != 0]['balls_bowled_6'].values[0]

                        player_list.loc[(player_list['player_name'] == player) & (player_list['season'] == str(season)),'balls_bowled_15'] = player_list[player_list['player_name'] == player][player_list['season'] == str(season)]['balls_bowled_15'].values[0] + len(match_data[match_data['bowler'] == player][match_data['ball'] >= 15.0].index) - len(match_data[match_data['bowler'] == player][match_data['ball'] >= 15.0][match_data['extras'] != 0].index)

                        player_list.loc[(player_list['player_name'] == player) & (player_list['season'] == str(season)),'balls_bowled_6'] = player_list[player_list['player_name'] == player][player_list['season'] == str(season)]['balls_bowled_6'].values[0] + len(match_data[match_data['bowler'] == player][match_data['ball'] < 6.0].index) - len(match_data[match_data['bowler'] == player][match_data['ball'] < 6.0][match_data['extras'] != 0].index)

                        player_list.loc[(player_list['player_name'] == player) & (player_list['season'] == str(season)),'balls_bowled_middle'] = player_list[player_list['player_name'] == player][player_list['season'] == str(season)]['balls_bowled_middle'].values[0] + len(match_data[match_data['bowler'] == player][match_data['ball'] >= 6.0][match_data['ball'] < 15.0].index) - len(match_data[match_data['bowler'] == player][match_data['ball'] >= 6.0][match_data['ball'] < 15.0][match_data['extras'] != 0].index)

                        player_list.loc[(player_list['player_name'] == player) & (player_list['season'] == str(season)),'extras_given'] = player_list[player_list['player_name'] == player][player_list['season'] == str(season)]['extras_given'].values[0] + len(match_data[match_data['bowler'] == player][match_data['extras'] != 0].index)

                        player_list.loc[(player_list['player_name'] == player) & (player_list['season'] == str(season)),'runs_given'] = player_list[player_list['player_name'] == player][player_list['season'] == str(season)]['runs_given'].values[0] + match_data[match_data['bowler'] == player][match_data['extras'] != 0]['extras'].sum() + match_data[match_data['bowler'] == player][match_data['runs_scored'] != 0]['runs_scored'].sum()

                        player_list.loc[(player_list['player_name'] == player) & (player_list['season'] == str(season)),'boundaries_given'] = player_list[player_list['player_name'] == player][player_list['season'] == str(season)]['boundaries_given'].values[0] + len(match_data[match_data['bowler'] == player][match_data['runs_scored'] == 4].index) + len(match_data[match_data['bowler'] == player][match_data['runs_scored'] == 6].index)

                        player_list.loc[(player_list['player_name'] == player) & (player_list['season'] == str(season)),'runs_last_5'] = player_list[player_list['player_name'] == player][player_list['season'] == str(season)]['runs_last_5'].values[0] + match_data[match_data['batsman_on_strike'] == player][match_data['ball']>=15.0]['runs_scored'].sum()

                        player_list.loc[(player_list['player_name'] == player) & (player_list['season'] == str(season)),'runs_middle'] = player_list[player_list['player_name'] == player][player_list['season'] == str(season)]['runs_middle'].values[0] + match_data[match_data['batsman_on_strike'] == player][match_data['ball']<15.0][match_data['ball']>=6.0]['runs_scored'].sum()

                        player_list.loc[(player_list['player_name'] == player) & (player_list['season'] == str(season)),'runs_first_6'] = player_list[player_list['player_name'] == player][player_list['season'] == str(season)]['runs_first_6'].values[0] + match_data[match_data['batsman_on_strike'] == player][match_data['ball'] < 6.0]['runs_scored'].sum()

                        player_list.loc[(player_list['player_name'] == player) & (player_list['season'] == str(season)),'boundaries_last_5'] = player_list[player_list['player_name'] == player][player_list['season'] == str(season)]['boundaries_last_5'].values[0] +len(match_data[match_data['batsman_on_strike'] == player][match_data['ball'] > 15.0][match_data['runs_scored'] == 4].index) + len(match_data[match_data['batsman_on_strike'] == player][match_data['ball'] > 15.0][match_data['runs_scored'] == 6].index)

                        player_list.loc[(player_list['player_name'] == player) & (player_list['season'] == str(season)),'boundaries_first_6'] = player_list[player_list['player_name'] == player][player_list['season'] == str(season)]['boundaries_first_6'].values[0] +len(match_data[match_data['batsman_on_strike'] == player][match_data['ball'] < 6.0][match_data['runs_scored'] == 4].index) + len(match_data[match_data['batsman_on_strike'] == player][match_data['ball'] < 6.0][match_data['runs_scored'] == 6].index)

                        player_list.loc[(player_list['player_name'] == player) & (player_list['season'] == str(season)),'runs_given_6'] = player_list[player_list['player_name'] == player][player_list['season'] == str(season)]['runs_given_6'].values[0] + match_data[match_data['bowler'] == player][match_data['ball'] < 6.0][match_data['extras'] != 0]['extras'].sum() + match_data[match_data['bowler'] == player][match_data['ball'] < 6.0][match_data['runs_scored'] != 0]['runs_scored'].sum()

                        player_list.loc[(player_list['player_name'] == player) & (player_list['season'] == str(season)),'runs_given_middle'] = player_list[player_list['player_name'] == player][player_list['season'] == str(season)]['runs_given_middle'].values[0] + match_data[match_data['bowler'] == player][match_data['ball'] >= 6.0][match_data['ball'] < 15.0][match_data['extras'] != 0]['extras'].sum() + match_data[match_data['bowler'] == player][match_data['ball'] >= 6.0][match_data['ball'] < 15.0][match_data['runs_scored'] != 0]['runs_scored'].sum()

                        player_list.loc[(player_list['player_name'] == player) & (player_list['season'] == str(season)),'runs_given_15'] = player_list[player_list['player_name'] == player][player_list['season'] == str(season)]['runs_given_15'].values[0] + match_data[match_data['bowler'] == player][match_data['ball'] >= 15.0][match_data['extras'] != 0]['extras'].sum() + match_data[match_data['bowler'] == player][match_data['ball'] >= 15.0][match_data['runs_scored'] != 0]['runs_scored'].sum()

                        if len(player_list[player_list['player_name'] == player][player_list['season'] == str(season)]['balls_bowled_6'].index) > 0 and len(player_list[player_list['player_name'] == player][player_list['season'] == str(season)]['runs_given_6'].index) > 0:
                            player_list.loc[(player_list['player_name'] == player) & (player_list['season'] == str(season)),'economy_first_6'] = round(player_list[player_list['player_name'] == player][player_list['season'] == str(season)]['runs_given_6'].values[0] * 6 / player_list[player_list['player_name'] == player][player_list['season'] == str(season)]['balls_bowled_6'].values[0],2)

                        if len(player_list[player_list['player_name'] == player][player_list['season'] == str(season)]['balls_bowled_15'].index) > 0 and len(player_list[player_list['player_name'] == player][player_list['season'] == str(season)]['runs_given_15'].index) > 0:
                            player_list.loc[(player_list['player_name'] == player) & (player_list['season'] == str(season)),'economy_last_5'] = round(player_list[player_list['player_name'] == player][player_list['season'] == str(season)]['runs_given_15'].values[0] * 6 / player_list[player_list['player_name'] == player][player_list['season'] == str(season)]['balls_bowled_15'].values[0],2)

                        if len(player_list[player_list['player_name'] == player][player_list['season'] == str(season)]['balls_bowled_middle'].index) > 0 and len(player_list[player_list['player_name'] == player][player_list['season'] == str(season)]['runs_given_middle'].index) > 0:
                            player_list.loc[(player_list['player_name'] == player) & (player_list['season'] == str(season)),'economy_middle'] = round(player_list[player_list['player_name'] == player][player_list['season'] == str(season)]['runs_given_middle'].values[0] * 6 / player_list[player_list['player_name'] == player][player_list['season'] == str(season)]['balls_bowled_middle'].values[0],2)

                        player_list.loc[(player_list['player_name'] == player) & (player_list['season'] == str(season)),'wickets_first_6'] = player_list[player_list['player_name'] == player][player_list['season'] == str(season)]['wickets_first_6'].values[0] +len(match_data[match_data['bowler'] == player][match_data['ball'] < 6.0][match_data['way_out'] != 0.0][match_data['way_out'] != "run out"].index)

                        player_list.loc[(player_list['player_name'] == player) & (player_list['season'] == str(season)),'wickets_last_5'] = player_list[player_list['player_name'] == player][player_list['season'] == str(season)]['wickets_last_5'].values[0] +len(match_data[match_data['bowler'] == player][match_data['ball'] >= 15.0][match_data['way_out'] != 0.0][match_data['way_out'] != "run out"].index)
                    #print(player_list)
    return player_list


# In[44]:


match_information = pd.read_csv('/home/griffonuser/DS_Practise/Capstone/match_information.csv')
import warnings
warnings.filterwarnings("ignore")
season_wise_player_stats_list = current_player_season_wise(match_information,data_path)


# In[ ]:


points = []
for idx in season_wise_player_stats_list.index:
    if season_wise_player_stats_list['player_name'][idx] in ipl_player_points['player_ipl_name'].unique():
        temp = ipl_player_points[ipl_player_points['player_ipl_name'] == season_wise_player_stats_list['player_name'][idx]][season_wise_player_stats_list['season'][idx]].values[0]
        points.append(temp)
    else:
        points.append(0)


# In[ ]:


season_wise_player_stats_list['season_points'] = points
if '' in season_wise_player_stats_list.columns:
    season_wise_player_stats_list =  season_wise_player_stats_list.drop(columns = [''])
season_wise_player_stats_list.to_csv("season_wise_player_stats_list.csv", index = False)


# ## Training and Test Set
# 
# ## Training Set: 2008 - 2018 Data
# 
# ## Testing Set: 2019 Data

# In[375]:


season_wise_player_stats_list = pd.read_csv('season_wise_player_stats_list.csv')
training_data = season_wise_player_stats_list[season_wise_player_stats_list['season'] != 2019][season_wise_player_stats_list['season_points'] != 0 ].fillna(0)
testing_data = season_wise_player_stats_list[season_wise_player_stats_list['season'] == 2019].fillna(0)


# In[302]:


training_data = training_data.loc[:,~training_data.columns.isin(['ball_faced','balls_bowled','runs_given_15', 'runs_given_6', 'runs_given_middle','runs_given','balls_bowled_15','balls_bowled_6','balls_bowled_middle','player_name'])].replace(np.inf, np.NaN).fillna(0)
testing_data = testing_data.loc[:,~testing_data.columns.isin(['ball_faced','balls_bowled','runs_given_15', 'runs_given_6', 'runs_given_middle','runs_given','balls_bowled_15','balls_bowled_6','balls_bowled_middle','player_name'])].replace(np.inf, np.NaN).fillna(0)
print(training_data.columns)
from sklearn.decomposition import PCA
pca = PCA()

pca.fit(training_data)
print(pca.explained_variance_ratio_)


# In[432]:


training_data = training_data.loc[:,~training_data.columns.isin(['df_index','ball_faced','balls_bowled','runs_given_15', 'runs_given_6', 'runs_given_middle','runs_given','balls_bowled_15','balls_bowled_6','balls_bowled_middle','player_name'])].replace(np.inf,np.NaN).fillna(0)
testing_data = testing_data.loc[:,~testing_data.columns.isin(['df_index','ball_faced','balls_bowled','runs_given_15', 'runs_given_6', 'runs_given_middle','runs_given','balls_bowled_15','balls_bowled_6','balls_bowled_middle','player_name'])].replace(np.inf,np.NaN).fillna(0)
testing_data = testing_data[testing_data["season_points"] != 0]
X_train = training_data.loc[:,~training_data.columns.isin(['season_points','season'])]
y_train = training_data.loc[:,training_data.columns.isin(['season_points'])]
X_test = testing_data.loc[:,~testing_data.columns.isin(['season_points','season'])]
y_test = testing_data.loc[:,testing_data.columns.isin(['season_points'])]

print(X_test.shape)


# In[376]:


import pandas_profiling
pandas_profiling.ProfileReport(training_data)


# In[433]:


from sklearn.linear_model import LinearRegression

reg = LinearRegression().fit(X_train, y_train)


# In[434]:


reg.score(X_train, y_train)


# In[435]:


reg.coef_


# In[436]:


training_data.to_csv('/home/griffonuser/DS_Practise/Capstone/training_data.csv')
testing_data.to_csv('/home/griffonuser/DS_Practise/Capstone/testing_data.csv')


# In[437]:


from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import StratifiedKFold
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import MinMaxScaler


# In[438]:


imputer = SimpleImputer(strategy='median')
# Train on the training features
imputer.fit(X_train)
# Transform both training data and testing data
X_train_i = imputer.transform(X_train)
X_test_i = imputer.transform(X_test)


# In[439]:


scaler = MinMaxScaler(feature_range=(0,1))
scaler.fit(X_train_i)
scale = MinMaxScaler(feature_range=(0,1))
X_train_s = scaler.transform(X_train_i)
X_test_s = scaler.transform(X_test_i)
scale.fit(y_train)
y_train_s = scale.transform(y_train)
y_test_s = scale.transform(y_test)


# In[517]:


X_train_i.shape


# In[411]:


len(X_train) + len(X_test)


# ## Gradient Boosted Classifier

# In[516]:


import matplotlib.pyplot as plt

#from sklearn import *

from sklearn.ensemble import RandomForestRegressor,GradientBoostingRegressor,VotingRegressor,AdaBoostRegressor
from sklearn.linear_model import LinearRegression
from sklearn.svm import SVR

from sklearn.model_selection import cross_val_score



# Training classifiers
reg1 = GradientBoostingRegressor(random_state=1, n_estimators=10)
reg2 = RandomForestRegressor(random_state=1, n_estimators=10)
reg3 = LinearRegression()
regr = AdaBoostRegressor(random_state=0, n_estimators=100)
ereg = VotingRegressor([('gb', reg1), ('rf', reg2), ('lr', reg3),('ada', regr)])

reg1.fit(X_train_i, y_train)
reg2.fit(X_train_i, y_train)
reg3.fit(X_train_i, y_train)
regr.fit(X_train_i, y_train)
ereg.fit(X_train_i, y_train)

xt = X_test_i[:40]

plt.figure(figsize=(10, 10))
           
plt.plot(reg1.predict(xt), 'gd', label='GradientBoostingRegressor')
plt.plot(reg2.predict(xt), 'b^', label='RandomForestRegressor')
plt.plot(reg3.predict(xt), 'ys', label='LinearRegression')
plt.plot(regr.predict(xt), 'y*', label='Adaboost')
plt.plot(ereg.predict(xt), 'r*', label='VotingRegressor')
plt.tick_params(axis='x', which='both', bottom=False, top=False,
                labelbottom=False)
plt.ylabel('predicted')
plt.xlabel('training samples')
plt.legend(loc="best")
plt.title('Comparison of individual predictions with averaged')
plt.show()


# In[413]:


print("Gradient Boosted Reg Training R2:",metrics.r2_score(y_train,reg1.predict(X_train_i)))
print("RandomForestRegressor Training R2:",metrics.r2_score(y_train,reg2.predict(X_train_i)))
print("LinearRegression Training R2:",metrics.r2_score(y_train,reg3.predict(X_train_i)))
print("AdaboostRegressor Training R2:",metrics.r2_score(y_train,regr.predict(X_train_i)))
print("VotingRegressor Training R2:",metrics.r2_score(y_train,ereg.predict(X_train_i)))


# In[414]:


print("Gradient Boosted Reg Testing R2:",metrics.r2_score(y_test,reg1.predict(X_test_i)))
print("RandomForestRegressor Testing R2:",metrics.r2_score(y_test,reg2.predict(X_test_i)))
print("LinearRegression Testing R2:",metrics.r2_score(y_test,reg3.predict(X_test_i)))
print("AdaboostRegressor Testing R2:",metrics.r2_score(y_test,regr.predict(X_test_i)))
print("VotingRegressor Testing R2:",metrics.r2_score(y_test,ereg.predict(X_test_i)))


# In[415]:


print("Gradient Boosted Reg Training mean_squared_error:",metrics.mean_squared_error(y_train,reg1.predict(X_train_i)))
print("RandomForestRegressor Training mean_squared_error:",metrics.mean_squared_error(y_train,reg2.predict(X_train_i)))
print("LinearRegression Training mean_squared_error:",metrics.mean_squared_error(y_train,reg3.predict(X_train_i)))
print("AdaboostRegression Training mean_squared_error:",metrics.mean_squared_error(y_train,regr.predict(X_train_i)))
print("VotingRegressor Training mean_squared_error:",metrics.mean_squared_error(y_train,ereg.predict(X_train_i)))
print("Gradient Boosted Reg Testing mean_squared_error:",metrics.mean_squared_error(y_test,reg1.predict(X_test_i)))
print("RandomForestRegressor Testing mean_squared_error:",metrics.mean_squared_error(y_test,reg2.predict(X_test_i)))
print("LinearRegression Testing mean_squared_error:",metrics.mean_squared_error(y_test,reg3.predict(X_test_i)))
print("AdaboostRegression Testing mean_squared_error:",metrics.mean_squared_error(y_test,regr.predict(X_test_i)))
print("VotingRegressor Testing mean_squared_error:",metrics.mean_squared_error(y_test,ereg.predict(X_test_i)))


# In[416]:


print("Gradient Boosted Reg Training mean_absolute_error:",metrics.mean_absolute_error(y_train,reg1.predict(X_train_i)))
print("RandomForestRegressor Training mean_absolute_error:",metrics.mean_absolute_error(y_train,reg2.predict(X_train_i)))
print("LinearRegression Training mean_absolute_error:",metrics.mean_absolute_error(y_train,reg3.predict(X_train_i)))
print("AdaboostRegression Training mean_absolute_error:",metrics.mean_absolute_error(y_train,regr.predict(X_train_i)))
print("VotingRegressor Training mean_absolute_error:",metrics.mean_absolute_error(y_train,ereg.predict(X_train_i)))
print("Gradient Boosted Reg Testing mean_absolute_error:",metrics.mean_absolute_error(y_test,reg1.predict(X_test_i)))
print("RandomForestRegressor Testing mean_absolute_error:",metrics.mean_absolute_error(y_test,reg2.predict(X_test_i)))
print("LinearRegression Testing mean_absolute_error:",metrics.mean_absolute_error(y_test,reg3.predict(X_test_i)))
print("AdaboostRegression Testing mean_absolute_error:",metrics.mean_absolute_error(y_test,regr.predict(X_test_i)))
print("VotingRegressor Testing mean_absolute_error:",metrics.mean_absolute_error(y_test,ereg.predict(X_test_i)))


# In[417]:


print("Gradient Boosted Reg Training r2_score:",metrics.r2_score(y_train,reg1.predict(X_train_i)))
print("RandomForestRegressor Training r2_score:",metrics.r2_score(y_train,reg2.predict(X_train_i)))
print("LinearRegression Training r2_score:",metrics.r2_score(y_train,reg3.predict(X_train_i)))
print("AdaboostRegression Training r2_score:",metrics.r2_score(y_train,regr.predict(X_train_i)))
print("VotingRegressor Training r2_score:",metrics.r2_score(y_train,ereg.predict(X_train_i)))
print("Gradient Boosted Reg Testing r2_score:",metrics.r2_score(y_test,reg1.predict(X_test_i)))
print("RandomForestRegressor Testing r2_score:",metrics.r2_score(y_test,reg2.predict(X_test_i)))
print("LinearRegression Testing r2_score:",metrics.r2_score(y_test,reg3.predict(X_test_i)))
print("AdaboostRegression Testing r2_score:",metrics.r2_score(y_test,regr.predict(X_test_i)))
print("VotingRegressor Testing r2_score:",metrics.r2_score(y_test,ereg.predict(X_test_i)))


# In[418]:


print("Gradient Boosted Reg Training explained_variance_score:",metrics.explained_variance_score(y_train,reg1.predict(X_train_i)))
print("RandomForestRegressor Training explained_variance_score:",metrics.explained_variance_score(y_train,reg2.predict(X_train_i)))
print("LinearRegression Training explained_variance_score:",metrics.explained_variance_score(y_train,reg3.predict(X_train_i)))
print("AdaboostRegression Training explained_variance_score:",metrics.explained_variance_score(y_train,regr.predict(X_train_i)))
print("VotingRegressor Training explained_variance_score:",metrics.explained_variance_score(y_train,ereg.predict(X_train_i)))
print("Gradient Boosted Reg Testing explained_variance_score:",metrics.explained_variance_score(y_test,reg1.predict(X_test_i)))
print("RandomForestRegressor Testing explained_variance_score:",metrics.explained_variance_score(y_test,reg2.predict(X_test_i)))
print("LinearRegression Testing explained_variance_score:",metrics.explained_variance_score(y_test,reg3.predict(X_test_i)))
print("AdaboostRegression Testing explained_variance_score:",metrics.explained_variance_score(y_test,regr.predict(X_test_i)))
print("VotingRegressor Testing explained_variance_score:",metrics.explained_variance_score(y_test,ereg.predict(X_test_i)))


# ## Cross Validation of Generated Models

# In[419]:


from sklearn.model_selection import cross_validate

scores = cross_validate(reg1, X_train_i, y_train, cv=5,scoring=('r2', 'neg_mean_squared_error','neg_mean_absolute_error'),return_train_score=True)
print("Testing Mean Squared Error Gradient Boosted : ",scores['test_neg_mean_squared_error'],"\nTesting Mean Absolute Error Gradient Boosted : ",scores['test_neg_mean_absolute_error'],"\nTesting R2 Gradient Boosted : ",scores['test_r2'])
print("\nTraining Mean Squared Error Gradient Boosted : ",scores['train_neg_mean_squared_error'],"\nTraining Mean Absolute Error Gradient Boosted : ",scores['train_neg_mean_absolute_error'],"\nTraining R2 Gradient Boosted : ",scores['train_r2'])


# In[420]:


scores = cross_validate(reg2, X_train_i, y_train, cv=5,scoring=('r2', 'neg_mean_squared_error','neg_mean_absolute_error'),return_train_score=True)
print("Testing Mean Squared Error RandomForestRegressor: ",scores['test_neg_mean_squared_error'],"\nTesting Mean Absolute Error RandomForestRegressor: ",scores['test_neg_mean_absolute_error'],"\nTesting R2 RandomForestRegressor: ",scores['test_r2'])
print("\nTraining Mean Squared Error RandomForestRegressor: ",scores['train_neg_mean_squared_error'],"\nTraining Mean Absolute Error RandomForestRegressor: ",scores['train_neg_mean_absolute_error'],"\nTraining R2 RandomForestRegressor: ",scores['train_r2'])


# In[421]:


scores = cross_validate(reg3, X_train_i, y_train, cv=5,scoring=('r2', 'neg_mean_squared_error','neg_mean_absolute_error'),return_train_score=True)
print("Testing Mean Squared Error LinearRegression: ",scores['test_neg_mean_squared_error'],"\nTesting Mean Absolute Error LinearRegression: ",scores['test_neg_mean_absolute_error'],"\nTesting R2 LinearRegression: ",scores['test_r2'])
print("\nTraining Mean Squared Error LinearRegression: ",scores['train_neg_mean_squared_error'],"\nTraining Mean Absolute Error LinearRegression: ",scores['train_neg_mean_absolute_error'],"\nTraining R2 LinearRegression: ",scores['train_r2'])


# In[527]:


y_lin_train = reg3.predict(X_train_i)
fig, ax = plt.subplots()
ax.scatter(y_train, y_lin_train)
ax.plot([y_train.min(), y_train.max()], [y_train.min(), y_train.max()], 'k--', lw=4)
ax.set_xlabel('Measured')
ax.set_ylabel('Predicted')
plt.title("train predicted vs true")
plt.show()

y_lin_test = reg3.predict(X_test_i)
fig, ax = plt.subplots()
ax.scatter(y_test, y_lin_test)
ax.plot([y_train.min(), y_train.max()], [y_train.min(), y_train.max()], 'k--', lw=4)
ax.set_xlabel('Measured')
ax.set_ylabel('Predicted')
plt.title("test predicted vs true")
plt.show()


# In[423]:


scores = cross_validate(regr, X_train_i, y_train, cv=5,scoring=('r2', 'neg_mean_squared_error','neg_mean_absolute_error'),return_train_score=True)
print("Testing Mean Squared Error AdaboostRegression: ",scores['test_neg_mean_squared_error'],"\nTesting Mean Absolute Error AdaboostRegression: ",scores['test_neg_mean_absolute_error'],"\nTesting R2 AdaboostRegression: ",scores['test_r2'])
print("\nTraining Mean Squared Error AdaboostRegression: ",scores['train_neg_mean_squared_error'],"\nTraining Mean Absolute Error AdaboostRegression: ",scores['train_neg_mean_absolute_error'],"\nTraining R2 AdaboostRegression: ",scores['train_r2'])


# In[424]:


scores = cross_validate(ereg, X_train_i, y_train, cv=5,scoring=('r2', 'neg_mean_squared_error','neg_mean_absolute_error'),return_train_score=True)
print("Testing Mean Squared Error VotingRegressor: ",scores['test_neg_mean_squared_error'],"\nTesting Mean Absolute Error VotingRegressor: ",scores['test_neg_mean_absolute_error'],"\nTesting R2 VotingRegressor: ",scores['test_r2'])
print("\nTraining Mean Squared Error VotingRegressor: ",scores['train_neg_mean_squared_error'],"\nTraining Mean Absolute Error VotingRegressor: ",scores['train_neg_mean_absolute_error'],"\nTraining R2 VotingRegressor: ",scores['train_r2'])


# In[425]:


X_train_i.shape


# ## Deep Learning Regression

# In[332]:


import pandas
from keras.models import Sequential
from keras.layers import Dense
from keras.wrappers.scikit_learn import KerasRegressor
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline


# In[333]:


from keras import backend as K
import importlib
def set_keras_backend(backend):

    if K.backend() != backend:
        os.environ['KERAS_BACKEND'] = backend
        importlib.reload(K)
        assert K.backend() == backend

set_keras_backend("theano")

def coeff_determination(y_true, y_pred):
    #r2 = sklearn.metrics.r2(y_true, y_pred)
    from keras import backend as K
    SS_res =  K.sum(K.square( y_true-y_pred ))
    SS_tot = K.sum(K.square( y_true - K.mean(y_true) ) )
    return ( 1 - SS_res/(SS_tot + 1e-10))
    #return r2


# In[441]:


def baseline_model():
    # create model 
    model = Sequential()
    model.add(Dense(17, input_dim=19, kernel_initializer='normal', activation='relu'))
    model.add(Dense(1, kernel_initializer='normal'))
    # Compile model
    model.compile(loss='mean_squared_error', optimizer='adam',metrics=['mae','mse',coeff_determination])
    return model


# In[442]:


estimator_baseline = KerasRegressor(build_fn=baseline_model, epochs=100, batch_size=5, verbose=1)
kfold = KFold(n_splits=3)
results_baseline = cross_val_score(estimator, X_train_s, y_train, cv=kfold)
print("Results: %.2f (%.2f) MSE" % (results.mean(), results.std()))


# In[443]:


import seaborn as sns
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')

estimator_baseline.fit(X_train_s, y_train)
y_pred_train = estimator_baseline.predict(X_train_s)
fig, ax = plt.subplots()
ax.scatter(y_train, y_pred_train)
ax.plot([y_train.min(), y_train.max()], [y_train.min(), y_train.max()], 'k--', lw=4)
ax.set_xlabel('Measured')
ax.set_ylabel('Predicted')
plt.title("train predicted vs true")
plt.show()

y_pred_test = estimator_baseline.predict(X_test_s)
fig, ax = plt.subplots()
ax.scatter(y_test, y_pred_test)
ax.plot([y_train.min(), y_train.max()], [y_train.min(), y_train.max()], 'k--', lw=4)
ax.set_xlabel('Measured')
ax.set_ylabel('Predicted')
plt.title("test predicted vs true")
plt.show()


# In[444]:


from sklearn.metrics import r2_score
r2_score(y_test,pd.DataFrame(y_pred_test))


# In[445]:


estimators_pipeline_baseline = []
estimators_pipeline_baseline.append(('standardize', StandardScaler()))
estimators_pipeline_baseline.append(('mlp', KerasRegressor(build_fn=baseline_model, epochs=50, batch_size=5, verbose=1)))
pipeline_baseline = Pipeline(estimators_pipeline_baseline)
kfold = KFold(n_splits=3)
results_baseline = cross_val_score(pipeline_baseline, X_train_s, y_train, cv=kfold)
print("Results: %.2f (%.2f) MSE" % (results.mean(), results.std()))


# In[446]:


pipeline_baseline.fit(X_train_s, y_train)
y_pred_pipeline_baseline = pipeline_baseline.predict(X_train_s)
fig, ax = plt.subplots()
ax.scatter(y_train, y_pred_pipeline_baseline)
ax.plot([y_train.min(), y_train.max()], [y_train.min(), y_train.max()], 'k--', lw=4)
ax.set_xlabel('Measured')
ax.set_ylabel('Predicted')
plt.title("train predicted vs true for pipeline basline model")
plt.show()

y_pred_test_pipeline_baseline = pipeline_baseline.predict(X_test_s)
fig, ax = plt.subplots()
ax.scatter(y_test, y_pred_test_pipeline_baseline)
ax.plot([y_train.min(), y_train.max()], [y_train.min(), y_train.max()], 'k--', lw=4)
ax.set_xlabel('Measured')
ax.set_ylabel('Predicted')
plt.title("test predicted vs true for pipeline basline model")
plt.show()

print(r2_score(y_test,pd.DataFrame(y_pred_test_pipeline_baseline)))


# In[447]:


print(r2_score(y_train,pd.DataFrame(y_pred_pipeline_baseline)))


# In[448]:


def larger_model():
    # create model
    model = Sequential()
    model.add(Dense(19, input_dim=19, kernel_initializer='normal', activation='relu'))
    model.add(Dense(6, kernel_initializer='normal', activation='relu'))
    model.add(Dense(6, kernel_initializer='normal', activation='relu'))
    model.add(Dense(1, kernel_initializer='normal'))
    # Compile model
    model.compile(loss='mean_squared_error', optimizer='adam',metrics=['mae','mse',coeff_determination])
    return model


# In[449]:


estimators_larger= []
estimators_larger.append(('standardize', StandardScaler()))
estimators_larger.append(('mlp', KerasRegressor(build_fn=larger_model, epochs=50, batch_size=5, verbose=1)))
pipeline_larger = Pipeline(estimators_larger)
kfold = KFold(n_splits=3)
results = cross_val_score(pipeline_larger, X_train_s, y_train, cv=kfold)
print("Results Larger Model: %.2f (%.2f) MSE" % (results.mean(), results.std()))


# In[450]:


pipeline_larger.fit(X_train_s, y_train)
y_pred_pipeline_larger = pipeline_larger.predict(X_train_s)
fig, ax = plt.subplots()
ax.scatter(y_train, y_pred_pipeline_larger)
ax.plot([y_train.min(), y_train.max()], [y_train.min(), y_train.max()], 'k--', lw=4)
ax.set_xlabel('Measured')
ax.set_ylabel('Predicted')
plt.title("train predicted vs true for pipeline larger model")
plt.show()

y_pred_test_pipeline_larger = pipeline_larger.predict(X_test_s)
fig, ax = plt.subplots()
ax.scatter(y_test, y_pred_test_pipeline_larger)
ax.plot([y_train.min(), y_train.max()], [y_train.min(), y_train.max()], 'k--', lw=4)
ax.set_xlabel('Measured')
ax.set_ylabel('Predicted')
plt.title("test predicted vs true for pipeline larger model")
plt.show()

print(r2_score(y_test,pd.DataFrame(y_pred_test_pipeline_larger)))


# In[451]:


print(r2_score(y_train,pd.DataFrame(y_pred_pipeline_larger)))


# In[452]:


def wider_model():
    # create model
    model = Sequential()
    model.add(Dense(30, input_dim=19, kernel_initializer='normal', activation='relu'))
    model.add(Dense(1, kernel_initializer='normal'))
    # Compile model
    model.compile(loss='mean_squared_error', optimizer='adam',metrics=['mae','mse'])
    return model


# In[453]:


estimators_wider = []
estimators_wider.append(('standardize', StandardScaler()))
estimators_wider.append(('mlp', KerasRegressor(build_fn=wider_model, epochs=50, batch_size=1, verbose=1)))
pipeline_wider = Pipeline(estimators_wider)
kfold = KFold(n_splits=3)
results = cross_val_score(pipeline_wider, X_train_s, y_train, cv=kfold)
print("Results Wider Model: %.2f (%.2f) MSE" % (results.mean(), results.std()))


# In[454]:


pipeline_wider.fit(X_train_s, y_train)
y_pred_pipeline_wider = pipeline_wider.predict(X_train_s)
fig, ax = plt.subplots()
ax.scatter(y_train, y_pred_pipeline_wider)
ax.plot([y_train.min(), y_train.max()], [y_train.min(), y_train.max()], 'k--', lw=4)
ax.set_xlabel('Measured')
ax.set_ylabel('Predicted')
plt.title("train predicted vs true for pipeline wider model")
plt.show()

y_pred_test_pipeline_wider = pipeline_wider.predict(X_test_s)
fig, ax = plt.subplots()
ax.scatter(y_test, y_pred_test_pipeline_wider)
ax.plot([y_train.min(), y_train.max()], [y_train.min(), y_train.max()], 'k--', lw=4)
ax.set_xlabel('Measured')
ax.set_ylabel('Predicted')
plt.title("test predicted vs true for pipeline wider model")
plt.show()

print(r2_score(y_test,pd.DataFrame(y_pred_test_pipeline_wider)))


# In[455]:


print(r2_score(y_train,pd.DataFrame(y_pred_pipeline_wider)))


# In[456]:


print("Baseline Deep Learning Training r2_score:",r2_score(y_train,pd.DataFrame(y_pred_train)))
print("Baseline Deep Learning Testing r2_score:",r2_score(y_test,pd.DataFrame(y_pred_test)))
print("Baseline Deep Learning Pipelined Training r2_score:",r2_score(y_train,pd.DataFrame(y_pred_pipeline_baseline)))
print("Baseline Deep Learning Pipelined Testing r2_score:",r2_score(y_test,pd.DataFrame(y_pred_test_pipeline_baseline)))
print("Larger Deep Learning Pipelined Training r2_score:",r2_score(y_train,pd.DataFrame(y_pred_pipeline_larger)))
print("Larger Deep Learning Pipelined Testing r2_score:",r2_score(y_test,pd.DataFrame(y_pred_test_pipeline_larger)))
print("Wider Deep Learning Pipelined Training r2_score:",r2_score(y_train,pd.DataFrame(y_pred_pipeline_wider)))
print("Wider Deep Learning Pipelined Testing r2_score:",r2_score(y_test,pd.DataFrame(y_pred_test_pipeline_wider)))


# In[457]:


print("Baseline Deep Learning Training mean_squared_error:",mean_squared_error(y_train,pd.DataFrame(y_pred_train)))
print("Baseline Deep Learning Testing mean_squared_error:",mean_squared_error(y_test,pd.DataFrame(y_pred_test)))
print("Baseline Deep Learning Pipelined Training mean_squared_error:",mean_squared_error(y_train,pd.DataFrame(y_pred_pipeline_baseline)))
print("Baseline Deep Learning Pipelined Testing mean_squared_error:",mean_squared_error(y_test,pd.DataFrame(y_pred_test_pipeline_baseline)))
print("Larger Deep Learning Pipelined Training mean_squared_error:",mean_squared_error(y_train,pd.DataFrame(y_pred_pipeline_larger)))
print("Larger Deep Learning Pipelined Testing mean_squared_error:",mean_squared_error(y_test,pd.DataFrame(y_pred_test_pipeline_larger)))
print("Wider Deep Learning Pipelined Training mean_squared_error:",mean_squared_error(y_train,pd.DataFrame(y_pred_pipeline_wider)))
print("Wider Deep Learning Pipelined Testing mean_squared_error:",mean_squared_error(y_test,pd.DataFrame(y_pred_test_pipeline_wider)))


# ## Best Model performance is from Linear Regressor model with R2 value of 0.85 for test set.
# 
# ## The Best Model and requirements are pickled and saved for deployment

# In[620]:


import pickle
filename = '/home/griffonuser/DS_Practise/Capstone/finalized_model_deep_learning.pkl'
pickle.dump(pipeline_wider, open(filename, 'wb'))


# In[621]:


model = pickle.load(open('/home/griffonuser/DS_Practise/Capstone/finalized_model_deep_learning.pkl','rb'))


# In[519]:


filename1 = '/home/griffonuser/DS_Practise/Capstone/finalized_model.pkl'
pickle.dump(reg3, open(filename1, 'wb'))


# In[520]:


model1 = pickle.load(open('/home/griffonuser/DS_Practise/Capstone/finalized_model.pkl','rb'))


# In[626]:


filename_standard_scaler = '/home/griffonuser/DS_Practise/Capstone/scaler_model.pkl'
pickle.dump(scale,open(filename_standard_scaler,'wb'))

