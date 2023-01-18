import streamlit as st
import pandas as pd
import preprocessor,helper
import datetime as dt
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff

df = pd.read_csv('gun_violence.csv')
df = preprocessor.preprocess(df)

st.sidebar.title("Gun Crimes Analysis 2013-2022")
st.sidebar.image('image.jpg')
user_menu = st.sidebar.radio(
    'Select an Option',
    ('Total Gun Crimes','Overall Analysis','Visualize by Map','Top 10 places of crime')
)

if user_menu == 'Total Gun Crimes':
    st.sidebar.header("Total Gun Crimes")
    years,state = helper.state_year_list(df)

    selected_year = st.sidebar.selectbox("Select Year",years)
    selected_state = st.sidebar.selectbox("Select State", state)

    tally = helper.fetch_medal_tally(df,selected_year,selected_state)
    if selected_year == 'Overall' and selected_state == 'Overall':
        st.title("Overall Tally")
    if selected_year != 'Overall' and selected_state == 'Overall':
        st.title("Crimes in " + str(selected_year) + " USA")
    if selected_year == 'Overall' and selected_state != 'Overall':
        st.title(selected_state + " gun crimes")
    if selected_year != 'Overall' and selected_state != 'Overall':
        st.title(selected_state + " crimes in " + str(selected_year) + " USA")
    tally.columns = ['State','People killed', 'People injured', 'Total Victims']
    st.table(tally)

if user_menu == 'Overall Analysis':
    #editions = df['year'].unique().shape[0] - 1
    cities = df['city'].unique().shape[0]
    states = df['state'].unique().shape[0]
    people_killed = df['n_killed'].sum()
    people_injured = df['n_injured'].sum()
    victims = df['total victims'].sum()


    st.title("Top Statistics")
    st.title("")
    st.title("")
    col1,col2,col3 = st.columns(3)
    with col1:
        st.header("Cities")
        st.title(cities)
    with col2:
        st.header("States")
        st.title(states)
    with col3:
        st.header("Victims")
        st.title(victims)
    st.title("")
    st.title("")
    col1, col2 = st.columns(2)
    with col1:
        st.header("People killed")
        st.title(people_killed)
    with col2:
        st.header("People injured")
        st.title(people_injured)

    years, state = helper.state_year_list(df)
    selected_state = st.sidebar.selectbox("Select State to see year-wise crimes", state)
    if selected_state == 'Overall':
        df4 = df.groupby('year')['total victims'].sum().to_frame()
        state_over_time = df4.reset_index(level=0)
        fig = px.line(state_over_time, x='year', y='total victims')
        st.title("Crimes over the years in " + selected_state)
        st.plotly_chart(fig)
    else:
        state_over_time = helper.data_over_time(df,'state',selected_state)
        fig = px.line(state_over_time, x='year', y='total victims')
        st.title("Crimes over the years in " + selected_state)
        st.plotly_chart(fig)
        fig = px.line(state_over_time, x='year', y='total victims')
        st.title("Crime comparison in cities in  " + selected_state)
        fig = px.bar(helper.city_bar(df,selected_state), x='city', y='total victims')
        st.plotly_chart(fig)


#
if user_menu == 'Visualize by Map':

    st.sidebar.title('Visualize Map')
    st.header("Maximum people were killed in these cities")
    data =  pd.read_csv('cord.csv')
    fig = px.scatter_mapbox(data, lat="lat", lon="long", hover_name="city",
                            color_discrete_sequence=["red"], zoom=3, height=700)
    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

    st.plotly_chart(fig)

if user_menu == 'Top 10 places of crime':
    st.sidebar.title('Top 10 places of crime')
    c=['state','city']
    #c=['Top 10 dangerous cities in US','Top 10 states that need attention to their laws']
    selected_option = st.sidebar.selectbox('Select',c)
    data = helper.top_10(df,selected_option)
    if selected_option=='city':
        st.title("Top 10 dangerous cities in USA ")
    else:
        st.title("Top 10 states that need immediate attention ")

    fig = px.bar(data, x=selected_option, y='n_killed',labels={'n_killed':"Number   of   people   killed"})
    st.plotly_chart(fig)


