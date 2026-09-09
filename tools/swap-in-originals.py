#!/usr/bin/env python3
"""
Point each artwork's `image` field at the largest same-artwork file actually
on disk, when one exists that's meaningfully bigger than what's currently
referenced (the pre-shrunk "web" copies used throughout the site).

Matches by fuzzy-normalized filename within the same folder as the current
`image` (strips size-suffix words/letters and punctuation), same approach
used to survey coverage before building the image pipeline. Only 38 of 168
artworks have a real larger original; this updates just those.

    python3 tools/swap-in-originals.py           # report only
    python3 tools/swap-in-originals.py --write    # update the .md files
"""

import argparse
import re
import sys
from pathlib import Path

import yaml
from PIL import Image

REPO = Path(__file__).resolve().parent.parent
SRC = REPO / "src"
COLLECTIONS_DIR = SRC / "collections"


def normalize(stem):
    s = stem.lower()
    s = re.sub(r"\b(icon|thumb|thumbnail)\b", "", s)
    s = re.sub(r"(ws|wl|sm|small|web)\b", "", s)
    s = re.sub(r"w\b", "", s)
    s = re.sub(r"[^a-z0-9]+", "", s)
    return s


def find_bigger(image_path: Path, cur_width: int, cur_height: int):
    folder = image_path.parent
    if not folder.exists():
        return None
    key = normalize(image_path.stem)
    cur_pixels = cur_width * cur_height
    best = None
    best_pixels = 0
    for f in folder.iterdir():
        if not f.is_file() or f.suffix.lower() not in (".jpg", ".jpeg", ".png"):
            continue
        if normalize(f.stem) != key:
            continue
        try:
            with Image.open(f) as im:
                px = im.size[0] * im.size[1]
        except Exception:
            continue
        if px > best_pixels:
            best_pixels, best = px, f
    if best and best != image_path and best_pixels > cur_pixels * 1.3:
        return best
    return None


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()

    swapped = 0
    for path in sorted(COLLECTIONS_DIR.glob("*.md")):
        raw = path.read_text(encoding="utf-8")
        _, front, rest = raw.split("---", 2)
        data = yaml.safe_load(front)
        changed = False

        for work in data.get("works", []):
            image_path = SRC / work["image"]
            bigger = find_bigger(image_path, work.get("image_width", 0), work.get("image_height", 0))
            if bigger:
                rel = bigger.relative_to(SRC).as_posix()
                print(f"  {path.stem:<34} {work['title'][:40]:<40} "
                      f"{work['image'].split('/')[-1]!r} -> {rel.split('/')[-1]!r}")
                if args.write:
                    work["image"] = rel
                    # Stale full-resolution metadata; the pipeline computes
                    # real dimensions at build time now, but drop these so
                    # nothing downstream accidentally trusts the old values.
                    work.pop("image_width", None)
                    work.pop("image_height", None)
                changed = True
                swapped += 1

        if args.write and changed:
            dumped = yaml.dump(data, sort_keys=False, allow_unicode=True,
                                default_flow_style=False, width=88)
            path.write_text(f"---\n{dumped}---{rest}", encoding="utf-8")

    print(f"\n{swapped} artworks {'updated' if args.write else 'would be updated'}", file=sys.stderr)


if __name__ == "__main__":
    main()
