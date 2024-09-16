import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

balls = pd.read_csv("datasets/IPL_Ball_by_Ball_2008_2022 (3).csv")
matches = pd.read_csv("datasets/IPL_Matches_2008_2022 (1).csv")
#name changes
changed_name = {
    'Delhi Daredevils': 'Delhi Capitals',
    'Kings XI Punjab': 'Punjab Kings',
    'Rising Pune Supergiants': 'Rising Pune Supergiant'
}
matches.replace(changed_name.keys(), changed_name.values(), inplace=True)
balls.replace(changed_name.keys(), changed_name.values(), inplace=True)

df1 = balls
df2 = matches

def player_statistics(player_name):
    batter_runs = df1[df1["batsman_run"] >= 1][["batter", "batsman_run"]].groupby("batter")["batsman_run"].sum().reset_index()
    p_runs = batter_runs[batter_runs["batter"] == player_name]
    t_runs = p_runs.iloc[0, 1]

    balls_faced = df1["batter"].value_counts().reset_index()
    tb_faced = balls_faced[balls_faced["batter"] == player_name].iloc[0,1]

    total_wic= df1[df1["isWicketDelivery"] == 1]["bowler"].value_counts().reset_index()
    total_bl_th = df1["bowler"].value_counts().reset_index()
    bowlerlist = total_wic["bowler"].tolist()
    if player_name in bowlerlist:
        total_wickets = total_wic[total_wic["bowler"] == player_name].iloc[0,1]
        total_balls_throw = total_bl_th[total_bl_th["bowler"] == player_name].iloc[0,1]
    else:
        total_wickets = "0"
        total_balls_throw = "0"

    runs_conc = df1.groupby(["bowler", "batsman_run"])["batsman_run"].sum().reset_index(allow_duplicates=True)
    runs_conc.rename(columns={'batsman_run': 'total_runs'}, inplace=True)
    runs_conc = runs_conc.loc[:, ~runs_conc.columns.duplicated(keep='last')]
    runs_conceded = runs_conc[runs_conc["bowler"] == player_name]["total_runs"].sum()

    if runs_conceded>=200:
        bowling_avg = runs_conceded/total_wickets 
    else:
        bowling_avg = 0  
    
    catches_df = df1[df1["kind"] == "caught"]["fielders_involved"].value_counts().reset_index()
    total_catch = catches_df[catches_df["fielders_involved"] == player_name].iloc[0,1]

    b_run = df1[df1["batsman_run"] >= 1]
    out_delivery = df1[df1["isWicketDelivery"] == 1]
    result = b_run.groupby("batter")["batsman_run"].sum() >= 500
    filtered_batters = b_run.groupby("batter")["batsman_run"].sum()[result]
    batting_avg = ((filtered_batters.sort_values(ascending=False))/ (out_delivery["batter"].value_counts()).sort_values(
        ascending=False)).sort_values(ascending=False).reset_index()
    batting_avg.columns = ["batter", "average"]
    b_avg = batting_avg[batting_avg["batter"] == player_name].iloc[0,1]

    batter_runs = df1[df1["batsman_run"] >= 1][["batter", "batsman_run"]].groupby("batter")["batsman_run"].sum()
    total_balls = df1["batter"].value_counts()
    srike_rate = ((batter_runs/total_balls) * 100).reset_index()
    s_rate = srike_rate[srike_rate["batter"] == player_name].iloc[0,1]

    merd_df = pd.merge(df1, df2, how='inner', on='ID')
    batsman_name = player_name
    batsman_data = merd_df[merd_df['batter'] == batsman_name]
    total_matches_played = batsman_data['ID'].nunique()

    runs_5 = merd_df[merd_df["isWicketDelivery"] == 1].groupby(["ID", "bowler"])["isWicketDelivery"].sum().sort_values(
        ascending = False).reset_index()
    wickets_5 = runs_5[runs_5["isWicketDelivery"] >= 5]["bowler"].value_counts().reset_index()
    wickets_4 = runs_5[runs_5["isWicketDelivery"] == 4]["bowler"].value_counts().reset_index()
    
    if player_name in wickets_5["bowler"].tolist():
        five_wick = wickets_5[wickets_5["bowler"] == player_name].iloc[0,1]
        four_wick = wickets_5[wickets_5["bowler"] == player_name].iloc[0,1]

    else:
        five_wick = 0
        four_wick = 0

    total_50_100 = batsman_data.groupby(["ID", "batter"])["batsman_run"].sum().reset_index()
    total_50 = total_50_100[(total_50_100["batsman_run"]>=50) & (total_50_100["batsman_run"]<100)].shape[0]
    total_100 = total_50_100[(total_50_100["batsman_run"]>=100)].shape[0]
    total_4 = batsman_data[batsman_data["batsman_run"] == 4].shape[0]
    total_6 = batsman_data[batsman_data["batsman_run"] == 6].shape[0]
    total_3 = batsman_data[batsman_data["batsman_run"] == 3].shape[0]
    high_score = total_50_100["batsman_run"].max()
    total_0 = total_50_100[(total_50_100["batsman_run"]==0)].shape[0]

    return (t_runs, tb_faced, b_avg, s_rate, total_matches_played, 
        total_50, total_100,total_4, total_6, total_3, high_score, 
        total_0, total_wickets, total_balls_throw, runs_conceded, 
        bowling_avg, total_catch, five_wick, four_wick)


def match_played_by_teams(df):
    fig = px.bar(newdf1, x='teams', y='count')

    for i, value in enumerate(newdf1['count']):
        fig.add_annotation(
            x=newdf1['teams'][i],
            y=value,
            text=str(value), showarrow=False)
        #fig.show()
    return fig.show()

def top_10_batsman(df1):
    b_run = df1[df1["batsman_run"] >= 1]
    top_10_bats = b_run.groupby("batter")["batsman_run"].sum().sort_values(ascending=False).reset_index().head(10)
    
    return top_10_bats

def top_10_wick(df1):
    top_10_wick = df1[df1["isWicketDelivery"] == 1]["bowler"].value_counts().reset_index().head(10)
    return top_10_wick

def max_balls_faced(df1):
    max_b_faced = df1["batter"].value_counts().reset_index().head(10)
    return max_b_faced

def destructive_batter(df1):
    death_over = df1[df1["overs"]>15]
    d_runs = death_over.groupby("batter")["batsman_run"].count()
    x = d_runs>500
    b_list = d_runs[x].index.tolist()

    final_death = death_over[death_over["batter"].isin(b_list)]

    death_runs = final_death.groupby("batter")["batsman_run"].sum()
    death_runs = death_runs.sort_values(ascending=False).reset_index().head(10)
    
    death_balls = final_death.groupby("batter")["batsman_run"].count().sort_values(ascending=False).head(10)
    dea_runs = final_death.groupby("batter")["batsman_run"].sum().sort_values(ascending=False)
    srike_rate_death = (dea_runs/death_balls)*100
    srike_rate_death = srike_rate_death.sort_values(ascending=False).reset_index()
    srike_rate_death.rename(columns = {"batsman_run":"Death Over SR"}, inplace=True) 
    srike_rate_death

    return death_runs, srike_rate_death

def orange_cap_holder(df1, df2):
    merge_df = df1.merge(df2, left_on="ID", right_on="ID")
    orange_cap = merge_df.groupby(["Season","batter"])["batsman_run"].sum().sort_values(
        ascending=False).reset_index().drop_duplicates(subset="Season",keep="first").sort_values("Season")
    
    return orange_cap

def purple_cap_holder(df1, df2):
    merge_df = df1.merge(df2, left_on="ID", right_on="ID")
    out_list1 = ['caught', 'caught and bowled', 'bowled', 'stumped','lbw']
    wick_deliv = merge_df[merge_df["isWicketDelivery"] == 1 & merge_df["kind"].isin(out_list1)]
    purple_cap = wick_deliv.groupby(["Season","bowler"])["isWicketDelivery"].sum().sort_values(
        ascending=False).reset_index().drop_duplicates(subset="Season",keep="first").sort_values("Season")

    return purple_cap

def top_umpires(df1, df2):
    merge_df = df1.merge(df2, left_on="ID", right_on="ID")
    grouped_df1 = merge_df.groupby(["MatchNumber", "Season", "Umpire1", "Umpire2"]).size().reset_index(name='TotalMatches')
    umpire_list = grouped_df1["Umpire1"].tolist() + grouped_df1["Umpire2"].tolist()
    umpire_df = pd.DataFrame(umpire_list)
    umpire_df.rename(columns = {0:"umpire_name"}, inplace=True)
    umpire_df = umpire_df.value_counts().head().reset_index()

    return umpire_df
    
def top_10_hunderds(df1, df2):
    merd_df = pd.merge(df1, df2, how='inner', on='ID')
    hunderds = merd_df.groupby(["ID", "batter"])["batsman_run"].sum().sort_values(ascending=False).reset_index()
    hun_100 = hunderds[hunderds["batsman_run"] >= 100]["batter"].value_counts().head(10).sort_values().reset_index()

    return hun_100

def top_10_fifities(df1, df2):
    merd_df = pd.merge(df1, df2, how='inner', on='ID')
    fift = merd_df.groupby(["ID", "batter"])["batsman_run"].sum().sort_values(ascending=False).reset_index()
    fif_50 = fift[(fift["batsman_run"] >= 50) & (fift["batsman_run"] <100)] ["batter"].value_counts().head(10).reset_index()

    return fif_50

def most_sixes(df1):
    six_6 = df1[["batter", "batsman_run"]]
    sixes = six_6[six_6["batsman_run"] == 6].value_counts().head(10).reset_index()

    return sixes

def most_fours(df1):
    four_4 = df1[["batter", "batsman_run"]]
    fours = four_4[four_4["batsman_run"] == 4].value_counts().head(10).reset_index()

    return fours

def five_wick(df1, df2):
    merd_df = pd.merge(df1, df2, how='inner', on='ID')
    runs_5 = merd_df[merd_df["isWicketDelivery"] == 1].groupby(["ID", "bowler"])["isWicketDelivery"].sum().sort_values(ascending = False).reset_index()
    wickets_5 = runs_5[runs_5["isWicketDelivery"] >= 5]["bowler"].value_counts().reset_index()

    return wickets_5

def most_threes(df1):
    three_3 = df1[["batter", "batsman_run"]]
    threes = three_3[three_3["batsman_run"] == 3].value_counts().head(10).reset_index()

    return threes

def dot_balls(df1):
    dot_0 = df1[["batter", "batsman_run"]]
    dots = dot_0[dot_0["batsman_run"] == 0].value_counts().head(10).reset_index()

    return dots