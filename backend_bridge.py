"""
Context Management Engine - Backend API Bridge
Directly launches the production-grade modular backend (backend/main.py).
"""
import os
import sys

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)

from backend.main import app

if __name__ == "__main__":
    import uvicorn
    print("\n" + "=" * 60)
    print("  Context Management Engine — Backend API Bridge")
    print("  Status: READY")
    print("  Server: http://127.0.0.1:8000")
    print("  Docs:   http://127.0.0.1:8000/docs")
    print("  Health: http://127.0.0.1:8000/api/health")
    print("=" * 60 + "\n", flush=True)
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")