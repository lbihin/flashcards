import logging
from typing import List

from src.db.tables import (
    Card,
    Theme,
    add_row,
    count_rows,
    delete_row,
    get_all_rows,
    get_row_by_id,
    get_rows_by,
    update_row,
)


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
    """Get all cards by theme.
    :param id_theme: The ID of the theme.
    """
    return get_rows_by(table=Card, id_theme=id_theme)


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
