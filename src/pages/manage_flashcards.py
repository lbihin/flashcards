import streamlit as st

from src.db import services

# Initialize session state for theme and card management
if "config_theme" not in st.session_state:
    st.session_state.config_theme = None

if "config_card" not in st.session_state:
    st.session_state.config_card = None

if "selected_theme_id" not in st.session_state:
    st.session_state.selected_theme_id = None

if "selected_card_id" not in st.session_state:
    st.session_state.selected_card_id = None

if "edit_mode" not in st.session_state:
    st.session_state.edit_mode = {"theme": False, "card": False}

with st.sidebar:
    with st.form("new_theme"):
        st.text_input("Ajouter un thème")
        st.form_submit_button("Ajouter")
# Callbacks
def select_theme(theme_id):
    st.session_state.selected_theme_id = theme_id
    st.session_state.selected_card_id = None
    st.session_state.edit_mode["card"] = False


def select_card(card_id):
    st.session_state.selected_card_id = card_id


def toggle_theme_edit_mode():
    st.session_state.edit_mode["theme"] = not st.session_state.edit_mode["theme"]


def toggle_card_edit_mode():
    st.session_state.edit_mode["card"] = not st.session_state.edit_mode["card"]


def reset_edit_modes():
    st.session_state.edit_mode = {"theme": False, "card": False}


def create_new_theme(theme_name):
    if theme_name:
        new_theme = services.create_theme(theme_name)
        if new_theme:
            st.success(f"Theme '{theme_name}' created successfully!")
            st.session_state.selected_theme_id = new_theme.id
            return True
    return False


def update_existing_theme(theme_id, theme_name):
    if theme_id and theme_name:
        updated_theme = services.update_theme(theme_id, theme_name)
        if updated_theme:
            st.success(f"Theme updated successfully!")
            return True
    return False


def delete_existing_theme(theme_id):
    if theme_id:
        services.delete_theme(theme_id)
        st.session_state.selected_theme_id = None
        st.session_state.selected_card_id = None
        st.success("Theme deleted successfully!")


def create_new_card(question, answer, probability, theme_id):
    if question and answer and theme_id:
        try:
            prob = float(probability)
            if prob < 0.1 or prob > 1.0:
                st.error("Probability must be between 0.1 and 1.0")
                return False

            new_card = services.create_card(question, answer, prob, theme_id)
            if new_card:
                st.success("Flashcard created successfully!")
                st.session_state.selected_card_id = new_card.id
                return True
        except ValueError:
            st.error(
                "Invalid probability value. Please enter a number between 0.1 and 1.0"
            )
    return False


def update_existing_card(card_id, question, answer, probability, theme_id):
    if card_id and question and answer and theme_id:
        try:
            prob = float(probability)
            if prob < 0.1 or prob > 1.0:
                st.error("Probability must be between 0.1 and 1.0")
                return False

            updated_card = services.update_card(
                card_id, question, answer, prob, theme_id
            )
            if updated_card:
                st.success("Flashcard updated successfully!")
                return True
        except ValueError:
            st.error(
                "Invalid probability value. Please enter a number between 0.1 and 1.0"
            )
    return False


def delete_existing_card(card_id):
    if card_id:
        services.delete_card(card_id)
        st.session_state.selected_card_id = None
        st.success("Flashcard deleted successfully!")


# Page layout
st.title("Manage Themes and Flashcards")

# Split the screen into two columns
theme_col, card_col = st.columns(2)

# THEME MANAGEMENT
with theme_col:
    st.header("Themes")

    # Get all themes
    themes = services.get_all_themes()

    # New theme creation
    with st.expander("Create New Theme", expanded=not bool(themes)):
        with st.form("new_theme_form"):
            new_theme_name = st.text_input("Theme Name")
            submit_theme = st.form_submit_button("Create Theme")

            if submit_theme:
                create_new_theme(new_theme_name)
                st.rerun()

    # Display existing themes
    if themes:
        # Create a selection container for themes
        theme_options = {theme.theme: theme.id for theme in themes}
        theme_names = list(theme_options.keys())

        selected_theme_name = st.radio(
            "Select a theme:",
            options=theme_names,
            key="theme_selector",
            on_change=lambda: select_theme(
                theme_options[st.session_state.theme_selector]
            ),
        )

        selected_theme_id = theme_options[selected_theme_name]

        # Theme management actions
        if selected_theme_id:
            col1, col2 = st.columns(2)

            with col1:
                if st.button("Edit Theme", key="edit_theme_btn"):
                    toggle_theme_edit_mode()

            with col2:
                if st.button("Delete Theme", key="delete_theme_btn"):
                    if st.session_state.selected_theme_id == selected_theme_id:
                        delete_existing_theme(selected_theme_id)
                        st.rerun()

            # Edit theme form
            if st.session_state.edit_mode["theme"]:
                with st.form("edit_theme_form"):
                    current_theme = services.get_theme(selected_theme_id)
                    updated_theme_name = st.text_input(
                        "Theme Name", value=current_theme.theme
                    )

                    col1, col2 = st.columns(2)
                    with col1:
                        cancel = st.form_submit_button("Cancel")
                        if cancel:
                            toggle_theme_edit_mode()
                            st.rerun()

                    with col2:
                        save = st.form_submit_button("Save")
                        if save:
                            if update_existing_theme(
                                selected_theme_id, updated_theme_name
                            ):
                                toggle_theme_edit_mode()
                                st.rerun()
    else:
        st.info("No themes available. Create a theme to get started.")

# CARD MANAGEMENT
with card_col:
    st.header("Flashcards")

    if st.session_state.selected_theme_id:
        selected_theme = services.get_theme(st.session_state.selected_theme_id)
        st.subheader(f"Theme: {selected_theme.theme}")

        # Get cards for the selected theme
        cards = services.get_cards_by_theme(st.session_state.selected_theme_id)

        # New card creation
        with st.expander("Create New Flashcard", expanded=not bool(cards)):
            with st.form("new_card_form"):
                new_card_question = st.text_area("Question")
                new_card_answer = st.text_area("Answer")
                new_card_probability = st.number_input(
                    "Probability", min_value=0.1, max_value=1.0, value=0.5, step=0.05
                )

                submit_card = st.form_submit_button("Create Flashcard")

                if submit_card:
                    if create_new_card(
                        new_card_question,
                        new_card_answer,
                        new_card_probability,
                        st.session_state.selected_theme_id,
                    ):
                        st.rerun()

        # Display existing cards
        if cards:
            st.write(f"Number of flashcards: {len(cards)}")

            for card in cards:
                with st.container(border=True):
                    col1, col2 = st.columns([3, 1])

                    with col1:
                        st.write(f"**Q: {card.question}**")

                    with col2:
                        if st.button("Select", key=f"select_card_{card.id}"):
                            select_card(card.id)

            # Card details and management
            if st.session_state.selected_card_id:
                selected_card = services.get_card(st.session_state.selected_card_id)

                if selected_card:
                    st.divider()
                    st.subheader("Card Details")

                    if not st.session_state.edit_mode["card"]:
                        st.write(f"**Question:** {selected_card.question}")
                        st.write(f"**Answer:** {selected_card.reponse}")
                        st.write(f"**Probability:** {selected_card.probabilite}")

                        col1, col2 = st.columns(2)
                        with col1:
                            if st.button("Edit Flashcard"):
                                toggle_card_edit_mode()
                                st.rerun()

                        with col2:
                            if st.button("Delete Flashcard"):
                                delete_existing_card(selected_card.id)
                                st.rerun()
                    else:
                        # Edit card form
                        with st.form("edit_card_form"):
                            edit_question = st.text_area(
                                "Question", value=selected_card.question
                            )
                            edit_answer = st.text_area(
                                "Answer", value=selected_card.reponse
                            )
                            edit_probability = st.number_input(
                                "Probability",
                                min_value=0.1,
                                max_value=1.0,
                                value=float(selected_card.probabilite),
                                step=0.05,
                            )

                            col1, col2 = st.columns(2)
                            with col1:
                                cancel = st.form_submit_button("Cancel")
                                if cancel:
                                    toggle_card_edit_mode()
                                    st.rerun()

                            with col2:
                                save = st.form_submit_button("Save")
                                if save:
                                    if update_existing_card(
                                        selected_card.id,
                                        edit_question,
                                        edit_answer,
                                        edit_probability,
                                        selected_card.id_theme,
                                    ):
                                        toggle_card_edit_mode()
                                        st.rerun()
        else:
            st.info(
                "No flashcards available for this theme. Create a flashcard to get started."
            )
    else:
        st.info("Select a theme to manage its flashcards.")
