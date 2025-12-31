# agent/sanitizer.py
import hashlib

def sanitize(findings):
    safe = []
    for f in findings:
        safe.append({
            "file_hash": hashlib.sha256(f["file"].encode()).hexdigest()[:12],
            "issues": f["issues"]
        })
    return safe
