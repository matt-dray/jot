"""
Read, write, and return content for config and jot files.
"""

import argparse
import datetime as dt
import json
from pathlib import Path
from platformdirs import user_config_path
import re

from rich.console import Console
from rich.prompt import Prompt

console = Console()


def get_config_path(
    config_file: str = "config.json", config_dir: Path | None = None
) -> Path:
    """
    Build the path to the config file in the user's config directory.

    Args:
        config_file (str): The file name for the config file.
        config_dir (Path): The user's config directory.

    Returns:
        Path: The file path to the config file.
    """
    stub = config_dir if config_dir is not None else user_config_path("jot")
    config_path = stub / config_file
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
    config_path.parent.mkdir(parents=True, exist_ok=True)
    json_dict = {"JOT_PATH": jot_path.as_posix()}
    with config_path.open("w", encoding="utf-8") as f:
        json.dump(json_dict, f)
    console.print(f":white_check_mark: Created config file at [green]{config_path}[/]")
    console.print(f":white_check_mark: Set JOT_PATH variable to [green]{jot_path}[/]")


def write_jotting(
    jot_path: Path, args: argparse.Namespace, now_dt=dt.datetime.now
) -> None:
    """
    Prepend a new jotting with a timestamp to the jot file.

    Args:
        jot_path (Path): The path to the jot file.
        args (argparse.Namespace): Arguments collected from the argument parser.
        now_dt (dt.datetime): Datetime of execution.

    Returns:
        None: Prints output.
    """
    jot_file_content = ""

    if jot_path.exists():
        jot_file_content = jot_path.read_text(encoding="utf-8")
    else:
        jot_path.write_text("", encoding="utf-8")
        console.print(f":white_check_mark: Created jot file at [green]{jot_path}[/]")

    timestamp = now_dt().strftime("%Y-%m-%d %H:%M")
    jot_path.write_text(
        f"[{timestamp}] {args.text}\n{jot_file_content}",
        encoding="utf-8",
    )
    console.print(f":white_check_mark: Jotted at {timestamp}")


def create_jot_file(prompt_user=Prompt.ask) -> Path:
    """
    Prompt the user for a jot file path and create it.

    Args:
        prompt_user (Prompt.ask): Prompt the user for input.

    Returns:
        Path: The file path to the jot file.
    """
    while True:
        jot_path_str = prompt_user(":pencil: Provide a path for the jot file (.txt)")

        if Path(jot_path_str).suffix != ".txt":
            console.print(":x: You must provide a .txt file path. Try again.")
            continue

        jot_path = Path(jot_path_str).expanduser().resolve()

        if jot_path.exists():
            confirm = prompt_user(":exclamation: File already exists. Use it? y/n")
            if confirm.lower() != "y":
                continue
        else:
            jot_path.parent.mkdir(parents=True, exist_ok=True)
            jot_path.touch()

        return jot_path


def check_in_period(
    line: str, period_from: dt.datetime | None, period_to: dt.datetime | None
) -> bool:
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
        console.print(
            f":x: Couldn't find the jot file recorded in the config: [green]{jot_path}[/]",
            "\n:pencil: Try 'jot hello' to create it and add a jotting.",
        )
        return

    lines = jot_path.read_text(encoding="utf-8").splitlines()

    if period_to is not None or period_from is not None:
        lines = [
            line for line in lines if check_in_period(line, period_from, period_to)
        ]

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
        console.print(
            f":x: Couldn't find the jot file recorded in the config: [green]{jot_path}[/]",
            "\n:pencil: Try 'jot hello' to create it and add a jotting.",
        )
        return

    with jot_path.open("r", encoding="utf-8") as f:
        lines = [line.rstrip("\n") for line in f]
    matches = [line for line in lines if re.search(search_term, line)]

    if period_to is not None or period_from is not None:
        matches = [
            line for line in matches if check_in_period(line, period_from, period_to)
        ]

    if limit is not None:
        matches = matches[:limit]

    for line in matches:
        console.print(f"{line}")


def print_paths(config_dir: Path | None = None) -> None:
    """
    Print the expected path to the config file and read the jot path from it.

    Args:
        config_file (str): The file name for the config file.
        config_dir (Path): The user's config directory.

    Returns:
        None: Prints output.
    """
    config_path = get_config_path(config_dir=config_dir)
    if not config_path.exists():
        console.print(
            f":x: Couldn't find the config file in the expected location: [red]{config_path}[/]"
        )
        return

    console.print(f":round_pushpin: Config file: [green]{config_path}[/]")

    jot_path = read_jot_path(config_path)
    if not jot_path.exists():
        console.print(
            f":x: Couldn't find the jot file in the expected location: [red]{jot_path}[/]"
        )
        return

    console.print(f":round_pushpin: Jot file: [green]{jot_path}[/]")


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
