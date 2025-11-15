import json
import re
import os
import sys
import subprocess
import tempfile
from collections import deque

def load_config(file_path):
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        sys.exit("Error: Config file not found")
    except json.JSONDecodeError:
        sys.exit("Error: Config file contains invalid JSON")

def validate_config(config):
    required_keys = {"package_name", "repository_url_or_path", "repository_mode",
                     "package_version", "max_depth", "test_mode"}
    if not required_keys.issubset(config.keys()):
        missing = required_keys - set(config.keys())
        sys.exit(f"Error: Config missing required keys: {', '.join(missing)}")

    package_name = config["package_name"]
    if not re.match(r'^[a-zA-Z0-9_-]+$', package_name):
        sys.exit("Error: package_name must contain only Latin letters, digits, hyphens, or underscores")

    if config["repository_mode"] != "download":
        sys.exit("Error: Stage 2 requires repository_mode = 'download'")

    url = config["repository_url_or_path"]
    if not re.match(r'^https?://', url):
        sys.exit("Error: repository_url_or_path must be a valid HTTPS/HTTP URL")

    version = config["package_version"]
    if not re.match(r'^\d+\.\d+\.\d+([.-]\w+)*$', version):
        sys.exit("Error: package_version must be in semantic versioning format (e.g., 1.0.0)")

    if not isinstance(config["max_depth"], int) or config["max_depth"] <= 0:
        sys.exit("Error: max_depth must be a positive integer")

    if not isinstance(config["test_mode"], bool):
        sys.exit("Error: test_mode must be a boolean")

def try_checkout_version(repo_dir, version):
    candidates = [f"v{version}", version]
    for tag in candidates:
        try:
            subprocess.run(["git", "checkout", "--quiet", "--force", tag], cwd=repo_dir, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return True
        except subprocess.CalledProcessError:
            continue
    return False

def parse_package_version(cargo_path):
    in_package = False
    try:
        with open(cargo_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line == "[package]":
                    in_package = True
                    continue
                if line.startswith('[') and line != "[package]":
                    in_package = False
                if in_package and line.startswith("version"):
                    match = re.search(r'version\s*=\s*["\']([^"\']+)["\']', line)
                    if match:
                        return match.group(1)
    except Exception as e:
        sys.exit(f"Error reading package version: {e}")
    return None

def parse_dependencies(cargo_path):
    dependencies = []
    in_deps = False

    with open(cargo_path, 'r', encoding='utf-8') as f:
        for line in f:
            stripped = line.strip()
            if not stripped or stripped.startswith('#'):
                continue

            if stripped == "[dependencies]":
                in_deps = True
                continue
            if stripped.startswith('[') and stripped != "[dependencies]":
                in_deps = False
                continue

            if in_deps:
                match_simple = re.match(r'^([a-zA-Z0-9_-]+)\s*=\s*["\']([^"\']+)["\']', stripped)
                if match_simple:
                    name, version = match_simple.groups()
                    dependencies.append(f"{name} = {version}")
                    continue

                match_table = re.match(r'^([a-zA-Z0-9_-]+)\s*=\s*{', stripped)
                if match_table:
                    name = match_table.group(1)
                    next_line = next(f, '').strip()
                    if next_line.startswith('version'):
                        match_ver = re.search(r'version\s*=\s*["\']([^"\']+)["\']', next_line)
                        if match_ver:
                            version = match_ver.group(1)
                            dependencies.append(f"{name} = {version}")
                    continue

                match_inline = re.search(r'([a-zA-Z0-9_-]+)\s*=\s*{\s*version\s*=\s*["\']([^"\']+)["\']', stripped)
                if match_inline:
                    name, version = match_inline.groups()
                    dependencies.append(f"{name} = {version}")
                    continue

    return dependencies

def build_dependency_graph(start_package, max_depth, test_mode=False, cargo_path=None):
    graph = {} 
    visited = set()  
    queue = deque([(start_package, 0)])  

    if test_mode:

        graph[start_package] = ["A = 1.0", "B = 2.0"]
        graph["A"] = ["C = 3.0"]
        graph["B"] = ["D = 4.0"]
        graph["C"] = []
        graph["D"] = []
    else:
        if cargo_path and os.path.exists(cargo_path):
            graph[start_package] = parse_dependencies(cargo_path)
        else:
            graph[start_package] = []

    while queue and queue[0][1] < max_depth:
        package, depth = queue.popleft()
        if package in visited:
            continue
        visited.add(package)


        deps = graph[package]
        for dep in deps:
            dep_name = dep.split(" = ")[0]  
            if dep_name not in visited:
                queue.append((dep_name, depth + 1))
                if dep_name not in graph:
                    graph[dep_name] = []  

    return graph

def print_graph(graph):
    print("\nDependency Graph:")
    for package, deps in graph.items():
        for dep in deps:
            print(f"{package} -> {dep}")

def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python app.py <config.json>")

    config = load_config(sys.argv[1])
    validate_config(config)

    print("Configuration:")
    for k, v in config.items():
        print(f"{k}: {v}")

    version = config["package_version"]
    repo_url = config["repository_url_or_path"]
    test_mode = config["test_mode"]

    with tempfile.TemporaryDirectory() as temp_dir:
        repo_dir = os.path.join(temp_dir, "repo")
        print(f"\nCloning repository...")
        subprocess.run(["git", "clone", "--quiet", repo_url, repo_dir], check=True, stdout=subprocess.DEVNULL)

        print(f"Checking out version {version}...")
        if not try_checkout_version(repo_dir, version):
            sys.exit(f"Error: Could not checkout version {version}. Tag not found.")

        cargo_path = os.path.join(repo_dir, "Cargo.toml")
        if not os.path.exists(cargo_path):
            sys.exit("Error: Cargo.toml not found in repository root")

        actual_version = parse_package_version(cargo_path)
        if actual_version and actual_version != version:
            print(f"Warning: Cargo.toml declares version {actual_version}, but {version} was requested.")

        graph = build_dependency_graph(config["package_name"], config["max_depth"], test_mode, cargo_path)
        print_graph(graph)

if __name__ == "__main__":
    main()
