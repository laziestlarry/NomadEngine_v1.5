import os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(ROOT)

from core.bootstrap import bootstrap_system

if __name__ == "__main__":
    bootstrap_system()
    print("=== NOMAD v1.5 SYSTEM ONLINE ===")
