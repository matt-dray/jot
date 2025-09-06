# jot <a href="https://www.github.com/matt-dray/jot"><img src='https://www.rostrum.blog/posts/2025-08-30-jot-options/resources/jot.png' height='150px' align='right' alt='Terribly drawn image of the word "jot" in cursive with a pencil at the end of the letter "t". The dot of the letter "i" is a red love heart.'></a>

[![Project Status: Active – The project has reached a stable, usable state and is being actively developed.](https://www.repostatus.org/badges/latest/active.svg)](https://www.repostatus.org/#active)
[![Blog
posts](https://img.shields.io/badge/rostrum.blog-posts-008900?labelColor=000000&logo=data%3Aimage%2Fgif%3Bbase64%2CR0lGODlhEAAQAPEAAAAAABWCBAAAAAAAACH5BAlkAAIAIf8LTkVUU0NBUEUyLjADAQAAACwAAAAAEAAQAAAC55QkISIiEoQQQgghRBBCiCAIgiAIgiAIQiAIgSAIgiAIQiAIgRAEQiAQBAQCgUAQEAQEgYAgIAgIBAKBQBAQCAKBQEAgCAgEAoFAIAgEBAKBIBAQCAQCgUAgEAgCgUBAICAgICAgIBAgEBAgEBAgEBAgECAgICAgECAQIBAQIBAgECAgICAgICAgECAQECAQICAgICAgICAgEBAgEBAgEBAgICAgICAgECAQIBAQIBAgECAgICAgIBAgECAQECAQIBAgICAgIBAgIBAgEBAgECAgECAgICAgICAgECAgECAgQIAAAQIKAAAh%2BQQJZAACACwAAAAAEAAQAAAC55QkIiESIoQQQgghhAhCBCEIgiAIgiAIQiAIgSAIgiAIQiAIgRAEQiAQBAQCgUAQEAQEgYAgIAgIBAKBQBAQCAKBQEAgCAgEAoFAIAgEBAKBIBAQCAQCgUAgEAgCgUBAICAgICAgIBAgEBAgEBAgEBAgECAgICAgECAQIBAQIBAgECAgICAgICAgECAQECAQICAgICAgICAgEBAgEBAgEBAgICAgICAgECAQIBAQIBAgECAgICAgIBAgECAQECAQIBAgICAgIBAgIBAgEBAgECAgECAgICAgICAgECAgECAgQIAAAQIKAAA7)](https://www.rostrum.blog/index.html#category=jot)

Minimal opinionated Python command-line interface (CLI) to jot timestamped thoughts.

## Install

Recommended:

1. Install [uv](https://docs.astral.sh/uv/).
2. Run `uv tool install git+https://github.com/matt-dray/jot` in a terminal.

To update: `uv tool update jot`.

## CLI

### Write

Open a terminal and write a jotting:

```bash
jot "ate an apple"
```

The first time you run `jot`, you'll be prompted for a path to a text file where your jottings will be written. The file path will be stored under the `JOT_PATH` key in a `jot-config.json` file saved to the location given by pathlib's `Path.home()`.

Each jotting is timestamped and prepended to the text file in the form `[2025-08-25 11:15] ate an apple`.

### Options

You can append optional flags. For example:

* `jot -l 5` to show the last 5 jottings
* `jot -s apple` to search for 'apple' in jottings
* `jot -s apple -l 3` to search for 'apple' _and_ limit to 3 jottings
* `jot -s "2025-08-2([5-9]).*apple"` to search with regex for 'apple' in a given work week
* `jot -v` to get the version number
* `jot -h` to show the help file

## Python

jot is CLI-first, but you can also import its functions to a Python session. For example:

```python
from jot import *
config_path = build_config_path()
jot_path = get_jot_path(config_path)
search_jottings(jot_path, "apple")
```

## Notes

* I developed this to help me remember the tasks I've done during my day job and later reflect.
* Your kilometerage may vary; [leave an issue](https://github.com/matt-dray/jot/issues) if you find bugs or have suggestions.
* [v0.1.0](https://github.com/matt-dray/jot/releases/tag/v0.1.0) developed via LLM, [v0.2.0](https://github.com/matt-dray/jot/compare/v0.1.0...v0.2.0) rewritten with my brain (you can [read about it](https://www.rostrum.blog/posts/2025-08-25-jot/)).
