import random
from datetime import datetime, timedelta
from typing import Literal

import pytest
from pytest_bdd import given, parsers, scenarios, then, when

from src.db import config
from src.db.config import setup_config
from src.db.services import (
    create_card,
    get_card,
    get_stats,
    update_card_probability,
    update_stats,
)
from src.db.tables import Stat, add_row, count_rows, init_db

scenarios("features/stats_operations.feature")


@pytest.fixture
def session():
    # Use an in-memory database for tests
    TEST_DATABASE_URL = ":memory:"  # In-memory database
    setup_config(TEST_DATABASE_URL)

    init_db()  # Initialize the in-memory database for each test
    with config.get_session() as session:
        yield session


@given(
    "the database is initialized", target_fixture="init_database"
)  # Inject the session
def initialize_database(session):
    # Database is already initialized by the session fixture
    pass  # Nothing to do here


@given(parsers.parse("a card exists with ID {card_id} and probability {probability}"))
def ensure_card_exists(card_id, probability):
    new_card = create_card(
        question="question", reponse="reponse", probabilite=probability, id_theme=2
    )
    assert new_card.id == int(card_id)


@when(parsers.parse("the card with ID {card_id} with {is_correct} answer is updated"))
def update_card_probability_with_id(
    card_id, is_correct: Literal["correct", "incorrect"]
):
    correct = is_correct == "correct"
    update_card_probability(card_id=int(card_id), is_correct=correct)


@then(
    parsers.parse(
        "the card with ID {card_id} should have the probability {probability}"
    )
)
def check_card_probability(card_id, probability):
    retrieved_card = get_card(card_id)
    assert retrieved_card.probabilite == float(probability)


@then(
    parsers.parse(
        "an error should be logged indicating the card with ID {card_id} was not found"
    )
)
def check_error_card_not_found(caplog, card_id):
    assert any(
        record.levelname == "ERROR"
        and f"Row in table 'cards' with id={card_id} not found." in record.message
        for record in caplog.records
    )


@given(
    parsers.parse(
        "stat exist or is created and contain {positive_answer_cnt} correct answers and {negative_answer_cnt} incorrect answers"
    )
)
def ensure_stats_exists_with_predefined_answers(
    positive_answer_cnt, negative_answer_cnt
):
    stat = add_row(
        table=Stat,
        date=datetime.today(),
        bonnes_reponses=int(positive_answer_cnt),
        mauvaises_reponses=int(negative_answer_cnt),
    )
    assert stat is not None


@when(parsers.parse("the stat is updated with a {is_correct} answer"))
def check_stat_with_id(is_correct: Literal["correct", "incorrect"]):
    correct = is_correct == "correct"
    update_stats(is_correct=correct)


@then(
    parsers.parse(
        "the stat should have {positive_answer_cnt} correct answers and {negative_answer_cnt} incorrect answers"
    )
)
def check_stat_counters(session, positive_answer_cnt, negative_answer_cnt):
    stat = (
        session.query(Stat).filter_by(date=datetime.now().strftime("%Y-%m-%d")).first()
    )
    assert stat.bonnes_reponses == int(positive_answer_cnt)
    assert stat.mauvaises_reponses == int(negative_answer_cnt)


@given("the daily stat does not exist")
def ensure_no_stats_exists(session):
    stat = session.query(Stat).filter_by(date=datetime.now().date()).first()
    assert stat is None


@given(parsers.parse("{counter} stats exists"))
def ensure_stats_exists(counter):
    for i in range(int(counter)):
        date = datetime.today() - timedelta(days=i)
        add_row(
            table=Stat,
            date=date,
            bonnes_reponses=random.randint(1, 10),
            mauvaises_reponses=random.randint(1, 10),
        )
    assert count_rows(Stat) == int(counter)


@when("all stats are retrieved", target_fixture="retrieved_cards")
def retrieve_stats():
    return get_stats()


@then(parsers.parse("{exp_counter} stats are retrieved"))
def check_retrieved_stats(retrieved_cards, exp_counter):
    assert len(retrieved_cards) == int(exp_counter)
