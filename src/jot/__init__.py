"""
Minimal opinionated Python CLI to jot timestamped thoughts.
"""

from .files import (
    create_jot_file,
    get_config_path,
    read_config,
    write_to_config,
    write_jotting,
)

from .options import (
    check_in_period,
    list_jottings,
    print_paths,
    search_jottings,
    upload_jottings,
)

__all__ = [
    "check_in_period",
    "create_jot_file",
    "get_config_path",
    "list_jottings",
    "print_paths",
    "read_config",
    "search_jottings",
    "upload_jottings,write_to_config",
    "write_jotting",
    "write_to_config",
    "upload_jottings",
]
