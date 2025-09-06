"""
Read, write, and return content for config and jot files.
"""

import argparse
import datetime as dt
import json
from pathlib import Path
import re


def build_config_path(json_path: Path = ".jot-config.json") -> Path:
    """Return the path to the config file in the user's home directory."""
    config_path = Path.home() / json_path
    return config_path


def get_jot_path(config_path: Path) -> Path:
    """Load the jot file path from the config file."""
    config_text = config_path.read_text()
    config_json = json.loads(config_text)
    jot_path_text = config_json["JOT_PATH"]
    jot_path = Path(jot_path_text)
    return jot_path


def write_to_config(config_path: Path, jot_path: Path) -> None:
    """Write the jot file path to the config file."""
    json_dict = {"JOT_PATH": jot_path.as_posix()}
    with config_path.open("w", encoding="utf-8") as f:
        json.dump(json_dict, f)
    print(f"Config file written to {config_path}")
    print(f"Text file path set to {jot_path}")


def write_jotting(jot_path: Path, args=argparse.Namespace) -> None:
    """Prepend a new jotting with a timestamp to the jot file."""

    jot_file_content = ""
    if jot_path.exists():
        with jot_path.open("r", encoding="utf-8") as f:
            jot_file_content = f.read()

    timestamp = dt.datetime.now().strftime("[%Y-%m-%d %H:%M]")
    jot_path.write_text(
        f"{timestamp} {args.text}\n{jot_file_content}", encoding="utf-8"
    )
    print(f'Wrote "{args.text}" to {jot_path}')


def generate_jot() -> Path:
    """Prompt the user for a jot file path and create it."""
    jot_path_user = input("Path to text file: ")
    jot_path = Path(jot_path_user).expanduser().resolve()
    jot_path.touch()
    return jot_path


def list_jottings(jot_path: Path, n: int = None) -> None:
    """Print the last n jottings from the jot file."""
    if not jot_path.exists():
        print("No jottings yet. Try 'jot hello'.")
        return

    lines = jot_path.read_text().splitlines()

    if n is None:
        lines_to_show = lines
    else:
        lines_to_show = lines[:n]

    for line in lines_to_show:
        print(line)


def search_jottings(jot_path: Path, search_term: str, limit: int = None) -> None:
    """Search for a term in your jottings (regular expressions supported)."""
    if not jot_path.exists():
        print("No jottings yet. Try 'jot hello'.")
        return

    with jot_path.open("r", encoding="utf-8") as f:
        lines = [line.rstrip("\n") for line in f]
    matches = [line for line in lines if re.search(search_term, line)]

    if limit is not None:
        matches = matches[:limit]

    for line in matches:
        print(line)


__all__ = [
    "build_config_path",
    "generate_jot",
    "get_jot_path",
    "list_jottings",
    "search_jottings",
    "write_to_config",
    "write_jotting",
]
