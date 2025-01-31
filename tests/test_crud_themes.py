# Load the feature file
import pytest
from pytest_bdd import given, scenarios, then, when

from src.db import config
from src.db.config import setup_config
from src.db.entities import Theme, init_db
from src.db.services import create_theme


scenarios("features/crud_themes.feature")


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


@when('a new theme is created with name "Science"', target_fixture="theme_created")
def create_new_theme(session):
    return create_theme("Science")


@then('the theme "Science" should be present in the database')
def check_theme_created(session):
    retrieved_theme = session.query(Theme).filter_by(theme="Science").first()
    assert retrieved_theme is not None
    assert retrieved_theme.theme == "Science"
    assert retrieved_theme.id is not None
    assert retrieved_theme.id > 0


@given('a theme exists with name "Math"', target_fixture="existing_theme")
def ensure_theme_exists(session):
    return session.query(Theme).filter_by(theme="Math").first()


@when('a new theme is created with name "Math"')
def create_existing_theme():
    return create_theme("Math")


@then("an error should be logged indicating the theme already exists")
def check_theme_already_exists(caplog):
    assert any(
        record.levelname == "ERROR" and "Theme 'Math' already exists" in record.message
        for record in caplog.records
    )
