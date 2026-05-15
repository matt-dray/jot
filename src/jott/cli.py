"""
CLI entry with argument parser.
"""

import argparse
from dateutil.parser import parse as date_time
from importlib.metadata import version
from jott.core import (
    create_jott_file,
    get_config_path,
    list_jottings,
    print_paths,
    read_jott_path,
    search_jottings,
    write_to_config,
    write_jotting,
)


def main() -> None:
    """
    CLI entry point for jott.

    Returns:
        None: Performs action depending on user input.
    """
    parser = argparse.ArgumentParser(
        prog="jott",
        description="Minimal opinionated Python CLI to jot timestamped thoughts.",
        epilog=(
            "examples:\n"
            "  jott 'ate an apple'    add a new jotting\n"
            "  jott -l 5              show last 5 jottings\n"
            "  jott -s apple          search for 'apple' in jottings\n"
            "  jott -s apple -l 3     search for 'apple' and limit to last 3 jottings\n"
            f"\nsource: https://github.com/matt-dray/jot (v{version('jott')})"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "text",
        nargs="?",
        type=str,
        help="text to write to jott file",
    )
    parser.add_argument("-v", "--version", action="version", version=version("jott"))
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
        help="print paths to config and jott files",
    )
    args = parser.parse_args()

    config_path = get_config_path()

    if config_path.exists():
        jott_path = read_jott_path(config_path)
    else:
        jott_path = create_jott_file()
        write_to_config(config_path, jott_path)

    if args.where:
        print_paths()
    elif args.search:
        search_jottings(jott_path, args.search, args.list, args.from_date, args.to_date)
    elif args.list is not None:
        list_jottings(jott_path, args.list, args.from_date, args.to_date)
    elif args.from_date is not None or args.to_date is not None:
        list_jottings(jott_path, None, args.from_date, args.to_date)
    elif args.text:
        write_jotting(jott_path, args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
