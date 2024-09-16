import streamlit as st
import pandas as pd


st.set_page_config(page_title="Overall Analysis")

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

st.image("ipl_home.jpg", width=500)
col5, col6 = st.columns(2)




with col5:
        season = df2["Season"].nunique()
        st.markdown("##### :green[Seasons] :sports_medal:")
        st.header(season)

        total_wick = df1[df1["isWicketDelivery"] == 1]["bowler"].value_counts().sum()
        st.markdown("##### :green[Wickets] :cricket:")
        st.header(total_wick)

        sixes = df1[df1["batsman_run"] == 6]["batsman_run"].count()
        st.markdown("##### :green[Total 6s] :six:")
        st.header(sixes)

        merd_df = pd.merge(df1, df2, how='inner', on='ID')
        hunderds = merd_df.groupby(["ID", "batter"])["batsman_run"].sum().reset_index()
        hun_100 = hunderds[hunderds["batsman_run"] >= 100]["batsman_run"].count()
        st.markdown("##### :green[Total 100s] :100:")
        st.header(hun_100)

with col6:
        b_run = df1[df1["batsman_run"] >= 1]
        top_10_bats = b_run.groupby("batter")["batsman_run"].sum().sum()
        st.markdown("##### :green[Runs] :cricket_bat_and_ball:")
        st.header(top_10_bats)

        total_balls = df1.shape[0]
        st.markdown("##### :green[Balls] :softball:")
        st.header(total_balls)

        fours = df1[df1["batsman_run"] == 4]["batsman_run"].count()
        st.markdown("##### :green[Total 4s] :four:")
        st.header(fours)

        merd_df = pd.merge(df1, df2, how='inner', on='ID')
        fift = merd_df.groupby(["ID", "batter"])["batsman_run"].sum().reset_index()
        hun_50 = fift[(fift["batsman_run"] >= 50) & (fift["batsman_run"] < 100)]["batsman_run"].count()
        st.markdown("##### :green[Total 50s] :five::zero:")
        st.header(hun_50)

    #     st.markdown("<div style='border-left: 2px solid #FFF; height: 100px;'></div>", unsafe_allow_html=True)

