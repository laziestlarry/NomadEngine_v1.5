import json
from typing import Any

def pretty(obj: Any) -> str:
    return json.dumps(obj, indent=2, ensure_ascii=False)

def safe_json(obj: Any):
    try:
        return json.loads(json.dumps(obj))
    except:
        return {"_json_error": "unserializable"}