import ast

class ComplexityAnalyzer(ast.NodeVisitor):

    def __init__(self):
        self.loop_depth = 0
        self.max_loop_depth = 0
        self.recursive_calls = 0
        self.current_function = None
        self.data_structures = 0
        self.slice_used = False

    def visit_For(self, node):
        self.loop_depth += 1
        self.max_loop_depth = max(self.max_loop_depth, self.loop_depth)
        self.generic_visit(node)
        self.loop_depth -= 1

    def visit_While(self, node):
        self.loop_depth += 1
        self.max_loop_depth = max(self.max_loop_depth, self.loop_depth)
        self.generic_visit(node)
        self.loop_depth -= 1

    def visit_FunctionDef(self, node):
        prev = self.current_function
        self.current_function = node.name
        self.generic_visit(node)
        self.current_function = prev

    def visit_Call(self, node):
        if isinstance(node.func, ast.Name):
            if node.func.id == self.current_function:
                self.recursive_calls += 1
        self.generic_visit(node)

    def visit_Subscript(self, node):
        # Detect slicing like arr[:mid]
        if isinstance(node.slice, ast.Slice):
            self.slice_used = True
        self.generic_visit(node)

    def visit_List(self, node):
        self.data_structures += 1
        self.generic_visit(node)

    def visit_Dict(self, node):
        self.data_structures += 1
        self.generic_visit(node)

    def visit_Set(self, node):
        self.data_structures += 1
        self.generic_visit(node)


def analyze_code(code):

    try:
        tree = ast.parse(code)
    except:
        return "Invalid Python code", ["Enter valid Python code"]

    analyzer = ComplexityAnalyzer()
    analyzer.visit(tree)

    hints = []

    # -------- TIME COMPLEXITY --------

    if analyzer.recursive_calls > 1 and analyzer.slice_used:

        time_complexity = "O(n log n)"
        hints.append("Divide and Conquer recursion detected.")

    elif analyzer.recursive_calls > 1:

        time_complexity = "O(2^n)"
        hints.append("Multiple recursive calls detected.")

    elif analyzer.recursive_calls == 1:

        time_complexity = "O(n)"
        hints.append("Single recursion detected.")

    else:

        if analyzer.max_loop_depth == 0:
            time_complexity = "O(1)"

        elif analyzer.max_loop_depth == 1:
            time_complexity = "O(n)"

        elif analyzer.max_loop_depth == 2:
            time_complexity = "O(n²)"
            hints.append("Nested loops detected.")

        else:
            time_complexity = f"O(n^{analyzer.max_loop_depth})"
            hints.append("Multiple nested loops detected.")

    # -------- SPACE COMPLEXITY --------

    if analyzer.data_structures > 0 or analyzer.slice_used:
        space_complexity = "O(n)"
        hints.append("Extra memory usage detected.")

    else:
        space_complexity = "O(1)"

    result = f"Time Complexity: {time_complexity} | Space Complexity: {space_complexity}"

    if not hints:
        hints.append("Code looks optimized.")

    return result, hints