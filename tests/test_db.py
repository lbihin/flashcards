import os
import pytest
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker
from src.db.entities import Theme, init_db, DATABASE_PATH

from pytest_bdd import scenarios, given, when, then

# Load the feature file
scenarios('test_db.feature')

@pytest.fixture
def engine():
    return create_engine(f'sqlite:///{DATABASE_PATH}')

@pytest.fixture
def session(engine):
    Session = sessionmaker(bind=engine)
    return Session()

@given('the database does not exist')
def remove_database():
    if os.path.exists(DATABASE_PATH):
        os.remove(DATABASE_PATH)

@given('the database path is invalid')
def invalid_database_path(monkeypatch):
    invalid_path = DATABASE_PATH.replace('flashcards.db', 'invalid.db')
    monkeypatch.setattr('src.db.entities.DATABASE_PATH', invalid_path)

@given('a theme with a duplicate name exists')
def duplicate_theme(session):
    theme = Theme(theme="Math")
    session.add(theme)
    session.commit()

@when('the init_db function is called')
def call_init_db():
    init_db()

@when('the init_db function is called again')
def call_init_db_again():
    init_db()

@then('the database and tables should be created')
def check_tables_created(engine):
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    assert 'cards' in tables

@then('predefined themes should be inserted')
def check_predefined_themes(session):
    themes = session.query(Theme).all()
    assert len(themes) > 0

@then('an error should be logged')
def check_error_logged(caplog):
    assert any(record.levelname == 'ERROR' for record in caplog.records)
