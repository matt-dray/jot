"""
Read, write, and return content for config and jot files.
"""

import argparse
import datetime as dt
import json
from pathlib import Path
import re


def get_config_path(config_file: Path = ".jot-config.json") -> Path:
    """
    Build the path to the config file in the user's home directory.

    Args:
        config_file (Path): The file name for the config file.

    Returns:
        Path: The file path to the config file.
    """
    config_path = Path.home() / config_file
    return config_path


def get_jot_path(config_path: Path) -> Path:
    """
    Read the jot file path from the config file.

    Args:
        config_path (Path): The path to the config file.

    Returns:
        Path: The file path to the jot file.
    """
    config_text = config_path.read_text()
    config_json = json.loads(config_text)
    jot_path_text = config_json["JOT_PATH"]
    jot_path = Path(jot_path_text)
    return jot_path


def write_to_config(config_path: Path, jot_path: Path) -> None:
    """
    Write the jot file path to the config file.

    Args:
        config_path (Path): The path to the config file.
        jot_path (Path): The path to the jot file.

    Returns:
        None: Prints output.
    """
    json_dict = {"JOT_PATH": jot_path.as_posix()}
    with config_path.open("w", encoding="utf-8") as f:
        json.dump(json_dict, f)
    print(f"Config file written to {config_path}")
    print(f"Text file path set to {jot_path}")


def write_jotting(jot_path: Path, args=argparse.Namespace) -> None:
    """
    Prepend a new jotting with a timestamp to the jot file.

    Args:
        jot_path (Path): The path to the jot file.
        args (argparse.Namespace): Arguments collected from the argument parser.

    Returns:
        None: Prints output.
    """

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
    """
    Prompt the user for a jot file path and create it

    Returns:
        Path: The file path to the jot file.
    """
    jot_path_user = input("Path to text file: ")
    jot_path = Path(jot_path_user).expanduser().resolve()
    jot_path.touch()
    return jot_path


def list_jottings(jot_path: Path, limit: int = None) -> None:
    """
    Print the last n jottings from the jot file.

    Args:
        jot_path (Path): The path to the jot file.
        limit (int): Maximum number of recent jottings to print.

    Returns:
        None: Prints output.
    """
    if not jot_path.exists():
        print("No jottings yet. Try 'jot hello'.")
        return

    lines = jot_path.read_text().splitlines()

    if limit is None:
        lines_to_show = lines
    else:
        lines_to_show = lines[:limit]

    for line in lines_to_show:
        print(line)


def search_jottings(jot_path: Path, search_term: str, limit: int = None) -> None:
    """
    Search for a term in your jottings (regular expressions supported).

    Args:
        jot_path (Path): The path to the jot file.
        search_term (str): Text string to search (regular expressions supported).
        limit (int): Maximum number of recent jottings to print.

    Returns:
        None: Prints output.
    """
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
    "get_config_path",
    "generate_jot",
    "get_jot_path",
    "list_jottings",
    "search_jottings",
    "write_to_config",
    "write_jotting",
]
