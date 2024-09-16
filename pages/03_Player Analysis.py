import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import functions
st.set_page_config(page_title="Player Analysis")

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

tab1, tab2 = st.tabs(["Analysis 1", "Analysis 2"])

with tab1:
    orange_cap = functions.orange_cap_holder(df1, df2)
    orange_cap["Season_run"] = orange_cap["Season"].astype("str") + "=>" + orange_cap["batsman_run"].astype("str")
    # st.table(orange_cap.reset_index(drop=True))

    fig = px.bar(orange_cap, x='batter', y='Season_run', text_auto=True)
    fig.update_xaxes(tickangle=45)
    fig.update_layout(title="Orange Cap Holders 2008-2022", title_x=0.4, title_y=1, width=850, height=430)
    fig.update_traces(marker_color='orange', marker_line_color='black', marker_line_width=2, opacity=1)
    st.plotly_chart(fig)

    st.markdown("****")

    purple_cap = functions.purple_cap_holder(df1, df2)
    purple_cap["Season_wickets"] = purple_cap["Season"].astype("str") + "=>" + purple_cap[
        "isWicketDelivery"].astype("str")

    # st.table(purple_cap.reset_index(drop=True))

    fig = px.bar(purple_cap, x='bowler', y='Season_wickets', text_auto=True)
    fig.update_xaxes(tickangle=45)
    fig.update_layout(title="Purple Cap Holders 2008-2022", title_x=0.4, title_y=1, width=900, height=400)
    fig.update_traces(marker_color='purple', marker_line_color='black', marker_line_width=2, opacity=1)
    st.plotly_chart(fig)

    st.markdown("****")

    total_hun = functions.top_10_hunderds(df1, df2)
    fig = px.bar(total_hun, x='count', y='batter', orientation="h", text_auto=True)
    fig.update_xaxes(tickangle=45)
    fig.update_layout(title="Most 100s by a Batsman 2008-2022", title_x=0.4, title_y=1, width=900, height=400)
    fig.update_traces(marker_color=total_hun["count"], marker_line_color='black', marker_line_width=2, opacity=1)
    st.plotly_chart(fig)

    st.markdown("****")

    most_6 = functions.most_sixes(df1)
    fig = px.funnel(most_6, x="batter", y='count')
    fig.update_xaxes(tickangle=45)
    fig.update_layout(title="Most 6s by a Batsman 2008-2022", title_x=0.4, title_y=1, width=900, height=400)
    fig.update_traces(marker_color='cyan', marker_line_color='black', marker_line_width=2, opacity=1)
    st.plotly_chart(fig)

    st.markdown("****")

    catches_df = df1[df1["kind"] == "caught"]["fielders_involved"].value_counts().head(20).reset_index()
    fig = px.scatter(catches_df, x="fielders_involved", y="count", size="count", color="fielders_involved",
                     size_max=45)
    for i, value in enumerate(catches_df['count']):
        fig.add_annotation(
            x=catches_df['fielders_involved'][i],
            y=value,
            text=str(value), showarrow=False, bgcolor="black")
    fig.update_layout(title="Most Catches by a player", title_x=0.35, title_y=0.95, width=1000, height=450)
    fig.update_traces(marker_line_color='black', marker_line_width=0.5, opacity=1)
    st.plotly_chart(fig)

with tab2:
    aj = functions.top_10_batsman(df1)
    fig = px.bar(aj, x="batter", y="batsman_run")
    for i, value in enumerate(aj['batsman_run']):
        fig.add_annotation(
            x=aj['batter'][i],
            y=value,
            text=str(value), showarrow=False, bgcolor="black")
    fig.update_layout(title="Top 10 batsmans by runs", title_x=0.4, title_y=1, width=900, height=400)
    fig.update_traces(marker_color='red', marker_line_color='black', marker_line_width=2, opacity=1)
    st.plotly_chart(fig)

    st.markdown("****")

    wick = functions.top_10_wick(df1)
    fig = px.bar(wick, x="bowler", y="count")
    for i, value in enumerate(wick['count']):
        fig.add_annotation(
            x=wick['bowler'][i],
            y=value,
            text=str(value), showarrow=False, bgcolor="black")
    fig.update_layout(title="Top 10 wicket takers in IPL 2008-2022", title_x=0.35, title_y=1, width=900, height=400)
    fig.update_traces(marker_color='green')
    st.plotly_chart(fig)

    st.markdown("****")

    mbf = functions.max_balls_faced(df1)
    fig = px.bar(mbf, x="batter", y="count")
    for i, value in enumerate(mbf['count']):
        fig.add_annotation(
            x=mbf['batter'][i],
            y=value,
            text=str(value), showarrow=False, bgcolor="black")
    fig.update_layout(title="Maximum balls faced by a batsman(Top 10)", title_x=0.35, title_y=1, width=900,
                      height=400)
    st.plotly_chart(fig)

    st.markdown("****")

    death_runs, death_strike_rate = functions.destructive_batter(df1)
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("<center><font size='4'><b>Batman runs in death overs (top 10)</b></font></center>",
                    unsafe_allow_html=True)

        st.table(death_runs)
    with col2:
        st.markdown("<center><font size='4'><b>Strike  rate in death overs (top 10)</b></font></center>",
                    unsafe_allow_html=True)

        st.table(death_strike_rate)

    st.markdown("****")

    st.markdown("<center><font size='5'><b>Bowling Average of Bowlers (top 10)</b></font></center>",
                unsafe_allow_html=True)

    runs_conc = df1.groupby(["bowler", "batsman_run"])["batsman_run"].sum().reset_index(allow_duplicates=True)
    runs_conc = runs_conc.loc[:, ~runs_conc.columns.duplicated(keep='last')]
    runs_conc = runs_conc.groupby("bowler")["batsman_run"].sum().sort_values().reset_index()
    runs_conc1 = runs_conc[runs_conc["batsman_run"] > 1000].sort_values("batsman_run", ascending=False)

    total_wic1 = df1[df1["isWicketDelivery"] == 1]["bowler"].value_counts().reset_index().sort_values("bowler",
                                                                                                      ascending=False)

    merged_df2 = pd.merge(runs_conc1, total_wic1, on='bowler', how='inner')
    merged_df2['Bowling Average'] = merged_df2['batsman_run'] / merged_df2['count']
    Bowling_Average = merged_df2[merged_df2["count"] >= 70].sort_values("Bowling Average",
                                                                        ascending=True).reset_index(drop=True)
    st.table(Bowling_Average.head(10))

    st.markdown("****")

    st.markdown("<center><font size='5'><b>Batting Average of Batsmen (top 10)</b></font></center>",
                unsafe_allow_html=True)

    b_run = df1[df1["batsman_run"] >= 1]
    out_delivery = df1[df1["isWicketDelivery"] == 1]
    result = b_run.groupby("batter")["batsman_run"].sum() >= 500
    filtered_batters = b_run.groupby("batter")["batsman_run"].sum()[result]
    batting_avg = ((filtered_batters.sort_values(ascending=False)) / (
        out_delivery["batter"].value_counts()).sort_values(
        ascending=False)).sort_values(ascending=False).head(10).reset_index()
    batting_avg.rename(columns={"batter": "batter", 0: "average"}, inplace=True)
    st.table(batting_avg)

    st.markdown("****")

    merge_df = df1.merge(df2, left_on="ID", right_on="ID")
    fig = px.pie(merge_df[merge_df["isWicketDelivery"] == 1], names="kind", width=1000, height=500)
    fig.update_layout(title="Type of Outs in IPL", title_x=0.5, width=700, height=400)
    st.plotly_chart(fig)

expander3 = st.expander("See Explanation")
with expander3:
    st.write("""Discover deeper insights within the "Player-Wise Analysis" section through two 
                 specialized tabs: "Analysis 1" and "Analysis 2." These tabs offer tailored avenues 
                 for users to explore diverse dimensions of player performance, statistics,
                   and trends within the IPL dataset. Whether examining batting averages,
                     bowling figures, or player contributions across seasons, each tab provides 
                     a focused platform to analyze and interpret player-centric data effectively.
                 Insights >>""")
    message = """* Orange Cap Holders
                    * Purple Cap Holders
                    * Most 6s by a Batsman in IPL (2008–2022)
                    * Top 10 Batsman by Runs
                    * Type of Dismissals in IPL
                    * Most 100s by a Batsman
                    * Most Catches By a Player
                    * Top 10 Wickets Takers in IPL
                    * Maximum Balls faced by a Batsman
                    * Batsman runs and strike rate in death overs
                    * Bowling Average of Bowlers (top 10)
                    * Batting Average of Batsmen (top 10)"""
    lines = message.split("\n")
    for i in lines:
        st.write(i)

