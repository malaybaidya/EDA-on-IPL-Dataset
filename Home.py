import streamlit as st
import streamlit.components.v1 as stc

st.set_page_config(
    page_title="Home",
)
st.sidebar.success("select a demo above")
html_temp = """
			<div style="background-color:#8A9A5B;padding:10px;border-radius:10px">
			<h1 style="color:white;text-align:center;"> The Exploratory Data Analysis on the IPL dataset</h1>
			
			</div>
			"""
stc.html(html_temp)
st.image(
    'https://upload.wikimedia.org/wikipedia/en/thumb/8/84/Indian_Premier_League_Official_Logo.svg/1200px-Indian_Premier_League_Official_Logo.svg.png')

st.write("""
			
##### 1.Conducted in-depth analysis of the IPL dataset (a large dataset of over 200,000 rows) to uncover trends and patterns related to team performance, player statistics, match outcomes, etc.
##### 2.Utilized Python libraries like Pandas, Matplotlib, and Seaborn for data manipulation and visualization.
##### 3.Created visualizations (e.g., bar plots, heatmaps, histograms) to present findings on player performance and match trends.
##### 4.Used machine learning techniques (e.g., Logistic Regression, Random Forest) to build and evaluate the win probability predictor, achieving a competitive accuracy.

				""")