import os

import pytest
from pytest_bdd import given, scenarios, then, when
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker

from src.db import config
from src.db.config import setup_config
from src.db.entities import Card, Theme, init_db

TEST_DATABASE_PATH = os.path.join(os.path.dirname(__file__), "test_flashcards.db")
setup_config(TEST_DATABASE_PATH)

# Load the feature file
scenarios("features/init_db.feature")


@pytest.fixture
def session():
    Session = sessionmaker(bind=config.engine)
    with Session() as session:
        yield session
    if os.path.exists(TEST_DATABASE_PATH):
        os.remove(TEST_DATABASE_PATH)


# Database Initialization Scenarios
@given("the database does not exist")
def remove_database():
    if os.path.exists(TEST_DATABASE_PATH):
        os.remove(TEST_DATABASE_PATH)


@given("the database path is invalid")
def invalid_database_path(monkeypatch):
    invalid_path = TEST_DATABASE_PATH.replace("test_flashcards.db", "invalid.db")
    monkeypatch.setattr("src.db.config.DATABASE_PATH", invalid_path)


@when("the init_db function is called")
def call_init_db():
    init_db()


@when("the init_db function is called again")
def call_init_db_again():
    init_db()


@then("the database and tables should be created")
def check_tables_created():
    inspector = inspect(config.engine)
    tables = inspector.get_table_names()
    assert "cards" in tables  # Replace "cards" with the actual table name


@then("predefined themes should be inserted")
def check_predefined_themes(session):
    themes = session.query(Theme).all()
    assert len(themes) == 3


@then("an error should be logged")
def check_error_logged(caplog):
    assert any(record.levelname == "ERROR" for record in caplog.records)
