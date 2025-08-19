def main():

    import argparse
    import datetime as dt
    import json
    from pathlib import Path

    # Set up parser
    parser = argparse.ArgumentParser(
        prog = "jot",
        description = "Minimal Python CLI to jot timestamped thoughts."
    )
    parser.add_argument("text", help = "Text to write to file.", type = str)
    args = parser.parse_args()

    # Read/write config file
    config_path = Path.home()/".jot_config.json"
    if config_path.exists():
        jot_path = json.loads(config_path.read_text())["JOT_PATH"]
    else:
        # Receive user input
        jot_path_user = input("Full text file path: ")
        jot_path = Path(jot_path_user)
        jot_path.touch()
        # Write to config
        config_file = open(config_path, mode = "w")
        try:
            json_dict = {"JOT_PATH": str(jot_path)}
            json_string = json.dumps(json_dict)
            config_file.write(json_string)
            print(f"Config file written to {config_path}")
            print(f"Text file path set to {jot_path}")
        finally:
            config_file.close()

    # Read existing jottings
    jot_file = open(jot_path, mode = "r")
    try:
        jot_file_content = jot_file.read()
    finally:
        jot_file.close()

    # Prepend new jotting
    jot_file = open(jot_path, mode = "w")
    try:
        timestamp = dt.datetime.now().strftime("[%Y-%m-%d %H:%M]")
        # Prepend to file
        jot_file.write(f"{timestamp} {args.text}\n{jot_file_content}")
        print(f"Wrote \"{args.text}\" to {jot_path}")
    finally:
        jot_file.close()

if __name__ == "__main__":
    main()