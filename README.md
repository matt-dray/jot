# jot

[![Project Status: Active – The project has reached a stable, usable state and is being actively developed.](https://www.repostatus.org/badges/latest/active.svg)](https://www.repostatus.org/#active)
[![Blog
posts](https://img.shields.io/badge/rostrum.blog-posts-008900?labelColor=000000&logo=data%3Aimage%2Fgif%3Bbase64%2CR0lGODlhEAAQAPEAAAAAABWCBAAAAAAAACH5BAlkAAIAIf8LTkVUU0NBUEUyLjADAQAAACwAAAAAEAAQAAAC55QkISIiEoQQQgghRBBCiCAIgiAIgiAIQiAIgSAIgiAIQiAIgRAEQiAQBAQCgUAQEAQEgYAgIAgIBAKBQBAQCAKBQEAgCAgEAoFAIAgEBAKBIBAQCAQCgUAgEAgCgUBAICAgICAgIBAgEBAgEBAgEBAgECAgICAgECAQIBAQIBAgECAgICAgICAgECAQECAQICAgICAgICAgEBAgEBAgEBAgICAgICAgECAQIBAQIBAgECAgICAgIBAgECAQECAQIBAgICAgIBAgIBAgEBAgECAgECAgICAgICAgECAgECAgQIAAAQIKAAAh%2BQQJZAACACwAAAAAEAAQAAAC55QkIiESIoQQQgghhAhCBCEIgiAIgiAIQiAIgSAIgiAIQiAIgRAEQiAQBAQCgUAQEAQEgYAgIAgIBAKBQBAQCAKBQEAgCAgEAoFAIAgEBAKBIBAQCAQCgUAgEAgCgUBAICAgICAgIBAgEBAgEBAgEBAgECAgICAgECAQIBAQIBAgECAgICAgICAgECAQECAQICAgICAgICAgEBAgEBAgEBAgICAgICAgECAQIBAQIBAgECAgICAgIBAgECAQECAQIBAgICAgIBAgIBAgEBAgECAgECAgICAgICAgECAgECAgQIAAAQIKAAA7)](https://www.rostrum.blog/index.html#category=jot)

Minimal opinionated Python CLI to jot timestamped thoughts.

## Install

1. Install [uv](https://docs.astral.sh/uv/).
2. Run `uv tool install git+https://github.com/matt-dray/jot` in a terminal.

To update: `uv tool update jot`.

## Use

### Write

Open a terminal and write a jotting:

```bash
jot "ate an apple"
```

The first time you run `jot`, you'll be prompted for a path to a text file where your jottings will be written. The (resolved, absolute and POSIX-standardised) file path will be stored under the `JOT_PATH` key in a `jot_config.json` file saved to your computer's home folder.

Each jotting is prepended to the text file in the form `[YYYY-MM-DD HH:MM] ate an apple`.

### Options

Other options are to use the:

* `--help` or `-h` flag for documentation, like `jot -h`
* `--list` or `-l` flag to show the last _n_ jottings, like `jot -l 5`
* `--search` or `-s` flag to search your jottings for a given term, like `jot -s "apple"` (regular expressions supported)

## Notes

* Developed to help me remember the tasks I've done during my day job.
* Your kilometerage may vary; [leave an issue](https://github.com/matt-dray/jot/issues) if you find bugs or have suggestions.
* [v0.1.0](https://github.com/matt-dray/jot/releases/tag/v0.1.0) developed via LLM, [v0.2.0](https://github.com/matt-dray/jot/compare/v0.1.0...v0.2.0) rewritten with my brain (you can [read about it](https://www.rostrum.blog/posts/2025-08-25-jot/)).
