import os
from sqlalchemy import create_engine
from core.settings import settings

def init_engine(db_path: str = None):
    """
    Initialize a SQLite engine, creating directories if necessary.
    """
    if db_path is None:
        db_path = settings.DB_PATH

    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    engine = create_engine(
        f"sqlite:///{db_path}",
        connect_args={"check_same_thread": False},
        echo=False,
        future=True,
    )
    return engine