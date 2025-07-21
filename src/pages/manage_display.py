import datetime

import plotly.express as px
import streamlit as st

from src.db import services

TODAY = "Aujourd´hui"
LAST_5_DAY = "5 derniers jours"
LAST_MONTH = "Dernier mois"
THIS_YEAR = "Cette année"
PERIODS = [TODAY, LAST_5_DAY, LAST_MONTH, THIS_YEAR]

st.title("Rapport d´activité")
st.divider()


period_selection = st.segmented_control("Selectionner une période:", PERIODS)

today = datetime.datetime.today()
datetime.timedelta()

if period_selection == TODAY:
    start_date, end_date = today, today
elif period_selection == LAST_5_DAY:
    start_date, end_date = today - datetime.timedelta(days=5), today
elif period_selection == LAST_MONTH:
    start_date, end_date = today - datetime.timedelta(days=30), today
elif period_selection == THIS_YEAR:
    start_date, end_date = today - datetime.timedelta(days=365), today
else:
    start_date, end_date = None, None

stats = services.get_stats(start_date=start_date, end_date=end_date)


def prepare_data(stats):
    data = [
        {
            "date": stat.date,
            "bonnes_reponses": stat.bonnes_reponses,
            "mauvaises_reponses": stat.mauvaises_reponses,
        }
        for stat in stats
    ]
    pie_data = {
        "Réponses": ["Bonnes réponses", "Mauvaises réponses"],
        "Nombre": [
            sum(d["bonnes_reponses"] for d in data),
            sum(d["mauvaises_reponses"] for d in data),
        ],
    }
    return data, pie_data


if stats:
    # Préparer les données pour les graphiques
    data, pie_data = prepare_data(stats)

    COLOR_MAP = {"Bonnes réponses": "green", "Mauvaises réponses": "red"}

    # Graphique circulaire (pie chart)
    pie_fig = px.pie(
        pie_data,
        names="Réponses",
        values="Nombre",
        title="Répartition des réponses",
        color="Réponses",
        color_discrete_map=COLOR_MAP,
    )
    pie_fig.update_layout(
        legend=dict(orientation="h", yanchor="top", y=-0.2, xanchor="center", x=0.5)
    )

    # Préparer les données pour le graphique linéaire avec des noms correspondant à COLOR_MAP
    line_data = [
        {
            "date": d["date"],
            "Type de réponse": "Bonnes réponses",
            "Nombre": d["bonnes_reponses"],
        }
        for d in data
    ] + [
        {
            "date": d["date"],
            "Type de réponse": "Mauvaises réponses",
            "Nombre": d["mauvaises_reponses"],
        }
        for d in data
    ]

    # Graphique linéaire (line chart)
    line_fig = px.line(
        line_data,
        x="date",
        y="Nombre",
        color="Type de réponse",
        labels={"Nombre": "Nombre de réponses", "Type de réponse": "Type de réponse"},
        title="Évolution des réponses par date",
        color_discrete_map=COLOR_MAP,
    )

    line_fig.update_xaxes(
        tickangle=45,
        tickformat="%Y-%m-%d",
        title_text="Date",
    )

    c_pie, c_scatter = st.columns((2, 3))
    c_pie.plotly_chart(pie_fig, use_container_width=True)
    c_scatter.plotly_chart(line_fig, use_container_width=True)
else:
    st.warning(
        "Aucune donnée n'a été trouvée pour la période sélectionnée. Essayez une autre période."
    )
