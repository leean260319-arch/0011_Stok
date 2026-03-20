import ast
import os
import sys
from collections import defaultdict

def get_imports(file_path):
    """Parses a Python file and extracts imported module names."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            tree = ast.parse(f.read(), filename=file_path)
    except Exception as e:
        return []

    imports = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.append(alias.name)
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                imports.append(node.module)
    return imports

def find_cycles(graph):
    """Finds cycles in the dependency graph."""
    visited = set()
    stack = set()
    cycles = []

    def dfs(node, path):
        visited.add(node)
        stack.add(node)
        path.append(node)

        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                dfs(neighbor, path)
            elif neighbor in stack:
                # Cycle detected
                cycle = path[path.index(neighbor):] + [neighbor]
                cycles.append(cycle)

        path.pop()
        stack.remove(node)

    for node in list(graph.keys()):
        if node not in visited:
            dfs(node, [])

    return cycles

def main():
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    oais_dir = os.path.join(project_root, 'oais')

    if not os.path.exists(oais_dir):
        print(f"Error: {oais_dir} does not exist.")
        return

    dependency_graph = defaultdict(set)
    py_files = {}

    # 1. Map all oais modules
    for root, _, files in os.walk(oais_dir):
        for file in files:
            if file.endswith('.py') and file != '__init__.py': # __init__.py usually aggregates, check submodules
                full_path = os.path.join(root, file)
                module_name = 'oais.' + os.path.relpath(full_path, oais_dir).replace(os.sep, '.').replace('.py', '')
                py_files[module_name] = full_path

    # 2. Build dependency graph
    for module_name, file_path in py_files.items():
        imported_modules = get_imports(file_path)
        for imp in imported_modules:
            if imp.startswith('oais.') or imp.startswith('.'):
                 # Convert relative imports to absolute for simple checking (simplified)
                 # This is a basic checker, might miss complex relative imports
                 target = imp
                 if imp.startswith('.'):
                     # Very naive relative import handling
                     target = 'oais.' + imp.lstrip('.')

                 # Only track internal dependencies
                 if target in py_files and target != module_name:
                     dependency_graph[module_name].add(target)
            elif imp == 'oais':
                 # Importing root package
                 pass

    # 3. Find cycles
    cycles = find_cycles(dependency_graph)

    if cycles:
        print(f"Found {len(cycles)} circular dependency chains:")
        for cycle in cycles:
            print(" -> ".join(cycle))
    else:
        print("No obvious circular dependencies found between oais submodules.")

    # 4. Check for 'from . import X' inside oais modules which is common cause
    print("\nChecking for potential 'from . import' issues in oais/__init__.py:")
    init_path = os.path.join(oais_dir, '__init__.py')
    if os.path.exists(init_path):
         imports = get_imports(init_path)
         print(f"oais/__init__.py imports: {imports}")

if __name__ == "__main__":
    main()
