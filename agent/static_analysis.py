# agent/static_analysis.py
import ast
from typing import List, Dict

class Analyzer(ast.NodeVisitor):
    """
    AST-based static analyzer to detect:
      - Deeply nested loops (>2 levels)
      - Deeply nested if statements (>2 levels)
      - Repeated computations (simple heuristics)
    """
    def __init__(self):
        self.issues: List[Dict] = []
        self.loop_stack: List[ast.AST] = []
        self.if_stack: List[ast.AST] = []
        self.seen_nodes: set = set()  # For detecting repeated computations

    # ---------------------
    # Visit loops
    # ---------------------
    def visit_For(self, node):
        self.loop_stack.append(node)
        if len(self.loop_stack) > 2:
            self.issues.append({
                "type": "deep_nested_loop",
                "line": node.lineno,
                "depth": len(self.loop_stack),
                "estimated_complexity": f"O(n^{len(self.loop_stack)})"
            })
        self.generic_visit(node)
        self.loop_stack.pop()

    def visit_While(self, node):
        self.loop_stack.append(node)
        if len(self.loop_stack) > 2:
            self.issues.append({
                "type": "deep_nested_loop",
                "line": node.lineno,
                "depth": len(self.loop_stack),
                "estimated_complexity": f"O(n^{len(self.loop_stack)})"
            })
        self.generic_visit(node)
        self.loop_stack.pop()

    # ---------------------
    # Visit if statements
    # ---------------------
    def visit_If(self, node):
        self.if_stack.append(node)
        if len(self.if_stack) > 2:
            self.issues.append({
                "type": "deep_nested_if",
                "line": node.lineno,
                "depth": len(self.if_stack)
            })
        self.generic_visit(node)
        self.if_stack.pop()

    # ---------------------
    # Detect repeated computations (simple heuristic)
    # ---------------------
    def visit_BinOp(self, node):
        node_dump = ast.dump(node)
        if node_dump in self.seen_nodes:
            self.issues.append({
                "type": "repeated_computation",
                "line": node.lineno
            })
        else:
            self.seen_nodes.add(node_dump)
        self.generic_visit(node)

# ---------------------
# Analyze a single file
# ---------------------
def analyze_file(path: str) -> List[Dict]:
    with open(path, encoding="utf-8") as f:
        source = f.read()
    tree = ast.parse(source)
    # Set parent references for repeated computation heuristics
    for node in ast.walk(tree):
        for child in ast.iter_child_nodes(node):
            child.parent = node
    analyzer = Analyzer()
    analyzer.visit(tree)
    return analyzer.issues

# ---------------------
# Analyze multiple files
# ---------------------
def analyze_files(file_paths: List[str]) -> Dict[str, List[Dict]]:
    """
    Accepts a list of Python file paths, returns a dictionary:
        {file_path: [list of issues]}
    """
    all_issues = {}
    for path in file_paths:
        issues = analyze_file(path)
        all_issues[path] = issues
    return all_issues
