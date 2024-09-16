import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import functions
st.set_page_config(page_title="Miscellaneous_Analysis")

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
    umpire = functions.top_umpires(df1, df2)
    fig = px.pie(umpire, values='count', names='umpire_name', hole=.4,
                 color_discrete_sequence=px.colors.sequential.Viridis)
    fig.update_traces(textinfo='value')
    fig.update_layout(title="Most matches as an umpire", title_x=0.5, width=700, height=400)
    st.plotly_chart(fig)

    st.markdown("****")

    total_fif = functions.top_10_fifities(df1, df2)
    fig = px.funnel(total_fif, x="batter", y='count')
    fig.update_xaxes(tickangle=45)
    fig.update_layout(title="Most 50s by a Batsman 2008-2022", title_x=0.4, title_y=1, width=900, height=400)
    fig.update_traces(marker_color="yellow", marker_line_color='black', marker_line_width=2, opacity=1)
    st.plotly_chart(fig)

    st.markdown("****")

    most_4 = functions.most_fours(df1)
    fig = px.scatter(most_4, x="batter", y='count', size="count", size_max=60, color=most_4["count"])
    fig.update_xaxes(tickangle=45)
    for i, value in enumerate(most_4['count']):
        fig.add_annotation(
            x=most_4['batter'][i],
            y=value,
            text=str(value), showarrow=False, bgcolor="black")
    fig.update_layout(title="Most 4s by a Batsman 2008-2022", title_x=0.4, title_y=1, width=900, height=400)
    fig.update_traces(marker_color=most_4["count"], marker_line_color='black', marker_line_width=2, opacity=1)
    st.plotly_chart(fig)

    st.markdown("****")

    five_wick = functions.five_wick(df1, df2)
    fig = px.funnel(five_wick, x="bowler", y="count")
    fig.update_xaxes(tickangle=45)
    fig.update_layout(title="5 Wicket bowlers 2008-2022", title_x=0.4, title_y=1, width=900, height=400)
    fig.update_traces(marker_color="brown", marker_line_color='black', marker_line_width=2, opacity=1)
    st.plotly_chart(fig)

with tab2:
    col1, col2, col3, col4, col5, col6, col7 = st.columns(7)
    with col1:
        sixes = df1[df1["batsman_run"] == 6]["batsman_run"].count()
        st.markdown("##### :green[Total 6s]")
        st.header(sixes)
    with col2:
        st.markdown("<div style='border-left: 2px solid #FFF; height: 100px;'></div>", unsafe_allow_html=True)

    with col3:
        fours = df1[df1["batsman_run"] == 4]["batsman_run"].count()
        st.markdown("##### :green[Total 4s]")
        st.header(fours)
    with col4:
        st.markdown("<div style='border-left: 2px solid #FFF; height: 100px;'></div>", unsafe_allow_html=True)

    with col5:
        merd_df = pd.merge(df1, df2, how='inner', on='ID')
        hunderds = merd_df.groupby(["ID", "batter"])["batsman_run"].sum().reset_index()
        hun_100 = hunderds[hunderds["batsman_run"] >= 100]["batsman_run"].count()
        st.markdown("##### :green[Total 100s]")
        st.header(hun_100)
    with col6:
        st.markdown("<div style='border-left: 2px solid #FFF; height: 100px;'></div>", unsafe_allow_html=True)

    with col7:
        merd_df = pd.merge(df1, df2, how='inner', on='ID')
        fift = merd_df.groupby(["ID", "batter"])["batsman_run"].sum().reset_index()
        hun_50 = fift[(fift["batsman_run"] >= 50) & (fift["batsman_run"] < 100)]["batsman_run"].count()
        st.markdown("##### :green[Total 50s]")
        st.header(hun_50)

    col1, col2, col3, col4, col5, col6, col7 = st.columns(7)

    with col1:
        season = df2["Season"].nunique()
        st.markdown("##### :green[Seasons]")
        st.header(season)
    with col2:
        st.markdown("<div style='border-left: 2px solid #FFF; height: 100px;'></div>", unsafe_allow_html=True)

    with col3:
        b_run = df1[df1["batsman_run"] >= 1]
        top_10_bats = b_run.groupby("batter")["batsman_run"].sum().sum()
        st.markdown("##### :green[Runs]")
        st.header(top_10_bats)
    with col4:
        st.markdown("<div style='border-left: 2px solid #FFF; height: 100px;'></div>", unsafe_allow_html=True)

    with col5:
        total_balls = df1.shape[0]
        st.markdown("##### :green[Balls]")
        st.header(total_balls)
    with col6:
        st.markdown("<div style='border-left: 2px solid #FFF; height: 100px;'></div>", unsafe_allow_html=True)

    with col7:
        total_wick = df1[df1["isWicketDelivery"] == 1]["bowler"].value_counts().sum()
        st.markdown("##### :green[Wickets]")
        st.header(total_wick)

    st.markdown("****")

    most_3 = functions.most_threes(df1)
    fig = px.scatter(most_3, x="batter", y='count', size="count", size_max=60, color=most_3["count"])
    fig.update_xaxes(tickangle=45)
    for i, value in enumerate(most_3['count']):
        fig.add_annotation(
            x=most_3['batter'][i],
            y=value,
            text=str(value), showarrow=False, bgcolor="black")
    fig.update_layout(title="Most 3s by a Batsman 2008-2022", title_x=0.4, title_y=1, width=900, height=400)
    fig.update_traces(marker_color="red", marker_line_color='black', marker_line_width=2, opacity=1)
    st.plotly_chart(fig)

    st.markdown("****")

    dots = functions.dot_balls(df1)
    fig = px.funnel(dots, y="batter", x="count")
    fig.update_xaxes(tickangle=45)
    fig.update_layout(title="Most dot balls by a batsman 2008-2022", title_x=0.4, title_y=1, width=900, height=450)
    fig.update_traces(marker_color="#2E8B57", marker_line_color='black', marker_line_width=2, opacity=1)
    st.plotly_chart(fig)

    st.markdown("****")
    st.markdown("<center><font size='6'><b>All Teams runs per over</b></font></center>", unsafe_allow_html=True)
    st.markdown("")
    st.markdown("")
    mask = df1["batsman_run"] >= 1
    six = df1[mask]
    pt = six.pivot_table(index="overs", columns="BattingTeam", values="batsman_run", aggfunc="sum")
    fig, ax = plt.subplots(figsize=(20, 20))
    ax = sns.heatmap(pt, annot=True, linewidth=.5, fmt='.5g')
    st.pyplot(fig)
    st.markdown("****")

    merd_df = pd.merge(df1, df2, how='inner', on='ID')
    total_10_scores = merd_df.groupby(["ID", "batter"])["batsman_run"].sum().reset_index()
    high_score = total_10_scores[["batter", "batsman_run"]]
    high_score = high_score.sort_values("batsman_run", ascending=False).reset_index().head(10)
    fig = px.scatter(high_score, x="batter", y="batsman_run", color="batter", size="batsman_run", size_max=60)
    for i, value in enumerate(high_score['batsman_run']):
        fig.add_annotation(
            x=high_score['batter'][i],
            y=value,
            text=str(value), showarrow=False, bgcolor="black")
    fig.update_layout(title="Top 10 Highest scorers in IPL", title_x=0.3, title_y=0.95, width=1000, height=500)
    st.plotly_chart(fig)
    st.markdown("<center><font size='6'><b>All Teams sixes per over</b></font></center>", unsafe_allow_html=True)
    st.markdown("")
    st.markdown("")
    mask = df1["batsman_run"] == 6
    six = df1[mask]
    pt = six.pivot_table(index="overs", columns="BattingTeam", values="batsman_run", aggfunc="count")
    fig, ax = plt.subplots(figsize=(20, 20))
    ax = sns.heatmap(pt, annot=True, linewidth=.5, fmt='.5g')
    st.pyplot(fig)
