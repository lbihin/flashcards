import logging
import os

from sqlalchemy import (
    Column,
    Date,
    Float,
    ForeignKey,
    Integer,
    String,
    create_engine,
    text,
)
from sqlalchemy.exc import IntegrityError, OperationalError
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

# Define the location of the database
DATABASE_PATH = os.path.join(os.path.expanduser("~"), ".flashcards", "flashcards.db")

# Define the engine
engine = create_engine(f"sqlite:///{DATABASE_PATH}", echo=True)

Base = declarative_base()


# Define the tables
class Card(Base):
    __tablename__ = "cards"

    id = Column(Integer, primary_key=True)
    question = Column(String)
    reponse = Column(String)
    probabilite = Column(Float, min=0.1, max=1)
    id_theme = Column(Integer, ForeignKey("themes.id", ondelete="RESTRICT"))

    theme = relationship("Theme", back_populates="cards")


class Theme(Base):
    __tablename__ = "themes"

    id = Column(Integer, primary_key=True)
    theme = Column(String, unique=True)

    cards = relationship("Card", back_populates="theme")


class Stat(Base):
    __tablename__ = "stats"

    id = Column(Integer, primary_key=True)
    bonnes_reponses = Column(Integer)
    mauvaises_reponses = Column(Integer)
    date = Column(Date)


def init_db():
    """Initialize the database."""

    # Ensure the directory exists
    os.makedirs(os.path.dirname(DATABASE_PATH), exist_ok=True)

    try:
        # Connect to the database
        with engine.connect() as conn:
            # Enable foreign keys for SQLite
            if conn.dialect.name == "sqlite":  # Only for SQLite
                conn.execute(text("PRAGMA foreign_keys = ON;"))

            Base.metadata.create_all(conn)

            # Create a Session
            Session = sessionmaker(bind=engine)
            session = Session()

            # Insert predefined themes
            try:
                themes = [Theme(theme=theme) for theme in ["Math", "SQL", "Git"]]
                session.add_all(themes)
                session.commit()

            except IntegrityError as e:
                session.rollback()
                logging.error(
                    f"An error occured during the insertion of predefined themes: {e}"
                )
            except Exception as e:
                session.rollback()
                logging.error(
                    f"An unexpected error occured during the insertion of predefined themes: {e}"
                )
            finally:
                session.close()

    except OperationalError as e:
        logging.error(f"An error occured during table creation: {e}")
    except Exception as e:
        logging.error(
            f"An unexpected error occured during database initialization: {e}"
        )
