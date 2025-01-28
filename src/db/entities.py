import contextlib
import logging
import os
import sqlite3

# Define the location of the database
DATABASE_PATH = os.path.join(os.path.expanduser("~"), ".flashcards", "flashcards.db")


def init_db():
    """Initialize the database."""

    # Ensure the directory exists
    os.makedirs(os.path.dirname(DATABASE_PATH), exist_ok=True)

    conn = sqlite3.connect(DATABASE_PATH)
    c = conn.cursor()
    c.execute("PRAGMA foreign_keys = ON;")

    try:
        # Create the tables
        tables = [
            """CREATE TABLE cards
            (id INTEGER PRIMARY KEY, 
            question TEXT, 
            reponse TEXT,
            probabilite REAL,
            id_theme INTEGER,
            FOREIGN KEY(id_theme) REFERENCES themes(id)
            );""",
            """CREATE TABLE themes
            (id INTEGER PRIMARY KEY,
            theme TEXT UNIQUE
            );""",
            """CREATE TABLE stats
            (id INTEGER PRIMARY KEY,
            bonnes_reponses INTEGER,
            mauvaises_reponses INTEGER,
            date DATE
            );""",
        ]
        with contextlib.suppress(sqlite3.OperationalError):
            for table in tables:
                c.execute(table)

        # Insert predefined themes
        themes = [("Math",), ("Science",), ("History",)]
        c.executemany("INSERT INTO themes (theme) VALUES (?);", themes)

    except sqlite3.IntegrityError as e:
        logging.warning(f"Integrity error occured: {e}")
    except sqlite3.Error as e:
        logging.error(f"Unexpected error occured: {e}")

    finally:
        conn.commit()
        conn.close()
