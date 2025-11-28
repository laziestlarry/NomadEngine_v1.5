import os
import sys
from pathlib import Path

ROOT = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def ensure_sys_path():
    root_str = str(ROOT)
    if root_str not in sys.path:
        sys.path.append(root_str)