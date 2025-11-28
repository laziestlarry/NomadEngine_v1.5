#!/usr/bin/env python
"""
demo_youtube_pipeline.py

Usage (from project root):

    PYTHONPATH=$(pwd) python scripts/demo_youtube_pipeline.py /path/to/transcript.txt

What it does:

1. Reads a transcript text file.
2. Builds an opportunity description (summarised).
3. Uses AceStrategy to classify & constitution-check the opportunity.
4. If allowed, creates a Blueprint row in the DB.
5. Emits events so you can see everything in /events/recent and /system/status.
"""

import sys
from pathlib import Path
from typing import Optional

from core.paths import ensure_sys_path
ensure_sys_path()

from db.engine import init_engine
from db.session import create_session
from db.models import Blueprint
from events.event_bus import EventBus
from ace.strategy import AceStrategy


def load_transcript(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def compress_text(text: str, max_chars: int = 2000) -> str:
    """Simple truncation-based 'summary' for now."""
    text = text.strip()
    if len(text) <= max_chars:
        return text
    return text[: max_chars - 100] + "\n\n...[truncated for Nomad demo]"


def create_blueprint_if_allowed(
    session,
    event_bus: EventBus,
    description: str,
    transcript_path: Path,
    source_label: str = "youtube_transcript_demo",
) -> Optional[int]:
    ace = AceStrategy(session, event_bus)

    decision = ace.evaluate_opportunity(
        description=description,
        source="youtube",
        context={"transcript_path": str(transcript_path)},
    )

    if not decision["allowed"]:
        print("\n[ACE] Opportunity did NOT pass constitutional checks.")
        print("Details:", decision["constitution_check"])
        return None

    # Create a simple blueprint row
    strategy = {
        "origin": "youtube_transcript_demo",
        "transcript_path": str(transcript_path),
        "scores": decision["scores"],
        "draft_steps": [
            "Extract high-value angles from transcript",
            "Design 1-3 monetizable offers (service or product)",
            "Define automation options (scripts, platforms)",
            "Prepare listing / outreach copy",
            "Log first income event once realized",
        ],
    }

    bp = Blueprint(
        title=f"YouTube-derived opportunity: {description[:80]}",
        source="youtube",
        status="new",
        strategy=strategy,
    )

    session.add(bp)
    session.commit()

    event_bus.publish(
        event_type="blueprint_created",
        category="blueprint",
        message=f"Blueprint #{bp.id} created from YouTube transcript demo",
        blueprint_id=bp.id,
        payload={
            "source": "youtube_transcript_demo",
            "scores": decision["scores"],
        },
    )

    print(f"\n[Nomad] Blueprint created: ID={bp.id}")
    print("Scores:", decision["scores"])
    return bp.id


def main():
    if len(sys.argv) < 2:
        print("Usage: python scripts/demo_youtube_pipeline.py /path/to/transcript.txt")
        sys.exit(1)

    transcript_path = Path(sys.argv[1]).expanduser().resolve()
    if not transcript_path.exists():
        print(f"Transcript file not found: {transcript_path}")
        sys.exit(1)

    print(f"[Demo] Using transcript: {transcript_path}")

    raw = load_transcript(transcript_path)
    summary = compress_text(raw, max_chars=1500)

    # Simple description: first few sentences / lines
    short_desc = summary.splitlines()[0][:200]

    engine = init_engine()
    session = create_session(engine)
    bus = EventBus()

    bp_id = create_blueprint_if_allowed(session, bus, short_desc, transcript_path)

    if bp_id is None:
        print("\n[Demo] No blueprint written (filtered by ACE).")
    else:
        print(f"[Demo] You can now inspect this via API / DB: blueprint #{bp_id}")


if __name__ == "__main__":
    main()
