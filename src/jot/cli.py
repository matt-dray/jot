"""
CLI entry with argument parser.
"""

import argparse
from dateutil.parser import parse as date_time
from importlib.metadata import version
from pathlib import Path

from .files import (
    create_jot_file,
    get_config_path,
    read_config,
    write_to_config,
    write_jotting,
)

from .options import list_jottings, print_paths, search_jottings, upload_jottings


def main() -> None:
    """
    CLI entry point for jot.

    Returns:
        None: Performs action depending on user input.
    """
    parser = argparse.ArgumentParser(
        prog="jot",
        description="Minimal opinionated Python CLI to jot timestamped thoughts.",
        epilog=(
            "examples:\n"
            "  jot 'ate an apple'    add a new jotting\n"
            "  jot -l 5              show last 5 jottings\n"
            "  jot -s apple          search for 'apple' in jottings\n"
            "  jot -s apple -l 3     search for 'apple' and limit to last 3 jottings\n"
            "  jot -u                upload to a GitHub gist (requires gh login)\n"
            f"\nsource: https://github.com/matt-dray/jot (v{version('jot-cli')})"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "text",
        nargs="?",
        type=str,
        help="text to write to file",
    )
    parser.add_argument("-v", "--version", action="version", version=version("jot-cli"))
    parser.add_argument(
        "-l",
        "--list",
        nargs="?",
        type=int,
        const=10,
        default=None,
        help="show last n jottings (default 10 if no number), "
        "combine with --search, --from-date, --to-date to limit results",
    )
    parser.add_argument(
        "-s",
        "--search",
        nargs="?",
        type=str,
        help="search jottings (regex supported), combine with "
        "--list, --from-date, --to-date to limit results",
    )
    parser.add_argument(
        "-f",
        "--from-date",
        type=date_time,
        default=None,
        help="list jottings starting from this date, combine with "
        "--list or --search to limit results",
    )
    parser.add_argument(
        "-t",
        "--to-date",
        type=date_time,
        default=None,
        help="list jottings before this date, combine with "
        "--list or --search to limit results",
    )
    parser.add_argument(
        "-w",
        "--where",
        action="store_true",
        help="print locations of config and jot files",
    )
    parser.add_argument(
        "-u",
        "--upload",
        action="store_true",
        help="upload jottings to a GitHub gist",
    )
    args = parser.parse_args()

    config_path = get_config_path()

    if config_path.exists():
        jot_path = read_config(config_path, "JOT_PATH")
        jot_path = Path(jot_path)
    else:
        jot_path = create_jot_file()
        write_to_config(config_path, "JOT_PATH", jot_path.as_posix())

    if args.where:
        print_paths()
    elif args.search:
        search_jottings(jot_path, args.search, args.list, args.from_date, args.to_date)
    elif args.list is not None:
        list_jottings(jot_path, args.list, args.from_date, args.to_date)
    elif args.from_date is not None or args.to_date is not None:
        list_jottings(jot_path, None, args.from_date, args.to_date)
    elif args.upload:
        upload_jottings(config_path)
    elif args.text:
        write_jotting(jot_path, args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
