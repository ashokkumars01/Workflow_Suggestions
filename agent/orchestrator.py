# agent/orchestrator.py
from agent.file_scanner import scan_repo
from agent.static_analysis import analyze_file
from agent.redundancy_detector import extract_functions
from agent.sanitizer import sanitize
from agent.gemini_agent import optimize
from agent.report import post_comment

# def main():
#     findings = []
#     fingerprints = {}

#     for file in scan_repo():
#         with open(file, encoding="utf-8") as f:
#             src = f.read()

#         issues = analyze_file(file)

#         for fn in extract_functions(src, file):
#             fingerprints.setdefault(fn["fingerprint"], []).append(fn)

#         if issues:
#             findings.append({"file": file, "issues": issues})

#     # Redundancy detection
#     for dup in fingerprints.values():
#         if len(dup) > 1:
#             findings.append({
#                 "file": "multiple",
#                 "issues": [{
#                     "type": "redundant_code",
#                     "occurrences": dup
#                 }]
#             })

#     if not findings:
#         return

#     safe = sanitize(findings)
#     suggestions = optimize(safe)
#     post_comment(suggestions)

# if __name__ == "__main__":
#     main()

#=============================================================================================

# def main():
#     findings = []
#     fingerprints = {}

#     for file in scan_repo():
#         with open(file, encoding="utf-8") as f:
#             src = f.read()

#         issues = analyze_file(file)

#         for fn in extract_functions(src, file):
#             fingerprints.setdefault(fn["fingerprint"], []).append(fn)

#         if issues:
#             findings.append({"file": file, "issues": issues})

#     # Redundancy detection
#     for dup in fingerprints.values():
#         if len(dup) > 1:
#             findings.append({
#                 "file": "multiple",
#                 "issues": [{"type": "redundant_code", "occurrences": dup}]
#             })

#     # DEBUG: show findings
#     print("DEBUG: Findings detected:", findings)

#     if not findings:
#         print("DEBUG: No findings detected.")
#         return

#     safe = sanitize(findings)
#     suggestions = optimize(safe)

#     # DEBUG: show suggestions before posting
#     print("DEBUG: Suggestions prepared:\n", suggestions)

#     post_comment(suggestions)


# if __name__ == "__main__":
#     main()

#=============================================================================================

def main():
    findings = []
    fingerprints = {}

    for file in scan_repo():
        print("DEBUG: Scanning file:", file)
        with open(file, encoding="utf-8") as f:
            src = f.read()

        issues = analyze_file(file)
        print(f"DEBUG: Issues found in {file}: {issues}")

        for fn in extract_functions(src, file):
            fingerprints.setdefault(fn["fingerprint"], []).append(fn)

        if issues:
            findings.append({"file": file, "issues": issues})

    # Redundancy detection
    for dup in fingerprints.values():
        if len(dup) > 1:
            findings.append({
                "file": "multiple",
                "issues": [{"type": "redundant_code", "occurrences": dup}]
            })

    # 🔹 Inject a dummy test finding to verify PR comment
    if not findings:
        print("DEBUG: No findings detected, injecting test finding...")
        findings.append({
            "file": "test_file.py",
            "issues": [{"type": "test_issue", "description": "This is a test PR comment"}]
        })

    safe = sanitize(findings)
    suggestions = optimize(safe)

    # DEBUG: show suggestions before posting
    print("DEBUG: Suggestions prepared:\n", suggestions)

    post_comment(suggestions)


if __name__ == "__main__":
    main()