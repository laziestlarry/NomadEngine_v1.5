from typing import Optional

from events.event_bus import EventBus
from core.logger import logger
from workers.python_worker import PythonWorker


class WorkerController:
    """
    High-level controller for workers.

    In v1.5, this focuses on the PythonWorker.
    Later, we add Node workers and platform-specific workers.
    """

    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus
        self.python_worker: Optional[PythonWorker] = None

    def start_python_worker(self, name: str = "python_worker_1"):
        if self.python_worker is not None:
            logger.warning("[WorkerController] Python worker already running.")
            return

        self.python_worker = PythonWorker(name=name, event_bus=self.event_bus)
        logger.info(f"[WorkerController] Python worker '{name}' instantiated.")
        # Note: we do not call run_forever() here to avoid blocking.
        # This is for manual control or future threaded start.
        return self.python_worker