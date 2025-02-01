import logging
from sqlalchemy.exc import IntegrityError
from typing import List

from src.db import config
from src.db.entities import Card, Theme


# --- CRUD operations for the Card entity ---


def create_card(question: str, reponse: str, probabilite: float, id_theme: int):
    """Create a new card in the database.
    :param question: The question of the card.
    :param reponse: The answer to the question.
    :param probabilite: The probability of the card.
    :param id_theme: The ID of the theme."""
    with config.get_session() as session:
        newCard = Card(
            question=question,
            reponse=reponse,
            probabilite=probabilite,
            id_theme=id_theme,
        )
        session.add(newCard)
        session.commit()
        logging.info(f"Card {newCard.id} created")
    return newCard


def get_card(id: int):
    """Get a card by its ID.
    :param id: The ID of the card.
    """
    with config.get_session() as session:
        return session.query(Card).filter_by(id=id).first()


def update_card(
    id: int, question: str, reponse: str, probabilite: float, id_theme: int
):
    """Update a card in the database.
    :param id: The ID of the card.
    :param question: The question of the card.
    :param reponse: The answer to the question.
    :param probabilite: The probability of the card.
    :param id_theme: The ID of the theme.
    """
    with config.get_session() as session:

        card = session.query(Card).filter_by(id=id).first()
        if card is None:
            logging.error(f"Card {id} not found")
            return
        card.question = question
        card.reponse = reponse
        card.probabilite = probabilite
        card.id_theme = id_theme

        session.commit()
        logging.info(f"Card {id} updated")
        return card


def delete_card(id: int):
    """Delete a card from the database.
    :param id: The ID of the card.
    """
    with config.get_session() as session:
        card = session.query(Card).filter_by(id=id).first()
        session.delete(card)
        session.commit()
        logging.info(f"Card {id} deleted")


def get_all_cards() -> List[Card]:
    """Get all cards from the database."""
    with config.get_session() as session:
        return session.query(Card).all()


def get_number_of_cards() -> int:
    """Get the number of cards in the database."""
    with config.get_session() as session:
        return session.query(Card).count()


def get_cards_by_theme(id_theme: int) -> List[Card]:
    """Get all cards by theme.
    :param id_theme: The ID of the theme.
    """
    with config.get_session() as session:
        return session.query(Card).filter_by(id_theme=id_theme).all()


# --- CRUD operations for the Themes entity ---
def create_theme(theme: str):
    """Create a new theme in the database.
    :param theme: The theme of the card."""
    with config.get_session() as session:
        try:
            new_theme = Theme(theme=theme)
            session.add(new_theme)
            session.commit()
            session.refresh(new_theme)
            logging.info(f"Theme '{theme}' created.")
        except IntegrityError:
            logging.error(f"Theme '{theme}' already exists.")
            return
    return new_theme


def get_theme(id_theme: int):
    """Get a theme by its ID.
    :param id_theme: The ID of the theme.
    """
    with config.get_session() as session:
        return session.query(Theme).filter_by(id=id_theme).first()
