#!/usr/bin/env python3
"""
Run extract-collection.py across every collection listed in roster.json.

    python3 tools/extract-all.py           # report only
    python3 tools/extract-all.py --write   # write src/collections/*.md

The roster maps each legacy page to its true collection number, title and URL
slug. Those mappings were established by reading the number-badge graphics and
cross-checking the artwork years against the exhibition list in the bio — the
legacy filenames themselves are unreliable (see CONTENT-NOTES.md).
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path

TOOLS = Path(__file__).resolve().parent


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true",
                        help="write the collection files rather than reporting")
    args = parser.parse_args()

    roster = json.loads((TOOLS / "roster.json").read_text(encoding="utf-8"))

    total = incomplete = 0
    gaps = []

    for entry in roster:
        command = [
            sys.executable, str(TOOLS / "extract-collection.py"), entry["prefix"],
            "--slug", entry["slug"],
            "--title", entry["title"],
            "--year", str(entry["year"]),
            "--number", str(entry["number"]),
        ]
        if args.write:
            command.append("--write")

        result = subprocess.run(command, capture_output=True, text=True, check=False)
        lines = [ln for ln in result.stderr.strip().splitlines() if ln.strip()]
        summary = next((ln for ln in lines if "works extracted" in ln), None)

        if not summary:
            print(f"!! {entry['prefix']}: FAILED\n{result.stderr}", file=sys.stderr)
            continue

        count = int(summary.split()[0])
        missing = int(summary.split(",")[1].split()[0])
        total += count
        incomplete += missing

        mark = "  " if missing == 0 else "!!"
        print(f"{mark} {entry['prefix']:<4} #{entry['number']:<3} "
              f"{entry['slug']:<34} {count:>3} works, {missing} incomplete")

        gaps += [f"   [{entry['prefix']}]{ln}"
                 for ln in lines if ln.startswith("    work")]

    print(f"\n{total} works across {len(roster)} collections, {incomplete} incomplete")
    if gaps:
        print("\nIncomplete entries (the original captions omit these fields):")
        print("\n".join(gaps))


if __name__ == "__main__":
    main()
