"""
CLI entry with argument parser.
"""

import argparse
from importlib.metadata import version
from jot.core import (
    create_jot_file,
    get_config_path,
    list_jottings,
    read_jot_path,
    search_jottings,
    write_to_config,
    write_jotting,
)


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

    config_path = get_config_path()

    if config_path.exists():
        jot_path = read_jot_path(config_path)
    else:
        jot_path = create_jot_file()
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
