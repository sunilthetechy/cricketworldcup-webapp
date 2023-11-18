#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

def convert_to_int(x):
    try:
        return int(float(x))
    except (ValueError, TypeError):
        return 0

df=pd.read_csv('cwc_cleaned_data.csv')


#TROPHY WINNERS

trophies=df.groupby('YEAR')['TROPHY WINNER'].agg(lambda x: x.mode().iloc[0]).to_dict()
x=list(trophies.keys())
y=list(trophies.values())
plt.figure(figsize=(9,6))
sns.countplot(y,palette='muted')
plt.xlabel('TEAMS')
plt.ylabel('Number of Trophies')
plt.title('World Cup Trophy Winners 1975 - 2019')
plt.show()



#TOTAL MATCHES WON
matches_won={}
teams=list(df['TEAM'].unique())
for team in teams:
    matches_won_count=len(df[(df['TEAM']==team) & (df['RESULT']=='WON')])
    print(f'{team} - {matches_won_count}')
    matches_won[team]=matches_won_count
t=list(matches_won.keys())
w=list(matches_won.values())
plt.figure(figsize=(12,6))
sns.barplot(t,w,palette='muted')
for i in range(len(t)):
    plt.text(i, w[i], str(w[i]), ha='center')
plt.xlabel('TEAMS')
plt.ylabel('Number of Matches Won')
plt.title('Matches Won by a Team in CWC')
custom_legend = {
    'AUS': 'Australia',
    'ENG': 'England',
    'IND': 'India',
    'PAK': 'Pakistan',
    'SL': 'Sri Lanka',
    'WI': 'West Indies',
    'EA': 'East Africa',
    'NZ': 'New Zealand',
    'CAN': 'Canada',
    'ZIM': 'Zimbabwe',
    'SA': 'South Africa',
    'UAE': 'United Arab Emirates',
    'NED': 'Netherlands',
    'KEN': 'Kenya',
    'SCO': 'Scotland',
    'BAN': 'Bangladesh',
    'NAM': 'Namibia',
    'BER': 'Bermuda',
    'IRE': 'Ireland',
    'AFG': 'Afghanistan',
} 
plt.xticks(rotation=45)
plt.show()




#TOTAL RUNS SCORED

total_sum=0
def total_runs(x):
    global total_sum 
    try:
        total_sum += int(x) 
    except ValueError as e:
        pass
team_runs = df.groupby('TEAM')['RUNS SCORED'].sum().to_dict()

x=list(team_runs.keys())
y=list(team_runs.values())
plt.figure(figsize=(10,8))
sns.barplot(x,y,palette='muted')
for i in range(len(x)):
    plt.text(i, y[i], str(y[i]), ha='center')
plt.xlabel('TEAMS')
plt.ylabel('TOTAL RUN SCORED')
plt.title('TOTAL RUNS SCORED BY A TEAM IN CWC 1975-2019')
plt.xticks(rotation=45)
plt.show()


# In[92]:

#MATCHES PLAYED
matches_played=dict(df['TEAM'].value_counts())
x=list(matches_played.keys())
y=list(matches_played.values())
plt.figure(figsize=(10,8))
sns.barplot(x,y,palette='muted')
for i in range(len(x)):
    plt.text(i, y[i], str(y[i]), ha='center')
plt.xlabel('TEAMS')
plt.ylabel('MATCHES PLAYED')
plt.title('TOTAL MATCHES PLAYED BY A TEAM IN CWC 1975-2019')
plt.xticks(rotation=45)
plt.show()




team='IND'


#RUNS SCORED BY A TEAM

df_team=df[df['TEAM']==team]
team_runs_year=df_team.groupby('YEAR')['RUNS SCORED'].sum().to_dict()
x=list(team_runs_year.keys())
y=list(team_runs_year.values())
x,y
plt.figure(figsize=(9,7))
sns.barplot(x,y,palette='muted')
for i in range(len(x)):
    plt.text(i, y[i], str(y[i]), ha='center')
plt.xlabel('YEARS')
plt.ylabel(f'RUNS SCORED BY {team}')
plt.title(f'RUNS SCORED BY {team} FROM 1975-2019')
plt.xticks(rotation=45)
plt.show()




#MATCHES PLAYED VS WON
matches_played=df_team.groupby('YEAR')['TEAM'].count()
matches_played=dict(matches_played)
matches_won={}
res = df_team.groupby('YEAR')['RESULT']
for i,j in res:
    matches_won[i]=len(j[j=='WON'])

x1=list(matches_won.keys())
y1=list(matches_won.values())
x2=list(matches_played.keys())
y2=list(matches_played.values())

years = list(matches_won.keys())
won_counts = list(matches_won.values())
played_counts = list(matches_played.values())
bar_width = 0.35

x = range(len(years))

fig, ax = plt.subplots(figsize=(10, 6))

bar1 = ax.bar(x, won_counts, width=bar_width, label='Matches Won', align='center',color='green')
bar2 = ax.bar([i + bar_width for i in x], played_counts, width=bar_width, label='Matches Played', align='center',color='orange')

ax.set_xlabel('Year')
ax.set_ylabel('Number of Matches')
ax.set_title('Matches Won vs. Matches Played by Year')

ax.set_xticks([i + bar_width / 2 for i in x])
ax.set_xticklabels(years)

ax.legend()

for i, v in enumerate(won_counts):
    ax.text(i, v, str(v), ha='center', va='bottom')
for i, v in enumerate(played_counts):
    ax.text(i + bar_width, v, str(v), ha='center', va='bottom')

plt.tight_layout()
plt.show()



#WICKETS TAKEN BY A TEAM

wickets=df_team.groupby('YEAR')['WICKETS TAKEN'].sum().to_dict()
wickets
matches_played=df_team.groupby('YEAR')['TEAM'].count().to_dict()
matches_played
x=list(wickets.values())
y=list(wickets.keys())
plt.figure(figsize=(10,6))
sns.barplot(y,x,palette='muted')
for i in range(len(y)):
    plt.text(i, x[i], str(x[i]), ha='center')
plt.xlabel('YEARS')
plt.ylabel('WICKETS TAKEN')
plt.title(f'WICKETS TAKEN BY{team} FROM 1975-2019')
plt.show()




