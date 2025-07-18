import logging

import pandas as pd
import streamlit as st

from src.db import services

# ---- session state ----
if "config_selected_card" not in st.session_state:
    st.session_state.config_selected_card = None

if "all_themes" not in st.session_state:
    st.session_state.all_themes = []

if "theme_lookup" not in st.session_state:
    st.session_state.theme_lookup = dict()


def reset():
    st.session_state.config_selected_card = None
    st.session_state.all_themes = services.get_all_themes()
    st.session_state.theme_lookup = {
        obj.theme: obj.id for obj in st.session_state.all_themes
    }
    st.rerun()


def cards_to_dataframe(cards: list) -> pd.DataFrame:
    """Convert a list of Card objects to a pandas DataFrame."""
    # Convert each Card object to a dictionary using the `to_dict` method
    data = [card.to_dict() for card in cards]
    # Create a DataFrame from the list of dictionaries
    return pd.DataFrame(data)


def _common_card_form(
    question_text: str = "", reponse_text: str = "", proba_slider: float = 0.5
):
    question = st.text_input("La question:", question_text)
    reponse = st.text_input("La réponse", reponse_text)
    proba = st.slider(
        "Probabilité d´occurence",
        min_value=0.1,
        value=proba_slider,
        max_value=0.9,
        step=0.1,
    )
    return question, reponse, proba


def display_new_card_form():
    with st.form("new_card_form", clear_on_submit=True):
        options = [th.theme for th in st.session_state.all_themes]
        selected_theme = st.selectbox("Le thème", options=options)
        question, reponse, proba = _common_card_form()

        if st.form_submit_button("Ajouter"):
            logging.info(f"Request to add new card")
            id_theme = st.session_state.theme_lookup[selected_theme]
            services.create_card(
                question=question,
                reponse=reponse,
                probabilite=proba,
                id_theme=id_theme,
            )
            reset()


def display_card_details():

    card = st.session_state.config_selected_card

    with st.form("card_detail_form"):

        question, reponse, proba = _common_card_form(
            question_text=card.question,
            reponse_text=card.reponse,
            proba_slider=card.probabilite,
        )

        col_btn_update, col_btn_delete = st.columns(2)
        with col_btn_update:
            if st.form_submit_button("Actualiser"):
                logging.info(f"Request to update card(id={card.id})")
                services.update_card(
                    id=card.id,
                    question=question,
                    reponse=reponse,
                    probabilite=proba,
                    id_theme=card.theme.id,
                )

                # Reset the configuration
                reset()

        with col_btn_delete:
            if st.form_submit_button("Supprimer"):
                logging.info(f"Request to delete card(id={card.id})")
                services.delete_card(card.id)
                reset()


def display_flascard(id_theme: int):
    logging.debug("Start to display flascard.")
    cards = services.get_cards_by_theme(id_theme=id_theme)
    if not cards:
        st.warning("Aucune flascards pour le thème sélectionné...")
        st.stop()

    # Convertir les cartes en DataFrame
    header_cols = st.columns((5, 5, 5, 2))  # Ajuster les proportions des colonnes
    header_cols[0].write("**Question**")
    header_cols[1].write("**Réponse**")
    header_cols[2].write("**Occurence (en %)**")

    for card in cards:
        with st.container():
            cols = st.columns((5, 5, 5, 2))  # Ajuster les proportions des colonnes
            cols[0].write(card.question)
            cols[1].write(card.reponse)
            cols[2].write(round(100 * card.probabilite))
            if cols[3].button("Modifier", key=f"modify_btn_{card.id}"):
                st.session_state.config_selected_card = (
                    card  # Stocker la carte sélectionnée
                )
                logging.info(f"Card avec id={card.id}")


def display_theme_form():
    with st.sidebar:
        with st.form("add_therme"):
            new_theme = st.text_input("Ajouter un theme")
            if st.form_submit_button("Ajouter"):
                services.create_theme(theme=new_theme)
                reset()
            options = [th.theme for th in st.session_state.all_themes]
            selected_theme = st.selectbox("Supprimer un theme", options=options)
            if st.form_submit_button("Supprimer"):
                theme_id = st.session_state.theme_lookup[selected_theme]
                services.delete_theme(id_theme=theme_id)
                reset()


# Page layout
st.title("Configurer les flashcards")


# affiche les themes
st.session_state.all_themes = services.get_all_themes()
st.session_state.theme_lookup = {
    obj.theme: obj.id for obj in st.session_state.all_themes
}

with st.expander("Ajouter une question"):
    display_new_card_form()

display_theme_form()

c_data, c_config = st.columns((3, 2))


with c_data:
    options = [th.theme for th in st.session_state.all_themes]
    selection = st.pills(
        "Sélectionner le thème à afficher",
        options,
        selection_mode="single",
        default=options[0],
    )
    if selection is None:
        st.warning("Aucun Thème n´est présent dans la banque de donnée...")
        st.stop()

    display_flascard(st.session_state.theme_lookup[selection])

if st.session_state.config_selected_card:
    with c_config:
        display_card_details()
