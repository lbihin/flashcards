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

if stats:
    # Préparer les données pour les graphiques
    data = [
        {
            "date": stat.date,
            "bonnes_reponses": stat.bonnes_reponses,
            "mauvaises_reponses": stat.mauvaises_reponses,
        }
        for stat in stats
    ]

    # Graphique circulaire (pie chart)
    pie_data = {
        "Réponses": ["Bonnes réponses", "Mauvaises réponses"],
        "Nombre": [
            sum(d["bonnes_reponses"] for d in data),
            sum(d["mauvaises_reponses"] for d in data),
        ],
    }
    pie_fig = px.pie(
        pie_data,
        names="Réponses",
        values="Nombre",
        title="Répartition des réponses",
        color="Réponses",
        color_discrete_map={"Bonnes réponses": "green", "Mauvaises réponses": "red"},
    )
    pie_fig.update_layout(
        legend=dict(orientation="h", yanchor="top", y=-0.2, xanchor="center", x=0.5)
    )

    # Graphique linéaire (line chart)
    line_fig = px.line(
        data,
        x="date",
        y=["bonnes_reponses", "mauvaises_reponses"],
        labels={"value": "Nombre de réponses", "variable": "Type de réponse"},
        title="Évolution des réponses par date",
        color_discrete_map={"bonnes_reponses": "green", "mauvaises_reponses": "red"},
    )
    # line_fig.update_layout(
    #     legend=dict(orientation="h", yanchor="top", y=-0.2, xanchor="center", x=0.5)
    # )
    line_fig.update_xaxes(
        tickangle=45,  # Incline les étiquettes à 45 degrés
        tickformat="%Y-%m-%d",  # Affiche uniquement les dates (année-mois-jour)
        title_text="Date",  # Ajoute un titre à l'axe X
    )

    c_pie, c_scatter = st.columns((2, 3))
    c_pie.plotly_chart(pie_fig, use_container_width=True)
    c_scatter.plotly_chart(line_fig, use_container_width=True)
else:
    st.write("Aucune donnée disponible pour la période sélectionnée.")
