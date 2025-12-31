# agent/file_scanner.py
import os

EXCLUDE = {".git", "venv", "node_modules", "__pycache__"}

def scan_repo():
    for root, dirs, files in os.walk("."):
        dirs[:] = [d for d in dirs if d not in EXCLUDE]
        for f in files:
            if f.endswith(".py"):
                yield os.path.join(root, f)
