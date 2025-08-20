import argparse
import datetime as dt
import json
from pathlib import Path


def build_config_path(json_path=".jot-config.json"):
    config_path = Path.home() / json_path
    return config_path


def get_jot_path(config_path):
    config_text = config_path.read_text()
    config_json = json.loads(config_text)
    jot_path = config_json["JOT_PATH"]
    return jot_path


def write_to_config(config_path, jot_path):
    config_file = open(config_path, mode="w")
    try:
        json_dict = {"JOT_PATH": jot_path.as_posix()}
        json_string = json.dumps(json_dict)
        config_file.write(json_string)
        print(f"Config file written to {config_path}")
        print(f"Text file path set to {jot_path}")
    finally:
        config_file.close()


def prepend_jotting(jot_path, args):

    # Read existing jottings
    jot_file = open(jot_path, mode="r")
    try:
        jot_file_content = jot_file.read()
    finally:
        jot_file.close()

    # Prepend new jotting
    jot_file = open(jot_path, mode="w")
    try:
        timestamp = dt.datetime.now().strftime("[%Y-%m-%d %H:%M]")
        # Prepend to file
        jot_file.write(f"{timestamp} {args.text}\n{jot_file_content}")
        print(f'Wrote "{args.text}" to {jot_path}')
    finally:
        jot_file.close()


def generate_jot():
    jot_path_user = input("Path to text file: ")
    jot_path = Path(jot_path_user).expanduser()
    jot_path.touch()
    return jot_path


def main():

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
