from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.engine import Engine

SessionLocal = None

def create_session(engine: Engine) -> Session:
    """
    Create a new SQLAlchemy Session from an engine.
    """
    global SessionLocal
    if SessionLocal is None:
        SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)

    return SessionLocal()