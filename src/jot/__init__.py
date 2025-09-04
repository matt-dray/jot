import argparse
import datetime as dt
from importlib.metadata import version
import json
from pathlib import Path
import re


def build_config_path(json_path=".jot-config.json"):
    """Return the path to the config file in the user's home directory."""
    config_path = Path.home() / json_path
    return config_path


def get_jot_path(config_path):
    """Load the jot file path from the config file."""
    config_text = config_path.read_text()
    config_json = json.loads(config_text)
    jot_path_text = config_json["JOT_PATH"]
    jot_path = Path(jot_path_text)
    return jot_path


def write_to_config(config_path, jot_path):
    """Write the jot file path to the config file."""
    json_dict = {"JOT_PATH": jot_path.as_posix()}
    with config_path.open("w", encoding="utf-8") as f:
        json.dump(json_dict, f)
    print(f"Config file written to {config_path}")
    print(f"Text file path set to {jot_path}")


def write_jotting(jot_path, args):
    """Prepend a new jotting with a timestamp to the jot file."""

    jot_file_content = ""
    if jot_path.exists():
        with jot_path.open("r", encoding="utf-8") as f:
            jot_file_content = f.read()

    timestamp = dt.datetime.now().strftime("[%Y-%m-%d %H:%M]")
    with jot_path.open("w", encoding="utf-8") as f:
        f.write(f"{timestamp} {args.text}\n{jot_file_content}")
    print(f'Wrote "{args.text}" to {jot_path}')


def generate_jot():
    """Prompt the user for a jot file path and create it."""
    jot_path_user = input("Path to text file: ")
    jot_path = Path(jot_path_user).expanduser().resolve()
    jot_path.touch()
    return jot_path


def list_jottings(jot_path, n=None):
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


def search_jottings(jot_path, search_term, limit=None):
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


def main():
    """CLI entry point for jot."""
    parser = argparse.ArgumentParser(
        prog="jot",
        description="Minimal opinionated Python CLI to jot timestamped thoughts.",
        epilog=(
            "examples:\n"
            "  jot 'ate an apple'    add a new jotting\n"
            "  jot -l 5              show last 5 jottings\n"
            "  jot -s apple          search for 'apple' in jottings\n"
            "  jot -s apple -l 3     search for 'apple' and limit to last 3 jottings\n"
            f"\nsource: https://github.com/matt-dray/jot (v{version('jot')})"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "text",
        nargs="?",
        type=str,
        help="text to write to file",
    )
    parser.add_argument("-v", "--version", action="version", version=version("jot"))
    parser.add_argument(
        "-l",
        "--list",
        nargs="?",
        type=int,
        const=10,
        default=None,
        help="show last n jottings (default 10 if no number), "
        "combine with --search to limit results",
    )
    parser.add_argument(
        "-s",
        "--search",
        nargs="?",
        type=str,
        help="search jottings (regex supported), "
        "combine with --list to limit results",
    )
    args = parser.parse_args()

    config_path = build_config_path()

    if config_path.exists():
        jot_path = get_jot_path(config_path)
    else:
        jot_path = generate_jot()
        write_to_config(config_path, jot_path)

    if args.search:
        search_jottings(jot_path, args.search, args.list)
    elif args.list is not None:
        list_jottings(jot_path, args.list)
    elif args.text:
        write_jotting(jot_path, args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
