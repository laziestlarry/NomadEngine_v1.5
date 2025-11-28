# launcher/start_python_worker.py

import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.append(ROOT)

from events.event_bus import EventBus
from workers.python_worker import PythonWorker


def main():
    bus = EventBus()
    worker = PythonWorker(name="python_worker_main", event_bus=bus, poll_interval=2.0)
    worker.run_forever()


if __name__ == "__main__":
    main()