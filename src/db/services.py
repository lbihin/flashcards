import logging
from datetime import datetime
from typing import List

from sqlalchemy.orm import joinedload

from src.db.tables import (
    Card,
    Stat,
    Theme,
    add_row,
    count_rows,
    delete_row,
    get_all_rows,
    get_row_by,
    get_row_by_id,
    update_row,
)

FACTEUR_PROBA_CORRECT = 0.9
FACTEUR_PROBA_INCORRECT = 1.1

# --- CRUD operations for the Card entity ---


def create_card(question: str, reponse: str, probabilite: float, id_theme: int):
    """Create a new card in the database.
    :param question: The question of the card.
    :param reponse: The answer to the question.
    :param probabilite: The probability of the card.
    :param id_theme: The ID of the theme."""
    new_card = add_row(
        table=Card,
        question=question,
        reponse=reponse,
        probabilite=probabilite,
        id_theme=id_theme,
    )
    logging.info(f"Card '{question}' created.")
    return new_card


def get_card(id: int) -> Card | None:
    """Get a card by its ID.
    :param id: The ID of the card.
    """
    return get_row_by_id(table=Card, id=id)


def update_card(
    id: int, question: str, reponse: str, probabilite: float, id_theme: int
) -> Card:
    """Update a card in the database.
    :param id: The ID of the card.
    :param question: The question of the card.
    :param reponse: The answer to the question.
    :param probabilite: The probability of the card.
    :param id_theme: The ID of the theme.
    """
    card = update_row(
        table=Card,
        id=id,
        question=question,
        reponse=reponse,
        probabilite=probabilite,
        id_theme=id_theme,
    )
    logging.info(f"Card {id} updated")
    return card


def delete_card(id: int):
    """Delete a card from the database.
    :param id: The ID of the card.
    """
    delete_row(table=Card, id=id)
    logging.info(f"Card {id} deleted")


def get_all_cards() -> List[Card]:
    """Get all cards from the database."""
    return get_all_rows(table=Card)


def get_number_of_cards() -> int:
    """Get the number of cards in the database."""
    return count_rows(table=Card)


def get_cards_by_theme(id_theme: int) -> List[Card]:
    """Get all cards by theme, with the theme relationship loaded."""
    return get_all_rows(table=Card, id_theme=id_theme, options=[joinedload(Card.theme)])


# --- CRUD operations for the Themes entity ---
def create_theme(theme: str):
    """Create a new theme in the database.
    :param theme: The theme of the card."""
    new_theme = add_row(table=Theme, theme=theme)
    logging.info(f"Theme '{theme}' created.")
    return new_theme


def get_theme(id_theme: int):
    """Get a theme by its ID.
    :param id_theme: The ID of the theme.
    """
    return get_row_by_id(table=Theme, id=id_theme)


def get_or_create_theme(name: str) -> Theme:
    """Get a theme by its name. Create it otherwise"""
    theme = get_row_by(Theme, theme=name)
    if theme is None:
        theme = create_theme(name)
    return theme


def update_theme(id_theme: int, theme: str):
    """Update a theme in the database.
    :param id_theme: The ID of the theme.
    :param theme: The theme of the card.
    """
    return update_row(table=Theme, id=id_theme, theme=theme)


def delete_theme(id_theme: int):
    """Delete a theme from the database.
    :param id_theme: The ID of the theme.
    """
    delete_row(table=Theme, id=id_theme)
    logging.info(f"Theme {id_theme} deleted")


def get_all_themes() -> List[Theme]:
    """Get all themes from the database."""
    return get_all_rows(table=Theme)


# --- operations for the Stats entity ---


def update_stats(is_correct: bool):
    """Update the statistics of the user.
    :param is_correct: Whether the user answered correctly or not."""
    # Check if the user has an entry today
    date = datetime.today().date()

    is_created = False

    if stats := get_row_by(table=Stat, date=date):
        # Update the stats
        if is_correct:
            row = update_row(
                table=Stat, id=stats.id, bonnes_reponses=stats.bonnes_reponses + 1
            )
        else:
            row = update_row(
                table=Stat, id=stats.id, mauvaises_reponses=stats.mauvaises_reponses + 1
            )
    else:
        # Create a new entry
        if is_correct:
            row = add_row(
                table=Stat, date=date, bonnes_reponses=1, mauvaises_reponses=0
            )
        else:
            row = add_row(
                table=Stat, date=date, bonnes_reponses=0, mauvaises_reponses=1
            )
        is_created = True

    return row, is_created


def update_card_probability(card_id: int, is_correct: bool):
    """Update the probability of a card.
    :param card_id: The ID of the card.
    :param is_correct: Whether the user answered correctly or not."""
    if card := get_card(card_id):
        fac = FACTEUR_PROBA_CORRECT if is_correct else FACTEUR_PROBA_INCORRECT
        new_prob = card.probabilite * fac

        # Limit the probability to be between 0.1 and 1.0
        new_prob = max(0.1, min(new_prob, 1.0))

        update_row(table=Card, id=card_id, probabilite=new_prob)
        logging.info(f"Card with ID {card_id} probability updated to {new_prob}")


def get_stats():
    """Get the statistics of the user."""
    return get_all_rows(table=Stat)
