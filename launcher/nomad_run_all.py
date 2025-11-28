# launcher/nomad_run_all.py

import os
import sys
import uvicorn

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.append(ROOT)

from core.bootstrap import bootstrap_system  # noqa: E402


def main():
    # Start core system (DB, EventBus, scheduler)
    bootstrap_system()

    # Start API (blocking)
    uvicorn.run(
        "api.server:app",
        host="127.0.0.1",
        port=9000,
        reload=False,
        log_level="info",
    )


if __name__ == "__main__":
    main()