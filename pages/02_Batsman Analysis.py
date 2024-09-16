import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import functions
st.set_page_config(page_title="Batsman Analysis")

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

#masked and merged dataset
seasondf = balls.merge(matches[["ID", "Season"]], on="ID", how="left")
seasondf["is_bowler_wicket"] = seasondf["kind"].apply(
    lambda x: 1 if x in ['caught', 'caught and bowled', 'bowled', 'stumped',
                         'lbw', 'hit wicket'] else 0)
seasondf["run_by_bowler"] = seasondf["extra_type"].apply(lambda x: 0 if x in ['legbyes', "byes"] else 1) * seasondf[
    "total_run"]
seasondf["is_fare_del"] = seasondf["extra_type"].apply(lambda x: 0 if x in ['wides', "noballs"] else 1)

select_batter = st.selectbox("Select Batsman", sorted(balls["batter"].unique()))
st.title("Batsman Analysis")
def batsman_analysis(select_batter):
    #player statistics
    st.subheader(select_batter)

    #player df
    batterdf = seasondf.copy()
    batterdf["isBatsmanBall"] = batterdf["extra_type"].apply(lambda x: 1 if x != "wides" else 0)
    bdf = batterdf[batterdf["batter"] == select_batter].copy()
    bdf["isBatterOut"] = bdf["batter"] == bdf["player_out"]
    bdf["isSix"] = bdf["batsman_run"] == 6
    bdf["isFour"] = bdf["batsman_run"] == 4
    df = bdf.groupby(["Season", "ID"], as_index=False)[
        ["batsman_run", "isBatsmanBall", "isBatterOut", "isSix", "isFour"]].sum()
    innings = df.groupby("Season")["ID"].count()
    df["is50"] = df["batsman_run"] >= 50
    df["is100"] = df["batsman_run"] >= 100
    df = df.groupby("Season").agg(
        {
            "batsman_run": ["sum", "max"],
            "isBatsmanBall": "sum",
            "isBatterOut": "sum",
            "isSix": "sum",
            "isFour": "sum",
            "is50": "sum",
            "is100": "sum"
        }
    )
    df["Innings"] = innings
    df["TotalRuns"] = df[("batsman_run", "sum")]
    df["Avg"] = df["TotalRuns"] / df[("isBatterOut", "sum")]
    df["Highest_Score"] = df[("batsman_run", "max")]
    df["Strike_Rate"] = df["TotalRuns"] / df[("isBatsmanBall", "sum")] * 100
    df["6s"] = df[("isSix", "sum")]
    df["4s"] = df[("isFour", "sum")]
    df["50s"] = df[("is50", "sum")]
    df["100s"] = df[("is100", "sum")]
    df = df.drop(columns=["batsman_run", "isBatsmanBall", "isBatterOut", "isSix", "isFour", "is50", "is100"])
    st.dataframe(df)

    #top stat
    col1, col2, col3 = st.columns(3)
    col4, col5, col6 = st.columns(3)
    col7, col8, col9 = st.columns(3)
    with col1:
        st.metric("Total Matches", df["Innings"].sum())
    with col2:
        st.metric("Total Run", df["TotalRuns"].sum())
    with col3:
        st.metric("Highest Run", df["Highest_Score"].max())
    with col4:
        st.metric("Strike Rate", (round(df["Strike_Rate"].mean(), 2)))
    with col5:
        st.metric("50s", df["50s"].sum())
    with col6:
        st.metric("100s", df["100s"].sum())
    with col7:
        st.metric("Average", (round(df["Avg"].mean(), 2)))
    with col8:
        st.metric("6s", df["6s"].sum())
    with col9:
        st.metric("4s", df["4s"].sum())

    #graphs
    #bar
    fig1 = px.bar(df, x=df.index, y="TotalRuns")
    fig1.update_layout(title="Run in every season", autosize=False, width=900, height=400, xaxis_tickangle=-45,
                       margin=dict(l=80, r=80, t=40, b=120))
    fig1.update_traces(marker_color='#ff7f0e', marker_line_color='black', marker_line_width=2, opacity=1)
    st.plotly_chart(fig1)
    #line-plot
    fig2 = px.line(df, x=df.index, y="Strike_Rate", markers=True)
    fig2.update_layout(title="Strike Rate in every season", autosize=False, width=900, height=500)
    st.plotly_chart(fig2)


batsman_analysis(select_batter)
