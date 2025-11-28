from fastapi import APIRouter

from workers.worker_controller import WorkerController
from events.event_bus import EventBus

router = APIRouter(prefix="/workers", tags=["workers"])

controller = None
bus = EventBus()  # clean instance; real system uses bootstrap’s bus


@router.post("/start/python")
def start_python_worker():
    global controller
    if controller is None:
        controller = WorkerController(bus)

    worker = controller.start_python_worker("python_worker_main")
    return {"status": "started", "worker": worker.name}