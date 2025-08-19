# jot

Minimal opinionated Python CLI to jot timestamped thoughts.

## Install

1. Download uv.
2. Clone this repo.
3. `cd path/to/cloned/repo`
4. `uv tool install . -e`

## Use

Open a terminal and type:

```bash
jot "ate an apple"
```

The first time you run `jot`, you'll be prompted for a full path to a text file where your jottings will be written. This path is stored in the config file `~/.jot_config.json` under the key `JOT_PATH`.

Your jotting will be prepended to the text file in the form `[YYYY-MM-DD HH:MM] ate an apple`.
