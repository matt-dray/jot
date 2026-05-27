import datetime as dt
from pathlib import Path

import pytest

import jot.options as options


@pytest.mark.parametrize(
    "line",
    [
        "spam",
        "[spam]",
        "[9999-99-99 99:99] spam",
    ],
)
def test_check_in_period_invalid(line):
    assert options.check_in_period(line, None, None) is False


def test_list_jottings(tmp_path: Path, capsys: pytest.CaptureFixture[str]):
    jot = tmp_path / "jot.txt"
    jot.write_text(
        "[2025-12-03 09:00] egg and spam\n"
        "[2025-12-02 09:00] spam and spam\n"
        "[2025-12-01 09:00] lobster thermidor\n"
    )

    options.list_jottings(jot, limit=2)

    out = capsys.readouterr().out
    assert "egg and spam" in out
    assert "spam and spam" in out
    assert "lobster thermidor" not in out


def test_search_jottings(tmp_path: Path, capsys: pytest.CaptureFixture[str]):
    jot = tmp_path / "jot.txt"
    jot.write_text(
        "[2025-12-03 09:00] egg and spam\n"
        "[2025-12-02 09:00] spam and spam\n"
        "[2025-12-01 09:00] lobster thermidor\n"
    )

    options.search_jottings(jot, "egg")

    out = capsys.readouterr().out
    assert "egg" in out
    assert "lobster" not in out


def test_check_in_period_valid():
    line = "[2025-12-25 09:00] spam"
    start = dt.datetime(2025, 12, 1)
    end = dt.datetime(2025, 12, 31)

    assert options.check_in_period(line, start, end)


def test_print_paths_missing_config(tmp_path: Path, capsys: pytest.CaptureFixture[str]):
    options.print_paths(config_dir=tmp_path)

    out = capsys.readouterr().out
    assert "Couldn't find the config file" in out
