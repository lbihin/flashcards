import streamlit as st

# ---- Main ----
st.markdown(
    """
    A simple flashcard application that allows you to create, manage, and study with flashcards.
    You can also visualize your progress and performance.
    """
)

STATIC_THEME = "PLACEHOLDER FOR THEME"
with st.container(height=900, border=True):
    with st.form(key="answer_form", clear_on_submit=True):
        st.header(f"Theme: {STATIC_THEME}", divider=True)
        st.subheader("Question:")
        st.write("PLACEHOLDER FOR QUESTION")
        answer = st.text_input("Your answer:", placeholder="Type your answer here...")
        st.form_submit_button("Submit")

        if answer != "":
            column_1, column_2 = st.columns(2)
            column_1.write(answer)
            column_2.write("PLACEHOLDER FOR ANSWER CHECKING")

            column_1.button("Bonne réponse", key="correct_answer")
            column_2.button("Mauvaise réponse", key="wrong_answer")