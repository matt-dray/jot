import sys
from datetime import datetime
from pathlib import Path
import json
from rich.console import Console

console = Console()

CONFIG_FILE = Path.home() / ".jot_config.json"

def get_file_path():
    if CONFIG_FILE.exists():
        try:
            config = json.loads(CONFIG_FILE.read_text())
            return Path(config["file_path"])
        except (json.JSONDecodeError, KeyError):
            console.print("[yellow]Warning:[/yellow] Config file is corrupted. Reconfiguring...")

    console.print("[cyan]Please enter the full path to the text file you want to use:[/cyan]")
    user_path = input("> ").strip()
    file_path = Path(user_path).expanduser()

    CONFIG_FILE.write_text(json.dumps({"file_path": str(file_path)}))
    console.print(f"[green]Saved file path to {CONFIG_FILE}[/green]")
    return file_path

def main():
    if len(sys.argv) < 2:
        console.print("[red]Error:[/red] Please provide a text string to append.")
        sys.exit(1)

    text = " ".join(sys.argv[1:])
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    line = f"[{now}] {text}\n"

    file_path = get_file_path()

    try:
        # Read existing lines
        if file_path.exists():
            with open(file_path, "r", encoding="utf-8") as f:
                lines = f.readlines()
        else:
            lines = []

        # Prepend the new line
        lines.insert(0, line)

        # Write back all lines
        with open(file_path, "w", encoding="utf-8") as f:
            f.writelines(lines)

        console.print(f"[green]Prepended to {file_path}:[/green] {line.strip()}")
    except Exception as e:
        console.print(f"[red]Error writing to file:[/red] {e}")

if __name__ == "__main__":
    main()
