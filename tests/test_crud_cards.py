import pytest
from pytest_bdd import given, scenarios, then, when

from src.db import config
from src.db.config import setup_config
from src.db.services import (
    create_card,
    delete_card,
    get_all_cards,
    get_card,
    get_cards_by_theme,
    get_number_of_cards,
    update_card,
)
from src.db.tables import Card, init_db

# Load the feature file
scenarios("features/crud_cards.feature")


@pytest.fixture
def session():
    # Use an in-memory database for tests
    TEST_DATABASE_URL = ":memory:"  # In-memory database
    setup_config(TEST_DATABASE_URL)

    init_db()  # Initialize the in-memory database for each test
    with config.get_session() as session:
        yield session
    # No need to explicitly delete for in-memory database


@given(
    "the database is initialized", target_fixture="init_database"
)  # Inject the session
def initialize_database():
    # Database is already initialized by the session fixture
    pass  # Nothing to do here


@when(
    'a new card is created with question "What is Python?", answer "A programming language", probability 0.5 and theme ID 2',
    target_fixture="card_created",
)
def create_new_card(session):
    return create_card("What is Python?", "A programming language", 0.5, 2)


@then("the card should be present in the database")
def check_card_present(session, card_created):
    retrieved_card = (
        session.query(Card).filter_by(question=card_created.question).first()
    )
    assert retrieved_card is not None
    assert retrieved_card.reponse == card_created.reponse


@given(
    'a card exists with question "What is Python?", answer "A programming language", probability 0.5 and theme ID 2',
    target_fixture="existing_card",
)
def ensure_card_exists():
    return create_card("What is Python?", "A programming language", 0.5, 2)


@when("the card is retrieved by its id", target_fixture="retrieved_card")
def retrieve_card(existing_card):
    return get_card(existing_card.id)


@then('the card should have the answer "A programming language"')
def check_card_answer(retrieved_card):
    assert retrieved_card.reponse == "A programming language"


@when('the card\'s answer is updated to "A snake"')
def update_card_answer(existing_card):
    update_card(existing_card.id, "What is Python?", "A snake", 0.5, 2)


@then('the card should have the updated answer "A snake"')
def check_updated_card_answer(existing_card):
    updated_card = get_card(existing_card.id)
    assert updated_card.reponse == "A snake"


@when("the card is deleted by ID", target_fixture="deleted_card_id")
def delete_card_by_id(existing_card):
    delete_card(existing_card.id)
    return existing_card.id


@then("the card should not be present in the database")
def check_card_not_present_by_id(session, deleted_card_id):
    card = session.query(Card).filter_by(id=deleted_card_id).first()
    assert card is None


@given("3 cards exist", target_fixture="three_cards")
def ensure_multiple_cards_exist(session):
    create_card(
        question="What is Python?",
        reponse="A programming language",
        probabilite=0.5,
        id_theme=2,
    )
    create_card(
        question="What is SQL?", reponse="A query language", probabilite=0.5, id_theme=2
    )
    create_card(
        question="What is Git?",
        reponse="A version control system",
        probabilite=0.5,
        id_theme=2,
    )


@when("all cards are retrieved", target_fixture="retrieved_cards")
def retrieve_all_cards():
    cards = get_all_cards()
    return cards


@then("3 cards are retrieved")
def check_retrieved_card(retrieved_cards):
    assert len(retrieved_cards) == 3


@when("the number of cards is retrieved", target_fixture="number_of_cards")
def retrieve_number_of_cards(session):
    number = get_number_of_cards()
    return number


@then("the number of cards should be 3")
def check_number_of_cards(number_of_cards):
    assert number_of_cards == 3


@given("2 cards exist with theme ID 1", target_fixture="two_theme_cards")
def ensure_multiple_cards_exist_with_theme(session):
    cards = [
        Card(
            question="What is Python?",
            reponse="A programming language",
            probabilite=0.5,
            id_theme=1,
        ),
        Card(
            question="What is SQL?",
            reponse="A query language",
            probabilite=0.5,
            id_theme=1,
        ),
    ]
    session.add_all(cards)
    session.commit()
    return cards


@when("the cards are retrieved by theme ID 1", target_fixture="retrieved_theme_cards")
def retrieve_cards_by_theme(session):
    cards = get_cards_by_theme(1)
    return cards


@then("the number of cards should be 2")
def check_number_of_cards_by_theme(retrieved_theme_cards):
    assert len(retrieved_theme_cards) == 2
