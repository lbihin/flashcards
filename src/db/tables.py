import logging
import os

from sqlalchemy import (
    Column,
    Date,
    Float,
    ForeignKey,
    Integer,
    String,
    text,
    CheckConstraint,
)
import sqlalchemy
from sqlalchemy.exc import SQLAlchemyError
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

                except SQLAlchemyError as e:
                    session.rollback()
                    logging.error(
                        f"An error occured during the insertion of predefined themes: {e}"
                    )
                except Exception as e:
                    session.rollback()
                    logging.error(
                        f"An unexpected error occured during the insertion of predefined themes: {e}"
                    )

    except SQLAlchemyError as e:
        logging.error(f"An error occured during table creation: {e}")
    except Exception as e:
        logging.error(
            f"An unexpected error occured during database initialization: {e}"
        )


def get_session(func):
    """Decorator to create a session context and handle exceptions."""

    def wrapper(*args, **kwargs):
        with config.get_session() as session:
            try:
                return func(*args, session=session, **kwargs)
            except SQLAlchemyError as e:
                session.rollback()
                logging.error(f"An error occured while execution on the database: {e}")
            except Exception as e:
                session.rollback()
                logging.error(f"Unexpected error occured: {e}")

    return wrapper


@get_session
def add_row(table, **kwargs):
    """Add a row to a table.
    :param session: The database session.
    :param table: The table to add the row to.
    :param kwargs: The row data."""
    session = kwargs.pop("session")  # type: sqlalchemy.orm.session.Session
    new_row = table(**kwargs)
    session.add(new_row)
    session.commit()
    session.refresh(new_row)
    logging.debug(f"Row {new_row.id} in table '{table.__tablename__}' created")
    return new_row


@get_session
def get_row_by_id(table, id, **kwargs):
    """Get a row by its ID or other filters.
    :param table: The table to query.
    :param id: The ID of the row (optional).
    :param kwargs: Additional filters."""
    session = kwargs.pop("session")  # type: sqlalchemy.orm.session.Session
    logging.debug(f"Retrieve row in table '{table.__tablename__}' with id={id}.")
    row = session.query(table).filter_by(id=id).first()
    if row is None:
        logging.debug(
            f"Row in table '{table.__tablename__}' with filters: id={id}, {kwargs} not found"
        )
    return row


@get_session
def get_rows_by(table, **kwargs):
    """Get rows from a table by filters.
    :param session: The database session.
    :param table: The table to query.
    :param kwargs: Filters for the query."""
    session = kwargs.pop("session")  # type: sqlalchemy.orm.session.Session
    logging.debug(
        f"Retrieve row in table '{table.__tablename__}' with filters: {kwargs}."
    )
    query = session.query(table)
    if not kwargs:
        raise ValueError("Filter condition in kwargs is missing")
    query = query.filter_by(**kwargs)
    row = query.all()
    if row is None:
        logging.debug(
            f"Row in table '{table.__tablename__}' with filters: {kwargs} not found"
        )
    return row


@get_session
def update_row(table, id, **kwargs):
    """Update a row in a table.
    :param session: The database session.
    :param table: The table to update the row in.
    :param id: The ID of the row to update.
    :param kwargs: The updated row data."""
    session = kwargs.pop("session")  # type: sqlalchemy.orm.session.Session
    row = session.query(table).filter_by(id=id).first()
    if row is not None:
        for key, value in kwargs.items():
            setattr(row, key, value)
        session.commit()
        session.refresh(row)
        logging.debug(f"Row in table '{table.__tablename__}' with id={id} updated")
        return row
    logging.error(
        f"Row in table '{table.__tablename__}' with id={id} not found for update"
    )


@get_session
def delete_row(table, id, **kwargs):
    """Delete a row from a table.
    :param session: The database session.
    :param table: The table to delete the row from.
    :param id: The ID of the row to delete."""
    session = kwargs.pop("session")  # type: sqlalchemy.orm.session.Session
    row = session.query(table).filter_by(id=id).first()
    session.delete(row)
    session.commit()
    logging.debug(f"Row {id} in table '{table.__tablename__}' deleted")


@get_session
def get_all_rows(table, **kwargs):
    """Get all rows from a table.
    :param session: The database session.
    :param table: The table to query."""
    session = kwargs.pop("session")  # type: sqlalchemy.orm.session.Session
    logging.debug(f"Retrieve all rows in table '{table.__tablename__}'.")
    return session.query(table).all()


@get_session
def count_rows(table, **kwargs):
    """Count the number of rows in a table.
    :param session: The database session.
    :param table: The table to count the rows of."""
    session = kwargs.pop("session")  # type: sqlalchemy.orm.session.Session
    logging.debug(f"Count rows in table '{table.__tablename__}'.")
    return session.query(table).count()
