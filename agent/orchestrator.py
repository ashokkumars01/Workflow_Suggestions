# agent/orchestrator.py
from .file_scanner import scan_repo
from .static_analysis import analyze_file
from .redundancy_detector import extract_functions
from .sanitizer import sanitize
from .gemini_agent import optimize
from .report import post_comment

def main():
    findings = []
    fingerprints = {}

    for file in scan_repo():
        with open(file, encoding="utf-8") as f:
            src = f.read()

        issues = analyze_file(file)

        for fn in extract_functions(src, file):
            fingerprints.setdefault(fn["fingerprint"], []).append(fn)

        if issues:
            findings.append({"file": file, "issues": issues})

    # Redundancy detection
    for dup in fingerprints.values():
        if len(dup) > 1:
            findings.append({
                "file": "multiple",
                "issues": [{
                    "type": "redundant_code",
                    "occurrences": dup
                }]
            })

    if not findings:
        return

    safe = sanitize(findings)
    suggestions = optimize(safe)
    post_comment(suggestions)

if __name__ == "__main__":
    main()
