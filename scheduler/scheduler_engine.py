from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor

from core.settings import settings
from core.logger import logger
from events.event_bus import EventBus
from events.event_definitions import EventType, EventCategory

from scheduler.jobs_alpha_scan import alpha_scan_job
from scheduler.jobs_income_scan import income_scan_job
from scheduler.jobs_health import health_check_job
from scheduler.jobs_retry import retry_failed_tasks_job
from scheduler.jobs_reconnect import reconnect_workers_job
from scheduler import context


scheduler = None


def start_scheduler_engine(event_bus: EventBus):
    """
    Full APScheduler engine with persistent job store and recurring jobs.

    NOTE: We no longer pass Session or EventBus as job kwargs,
    because they are not picklable when using SQLAlchemyJobStore.
    Instead:
      - EventBus is stored in scheduler.context.event_bus
      - Each job creates its own DB session as needed
    """

    global scheduler
    if scheduler is not None:
        logger.warning("[Scheduler] Already started.")
        return scheduler

    # Store event_bus globally for jobs
    context.event_bus = event_bus

    jobstores = {
        "default": SQLAlchemyJobStore(
            url=f"sqlite:///{settings.SCHEDULER_JOBSTORE}"
        )
    }

    executors = {
        "default": ThreadPoolExecutor(10),
        "processpool": ProcessPoolExecutor(4),
    }

    job_defaults = {
        "coalesce": False,
        "max_instances": 1,
    }

    scheduler = BackgroundScheduler(
        jobstores=jobstores,
        executors=executors,
        job_defaults=job_defaults,
        timezone="UTC",
    )

    # ---------------------------------------------------------
    # REGISTER JOBS (no kwargs that contain sessions or event_bus)
    # ---------------------------------------------------------

    scheduler.add_job(
        alpha_scan_job,
        trigger="interval",
        minutes=10,
        id="alpha_scan",
        replace_existing=True,
    )

    scheduler.add_job(
        income_scan_job,
        trigger="interval",
        minutes=15,
        id="income_scan",
        replace_existing=True,
    )

    scheduler.add_job(
        health_check_job,
        trigger="interval",
        minutes=2,
        id="health_check",
        replace_existing=True,
    )

    scheduler.add_job(
        retry_failed_tasks_job,
        trigger="interval",
        minutes=5,
        id="retry_failed",
        replace_existing=True,
    )

    scheduler.add_job(
        reconnect_workers_job,
        trigger="interval",
        minutes=3,
        id="reconnect_workers",
        replace_existing=True,
    )

    scheduler.start()

    # Emit event
    event_bus.publish(
        event_type=EventType.SCHEDULER_JOB_RUN,
        category=EventCategory.SCHEDULER,
        message="Scheduler fully initialized with persistent jobs."
    )

    logger.info("[Scheduler] Full scheduler engine started.")
    print("[Scheduler] Full scheduler engine started.")

    return scheduler