import random
from typing import TYPE_CHECKING, Optional

import streamlit as st

import src.db.services as services
from src.db.config import setup_config
from src.db.tables import Card

if TYPE_CHECKING:
    from src.db.tables import Card


if "init_db" not in st.session_state:
    st.session_state.init_db = False

if not st.session_state.init_db:
    setup_config()
    st.session_state.init_db = True

# ---- affichage local texte ou response ---
if "show_response" not in st.session_state:
    st.session_state.show_response = False

if "response_input" not in st.session_state:
    st.session_state.response_input = ""

# ---- selected themes ---
all_themes = services.get_all_themes()

if "usr_themes" not in st.session_state:
    st.session_state.usr_themes = all_themes

if len(all_themes) == 0:
    st.warning(
        "No themes available. Please create a theme first in the configuration page."
    )
    st.stop()


def update_statistics(is_correct: bool):
    services.update_stats(is_correct)
    st.toast("Les statistiques ont été actualisé avec succès!")
    reset()


def submit_response():
    st.session_state.show_response = True


@st.cache_data
def get_themes():
    return {theme.theme: theme for theme in services.get_all_themes()}


def get_card() -> Optional[Card]:
    cards = []
    for theme in st.session_state.usr_themes:
        cards.extend(services.get_cards_by_theme(theme.id))
    if cards:
        return random.choice(cards)
    return None


def reset():
    st.session_state.response_input = ""
    st.session_state.show_response = False


# ---- Main ----
st.markdown(
    """
    A simple flashcard application that allows you to create, manage, and study with flashcards.
    You can also visualize your progress and performance.
    """
)

with st.container(border=True):
    user_selection_names = [obj.theme for obj in st.session_state.usr_themes]
    user_selection_names = st.pills(
        "Sur quel sujet voulez-vous être interrogé?",
        options=[obj.theme for obj in all_themes],
        default=user_selection_names,
        selection_mode="multi",
    )

    # Update the user theme selection
    st.session_state.usr_themes = [
        theme for theme in all_themes if theme.theme in user_selection_names
    ]

    st.subheader("Question")

    # Get the question
    card = get_card()

    if card is None:
        st.warning("Aucune question disponible pour les thèmes selectionnés...")
        st.stop()

    st.info(card.question)

    if not st.session_state.show_response:
        st.text_area(
            "Votre réponse",
            placeholder="Entrez votre réponse ici...",
            height=150,
            key="response_input",  # Use a separate key for the widget
        )
        st.button(
            "Valider",
            on_click=submit_response,
            disabled=st.session_state.response_input == "",
        )
        # if st.button("Valider"):
        #     st.session_state.show_response = True

    if st.session_state.show_response:
        c_user, c_db = st.columns(2)

        with c_user:
            st.markdown(
                f"""
                <div style="background-color: #d4edda; padding: 10px; border-radius: 5px; border: 1px solid #c3e6cb;">
                    <strong>Votre réponse:</strong> <div>{st.session_state.response_input}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with c_db:
            st.markdown(
                f"""
                <div style="background-color: #fff3cd; padding: 10px; border-radius: 5px; border: 1px solid #ffeeba;">
                    <strong>La bonne réponse:</strong> <div>{card.reponse}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.write("#")
        c_header, c_oui, c_non, _ = st.columns((5, 1, 1, 11))
        c_header.subheader("Votre réponse était-elle correct?")

        c_oui.button(
            "Oui",
            use_container_width=True,
            on_click=update_statistics,
            kwargs={"is_correct": True},
        )
        c_non.button(
            "Non",
            use_container_width=True,
            on_click=update_statistics,
            kwargs={"is_correct": False},
        )


# if st.session_state.usr_answer != "":

#     usr_content_column, dbs_content_column = st.columns(2, border=True, gap="medium")

#     with usr_content_column:
#         st.write(st.session_state["usr_answer"])
#         feedback_columns = st.columns(2, gap="small")
#         feedback_columns[0].button(
#             "Yes! I´m right.",
#             icon="✅",
#             key="correct_answer",
#             use_container_width=True,
#             help="Your answer is correct",
#             on_click=update_statistics,
#             kwargs={"is_correct": True},
#         )

#         feedback_columns[1].button(
#             "Oh no! I´m wrong",
#             icon="❌",
#             key="wrong_answer",
#             use_container_width=True,
#             help="Your answer is wrong",
#             on_click=update_statistics,
#             kwargs={"is_correct": False},
#         )

#     dbs_content_column.write("PLACEHOLDER FOR ANSWER CHECKING")
