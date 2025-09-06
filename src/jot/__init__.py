"""
Minimal opinionated Python CLI to jot timestamped thoughts.
"""

from .core import (
    generate_jot,
    get_config_path,
    get_jot_path,
    list_jottings,
    search_jottings,
    write_to_config,
    write_jotting,
)

__all__ = [
    "generate_jot",
    "get_config_path",
    "get_jot_path",
    "list_jottings",
    "search_jottings",
    "write_to_config",
    "write_jotting",
]
