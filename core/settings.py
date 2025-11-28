import os

class Settings:
    APP_NAME = "Nomad Engine v1.5"
    VERSION = "1.5.0"

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    DB_PATH = os.path.join(BASE_DIR, "db", "nomad_v15.db")
    LOG_PATH = os.path.join(BASE_DIR, "logs", "nomad.log")

    API_HOST = "127.0.0.1"
    API_PORT = 9001

    SCHEDULER_JOBSTORE = os.path.join(BASE_DIR, "db", "scheduler_jobs.sqlite")

    # Worker config
    WORKER_POLL_INTERVAL = 1.0

settings = Settings()
