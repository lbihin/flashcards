import streamlit as st

from src.db.config import setup_config

if "init_db" not in st.session_state:
    st.session_state.init_db = False

if not st.session_state.init_db:
    setup_config()
    st.session_state.init_db = True

# ---- Header ----
st.set_page_config(
    page_title="Flashcard Application",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="auto",
)

with st.sidebar:
    pages = [
        st.Page("pages/answer_flashcards.py", title="Quizz"),
        st.Page("pages/manage_flashcards.py", title="Configuration_old"),
        st.Page("pages/manage_temp.py", title="Configuration"),
        st.Page("pages/manage_display.py", title="Report"),
    ]

    pg = st.navigation(pages=pages)
pg.run()
