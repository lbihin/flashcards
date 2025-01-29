from contextlib import contextmanager
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_PATH = os.path.join(os.path.expanduser("~"), ".flashcards", "flashcards.db")
engine = create_engine(f"sqlite:///{DATABASE_PATH}", echo=False)

def setup_config(path: str|None = None):
    global DATABASE_PATH
    if path is not None:  # Only update if a new path is provided
        DATABASE_PATH = path

    global engine
    if engine:  # Check if an engine already exists
        engine.dispose()
    engine = create_engine(f"sqlite:///{DATABASE_PATH}", echo=False)

@contextmanager
def get_session():
    """Provide a transactional scope around a series of operations."""
    Session = sessionmaker(bind=engine)
    with Session() as session:
        yield session