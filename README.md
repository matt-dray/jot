# Jot CLI

Jot is a minimal, cross-platform Python command-line tool for quickly logging daily activities or notes with a timestamp. It prepends each entry with the current date and time (`[YYYY-MM-DD HH:MM]`) to a user-configurable text file.

*Note: This project was generated with assistance from OpenAI's ChatGPT.*

## Features
- Simple CLI interface.
- Persistent configuration of the text file path.
- Prepends new entries at the top of the file.
- Uses human-friendly colored output via `rich`.

## Installation

1. Clone or download this repository.
2. Navigate to the project directory:
   ```bash
   cd /path/to/jot
   ```
3. Install locally in editable mode:
   ```bash
   pip3 install --user --editable .
   ```
   - This will also install the `rich` library.
4. Make sure your scripts folder is in your PATH:
   - **macOS/Linux**:
     ```bash
     export PATH="$HOME/.local/bin:$PATH"
     echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
     ```
   - **Windows**:
     If you installed with `pip3 install --user`, the executable will usually be in:
     ```
     %APPDATA%\Python\Python312\Scripts
     ```
     *(replace `Python312` with your Python version)*

     To add it to your PATH:
     1. Press `Win + R`, type `sysdm.cpl`, and press Enter.
     2. Go to **Advanced** → **Environment Variables**.
     3. Under **User variables**, select **Path** and click **Edit**.
     4. Click **New** and paste the Scripts folder path above.
     5. Click OK on all dialogs.
     6. Restart your terminal or Command Prompt.

## Usage

Once installed, you can run `jot` from any terminal:

```bash
jot "Your text goes here"
```

The first time you run it, you will be prompted to provide a path to the text file where entries should be saved. This path is stored in `~/.jot_config.json` and used for future runs.

Example:
```bash
$ jot "Finished reading a book"
Prepended to /Users/username/journal.txt: [2025-08-14 10:30] Finished reading a book
```

## Notes
- Ensure Python 3.8+ is installed.
- Works on macOS, Linux, and Windows.
- Entries are prepended, so the newest item appears at the top.

## Dependencies
- `rich >= 13.0`

## License
MIT License
