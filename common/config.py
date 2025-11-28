import os
from pathlib import Path

ROOT = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

DB_PATH = ROOT / "storage" / "nomad.db"

API_PORT = int(os.getenv("NOMAD_API_PORT", 9000))