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
    CheckConstraint,
)
from sqlalchemy.exc import IntegrityError, OperationalError
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

from src.db import config


Base = declarative_base()



# Define the tables
class Card(Base):
    __tablename__ = "cards"

    id = Column(Integer, primary_key=True)
    question = Column(String)
    reponse = Column(String)
    probabilite = Column(Float)
    id_theme = Column(Integer, ForeignKey("themes.id", ondelete="RESTRICT"))

    theme = relationship("Theme", back_populates="cards")

    __table_args__ = (
        CheckConstraint(
            "probabilite >= 0.1 AND probabilite <= 1", name="probabilite_range"
        ),
    )


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
    """Initialize the database.
    :param path: The path to the database file."""

    if config.DATABASE_PATH != ":memory:":  # Skip for in-memory database
        # Ensure the directory exists
        os.makedirs(os.path.dirname(config.DATABASE_PATH), exist_ok=True)


    # if _engine_initialized
    # if _engine_initialized and config.DATABASE_PATH != ":memory:":  # Vérification supplémentaire pour in memory
    #     # Si l'engine a déjà été initialisé, comparer le path
    #     current_engine_path = config.engine.url.database
    #     if current_engine_path != config.DATABASE_PATH:
    #         raise ValueError(
    #             "Cannot change database path after initialization.  "
    #             f"Current: {current_engine_path}, Requested: {config.DATABASE_PATH}"
    #         )
    #     return

    # if config.DATABASE_PATH != ":memory:":  # Vérification du path pour in memory
    #     parent_dir = os.path.dirname(config.DATABASE_PATH)
    #     if not os.path.exists(parent_dir):
    #         raise ValueError(f"Parent directory does not exist: {parent_dir}")

    try:
        # Connect to the database
        with config.engine.connect() as conn:
            if conn.dialect.name == "sqlite":
                conn.execute(text("PRAGMA foreign_keys = ON;"))

            Base.metadata.create_all(conn)  # Use config.engine here

            Session = sessionmaker(bind=config.engine)  # and here
            with Session() as session:  # Use context manager
                try:
                    themes = [
                        Theme(theme=theme)
                        for theme in ["Math", "Programming Language", "Git"]
                    ]
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

    except OperationalError as e:
        logging.error(f"An error occured during table creation: {e}")
    except Exception as e:
        logging.error(
            f"An unexpected error occured during database initialization: {e}"
        )
