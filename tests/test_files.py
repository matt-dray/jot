import argparse
import datetime as dt
import json
from pathlib import Path

import jot.files as files


def test_get_config_path(tmp_path: Path):
    path = files.get_config_path(
        config_file="config.json",
        config_dir=tmp_path,
    )
    assert path == tmp_path / "config.json"


def test_write_and_read_config(tmp_path: Path):
    config = tmp_path / "config.json"
    jot = tmp_path / "jot.txt"

    files.write_to_config(config, "JOT_PATH", jot.as_posix())

    data = json.loads(config.read_text())
    assert data["JOT_PATH"] == jot.as_posix()
    assert Path(files.read_config(config, "JOT_PATH")) == jot


def test_write_jotting_prepends(tmp_path: Path):
    def fixed_now():
        return dt.datetime(2025, 12, 25, 1, 0)

    jot = tmp_path / "jot.txt"
    jot.write_text("[2025-12-24 23:00] egg\n")

    args = argparse.Namespace(text="spam")

    files.write_jotting(jot, args, now_dt=fixed_now)

    content = jot.read_text()
    assert content.startswith("[2025-12-25 01:00] spam")
    assert "egg" in content


def test_create_jot_file(tmp_path: Path):
    def prompt(_):
        return str(tmp_path / "spam.txt")

    jot = files.create_jot_file(prompt_user=prompt)

    assert jot.exists()
    assert jot.name == "spam.txt"
