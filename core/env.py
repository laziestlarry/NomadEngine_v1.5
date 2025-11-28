import os
from dotenv import load_dotenv

def load_env():
    env_path = os.path.join(os.getcwd(), ".env")
    if os.path.exists(env_path):
        load_dotenv(env_path)

    return {
        "OPENAI_API_KEY": os.getenv("OPENAI_API_KEY", ""),
        "TOLGKA_TOKEN": os.getenv("TOLGKA_TOKEN", ""),
        "REMOTASKS_KEY": os.getenv("REMOTASKS_KEY", ""),
        "NODE_WORKER_URL": os.getenv("NODE_WORKER_URL", "http://127.0.0.1:5000")
    }
