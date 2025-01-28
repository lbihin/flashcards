import sqlite3


def init_db():
    """Initialize the database."""
    conn = sqlite3.connect("flashcards.db")
    c = conn.cursor()
    c.execute("PRAGMA foreign_keys = ON;")

    # Create the tables
    c.execute(
        """CREATE TABLE cards
                 (id INTEGER PRIMARY KEY, 
                 question TEXT, 
                 reponse: TEXT,
                 probabilite: REAL,
                 id_theme: INTEGER,
                 FOREIGN KEY(id_theme) REFERENCES themes(id)
                 );"""
    )

    c.execute(
        """CREATE TABLE themes
                (id INTEGER PRIMARY KEY,
                theme TEXT
                );""")

    c.execute(
        """CREATE TABLE stats
              (id INTEGER PRIMARY KEY,
               bonnes_reponses INTEGER,
               mauvaises_reponses INTEGER,
               date DATE
               );"""
    )

    # Insert predefined themes
    themes = [('Math',), ('Science',), ('History',)]
    c.executemany("INSERT INTO themes (theme) VALUES (?);", themes)

    conn.commit()
    conn.close()
