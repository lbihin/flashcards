import pytest
from pytest_bdd import given, scenarios, then, when, parsers

from src.db import config
from src.db.config import setup_config
from src.db.tables import Theme, init_db
from src.db.services import create_theme, delete_theme, get_theme, update_theme


scenarios("features/crud_themes.feature")


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


@when('a new theme is created with name "Science"', target_fixture="theme_created")
def create_new_theme():
    return create_theme("Science")


@then('the theme "Science" should be present in the database')
def check_theme_created(theme_created):  # Add theme_created argument
    assert theme_created is not None
    assert theme_created.theme == "Science"
    assert theme_created.id is not None


@given(
    parsers.parse('a theme exists with ID {id_theme} and name "{theme}"'),
    target_fixture="existing_theme",
)
def ensure_theme_exists_by_id_and_name(session, id_theme, theme):
    theme_obj = session.query(Theme).filter_by(theme=theme).first()
    assert theme_obj.id == int(id_theme)
    assert theme_obj.theme == theme


@when('a new theme is created with name "Math"')
def create_existing_theme():
    return create_theme("Math")


@then("an error should be logged indicating the theme already exists")
def check_theme_already_exists(caplog):
    assert any(
        record.levelname == "ERROR"
        and "An error occured while execution on the database" in record.message
        for record in caplog.records
    )


@given(parsers.parse("a theme exists with ID {id_theme}"), target_fixture="id_theme")
def ensure_theme_exists_by_id(session, id_theme):
    return session.query(Theme).filter_by(id=id_theme).first()


@when(
    parsers.parse("the theme is retrieved by ID {id_theme}"),
    target_fixture="retrieved_theme",
)
def retrieve_theme_with_id(id_theme):
    return get_theme(int(id_theme))


@then(parsers.parse("the theme with ID {id_theme} should be returned"))
def check_theme_retrieved(retrieved_theme, id_theme):
    assert retrieved_theme is not None
    assert retrieved_theme.id == int(id_theme)


@then("no theme should be returned")
def check_no_theme_retrieved(retrieved_theme):
    assert retrieved_theme is None


@when(parsers.parse('the theme with ID {id_theme} is updated to "{theme}"'))
def update_theme_with_id(id_theme, theme):
    update_theme(id_theme=id_theme, theme=theme)


@then(parsers.parse('the theme with ID {id_theme} should have the name "{theme}"'))
def check_theme_updated(session, id_theme, theme):
    theme_obj = session.query(Theme).filter_by(id=int(id_theme)).first()
    assert theme_obj.theme == theme
    assert theme_obj.id == int(id_theme)


@then(
    parsers.parse(
        "an error should be logged indicating the row in {table} with ID {id_theme} was not found"
    )
)
def check_error_theme_not_found(caplog, table, id_theme):
    assert any(
        record.levelname == "ERROR"
        and f"Row in table '{table}' with id={id_theme} not found." in record.message
        for record in caplog.records
    )


@when(parsers.parse("the theme with ID {id_theme} is deleted"))
def delete_theme_by_id(id_theme):
    delete_theme(int(id_theme))


@then(
    parsers.parse("the theme with ID {id_theme} should not be present in the database")
)
def check_theme_deleted(session, id_theme):
    theme_obj = session.query(Theme).filter_by(id=int(id_theme)).first()
    assert theme_obj is None
