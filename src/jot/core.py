"""
Read, write, and return content for config and jot files.
"""

import argparse
import datetime as dt
import json
from pathlib import Path
import re
from rich.console import Console
from rich.prompt import Prompt

console = Console()


def get_config_path(config_file: str = ".jot-config.json") -> Path:
    """
    Build the path to the config file in the user's home directory.

    Args:
        config_file (Path): The file name for the config file.

    Returns:
        Path: The file path to the config file.
    """
    config_path = Path.home() / config_file
    return config_path


def read_jot_path(config_path: Path) -> Path:
    """
    Read the jot file path from the config file.

    Args:
        config_path (Path): The path to the config file.

    Returns:
        Path: The file path to the jot file.
    """
    config_text = config_path.read_text(encoding="utf-8")
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
    console.print(f":round_pushpin: Text file path set to [green]{jot_path}[/]")
    console.print(f":round_pushpin: Config file written to [green]{config_path}[/]")


def write_jotting(jot_path: Path, args: argparse.Namespace) -> None:
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
        jot_file_content = jot_path.read_text(encoding="utf-8")

    timestamp = dt.datetime.now().strftime("[%Y-%m-%d %H:%M]")
    jot_path.write_text(
        f"{timestamp} {args.text}\n{jot_file_content}", encoding="utf-8"
    )
    console.print(f':memo: Wrote [green]"{args.text}"[/green] to [green]{jot_path}[/]')


def create_jot_file() -> Path:
    """
    Prompt the user for a jot file path and create it

    Returns:
        Path: The file path to the jot file.
    """
    jot_path_user = Prompt.ask(
        ":round_pushpin: Path to text file",
    )
    jot_path = Path(jot_path_user).expanduser().resolve()
    jot_path.touch()
    return jot_path


def check_in_period(line: str, period_from: dt.datetime | None, period_to: dt.datetime | None) -> bool:
    if not line.startswith("[") or "]" not in line:
        return False
    stamp = line[1 : line.index("]")]
    try:
        date = dt.datetime.strptime(stamp, "%Y-%m-%d %H:%M")
    except ValueError:
        return False
    if period_from is not None and date < period_from:
        return False
    if period_to is not None and date > period_to:
        return False
    return True


def list_jottings(
    jot_path: Path,
    limit: int | None = None,
    period_from: dt.datetime | None = None,
    period_to: dt.datetime | None = None,
) -> None:
    """
    Print the last n jottings from the jot file.

    Args:
        jot_path (Path): The path to the jot file.
        limit (int | None): Maximum number of recent jottings to print.
        period_from (datetime | None): Only match from this date.
        period_to (datetime | None): Only match until this date.

    Returns:
        None: Prints output.
    """
    if not jot_path.exists():
        console.print(":x: No jottings yet. Try 'jot hello'.")
        return

    lines = jot_path.read_text(encoding="utf-8").splitlines()

    if period_to is not None or period_from is not None:
        lines = [line for line in lines if check_in_period(line, period_from, period_to)]

    if limit is not None:
        lines = lines[:limit]

    for line in lines:
        console.print(f"{line}")


def search_jottings(
    jot_path: Path,
    search_term: str,
    limit: int | None = None,
    period_from: dt.datetime | None = None,
    period_to: dt.datetime | None = None,
) -> None:
    """
    Search for a term in your jottings (regular expressions supported).

    Args:
        jot_path (Path): The path to the jot file.
        search_term (str): Text string to search (regular expressions supported).
        limit (int | None): Maximum number of recent jottings to print.
        period_from (datetime | None): Only match from this date.
        period_to (datetime | None): Only match until this date.

    Returns:
        None: Prints output.
    """
    if not jot_path.exists():
        console.print(":x: No jottings yet. Try 'jot hello'.")
        return

    with jot_path.open("r", encoding="utf-8") as f:
        lines = [line.rstrip("\n") for line in f]
    matches = [line for line in lines if re.search(search_term, line)]

    if period_to is not None or period_from is not None:
        matches = [line for line in matches if check_in_period(line, period_from, period_to)]

    if limit is not None:
        matches = matches[:limit]

    for line in matches:
        console.print(f"{line}")


def print_paths() -> None:
    """
    Print the expected path to the config file and read the jot path from it.

    Returns:
        None: Prints output.
    """
    config_path = get_config_path()
    if not config_path.exists():
        console.print(
            f":thinking: Config file not found in expected location: [red]{config_path}[/]"
        )
        return
    console.print(
        f":round_pushpin: Default path to config file: [green]{config_path}[/]"
    )
    jot_path = read_jot_path(config_path)
    if not jot_path.exists():
        print(f":thinking: Jot file not found in expected location: [red]{jot_path}[/]")
        return
    console.print(f":round_pushpin: Path to jot file: [green]{jot_path}[/]")


__all__ = [
    "create_jot_file",
    "get_config_path",
    "list_jottings",
    "print_paths",
    "read_jot_path",
    "search_jottings",
    "write_to_config",
    "write_jotting",
]
