"""
Minimal opinionated Python CLI to jot timestamped thoughts.
"""

from .core import (
    generate_jot,
    get_config_path,
    list_jottings,
    read_jot_path,
    search_jottings,
    write_to_config,
    write_jotting,
)

__all__ = [
    "generate_jot",
    "get_config_path",
    "list_jottings",
    "read_jot_path",
    "search_jottings",
    "write_to_config",
    "write_jotting",
]
