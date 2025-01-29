import os
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.db import config
from src.db.config import setup_config
from src.db.entities import Card, Theme, init_db
from src.db.services import (
    create_card,
    delete_card,
    get_all_cards,
    get_cards_by_theme,
    get_number_of_cards,
)

from pytest_bdd import scenarios, given, when, then

TEST_DATABASE_PATH = os.path.join(os.path.dirname(__file__), "test_flashcards.db")
setup_config(TEST_DATABASE_PATH)

# Load the feature file
scenarios("features/crud_cards.feature")

@pytest.fixture
def session():
    with config.get_session() as session:
        yield session
    if os.path.exists(TEST_DATABASE_PATH):
        os.remove(TEST_DATABASE_PATH)


# CRUD Operations Scenarios
@given("the database is initialized")
def initialize_database():
    if os.path.exists(TEST_DATABASE_PATH):
        os.remove(TEST_DATABASE_PATH)
    init_db()

@when('a new card is created with question "What is Python?", answer "A programming language", probability 0.5 and theme ID 2')
def create_new_card():
    create_card("What is Python?", "A programming language", 0.5, 2)

@then("the card should be present in the database")
def check_card_present(session):
    card = session.query(Card).filter_by(question="What is Python?").first()
    assert card is not None
    assert card.reponse == "A programming language"

@given('a card exists with ID 1, question "What is Python?", answer "A programming language", probability 0.5 and theme ID 2')
def ensure_card_exists():
    create_card("What is Python?", "A programming language", 0.5, 2)

@when('the card is retrieved by id 1')
def retrieve_card(session):
    session.card = session.query(Card).filter_by(id=1).first()

@then('the card should have the answer "A programming language"')
def check_card_answer(session):
    assert session.card.reponse == "A programming language"

@then('the card should have the updated answer "A snake"')
def check_updated_card_answer(session):
    card = session.query(Card).filter_by(id=1).first()
    assert card.reponse == "A snake"

@when('the card is deleted by ID 1')
def delete_card_by_id():
    delete_card(1)

@then("the card should not be present in the database")
def check_card_not_present_by_id(session):
    card = session.query(Card).filter_by(id=1).first()
    assert card is None

@given("3 cards exist")
def ensure_multiple_cards_exist():
    create_card(question="What is Python?", reponse="A programming language", probabilite=0.5, id_theme=2)
    create_card(question="What is SQL?", reponse="A query language", probabilite=0.5, id_theme=2)
    create_card(question="What is Git?", reponse="A version control system", probabilite=0.5, id_theme=2)

@when("all cards are retrieved")
def retrieve_all_cards(session):
    session.cards = get_all_cards()

@then("the number of cards should be 3")
def check_number_of_cards(session):
    assert len(session.cards) == 3

@when("the number of cards is retrieved")
def retrieve_number_of_cards(session):
    session.number_of_cards = get_number_of_cards()

@then("the number of cards should be 3")
def check_retrieved_number_of_cards(session):
    assert session.number_of_cards == 3

@given("2 cards exist with theme ID 1")
def ensure_multiple_cards_exist_with_theme(session):
    theme = Theme(id=1, theme="Programming")
    session.add(theme)
    cards = [
        Card(question="What is Python?", reponse="A programming language", probabilite=0.5, id_theme=1),
        Card(question="What is SQL?", reponse="A query language", probabilite=0.5, id_theme=1),
    ]
    session.add_all(cards)
    session.commit()

@when("the cards are retrieved by theme ID 1")
def retrieve_cards_by_theme(session):
    session.cards_by_theme = get_cards_by_theme(1)

@then("the number of cards should be 2")
def check_number_of_cards_by_theme(session):
    assert len(session.cards_by_theme) == 2