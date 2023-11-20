from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64
import seaborn as sns

app = Flask(__name__)

# Load your data (CSV file) using Pandas
# Replace 'your_data.csv' with your actual data file.
df = pd.read_csv('cwc_cleaned_data.csv')

@app.route('/')
def index():
    return render_template('index.html')



team_mapping = {
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

def fullform(team):
    team = team.replace(" ", "")
    team = team_mapping.get(team, 'Unknown')
    return team
df.loc[(df['TEAM']=='PAK') & (df['AGAINST']=='IND') & (df['RESULT']=='WON'),'RESULT']='LOST'

@app.route('/overall-performance', methods=['GET'])
def overall_performance():

    trophy={}
    for year,winner in df.groupby('YEAR')['TROPHY WINNER']:
        trophy[year]=winner.mode()[0]

    from collections import Counter
    count=Counter(trophy.values())
    count=sorted(count.items(),key=lambda x:x[1],reverse=True)[:3]
    matches={}
    for i in df.groupby('TEAM')['TEAM']:
        matches[i[0]]=i[1].count()
    matches=sorted(matches.items(), key=lambda x: x[1], reverse=True)[:3]
    mostwins= {}
    for team, result in df.groupby('TEAM')['RESULT']:
        mostwins[team]=result[result=='WON'].count()
    mostwins=sorted(mostwins.items(),key=lambda i:i[1],reverse=True)[:3]
    mostlosts= {}
    for team, result in df.groupby('TEAM')['RESULT']:
        mostlosts[team]=result[result=='LOST'].count()
    mostlosts=sorted(mostlosts.items(),key=lambda i:i[1],reverse=True)[:3]
    mostruns={}
    for i in df.groupby('TEAM')['RUNS SCORED']:
        mostruns[i[0]]=i[1].sum()
    mostruns=sorted(mostruns.items(), key=lambda x: x[1], reverse=True)[:3] 
    mostwickets={}
    for i in df.groupby('TEAM')['WICKETS TAKEN']:
        mostwickets[i[0]]=i[1].sum()
    mostwickets=sorted(mostwickets.items(), key=lambda x: x[1], reverse=True)[:3]
    
    #TROPHY WINNERS

    trophies=df.groupby('YEAR')['TROPHY WINNER'].agg(lambda x: x.mode().iloc[0]).to_dict()
    x=list(trophies.keys())[1:]
    y=list(trophies.values())[1:]
    print(x,y)
    plt.figure(figsize=(9,6))
    sns.set(style="whitegrid")
    sns.countplot(y,palette='muted')

    plt.xlabel('TEAMS')
    plt.ylabel('Number of Trophies')
    plt.title('World Cup Trophy Winners 1975 - 2019')
    # plt.figure(figsize=(9,6))
    # sns.countplot(y)

    # plt.xlabel('TEAMS')
    # plt.ylabel('Number of Trophies')
    # plt.title('World Cup Trophy Winners 1975 - 2019')
    img_buf = io.BytesIO()
    plt.savefig(img_buf, format='png')
    img_buf.seek(0)
    op1 = base64.b64encode(img_buf.read()).decode()



    #TOTAL MATCHES WON
    matches_won={}
    teams=list(df['TEAM'].unique())
    for team in teams:
        matches_won_count=len(df[(df['TEAM']==team) & (df['RESULT']=='WON')])
        matches_won[team]=matches_won_count
    t=list(matches_won.keys())
    w=list(matches_won.values())
    plt.figure(figsize=(12,6))
    sns.barplot(x=t,y=w,palette='muted',hue=t,dodge=False)
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
    img_buf = io.BytesIO()
    plt.savefig(img_buf, format='png')
    img_buf.seek(0)
    op2 = base64.b64encode(img_buf.read()).decode()



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
    sns.barplot(x=x,y=y,palette='muted',hue=x,dodge=False)
    for i in range(len(x)):
        plt.text(i, y[i], str(y[i]), ha='center')
    plt.xlabel('TEAMS')
    plt.ylabel('TOTAL RUN SCORED')
    plt.title('TOTAL RUNS SCORED BY A TEAM IN CWC 1975-2019')
    plt.xticks(rotation=45)
    plt.show()
    img_buf = io.BytesIO()
    plt.savefig(img_buf, format='png')
    img_buf.seek(0)
    op3 = base64.b64encode(img_buf.read()).decode()


    #MATCHES PLAYED
    matches_played=dict(df['TEAM'].value_counts())
    x=list(matches_played.keys())
    y=list(matches_played.values())
    plt.figure(figsize=(10,8))
    sns.barplot(x=x,y=y,palette='muted',hue=x,dodge=False)
    for i in range(len(x)):
        plt.text(i, y[i], str(y[i]), ha='center')
    plt.xlabel('TEAMS')
    plt.ylabel('MATCHES PLAYED')
    plt.title('TOTAL MATCHES PLAYED BY A TEAM IN CWC 1975-2019')
    plt.xticks(rotation=45)
    plt.show()
    img_buf = io.BytesIO()
    plt.savefig(img_buf, format='png')
    img_buf.seek(0)
    op4 = base64.b64encode(img_buf.read()).decode()

    return render_template('overall-performance.html', chart1=op1, chart2=op2, chart3=op3,chart4=op4,matches=matches,mostwins=mostwins,mostwickets=mostwickets,mostlosts=mostlosts,mostruns=mostruns,fullform=fullform,count=count)

@app.route('/team', methods=['GET', 'POST'])
def select_team():
    if request.method == 'POST':
        selected_team = request.form['team']
        return redirect(url_for('team_insights', team=selected_team))
    return render_template('team.html')
@app.route('/team-insights/<team>', methods=['GET'])
def team_insights(team):
    df_team = df[df['TEAM'] == team]
    # Matches Played vs. Matches Won
    matches_played = df_team.groupby('YEAR')['TEAM'].count()
    matches_played = dict(matches_played)
    matches_won = {}
    res = df_team.groupby('YEAR')['RESULT']
    for i, j in res:
        matches_won[i] = len(j[j == 'WON'])

    years = list(matches_won.keys())
    won_counts = list(matches_won.values())
    played_counts = list(matches_played.values())
    bar_width = 0.35

    x = range(len(years))

    fig, ax = plt.subplots(figsize=(10, 6))

    bar1 = ax.bar(x, won_counts, width=bar_width, label='Matches Won', align='center', color='#75BF71')
    bar2 = ax.bar([i + bar_width for i in x], played_counts, width=bar_width, label='Matches Played', align='center', color='#D98B5F')

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

    img_buf = io.BytesIO()
    plt.savefig(img_buf, format='png')
    img_buf.seek(0)
    img1 = base64.b64encode(img_buf.read()).decode()

    team_runs_year=df_team.groupby('YEAR')['RUNS SCORED'].sum().to_dict()
    x=list(team_runs_year.keys())
    y=list(team_runs_year.values())
    plt.figure(figsize=(9,7))
    sns.barplot(x=x,y=y,palette='muted')
    for i in range(len(x)):
        plt.text(i, y[i], str(y[i]), ha='center')
    plt.xlabel('YEARS')
    plt.ylabel(f'RUNS SCORED BY {fullform(team)}')
    plt.title(f'RUNS SCORED BY {fullform(team)} FROM 1975-2019')
    plt.xticks(rotation=45)
    plt.show()
    img_buf = io.BytesIO()
    plt.savefig(img_buf, format='png')
    img_buf.seek(0)
    img2 = base64.b64encode(img_buf.read()).decode()
    #WICKETS TAKEN BY A TEAM

    wickets=df_team.groupby('YEAR')['WICKETS TAKEN'].sum().to_dict()
    wickets
    matches_played=df_team.groupby('YEAR')['TEAM'].count().to_dict()
    matches_played
    x=list(wickets.values())
    y=list(wickets.keys())
    plt.figure(figsize=(10,6))
    sns.barplot(x=y,y=x,palette='muted')
    for i in range(len(y)):
        plt.text(i, x[i], str(x[i]), ha='center')
    plt.xlabel('YEARS')
    plt.ylabel('WICKETS TAKEN')
    plt.title(f'WICKETS TAKEN BY {fullform(team)} FROM 1975-2019')
    plt.show()
    img_buf = io.BytesIO()
    plt.savefig(img_buf, format='png')
    img_buf.seek(0)
    img3 = base64.b64encode(img_buf.read()).decode()
    runs=df_team['RUNS SCORED'].sum()
    wickets=df_team['WICKETS TAKEN'].sum()
    won=df_team[df_team['RESULT']=='WON']['RESULT'].count()
    lost=df_team[df_team['RESULT']=='LOST']['RESULT'].count()
    tie=df_team[df_team['RESULT']=='TIE']['RESULT'].count()
    nr=df_team[df_team['RESULT']=='NR']['RESULT'].count()
    matches=df_team.shape[0]
    return render_template('team-insights.html', selected_team=team, chart1=img1,chart2=img2,chart3=img3,runs=runs,matches=matches,wickets=wickets,nr=nr,won=won,lost=lost,fullform=fullform)
@app.route('/head-to-head', methods=['GET', 'POST'])
def head_to_head():
    if request.method == 'POST':
        team1 = request.form['team1']
        team2 = request.form['team2']

       
        return redirect(url_for('head_to_head_stats', team1=team1, team2=team2))
    return render_template('head-to-head.html', teams=df['TEAM'].unique())
def lowercase(team):
        team=team.lower()
        return team
@app.route('/head-to-head-stats/<team1>-<team2>', methods=['GET'])
def head_to_head_stats(team1, team2):
    flag1=lowercase(team1)+'.png'
    flag2=lowercase(team2)+'.png'
    h2h = df[(df['TEAM'] == team1) & (df['AGAINST'] == team2)]
    matches_played = len(h2h)
    team1_won = (h2h['RESULT'] == 'WON').sum() 
    team1_lost = (h2h['RESULT'] == 'LOST').sum()
    draws = (h2h['RESULT'] == 'TIE').sum()
    noresult=(h2h['RESULT'] == 'NR').sum()
    team1_runs = h2h['RUNS SCORED'].sum()
    team1_wickets=h2h['WICKETS TAKEN'].sum()
    h2h = df[(df['TEAM'] == team2) & (df['AGAINST'] == team1)]
    team2_won = (h2h['RESULT'] == 'WON').sum() 
    team2_lost = (h2h['RESULT'] == 'LOST').sum()
    team2_runs = h2h['RUNS SCORED'].sum()
    team2_wickets = h2h['WICKETS TAKEN'].sum()
    return render_template('head-to-head-stats.html',lowercase=lowercase,fullform=fullform, matches=matches_played,team1=team1, team2=team2, team1_won=team1_won,team1_lost=team1_lost,team1_runs=team1_runs,team1_wickets=team1_wickets,team2_lost=team2_lost,team2_runs=team2_runs,team2_wickets=team2_wickets,team2_won=team2_won,noresult=noresult,draws=draws,flag1=flag1,flag2=flag2)

if __name__ == '__main__':
    app.run(host='0.0.0.0',port='5001')
