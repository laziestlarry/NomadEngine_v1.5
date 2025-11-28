from db.engine import init_engine
from db.session import create_session
from db.models import Blueprint

session = create_session(init_engine())

bp = Blueprint(
    title="YouTube Transcript → Summary → Package",
    source="test",
    status="new",
    strategy={
        "steps": [
            {"name": "download transcript"},
            {"name": "summarize transcript"},
            {"name": "generate audio"},
            {"name": "export package"},
            {"name": "log income"},
        ]
    },
)
session.add(bp)
session.commit()

print(f"Blueprint #{bp.id} seeded.")