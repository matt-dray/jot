"""
Read and write config and jot files.
"""

import argparse
import datetime as dt
import json
from pathlib import Path
from platformdirs import user_config_path

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


def read_config(config_path: Path, key: str) -> str:
    """
    Read the value from a key in the config file.

    Args:
        config_path (Path): The path to the config file.
        key (str): The key to read. Could be JOT_PATH or GIST_ID.

    Returns:
         str: Value for the config key, or None if not found.
    """
    config_text = config_path.read_text(encoding="utf-8")
    config_json = json.loads(config_text)
    value = config_json.get(key)
    if value is None:
        raise KeyError(f"{key} not found in config.")
    return value


def write_to_config(
    config_path: Path, key: str, value: str, prompt_user=Prompt.ask
) -> None:
    """
    Write a key-value pair to the config file.

    Args:
        config_path (Path): The path to the config file.
        key (str): The JSON key to be written to the config file.
        value (ste): The value for the JSON key to be written to the config file.
        prompt_user (Prompt.ask): Prompt the user for input.

    Returns:
        None: Writes to file and prints output.

    Notes:
        Any key-value is accepted, but JOT_PATH is required by jot and GIST_ID is optional.
    """
    if config_path.exists():
        with config_path.open("r", encoding="utf-8") as f:
            config = json.load(f)
    else:
        config = {}

    if key in config:
        overwrite = prompt_user(
            f":exclamation: [green]{key}[/] is already set to [green]{config[key]}[/]. Overwrite?",
            choices=["y", "n"],
        )
        if overwrite == "n":
            console.print(
                f":x: [green]{key}[/] will not be overwritten in the config file. Exiting."
            )
            return

    config[key] = value

    config_path.parent.mkdir(parents=True, exist_ok=True)
    with config_path.open("w", encoding="utf-8") as f:
        json.dump(config, f)

    console.print(f":white_check_mark: Set [green]{key}[/] to [green]{value}[/]")


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
            confirm = prompt_user(
                ":exclamation: File already exists. Use it?",
                choices=["y", "n"],
            )
            if confirm.lower() == "n":
                continue
        else:
            jot_path.parent.mkdir(parents=True, exist_ok=True)
            jot_path.touch()

        return jot_path


__all__ = [
    "create_jot_file",
    "get_config_path",
    "read_config",
    "write_to_config",
    "write_jotting",
]
