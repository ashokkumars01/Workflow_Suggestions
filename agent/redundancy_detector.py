# agent/redundancy_detector.py
import ast, hashlib

def normalize(node):
    for n in ast.walk(node):
        if isinstance(n, ast.Name):
            n.id = "_"
        elif isinstance(n, ast.Constant):
            n.value = "_"
    return node

def fingerprint(node):
    return hashlib.sha256(ast.dump(normalize(node)).encode()).hexdigest()

def extract_functions(source, file):
    tree = ast.parse(source)
    results = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            results.append({
                "file": file,
                "line": node.lineno,
                "fingerprint": fingerprint(node)
            })
    return results
