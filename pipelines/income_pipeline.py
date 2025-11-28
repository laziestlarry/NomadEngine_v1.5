from typing import Dict, Any, List
from sqlalchemy.orm import Session
from sqlalchemy import func

from db.models import IncomeRecord


def get_total_income(session: Session) -> Dict[str, Any]:
    total = session.query(func.coalesce(func.sum(IncomeRecord.amount), 0.0)).scalar()
    return {"total_income": float(total or 0.0)}


def get_income_by_platform(session: Session) -> List[Dict[str, Any]]:
    rows = (
        session.query(
            IncomeRecord.platform,
            func.coalesce(func.sum(IncomeRecord.amount), 0.0).label("total"),
            func.count(IncomeRecord.id).label("count"),
        )
        .group_by(IncomeRecord.platform)
        .all()
    )

    return [
        {
            "platform": r[0],
            "total": float(r[1]),
            "count": int(r[2]),
        }
        for r in rows
    ]


def get_recent_income(session: Session, limit: int = 20) -> List[Dict[str, Any]]:
    rows = (
        session.query(IncomeRecord)
        .order_by(IncomeRecord.received_at.desc())
        .limit(limit)
        .all()
    )

    return [
        {
            "id": r.id,
            "platform": r.platform,
            "amount": float(r.amount),
            "currency": r.currency,
            "received_at": r.received_at.isoformat() if r.received_at else None,
        }
        for r in rows
    ]