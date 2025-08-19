# jot

Minimal opinionated Python CLI to jot timestamped thoughts.

## Install

1. Install [uv](https://docs.astral.sh/uv/).
2. `git clone` this repo.
3. Navigate with `cd path/to/cloned/repo`.
4. Install with `uv tool install . -e`.

## Use

Open a terminal and type:

```bash
jot "ate an apple"
```

The first time you run `jot`, you'll be prompted for a full path to a text file where your jottings will be written. This path is stored in the config file `~/.jot_config.json` under the key `JOT_PATH`.

Your jotting will be prepended to the text file in the form `[YYYY-MM-DD HH:MM] ate an apple`.

## Notes

* Developed to help me remember my work tasks.
* Your kilometerage may vary.
* [v0.1.0](https://github.com/matt-dray/jot/releases/tag/v0.1.0) developed via LLM, v0.2.0 rewritten with my brain.
