import time
import datetime as dt
from typing import Optional, List

from sqlalchemy.orm import Session

from db.engine import init_engine
from db.session import create_session
from db.models import Worker, Task
from events.event_bus import EventBus
from events.event_definitions import EventType, EventCategory
from pipelines.execution_pipeline import (
    select_pending_tasks,
    mark_task_started,
    mark_task_completed,
    mark_task_failed,
)
from core.logger import logger


class PythonWorker:
    """
    Simple Python-based worker that processes tasks from the DB.

    For v1.5:
    - it simulates executing each task
    - in future versions we plug real platform logic / APIs here
    """

    def __init__(self, name: str, event_bus: EventBus, poll_interval: float = 2.0):
        self.name = name
        self.event_bus = event_bus
        self.poll_interval = poll_interval
        self._running = False

    def _get_session(self) -> Session:
        engine = init_engine()
        return create_session(engine)

    def _get_or_create_worker_row(self, session: Session) -> Worker:
        worker: Optional[Worker] = (
            session.query(Worker).filter(Worker.name == self.name).first()
        )
        if not worker:
            worker = Worker(
                name=self.name,
                kind="python",
                capabilities=["compute", "strategy", "prep"],
                is_active=True,
                last_seen_at=dt.datetime.utcnow(),
                last_heartbeat_at=dt.datetime.utcnow(),
            )
            session.add(worker)
            session.commit()
        return worker

    def _heartbeat(self, session: Session, worker: Worker) -> None:
        worker.last_seen_at = dt.datetime.utcnow()
        worker.last_heartbeat_at = dt.datetime.utcnow()
        session.add(worker)
        session.commit()

        self.event_bus.publish(
            event_type=EventType.WORKER_HEARTBEAT,
            category=EventCategory.WORKER,
            message=f"Python worker '{worker.name}' heartbeat.",
            worker_id=worker.id,
            payload={"worker_name": worker.name, "kind": worker.kind},
        )

    def _process_batch(self, session: Session, worker: Worker) -> int:
        tasks: List[Task] = select_pending_tasks(session, limit=5)
        if not tasks:
            return 0

        for t in tasks:
            try:
                mark_task_started(session, self.event_bus, t)

                # Simulated work:
                # later we map categories to real implementations
                time.sleep(0.1)

                mark_task_completed(session, self.event_bus, t)
            except Exception as e:
                logger.error(f"[PythonWorker] Error processing task #{t.id}: {e}")
                mark_task_failed(session, self.event_bus, t, str(e))

        return len(tasks)

    def run_forever(self):
        """
        Blocking loop: continuously checks for pending tasks.
        Intended to be launched by launcher/start_python_worker.py in future.
        """
        logger.info(f"[PythonWorker] Starting worker '{self.name}' run loop.")
        self._running = True

        while self._running:
            session = self._get_session()
            try:
                worker = self._get_or_create_worker_row(session)
                self._heartbeat(session, worker)
                processed = self._process_batch(session, worker)

                if processed == 0:
                    time.sleep(self.poll_interval)
            finally:
                session.close()

    def stop(self):
        self._running = False