# agent/static_analysis.py
import ast

class Analyzer(ast.NodeVisitor):
    def __init__(self):
        self.issues = []
        self.depth = 0

    def visit_For(self, node):
        self.depth += 1
        if self.depth > 2:
            self.issues.append({
                "type": "deep_nested_loop",
                "line": node.lineno,
                "depth": self.depth,
                "estimated_complexity": f"O(n^{self.depth})"
            })
        self.generic_visit(node)
        self.depth -= 1

    def visit_If(self, node):
        self.depth += 1
        if self.depth > 2:
            self.issues.append({
                "type": "deep_nested_if",
                "line": node.lineno,
                "depth": self.depth
            })
        self.generic_visit(node)
        self.depth -= 1

def analyze_file(path):
    with open(path, encoding="utf-8") as f:
        tree = ast.parse(f.read())
    analyzer = Analyzer()
    analyzer.visit(tree)
    return analyzer.issues
