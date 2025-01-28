import os
import sqlite3
import pytest
from src.db.entities import init_db, DATABASE_PATH


class TestEntities:

    @pytest.fixture
    def setup_db(self):
        # Ensure the database directory is clean before each test
        if os.path.exists(DATABASE_PATH):
            os.remove(DATABASE_PATH)
        yield
        # Clean up after each test
        if os.path.exists(DATABASE_PATH):
            os.remove(DATABASE_PATH)

    def test_init_db_creates_database(self, setup_db):
        # Act
        init_db()

        # Assert
        assert os.path.exists(DATABASE_PATH)

    def test_init_db_creates_tables(self, setup_db):
        # Act
        init_db()

        # Assert
        conn = sqlite3.connect(DATABASE_PATH)
        c = conn.cursor()

        c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='cards';")
        assert c.fetchone() is not None

        c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='themes';")
        assert c.fetchone() is not None

        c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='stats';")
        assert c.fetchone() is not None

        conn.close()

    def test_init_db_inserts_predefined_themes(self, setup_db):
        # Act
        init_db()

        # Assert
        conn = sqlite3.connect(DATABASE_PATH)
        c = conn.cursor()

        c.execute("SELECT theme FROM themes;")
        themes = c.fetchall()
        assert themes == [("Math",), ("Science",), ("History",)]

        conn.close()

    def test_db_already_exists(self, setup_db):
        # Arrange
        init_db()

        # Act (attempt to initialize the database again), No exception should be raised
        init_db()

        # Assert
        conn = sqlite3.connect(DATABASE_PATH)
        c = conn.cursor()

        c.execute("SELECT theme FROM themes;")
        themes = c.fetchall()
        assert themes == [("Math",), ("Science",), ("History",)]

        conn.close()
