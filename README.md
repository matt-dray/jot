# jott <a href="https://www.github.com/matt-dray/jott"><img src='https://www.rostrum.blog/posts/2025-08-30-jot-options/resources/jot.png' height='150px' align='right' alt='Terribly drawn image of the word "jot" in cursive with a pencil at the end of the letter "t". The dot of the letter "i" is a red love heart.'></a>

[![Project Status: Active – The project has reached a stable, usable state and is being actively developed.](https://www.repostatus.org/badges/latest/active.svg)](https://www.repostatus.org/#active)
[![Quality](https://github.com/matt-dray/jott/actions/workflows/quality.yaml/badge.svg)](https://github.com/matt-dray/jott/actions/workflows/quality.yaml)
[![Tests](https://github.com/matt-dray/jott/actions/workflows/tests.yaml/badge.svg)](https://github.com/matt-dray/jott/actions/workflows/tests.yaml)
[![Blog
posts](https://img.shields.io/badge/rostrum.blog-black?style=flat&labelColor=00ff00&logo=data%3Aimage%2Fgif%3Bbase64%2CR0lGODdhoACgAJEAAAAAAP%2F%2F%2FwAAAAAAACH5BAlkAAIALAAAAACgAKAAAAL%2FlI%2BpywgPY5u02hQzuLz7r0nfSBohVKbqdT7rS7UbTMNyjR93zoNtX9sBh7EfcSU8Kh3GJSnpVEKjnCkVaL0WT1pps2vJgr1cp3gMPufU6Cs7%2BG233zS6nByK2u%2FEPTLO1%2BWnMhi4BjhUaAhXtqS4aIOIJQmJpvhYqXVJmbm42dgZ%2BpkXWjqqUWrKOYGZioc60urat9ogOzsJ2nGLy3Oa0VtVy3AmUzy8wMuCrHBsTErMjCH9pytszfQMG40dRk34bcKpDZ0cLqDs3V3hTI5ie57OHj%2FuLsJdvnv%2BRL%2BObv8O3zYP8rbku3YwG0BW%2FRLmcjjPH8CA5vwxtIjj172K%2FwvhYRQITE67gc0mzgC5seRHS%2FUkmrwI8d%2FKMSNDotQGk%2BS0mWlaxjR5kqNOhUMN1Uy5s%2BNNFx5j3jlKUaVSoTapIvXks6i4iTmrStXKByrTpca6XtWxz0xWr0ntmY3ali1Wl3SnfpWLlqeghkDdxkrriG9fcvz0ahI8%2BFlhpyIRJ9YIdy5jso%2FBvh2bCXLlyVYjG3W82XJT0XNAhz4bkTNN06cx6zPshnXrxaQzv1TLNZg6u7Ry6zboN7Dv36Pd6blNvDhh3LyTEzXOPLjzu8uFN58u83oPoNg7K44Ovfvz6q%2FCi0%2FRuuz5w%2Blhr6%2FWvvZ7RvHxzn9Y3%2FP97fnt7%2F8%2F1J9%2B%2F2UUoIAD1lGgawf6kmBQ54mlHmVrkUedgQTWJV2F30mIoX8A%2FoScdxGKCOFxHVIYF4rj4aSchfSBxV2LG5I4oYsInsgihyAOp6GDve2oXXYZppijiCYCOeSKM%2FZYInioCWkekzUuSaSCiUw5opQ4Uqmkj3tt6WVeQTbZCZk0gnlZmIGYqSWS%2FhX0IYxYslmlmmFhmSadXaqCpoxZ1pkmn24%2BGSNZgYqCp596iilfT33qKOejtknaZqSD2hgMhIsuaKSiiXKamqVJMuohqFtdyiWpT5p6qqhRAsrqoZC%2BCdh6mn4aa6ezElrrg3PimiusuwoIJ6I81nmre4L%2Fjtrqq10WW9qxz%2F6qrLFjhlhpqb8Veiaqf3bHbba8SotduMhSq1ov5k4LJrQskdusiqoW6Su8UMobL73qAnsupcJO6m2e%2FO5pravjXuuvZAYTi%2B2%2FPS5La7sDz2vlZwlT%2FC3GsgK8cMX5pvqxne5GcnHIm96LqaMBe1oyyh7f2fK6GvsJ8cEdZxzyxpWcLHPONBccsbc89%2FrjzQLHTPSVSNt78lMTm%2Fy0y3Y6vTTCK5cZdc9S6wzJ0ExHTfXV3Rr9c7TpEjzsy5pNfeHZM6ctsmlHNor22EHT%2FXZ5q5Ztt83a6qp3ynWLy7B7IzuM0M1N833E2keL%2FZrb6MnNMuSJPv9NsuRbV062D9V6rnmyli%2FzOceYIx7s5IYnnbrjqWeOt8%2Bvwxf75rODs3rpt7t%2Bu%2Bqhsx4s773TdvrgkBQAADs%3D)](https://www.rostrum.blog/index.html#category=jott)

Minimal opinionated Python command-line interface (CLI) to jot timestamped thoughts.

## Install

Recommended:

1. Install [uv](https://docs.astral.sh/uv/).
2. Run `uv tool install git+https://github.com/matt-dray/jott` in a terminal.
3. Update with `uv tool update jott`.

Requires Python >=3.10. 

## CLI

### Write

Open a terminal and write a jotting:

```bash
jott "ate an apple"
```

The first time you run `jott`, you'll be prompted for a path to a text file ('jott file') where your jottings will be written.
The file path will be stored under the `JOTT_PATH` key in a `config.json` file, which is saved to the OS-dependent location resolved by `platformdirs.user_config_path("jott")`.

Each jotting is timestamped and prepended to your text file:

```
[2025-08-28 11:15] ate an apple
[2025-08-27 10:58] ate a kiwi
[2025-08-26 11:09] ate a pineapple
[2025-08-25 10:40] ate an apple and a pear
```

### Options

You can review your jottings using the provided options. For example:

* `jott -l 3` to <u>l</u>ist the last three
* `jott -s apple -l 1` to <u>s</u>earch for 'apple' and <u>l</u>imit to the most recent one
* `jott -s "[^pine]apple"` to <u>s</u>earch for 'apple' with a regular expression that excludes 'pineapple'
* `jott -f 20250825 -t 20250828` to return jottings <u>f</u>rom 25 Aug 2025 (inclusive) and <u>t</u>o 28 Aug 2025 (exclusive)

And for information:

* `jott -w` to show <u>w</u>here the config and jott files are
* `jott -v` to get the <u>v</u>ersion number
* `jott -h` to show the <u>h</u>elp file, which includes possible option combinations

## Notes

* I developed this tool to help me remember the tasks I've done during my day job and later reflect.
* Your kilometerage may vary; [leave an issue](https://github.com/matt-dray/jott/issues) if you find bugs or have suggestions.
* [v0.1.0](https://github.com/matt-dray/jot/releases/tag/v0.1.0) developed via LLM, [v0.2.0](https://github.com/matt-dray/jott/compare/v0.1.0...v0.2.0) rewritten with my brain (you can [read about it](https://www.rostrum.blog/posts/2025-08-25-jot/)).
