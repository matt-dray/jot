"""
Minimal opinionated Python CLI to jot timestamped thoughts.
"""

from .core import (
    build_config_path,
    generate_jot,
    get_jot_path,
    list_jottings,
    search_jottings,
    write_to_config,
    write_jotting,
)

__all__ = [
    "build_config_path",
    "generate_jot",
    "get_jot_path",
    "list_jottings",
    "search_jottings",
    "write_to_config",
    "write_jotting",
]
