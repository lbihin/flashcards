import os
from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

global _engine_initialized

DATABASE_PATH = os.path.join(os.path.expanduser("~"), ".flashcards", "flashcards.db")
engine = None
engine_initialized = False  # Variable globale pour suivre l'état de l'engine


def setup_config(path: str | None = None):
    """Set up the configuration for the database."""
    global engine_initialized
    global DATABASE_PATH

    if engine_initialized and path != DATABASE_PATH:
        raise ValueError(
            "Cannot change database path after the engine has been initialized"
        )

    if path is not None:  # Only update if a new path is provided
        DATABASE_PATH = path

    global engine
    engine = create_engine(f"sqlite:///{DATABASE_PATH}", echo=False)
    engine_initialized = True


@contextmanager
def get_session():
    """Provide a transactional scope around a series of operations."""
    Session = sessionmaker(bind=engine)
    with Session() as session:
        yield session
