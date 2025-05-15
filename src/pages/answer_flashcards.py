import streamlit as st

from src.db import services


def update_statistics(is_correct: bool):
    # services.update_stats(is_correct)
    pass


def get_themes():
    themes = services.get_all_themes()
    if themes is None:
        return {}
    return {theme.theme: theme for theme in services.get_all_themes()}


# ---- Main ----
st.markdown(
    """
    A simple flashcard application that allows you to create, manage, and study with flashcards.
    You can also visualize your progress and performance.
    """
)

THEMES = get_themes()
#
if "usr_answer" not in st.session_state:
    st.session_state.usr_answer = ""

if len(THEMES) == 0:
    st.warning(
        "No themes available. Please create a theme first in the configuration page."
    )
    st.stop()

else:
    with st.container(height=600, border=True):
        with st.form(key="answer_form", clear_on_submit=True, enter_to_submit=False):
            theme = st.selectbox(
                "Which theme do you want to study?",
                options=THEMES.keys(),
                index=0,
            )

            st.subheader("Question:")
            st.write("PLACEHOLDER FOR QUESTION")
            st.session_state.usr_answer = st.text_input(
                "Your answer:", placeholder="Type your answer here..."
            )
            if not st.form_submit_button("Submit"):
                st.session_state.usr_answer = ""

        if st.session_state.usr_answer != "":

            usr_content_column, dbs_content_column = st.columns(
                2, border=True, gap="medium"
            )

            with usr_content_column:
                st.write(st.session_state["usr_answer"])
                feedback_columns = st.columns(2, gap="small")
                feedback_columns[0].button(
                    "Yes! I´m right.",
                    icon="✅",
                    key="correct_answer",
                    use_container_width=True,
                    help="Your answer is correct",
                    on_click=update_statistics,
                    kwargs={"is_correct": True},
                )

                feedback_columns[1].button(
                    "Oh no! I´m wrong",
                    icon="❌",
                    key="wrong_answer",
                    use_container_width=True,
                    help="Your answer is wrong",
                    on_click=update_statistics,
                    kwargs={"is_correct": False},
                )

            dbs_content_column.write("PLACEHOLDER FOR ANSWER CHECKING")
