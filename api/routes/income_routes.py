from fastapi import APIRouter
from sqlalchemy.orm import Session

from db.engine import init_engine
from db.session import create_session
from pipelines.income_pipeline import (
    get_total_income,
    get_income_by_platform,
    get_recent_income,
)

router = APIRouter(prefix="/income", tags=["income"])


@router.get("/total")
def total_income():
    session = create_session(init_engine())
    return get_total_income(session)


@router.get("/platforms")
def income_by_platform():
    session = create_session(init_engine())
    return get_income_by_platform(session)


@router.get("/recent")
def recent_income():
    session = create_session(init_engine())
    return get_recent_income(session)