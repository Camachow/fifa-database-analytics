import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title='Players',
    page_icon='🧔',
    layout="wide"
)

df_players = st.session_state["playersData"]

clubes = df_players["club_name"].value_counts().index
club = st.sidebar.selectbox("Clube", clubes)

df_clubPlayers = df_players[df_players["club_name"] == club]

players = df_clubPlayers["long_name"].value_counts().index
player = st.sidebar.selectbox("Jogador", players)

df_playerVersions = df_players[df_players["long_name"] == player]

versions = sorted(df_playerVersions["fifa_version"].astype(int).unique(), reverse=True)
version = st.sidebar.selectbox("Versão", versions)


player_stats = df_players[(df_players["long_name"] == player) & (df_players["fifa_version"] == version)].iloc[0]

st.image(player_stats["image"])
st.title(f"{player_stats['long_name']}")

st.markdown(f"**Clube:** {player_stats['club_name']}")
st.markdown(f"**Position:** {player_stats['player_positions']}")

col1, col2, col3, col4 = st.columns(4)
col1.markdown(f"**Idade:** {player_stats['age']}")
col2.markdown(f"**Altura:** {player_stats['height_cm']/100}")
col3.markdown(f"**Peso:** {player_stats['weight_kg']}")
col4.markdown(f"**Nacionalidade:** {player_stats['nationality_name']}")

st.divider()
st.subheader(f"Overall {player_stats['overall']}")
st.progress(int(player_stats['overall']))

col1, col2, col3 = st.columns(3)
col1.metric(label="Valor de Mercado", value=(f"€ {player_stats['value_eur']:,}"))
col2.metric(label="Remuneração Semanal", value=(f"€ {player_stats['wage_eur']:,}"))
col3.metric(label="Potencial", value=(f"{player_stats['potential']}"))

#Gráfico de radar
st.subheader("Atributos")
data = {
    "Atributos": ["Pace", "Shooting", "Passing", "Dribbling", "Defending", "Physical"],
    "Valor": [player_stats["pace"], player_stats["shooting"], player_stats["passing"], player_stats["dribbling"], player_stats["defending"], player_stats["physic"]]
}

df_radar = pd.DataFrame(data)

#Criando o gráfico de radar
fig = px.line_polar(df_radar, r='Valor', theta='Atributos', line_close=True, text='Valor', color_discrete_sequence = ["green"])
fig.update_traces(fill='toself')

# Atualize o layout para mudar a cor da fonte
fig.update_layout(
    polar=dict(
        bgcolor="rgb(55, 55, 55)",
        radialaxis=dict(
            gridcolor="rgb(105, 105, 105)",
            visible=True,
            range=[0, 100],
            showticklabels=False
        ),
        angularaxis=dict(
            gridcolor="rgb(105, 105, 105)",
            visible=True,
        )
    ),
)

col1, col2 = st.columns(2)
col1.plotly_chart(fig)
col2.write(df_radar)

#Evolução do overall
df_evolucao = df_players[df_players["long_name"] == player]
df_evolucao = df_evolucao[["fifa_version", "overall"]]
df_evolucao = df_evolucao.sort_values(by="fifa_version")

fig = px.line(df_evolucao, x="fifa_version", y="overall", title=f"Evolução do Overall de {player}")
st.plotly_chart(fig)




