"""
Minimal opinionated Python CLI to jot timestamped thoughts.
"""

from .core import (
    create_jott_file,
    get_config_path,
    list_jottings,
    print_paths,
    read_jott_path,
    search_jottings,
    write_to_config,
    write_jotting,
)

__all__ = [
    "create_jott_file",
    "get_config_path",
    "list_jottings",
    "print_paths",
    "read_jott_path",
    "search_jottings",
    "write_to_config",
    "write_jotting",
]
