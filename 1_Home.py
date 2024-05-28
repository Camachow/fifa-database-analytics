import pandas as pd
import plotly.express as px
import streamlit as st
import webbrowser as wb
import missingno as msno
from datetime import datetime

st.set_page_config(
    page_title='Home',
    page_icon='⚽',
    layout="wide"
)

pd.set_option('display.max_columns', None)
pd.options.mode.chained_assignment = None

if "playersImages" not in st.session_state:
    df_images = pd.read_csv("FIFADataset/players-images.csv", low_memory=False, index_col=0)
    df_images = df_images[['full_name', 'image']].copy()
    st.session_state["playerImages"] = df_images

if "playersData" not in st.session_state:
    df_players = pd.read_csv("FIFADataset/male_players.csv", low_memory=False, index_col=0)
    df_players = pd.merge(df_players, df_images, left_on="long_name" , right_on="full_name", how="inner")
    #df_players = df_players[df_players["club_contract_valid_until_year"] >= datetime.today().year]
    #df_players = df_players[df_players["value_eur"] > 0]
    df_players = df_players.sort_values(by="overall", ascending = False)
    st.session_state["playersData"] = df_players

if "teamsData" not in st.session_state:
    df_teams = pd.read_csv("FIFADataset/male_teams.csv", index_col=0)
    st.session_state["teamsData"] = df_teams

if "players24Data" not in st.session_state:
    df_players24 = df_players[df_players["fifa_version"] == 24]
    st.session_state["players24Data"] = df_players24

st.write("# My EA Sports FC 24 Dataset!")
st.sidebar.markdown("Desenvolvido por [Rafael Camacho](https://www.linkedin.com/in/dev-rafael-camacho/)")

#Botão pro Kaggle
btn = st.button("Acesse os dados no Kaggle")
if btn:
    wb.open_new_tab("https://www.kaggle.com/datasets/stefanoleone992/ea-sports-fc-24-complete-player-dataset")

#Texto de introdução do projeto
st.markdown(
    """
    Context
    The datasets provided include the players data for the Career Mode from FIFA 15 to EA Sports FC 24. The data allows multiple comparisons for the same players across the last 10 versions of the videogame.


    Content:
    Every player, coach, and team available in FIFA 15, 16, 17, 18, 19, 20, 21, 22, 23, and also EA Sports FC 24

    All FIFA updates from 10th September 2015 until 22nd September 2023

    109 attributes for players, 8 attributes for coaches, and 54 attributes for teams

    URL of the scraped players, coaches, and teams

    Player positions, with the role in the club and in the national team

    Player attributes with statistics as Attacking, Skills, Defense, Mentality, GK Skills, etc.

    Player personal data like Nationality, Club, DateOfBirth, Wage, Salary, etc.

    Team data regarding their coaches, their overall value, and tactics


    Acknowledgements
    Data has been scraped from the publicly available website sofifa.com.

    As described in https://sofifa.com/robots.txt, there is no limitation at the time of scraping for collecting data for FIFA players, coaches, and teams.

    Limitations to scraping the website only relate to player comparisons and API.
    """
)