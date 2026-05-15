import argparse
import datetime as dt
import json
from pathlib import Path

import pytest

import jott.core as core


def test_get_config_path(tmp_path: Path):
    path = core.get_config_path(
        config_file="config.json",
        config_dir=tmp_path,
    )
    assert path == tmp_path / "config.json"


def test_write_and_read_config(tmp_path: Path):
    config = tmp_path / "config.json"
    jott = tmp_path / "jott.txt"

    core.write_to_config(config, jott)

    data = json.loads(config.read_text())
    assert data["JOTT_PATH"] == jott.as_posix()
    assert core.read_jott_path(config) == jott


def test_write_jotting_prepends(tmp_path: Path):
    def fixed_now():
        return dt.datetime(2025, 12, 25, 1, 0)

    jott = tmp_path / "jott.txt"
    jott.write_text("[2025-12-24 23:00] egg\n")

    args = argparse.Namespace(text="spam")

    core.write_jotting(jott, args, now_dt=fixed_now)

    content = jott.read_text()
    assert content.startswith("[2025-12-25 01:00] spam")
    assert "egg" in content


def test_create_jott_file(tmp_path: Path):
    def prompt(_):
        return str(tmp_path / "spam.txt")

    jott = core.create_jott_file(prompt_user=prompt)

    assert jott.exists()
    assert jott.name == "spam.txt"


def test_check_in_period_valid():
    line = "[2025-12-25 09:00] spam"
    start = dt.datetime(2025, 12, 1)
    end = dt.datetime(2025, 12, 31)

    assert core.check_in_period(line, start, end)


@pytest.mark.parametrize(
    "line",
    [
        "spam",
        "[spam]",
        "[9999-99-99 99:99] spam",
    ],
)
def test_check_in_period_invalid(line):
    assert core.check_in_period(line, None, None) is False


def test_list_jottings(tmp_path: Path, capsys: pytest.CaptureFixture[str]):
    jott = tmp_path / "jott.txt"
    jott.write_text(
        "[2025-12-03 09:00] egg and spam\n"
        "[2025-12-02 09:00] spam and spam\n"
        "[2025-12-01 09:00] lobster thermidor\n"
    )

    core.list_jottings(jott, limit=2)

    out = capsys.readouterr().out
    assert "egg and spam" in out
    assert "spam and spam" in out
    assert "lobster thermidor" not in out


def test_search_jottings(tmp_path: Path, capsys: pytest.CaptureFixture[str]):
    jott = tmp_path / "jott.txt"
    jott.write_text(
        "[2025-12-03 09:00] egg and spam\n"
        "[2025-12-02 09:00] spam and spam\n"
        "[2025-12-01 09:00] lobster thermidor\n"
    )

    core.search_jottings(jott, "egg")

    out = capsys.readouterr().out
    assert "egg" in out
    assert "lobster" not in out


def test_print_paths_missing_config(tmp_path: Path, capsys: pytest.CaptureFixture[str]):
    core.print_paths(config_dir=tmp_path)

    out = capsys.readouterr().out
    assert "Couldn't find the config file" in out
