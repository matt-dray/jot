import argparse
import datetime as dt
import json
from pathlib import Path


def build_config_path(json_path=".jot-config.json"):
    """Return the path to the config file in the user's home directory."""
    config_path = Path.home() / json_path
    return config_path


def get_jot_path(config_path):
    """Load the jot file path from the config file."""
    config_text = config_path.read_text()
    config_json = json.loads(config_text)
    jot_path = config_json["JOT_PATH"]
    return jot_path


def write_to_config(config_path, jot_path):
    """Write the jot file path to the config file."""
    json_dict = {"JOT_PATH": jot_path.as_posix()}
    with config_path.open("w") as f:
        json.dump(json_dict, f)
    print(f"Config file written to {config_path}")
    print(f"Text file path set to {jot_path}")


def prepend_jotting(jot_path, args):
    """Prepend a new jotting with a timestamp to the jot file."""

    jot_file_content = ""
    if jot_path.exists():
        with jot_path.open("r") as f:
            jot_file_content = f.read()

    timestamp = dt.datetime.now().strftime("[%Y-%m-%d %H:%M]")
    with jot_path.open("w") as f:
        f.write(f"{timestamp} {args.text}\n{jot_file_content}")
    print(f'Wrote "{args.text}" to {jot_path}')


def generate_jot():
    """Prompt the user for a jot file path and create it."""
    jot_path_user = input("Path to text file: ")
    jot_path = Path(jot_path_user).expanduser().resolve()
    jot_path.touch()
    return jot_path


def main():
    """CLI entry point for jot."""
    parser = argparse.ArgumentParser(
        prog="jot",
        description="Minimal opinionated Python CLI to jot timestamped thoughts.",
    )
    parser.add_argument("text", help="Text to write to file.", type=str)
    args = parser.parse_args()

    config_path = build_config_path()

    if config_path.exists():
        jot_path = get_jot_path(config_path)
    else:
        jot_path = generate_jot()
        write_to_config(config_path, jot_path)

    prepend_jotting(jot_path, args)


if __name__ == "__main__":
    main()
