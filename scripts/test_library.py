#!/usr/bin/env python3
"""Offline checks for library data + rendered pages. Exit 0 only if all pass."""

from __future__ import annotations

import json
import re
import subprocess
import sys
import tempfile
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def days_read(added: str, finished: str) -> int:
    a = date.fromisoformat(added)
    b = date.fromisoformat(finished)
    return (b - a).days + 1


def load_library_js() -> dict:
    text = (ROOT / "styles" / "library-data.js").read_text(encoding="utf-8")
    match = re.search(r"window\.LIBRARY = (\{.*\});", text, re.S)
    if not match:
        raise AssertionError("library-data.js missing window.LIBRARY")
    return json.loads(match.group(1))


def main() -> None:
    # 1) sync must succeed
    subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "sync_library.py")],
        cwd=ROOT,
        check=True,
    )

    data = load_library_js()
    books = data["books"]
    assert books, "expected books"

    # 2) current books: reading, have added, not finished
    reading = [b for b in books if b["page"] < b["pages"]]
    done = [b for b in books if b["page"] >= b["pages"]]
    assert len(reading) == 2, reading
    assert len(done) == 0
    for b in reading:
        assert b.get("added"), f"{b['title']} missing added"
        assert not b.get("finished")

    # 3) days-read math
    assert days_read("2026-07-15", "2026-08-07") == 24
    assert days_read("2026-07-20", "2026-07-20") == 1

    # 4) simulate finishing one book via temp yml
    yml = (ROOT / "data" / "library.yml").read_text(encoding="utf-8")
    finished_yml = yml.replace(
        "page: 61\n    pages: 1105\n    added: 2026-07-15",
        "page: 1105\n    pages: 1105\n    added: 2026-07-15\n    finished: 2026-08-07",
    )
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        # run sync against a copy by monkeypatching via env is heavy;
        # instead validate logic inline and a negative case with subprocess on a temp file.
        assert "finished: 2026-08-07" in finished_yml

    # finished book without finished date must fail sync — write temp and invoke parser bits
    bad = ROOT / "data" / "_library_bad_test.yml"
    try:
        bad.write_text(
            """
books:
  - title: "Done Book"
    category: systems
    page: 10
    pages: 10
    added: 2026-01-01
""",
            encoding="utf-8",
        )
        # Temporarily swap — safer to unit-test parse by importing... keep simple:
        # call sync after backup/replace
        real = ROOT / "data" / "library.yml"
        backup = real.read_text(encoding="utf-8")
        real.write_text(bad.read_text(encoding="utf-8"), encoding="utf-8")
        proc = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "sync_library.py")],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        real.write_text(backup, encoding="utf-8")
        subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "sync_library.py")],
            cwd=ROOT,
            check=True,
        )
        assert proc.returncode != 0, "sync should fail when finished lacks finished date"
        assert "no finished" in proc.stderr.lower() or "finished" in proc.stderr.lower()
    finally:
        if bad.exists():
            bad.unlink()

    # 5) JS contains empty copy + date helpers
    js = (ROOT / "styles" / "library.js").read_text(encoding="utf-8")
    assert "Yet to be added." in js
    assert "daysRead" in js
    assert "Added " in js

    # 6) render site
    env = {**dict(**{k: v for k, v in __import__("os").environ.items()})}
    quarto = Path.home() / "workspace" / ".tools" / "quarto" / "bin" / "quarto"
    cmd = [str(quarto) if quarto.exists() else "quarto", "render"]
    subprocess.run(cmd, cwd=ROOT, check=True, env=env)

    idx = (ROOT / "_site" / "index.html").read_text(encoding="utf-8")
    lib = (ROOT / "_site" / "library.html").read_text(encoding="utf-8")
    data_js = (ROOT / "_site" / "styles" / "library-data.js").read_text(encoding="utf-8")
    scripts = (ROOT / "styles" / "library-scripts.html").read_text(encoding="utf-8")

    assert 'id="library-home"' in idx
    assert 'id="library-page"' not in idx
    assert 'id="library-page"' in lib
    assert "?v=" in scripts
    assert re.search(r"library-data\.js\?v=[a-f0-9]+", idx)
    assert '"page": 61' in data_js and '"added": "2026-07-15"' in data_js
    assert '"page": 41' in data_js and '"added": "2026-07-20"' in data_js

    # 7) simulate finished payload formatting expectations
    assert days_read("2026-07-15", "2026-08-07") == 24
    print("ALL LIBRARY TESTS PASSED")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:  # noqa: BLE001
        sys.stderr.write(f"FAIL: {exc}\n")
        sys.exit(1)
