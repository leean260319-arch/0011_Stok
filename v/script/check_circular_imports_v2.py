import ast
import os
import sys
from collections import defaultdict

def get_imports(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            try:
                tree = ast.parse(f.read(), filename=file_path)
            except SyntaxError:
                return []
    except Exception:
        return []

    imports = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.append(alias.name)
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                # Resolve relative imports (naive)
                if node.level > 0:
                     # For simplicity in this script, we just treat .module as oais.module
                     # This is heuristic but identifying the cycle is usually enough
                     imports.append(f"oais.{node.module}" if node.module else "oais")
                else:
                    imports.append(node.module)
    return imports

def find_cycles(graph):
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
                cycle_start_index = path.index(neighbor)
                cycle = path[cycle_start_index:] + [neighbor]
                cycles.append(cycle)

        path.pop()
        stack.remove(node)

    for node in list(graph.keys()):
        if node not in visited:
            dfs(node, [])

    return cycles

def main():
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) # Project root
    oais_dir = os.path.join(root_dir, 'oais')

    print(f"Scanning {oais_dir}...")

    py_files = {}
    for root, _, files in os.walk(oais_dir):
        for file in files:
            if file.endswith('.py'):
                full_path = os.path.join(root, file)
                # Module name construction: oais.submodule
                rel_path = os.path.relpath(full_path, root_dir)
                module_name = rel_path.replace(os.sep, '.').replace('.py', '')
                py_files[module_name] = full_path

    graph = defaultdict(set)
    for module_name, file_path in py_files.items():
        # Skip checking __init__ imports for cycles unless necessary,
        # but usually __init__ is the aggregator causing issues.
        # Let's include everything.

        raw_imports = get_imports(file_path)
        for imp in raw_imports:
            # Normalize import
            target = imp
            if target.startswith('oais'):
                # We only care about imports within 'oais' package
                # Check if it maps to a known file
                # Exact match
                if target in py_files and target != module_name:
                    graph[module_name].add(target)
                else:
                    # Check if it's a parent package import (e.g. oais.utils.string -> oais.utils)
                    parts = target.split('.')
                    while len(parts) > 1:
                        parent = '.'.join(parts)
                        if parent in py_files and parent != module_name:
                             graph[module_name].add(parent)
                             break
                        parts.pop()

    cycles = find_cycles(graph)

    unique_cycles = []
    seen_sets = set()

    for c in cycles:
        # Normalize cycle representation for deduplication
        cycle_set = frozenset(c)
        if cycle_set not in seen_sets:
            seen_sets.add(cycle_set)
            unique_cycles.append(c)

    if unique_cycles:
        print(f"\n[CRITICAL] Found {len(unique_cycles)} circular dependency chains:")
        for i, cycle in enumerate(unique_cycles, 1):
            print(f"{i}. {' -> '.join(cycle)}")

        print("\nThese circular imports cause 'ImportError' or 'AttributeError' in Streamlit pages.")
    else:
        print("\n[OK] No direct module-level circular imports found via static AST analysis.")
        print("(Note: This script blindly checks top-level imports. Runtime import cycles might still exist if imports are conditional)")

if __name__ == "__main__":
    main()
