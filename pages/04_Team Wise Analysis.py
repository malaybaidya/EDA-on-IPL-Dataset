import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import functions
st.set_page_config(page_title="Team wise Analysis")

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
    team_runs = df1.groupby("BattingTeam")["batsman_run"].sum().reset_index()
    team_runs.rename(columns={"batsman_run": "Total_runs"}, inplace=True)
    fig = px.scatter(team_runs, x="BattingTeam", y="Total_runs", size="Total_runs", color="BattingTeam",
                     size_max=65)
    for i, value in enumerate(team_runs['Total_runs']):
        fig.add_annotation(
            x=team_runs['BattingTeam'][i],
            y=value,
            text=str(value), showarrow=False, bgcolor="black")
    fig.update_layout(title="Total Runs by IPL Teams", title_x=0.35, title_y=0.95, width=1000, height=550)
    st.plotly_chart(fig)

    st.markdown("****")

    newdf = df2["Team2"].value_counts() + df2["Team1"].value_counts()
    newdf1 = pd.DataFrame(newdf).reset_index()
    newdf1.rename(columns={"index": "teams"}, inplace=True)

    # ("Total match played by the each teams")
    fig = px.bar(newdf1, x='teams', y='count')

    for i, value in enumerate(newdf1['count']):
        fig.add_annotation(
            x=newdf1['teams'][i],
            y=value,
            text=str(value), showarrow=False, bgcolor="black")
    fig.update_layout(title="Total Matches played by the each team", title_x=0.3, title_y=0.9, autosize=False,
                      width=900, height=400)
    st.plotly_chart(fig)

    st.markdown("****")

    teams_count = df2.groupby("Season")["Team1"].nunique().reset_index()
    fig = px.scatter(teams_count, x="Season", y="Team1", size="Team1", size_max=60, color=teams_count["Team1"])
    for i, value in enumerate(teams_count['Team1']):
        fig.add_annotation(
            x=teams_count['Season'][i],
            y=value,
            text=str(value), showarrow=False, bgcolor="black")
    fig.update_layout(title="Total teams participating over the years", title_x=0.3, title_y=0.9, autosize=False,
                      width=900, height=500)
    st.plotly_chart(fig)

    st.markdown("****")

    col1, col2, col3 = st.columns(3)
    with col2:
        st.markdown("**<font size='4'>Total matches win by the teams**</font>", unsafe_allow_html=True)
        # <font size='5'>This is bold text with custom size</font>
    col1, col2 = st.columns(2)
    with col1:
        win_df = df2["WinningTeam"].value_counts().reset_index()
        st.table(win_df)

    with col2:
        fig = px.pie(win_df, values="count", names="WinningTeam")
        fig.update_layout(autosize=False, width=500, height=600)
        st.plotly_chart(fig)

    st.markdown("****")

    win_teams_df = df2[df2["MatchNumber"] == "Final"]
    final_win = win_teams_df["WinningTeam"].value_counts().reset_index()
    fig = px.bar(final_win, x='WinningTeam', y='count')
    for i, value in enumerate(final_win['count']):
        fig.add_annotation(
            x=final_win['WinningTeam'][i],
            y=value,
            text=str(value), showarrow=False, bgcolor="black")
    fig.update_layout(title="Total final wins by the teams", title_x=0.4, title_y=0.9, autosize=False, width=900,
                      height=400)
    fig.update_traces(marker_color='green', marker_line_color='black', marker_line_width=2, opacity=1)
    st.plotly_chart(fig)

    st.markdown("****")
    finals = df2[df2["MatchNumber"] == "Final"]
    most_finals = finals["Team1"].tolist() + finals["Team2"].tolist()
    most_final_play = pd.DataFrame(most_finals).value_counts().reset_index()
    most_final_play.rename(columns={0: "teams", "count": "count"}, inplace=True)
    fig = px.bar(most_final_play, x='teams', y='count')
    for i, value in enumerate(most_final_play['count']):
        fig.add_annotation(
            x=most_final_play['teams'][i],
            y=value,
            text=str(value), showarrow=False, bgcolor="black")
    fig.update_layout(title="Most Finals played by the teams", title_x=0.4, title_y=0.9, autosize=False, width=900,
                      height=400)
    fig.update_traces(marker_color='yellow', marker_line_color='black', marker_line_width=2, opacity=1)
    st.plotly_chart(fig)

with tab2:
    city_match = df2["City"].value_counts().reset_index()
    fig = px.bar(city_match, x="City", y="count", text="count", width=1000, height=600)
    fig.update_layout(title="Name of the matches hosted in different cities", title_x=0.3, title_y=0.9,
                      autosize=False, width=900, height=400, barmode='group', xaxis_tickangle=-45)
    fig.update_traces(texttemplate='%{text:.2s}', textposition='outside', marker_color='red',
                      marker_line_color='black')
    st.plotly_chart(fig)

    st.markdown("****")

    st.markdown("<center><font size='3'><b>Win percentage as batting team and bowling team</b></font></center>",
                unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        win_bat = (df2.Team1 == df2.WinningTeam)
        win_bat1 = win_bat.value_counts().reset_index()
        fig = px.pie(win_bat1, names="index", values="count")
        fig.update_layout(title="Win percentage as batting team", title_x=0.3, title_y=0.1,
                          legend=dict(yanchor="top", y=0.9, xanchor="right", x=0.2),
                          autosize=False, width=600, height=400, barmode='group', xaxis_tickangle=-45)

        st.plotly_chart(fig)

    with col2:
        win_field = (df2.Team2 == df2.WinningTeam)
        win_field1 = win_field.value_counts().reset_index()
        fig = px.pie(win_field1, names="index", values="count")
        fig.update_layout(title="Win percentage as bowling team", title_x=0.28, title_y=0.1,
                          legend=dict(yanchor="top", y=0.9, xanchor="right", x=0.2),
                          autosize=False, width=600, height=400, barmode='group', xaxis_tickangle=-45)

        st.plotly_chart(fig)
    st.markdown("****")

    st.markdown("<center><font size='3'><b>Matches Played vs Matches Won by the teams</b></font></center>",
                unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        team_con = pd.concat([df2["Team1"], df2["Team2"]])
        played_df = team_con.value_counts().reset_index()
        played_df.columns = ["teams", "played_count"]
        played_df["winning_count"] = df2["WinningTeam"].value_counts().reset_index()["count"]
        st.table(played_df)

    with col2:
        win_percentage = (df2["WinningTeam"].value_counts() / team_con.value_counts() * 100).sort_values(
            ascending=False).reset_index()
        fig = px.pie(win_percentage, names="index", values="count")
        fig.update_layout(autosize=False, width=550, height=800)
        st.plotly_chart(fig)
    st.markdown("****")

    col1, col2, col3, col4 = st.columns(4)

    with col2:
        win_toss = (df2.WinningTeam == df2.TossWinner)
        win_toss1 = win_toss.value_counts().reset_index()
        fig = px.pie(win_toss1, names="index", values="count", hole=.4,
                     color_discrete_sequence=px.colors.sequential.RdBu)
        fig.update_layout(title="Win Toss Win Match Analysis", title_x=0.25, title_y=1,
                          annotations=[dict(text='WTWM', x=0.5, y=0.5, font_size=17, showarrow=False)],
                          legend=dict(yanchor="top", y=1, xanchor="left", x=-0.2), autosize=False, width=500,
                          height=450)
        st.plotly_chart(fig)

    st.markdown("****")

    from plotly.subplots import make_subplots

    margin_df = df2[["WinningTeam", "WonBy", "Margin"]]
    won_by_wickets = margin_df[margin_df["WonBy"] == "Wickets"]
    won_by_runs = margin_df[margin_df["WonBy"] == "Runs"]
    fig = make_subplots(rows=2, cols=1,
                        subplot_titles=("Win Margin of Teams Won by Runs", "Win Margin of Teams Won by Wickets"))
    fig.add_trace(px.scatter(won_by_runs, x="WinningTeam", y="Margin", color="Margin").data[0], row=1, col=1)
    fig.add_trace(px.scatter(won_by_wickets, x="WinningTeam", y="Margin", color="Margin").data[0], row=2, col=1)
    fig.update_layout(width=1000, height=800)
    st.plotly_chart(fig)

expander2 = st.expander("See Explanation")
with expander2:
    st.write("""In the "Team-Wise Analysis" section, users can explore IPL team performance 
                 through two tabs: "Analysis 1" and "Analysis 2." 
                 These tabs offer distinct insights into various metrics and trends, 
                 enabling users to gain a comprehensive understanding of team dynamics.Like""")
    message = """* Total Runs by IPL Teams 
                 * Total Finals Wins by the teams
                 * Total Matches win by the Teams
                 * Total Matches played by each team
                 * Total teams participating over the years
                 * Most Finals played by the teams
                 * Win Toss-Win Match Analysis
                 * Most Finals played by the Teams
                 * Number of Matches hosted in different cities
                 * Win percentage as batting team and bowling team 
                 * Matches played vs Matches Won by the teams
                 * Win Margin of teams Won by runs and by Wickets"""
    lines = message.split("\n")

    # Print each line in the list
    for line in lines:
        st.write(line)

