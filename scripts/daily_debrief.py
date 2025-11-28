"""
Personal daily debrief script for NomadEngine v1.5.

Usage (from project root):
    python scripts/daily_debrief.py

This will print a short summary of:
- Recent income
- Task activity
- Blueprint activity
- Recent events (high level counts)
"""

import datetime as dt

from db.engine import init_engine
from db.session import create_session
from db.models import IncomeRecord, Task, Blueprint
from events.event_store import EventStore


def main(hours: int = 24) -> None:
    engine = init_engine()
    session = create_session(engine)

    since = dt.datetime.utcnow() - dt.timedelta(hours=hours)

    # Income summary
    income_rows = (
        session.query(IncomeRecord)
        .filter(IncomeRecord.received_at >= since)
        .order_by(IncomeRecord.received_at.desc())
        .all()
    )

    total_income = sum(r.amount for r in income_rows)
    income_count = len(income_rows)

    # Task activity
    completed_tasks = (
        session.query(Task)
        .filter(Task.completed_at >= since)
        .order_by(Task.completed_at.desc())
        .all()
    )

    failed_tasks = (
        session.query(Task)
        .filter(Task.last_error_at >= since)
        .order_by(Task.last_error_at.desc())
        .all()
    )

    # Blueprint activity
    new_blueprints = (
        session.query(Blueprint)
        .filter(Blueprint.created_at >= since)
        .order_by(Blueprint.created_at.desc())
        .all()
    )

    # Events summary (high-level)
    store = EventStore(session)
    recent_events = store.list_recent(limit=100)

    # ---- PRINT DEBRIEF ----
    print("=== NOMAD v1.5 DAILY DEBRIEF ===")
    print(f"Window: last {hours}h (since {since.isoformat()} UTC)")
    print()

    # Income
    print(">> Income")
    print(f"  Records: {income_count}")
    print(f"  Total:   {total_income:.2f} (raw sum of amount)")
    if income_rows:
        latest = income_rows[0]
        print(
            f"  Latest:  {latest.amount:.2f} {latest.currency} via {latest.platform} "
            f"at {latest.received_at.isoformat()}"
        )
    print()

    # Tasks
    print(">> Tasks")
    print(f"  Completed: {len(completed_tasks)}")
    print(f"  Failed:    {len(failed_tasks)}")
    if completed_tasks[:3]:
        print("  Recent completed:")
        for t in completed_tasks[:3]:
            print(f"    - #{t.id} {t.name} [{t.status}]")
    if failed_tasks[:3]:
        print("  Recent failed:")
        for t in failed_tasks[:3]:
            print(f"    - #{t.id} {t.name} (last_error_at={t.last_error_at})")
    print()

    # Blueprints
    print(">> Blueprints")
    print(f"  New in window: {len(new_blueprints)}")
    if new_blueprints[:3]:
        print("  Recent new:")
        for bp in new_blueprints[:3]:
            print(
                f"    - #{bp.id} {bp.title} "
                f"(ROI={bp.roi_score:.1f}, AUTO={bp.automation_score:.1f}, RISK={bp.risk_score:.1f})"
            )
    print()

    # Events
    print(">> Events")
    print(f"  Recent events fetched: {len(recent_events)}")
    by_category = {}
    for e in recent_events:
        cat = e.get("category") or "unknown"
        by_category[cat] = by_category.get(cat, 0) + 1
    if by_category:
        print("  By category:")
        for cat, count in sorted(by_category.items(), key=lambda x: x[0]):
            print(f"    - {cat}: {count}")

    print()
    print("=== END OF DEBRIEF ===")


if __name__ == "__main__":
    main()




