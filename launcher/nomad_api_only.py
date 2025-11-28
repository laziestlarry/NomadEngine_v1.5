# launcher/nomad_api_only.py

import os
import sys
import uvicorn

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.append(ROOT)


def main():
    uvicorn.run(
        "api.server:app",
        host="127.0.0.1",
        port=9000,
        reload=False,
        log_level="info",
    )


if __name__ == "__main__":
    main()