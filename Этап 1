import json
import re
import os
import sys


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
                     "package_version", "max_depth"}
    if not all(key in config for key in required_keys):
        raise ValueError("Error: Config missing required keys: " +
                         ", ".join(required_keys - set(config.keys())))


    package_name = config["package_name"]
    if not package_name.strip():
        raise ValueError("Error: package_name must not be empty")
    if not re.match(r'^[a-zA-Z0-9_-]+$', package_name):
        raise ValueError("Error: package_name must contain only Latin letters, digits, hyphens, or underscores")


    if config["repository_mode"] not in ["download", "local"]:
        raise ValueError("Error: repository_mode must be 'download' or 'local'")

    url_or_path = config["repository_url_or_path"]
    if not url_or_path:
        raise ValueError("Error: repository_url_or_path must not be empty")
    if config["repository_mode"] == "download":
        if not re.match(r'^https?://[\w\.-]+', url_or_path):
            raise ValueError("Error: repository_url_or_path must be a valid URL starting with http:// or https://")
    elif config["repository_mode"] == "local":
        if not os.path.exists(url_or_path):
            raise ValueError("Error: repository_url_or_path must point to an existing local path")

    package_version = config["package_version"]
    if not package_version:
        raise ValueError("Error: package_version must not be empty")
    if not re.match(r'^\d+\.\d+\.\d+([.-][\w-]+)*$', package_version):
        raise ValueError("Error: package_version must be in format like 'x.y.z' or 'x.y.z-...'")

    if not isinstance(config["max_depth"], int):
        raise ValueError("Error: max_depth must be an integer")
    if config["max_depth"] <= 0:
        raise ValueError("Error: max_depth must be a positive integer")


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python app.py <config.json>")

    config_file = sys.argv[1]
    try:
        config = load_config(config_file)
        validate_config(config)

        for key, value in config.items():
            print(f"{key}: {value}")

    except ValueError as e:
        sys.exit(str(e))
    except Exception as e:
        sys.exit(f"Unexpected error: {str(e)}")


if __name__ == "__main__":
    main()
