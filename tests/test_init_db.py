import os

import pytest
from pytest_bdd import given, parsers, scenarios, then, when
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.db import config
from src.db.config import setup_config
from src.db.tables import Theme, init_db

# Load the feature file
scenarios("features/database_initialization.feature")


@pytest.fixture
def session():
    # Use an in-memory database for tests
    TEST_DATABASE_URL = ":memory:"  # In-memory database
    setup_config(TEST_DATABASE_URL)

    init_db()  # Initialize the in-memory database for each test
    with config.get_session() as session:
        yield session


@given("the database does not exist")
def database_does_not_exist():
    pass  # No action needed for in-memory database


@when("the init_db function is called")
def init_db_called():
    init_db()


@then("the database and tables should be created")
def database_and_tables_created(session):
    from sqlalchemy import inspect

    inspector = inspect(session.bind)
    assert inspector.has_table("cards")
    assert inspector.has_table("themes")
    assert inspector.has_table("stats")


@then("predefined themes should be inserted")
def predefined_themes_inserted(session):
    theme_count = session.query(Theme).count()
    assert theme_count > 0


@given("the database path is invalid")
def database_path_invalid():
    return "/invalid/path/to/database.db"


@when("the init_db function is called with an invalid path")
def init_db_called_invalid_path(database_path_invalid):
    setup_config(database_path_invalid)
    with pytest.raises(ValueError) as excinfo:
        init_db()


@then("an error should be logged")
def error_should_be_logged(caplog):
    assert any(
        record.levelname == "ERROR"
        and "Parent directory for database does not exist" in record.message
        for record in caplog.records
    )


@then("a ValueError should be raised")
def value_error_should_be_raised(excinfo):
    assert "Parent directory for database does not exist" in str(excinfo.value)


@given("the database exists")
def database_exists(session):
    pass  # Database is already initialized by the session fixture


@when(
    "the setup_config function is called again with a different path",
    target_fixture="excinfo",
)
def setup_config_called_again_different_path():
    different_path = "/different/path/to/database.db"
    with pytest.raises(ValueError) as excinfo:
        setup_config(different_path)
    return excinfo


@then("a ValueError should be raised")
def cannot_change_path_value_error_raised(excinfo):
    assert "Cannot change database path" in str(excinfo.value)


@when("the init_db function is called again with the same path")
def init_db_called_again_same_path():
    init_db()


@then("no error should be raised")
def no_error_should_be_raised():
    pass  # No error expected


@then("no new themes should be inserted")
def no_new_themes_should_be_inserted(session):
    theme_count = session.query(Theme).count()
    assert theme_count == 3  # The number of themes should not increase
