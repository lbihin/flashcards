import logging
import os
import tempfile

import pytest
from pytest_bdd import given, scenarios, then, when
from sqlalchemy.exc import OperationalError

from src.db import config
from src.db.config import setup_config
from src.db.entities import Theme, init_db

# Load the feature file
scenarios("features/database_initialization.feature")


def reset_config():
    """Reset the config before running the tests"""
    config.engine_initialized = False
    config.engine.dispose()  # Fermer la connexion
    config.engine = None

@pytest.fixture(scope="function")  # Important: Scope is function
def test_db_path():
    """Provides a path to a temporary test database file (using tempfile)."""
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as tmp_file:
        db_path = tmp_file.name
        reset_config()
    yield db_path
    os.remove(db_path)  # Clean up after the test
    


@given("the database does not exist")
def database_does_not_exist(test_db_path):
    try:
        os.remove(test_db_path)
    except FileNotFoundError:
        pass


@when("the init_db function is called")
def init_db_called(test_db_path):
    setup_config(test_db_path)  # Setup config BEFORE calling init_db
    init_db()


@then("the database and tables should be created")
def database_and_tables_created(test_db_path):
    assert os.path.exists(test_db_path)
    with config.get_session() as session:  # Use the session to check tables
        from sqlalchemy import inspect

        inspector = inspect(session.bind)
        assert inspector.has_table("cards")
        assert inspector.has_table("themes")
        assert inspector.has_table("stats")


@then("predefined themes should be inserted")
def predefined_themes_inserted(test_db_path):  # Pass test_db_path here
    setup_config(test_db_path)  # Setup config BEFORE getting the session
    with config.get_session() as session:
        theme_count = session.query(Theme).count()
        assert theme_count > 0


@given("the database path is invalid")
def database_path_invalid():
    return "/invalid/path/to/database.db"


@when("the init_db function is called with an invalid path")
def init_db_called_invalid_path(invalid_db_path):
    setup_config(invalid_db_path)
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
def database_exists(test_db_path):
    setup_config(test_db_path)
    init_db()  # Initialize the DB for the "database exists" scenarios


@when(
    "the setup_config function is called again with a different path",
    target_fixture="excinfo",
)
def setup_config_called_again_different_path(test_db_path):
    different_path = os.path.join(os.path.dirname(test_db_path), "different_db.db")
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
def no_new_themes_should_be_inserted():
    with config.get_session() as session:
        theme_count = session.query(Theme).count()
        assert theme_count == 3  # The number of themes should not increase
