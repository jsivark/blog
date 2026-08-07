#!/usr/bin/env python3
"""Compile data/library.yml → styles/library-data.js for the site."""

from __future__ import annotations

import json
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.stderr.write("PyYAML required: pip install pyyaml\n")
    sys.exit(1)

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "data" / "library.yml"
OUT = ROOT / "styles" / "library-data.js"


def main() -> None:
    data = yaml.safe_load(SRC.read_text(encoding="utf-8")) or {}
    books = data.get("books") or []
    if not isinstance(books, list):
        sys.stderr.write("library.yml: 'books' must be a list\n")
        sys.exit(1)

    cleaned = []
    for i, raw in enumerate(books):
        if not isinstance(raw, dict):
            sys.stderr.write(f"library.yml: book #{i + 1} must be a mapping\n")
            sys.exit(1)
        title = str(raw.get("title") or "").strip()
        if not title:
            sys.stderr.write(f"library.yml: book #{i + 1} needs a title\n")
            sys.exit(1)
        try:
            page = int(raw.get("page", 0))
            pages = int(raw.get("pages", 0))
        except (TypeError, ValueError):
            sys.stderr.write(f"library.yml: '{title}' needs integer page/pages\n")
            sys.exit(1)
        if pages <= 0:
            sys.stderr.write(f"library.yml: '{title}' needs pages > 0\n")
            sys.exit(1)
        page = max(0, min(page, pages))
        cleaned.append(
            {
                "title": title,
                "author": str(raw.get("author") or "").strip(),
                "category": str(raw.get("category") or "other").strip().lower(),
                "page": page,
                "pages": pages,
            }
        )

    payload = json.dumps({"books": cleaned}, ensure_ascii=False, indent=2)
    OUT.write_text(
        f"/* Generated from data/library.yml — do not edit by hand. */\n"
        f"window.LIBRARY = {payload};\n",
        encoding="utf-8",
    )
    print(f"Wrote {OUT.relative_to(ROOT)} ({len(cleaned)} books)")


if __name__ == "__main__":
    main()
