import pytest
from pytest_bdd import given, scenarios, then, when, parsers

from src.db import config
from src.db.config import setup_config
from src.db.tables import Theme, init_db
from src.db.services import create_theme, get_theme


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


@given('a theme exists with name "Math"', target_fixture="existing_theme")
def ensure_theme_exists_by_name():
    return create_theme("Math")


@when('a new theme is created with name "Math"')
def create_existing_theme():
    return create_theme("Math")


@then("an error should be logged indicating the theme already exists")
def check_theme_already_exists(caplog):
    assert any(
        record.levelname == "ERROR" and "Theme 'Math' already exists" in record.message
        for record in caplog.records
    )


@given("a theme exists with ID 1", target_fixture="id_theme")
def ensure_theme_exists_by_id(session):
    return session.query(Theme).filter_by(id=1).first()


@when(
    parsers.parse("the theme is retrieved by ID {id_theme}"),
    target_fixture="retrieved_theme",
)
def retrieve_theme_with_id_1(session, id_theme):  # Add session argument
    return get_theme(int(id_theme))


@then(parsers.parse("the theme with ID {id_theme} should be returned"))
def check_theme_retrieved(retrieved_theme, id_theme):
    assert retrieved_theme is not None
    assert retrieved_theme.id == int(id_theme)


@then("no theme should be returned")
def check_no_theme_retrieved(retrieved_theme):
    assert retrieved_theme is None
