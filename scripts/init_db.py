# scripts/init_db.py
import os
from db.session import SessionLocal, engine
from db.models import Base
from db.migrations.init_db import run_migrations

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    run_migrations()
    print("[DB] Initialized & migrated.")