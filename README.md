# jot

[![Project Status: Concept – Minimal or no implementation has been done yet, or the repository is only intended to be a limited example, demo, or proof-of-concept.](https://www.repostatus.org/badges/latest/concept.svg)](https://www.repostatus.org/#concept)

Minimal opinionated Python CLI to jot timestamped thoughts.

## Install

1. Install [uv](https://docs.astral.sh/uv/).
2. In a terminal run `uv tool install git+https://github.com/matt-dray/jot`

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
