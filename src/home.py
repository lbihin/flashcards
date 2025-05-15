import streamlit as st

# ---- Header ----
st.set_page_config(
    page_title="Flashcard Application",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="auto",
)
st.title("Flashcard Application")

st.divider()


pages = [
    st.Page("pages/answer_flashcards.py", title="Quizz"),
    st.Page("pages/manage_flashcards.py", title="Configuration"),
    st.Page("pages/manage_display.py", title="Report"),
]

pg = st.navigation(pages=pages)
pg.run()
