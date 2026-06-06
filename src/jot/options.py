"""
Options available to the CLI user.
"""

import datetime as dt
from pathlib import Path
import re
import shutil
import socket
import subprocess

from .files import get_config_path, read_config, write_to_config

from rich.console import Console
from rich.prompt import Prompt

console = Console()


def check_in_period(
    line: str, period_from: dt.datetime | None, period_to: dt.datetime | None
) -> bool:
    """
    Check if a jotting falls within user-specified time period.

    Args:
        line (str): A single entry in the jot file.
        period_from (dt.datetime): Date (YYYYMMDD) start (inclusive).
        period_to (dt.datetime): Date (YYYYMMDD) end (exclusive).

    Returns:
        bool: Does the jotting fall in the time period?
    """
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


def print_paths(config_dir: Path | None = None) -> None:
    """
    Print the expected path to the config file and read the jot path from it.

    Args:
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

    jot_path = read_config(config_path, "JOT_PATH")
    jot_path = Path(jot_path)

    if not jot_path.exists():
        console.print(
            f":x: Couldn't find the jot file in the expected location: [red]{jot_path}[/]"
        )
        return

    console.print(f":round_pushpin: Jot file: [green]{jot_path}[/]")


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


def upload_jottings(config_path: Path, prompt_user=Prompt.ask) -> None:
    """
    Upload jot file contents to a GitHub gist.

    Args:
        config_path (Path): The path to the config file.
        prompt_user (Prompt.ask): Prompt the user for input.

    Returns:
        None: Uploads to GitHub and prints success.

    Notes:
        Requires the GitHub CLI (gh) to be installed and the user authenticated.
        Install the GitHub CLI at https://cli.github.com.
        Run 'gh auth login' before using this command.
    """
    if shutil.which("gh") is None:
        console.print(":x: GitHub CLI not found. Install it at https://cli.github.com.")
        return

    if _has_internet() is False:
        console.print(":x: No internet connection. Can't upload.")
        return

    result = subprocess.run(["gh", "auth", "status"], capture_output=True)
    if result.returncode != 0:
        console.print(":x: Not logged in to GitHub CLI. Run 'gh auth login' first.")
        return

    try:
        gist_id = read_config(config_path, "GIST_ID")
    except KeyError:
        console.print(":x: Couldn't find a gist ID recorded in the config.")
        while True:
            gist_id = prompt_user(":pencil: Provide a GitHub gist ID")
            if len(gist_id) != 32:
                console.print(
                    ":x: You must provide a 32-character GitHub gist ID hash. Try again."
                )
                continue
            else:
                break
        write_to_config(config_path, "GIST_ID", gist_id)

    result = subprocess.run(
        ["gh", "gist", "view", gist_id],
        capture_output=True,
    )
    if result.returncode != 0:
        console.print(f":x: Couldn't find a gist with ID {gist_id}.")
        return

    try:
        jot_path = read_config(config_path, "JOT_PATH")
    except KeyError:
        console.print(
            ":x: Couldn't find a jot file path recorded in the config.",
            "\n:pencil: Try 'jot hello' to create it and add a jotting.",
        )
        return

    result = subprocess.run(["gh", "gist", "edit", gist_id, jot_path])
    if result.returncode != 0:
        console.print(":x: Upload failed.")
        return
    console.print(":white_check_mark: Success.")


def _has_internet() -> bool:
    try:
        socket_check = socket.create_connection(
            ("8.8.8.8", 53),  # Google's DNS server, DNS port
            timeout=3,  # fail if it takes longer than this
        )
        socket_check.close()
        return True
    except OSError:
        return False


__all__ = [
    "check_in_period",
    "list_jottings",
    "print_paths",
    "search_jottings",
    "upload_jottings",
]
