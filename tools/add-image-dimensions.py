#!/usr/bin/env python3
"""
Add real pixel dimensions (image_width/image_height) to every artwork's full-
size image across all collection data files. PhotoSwipe needs these upfront to
size its zoom/pan viewport correctly -- without them it has to guess and
re-flow after the image loads.

    python3 tools/add-image-dimensions.py            # report only
    python3 tools/add-image-dimensions.py --write     # update the .md files
"""

import argparse
import sys
from pathlib import Path

import yaml
from PIL import Image

REPO = Path(__file__).resolve().parent.parent
SRC = REPO / "src"
COLLECTIONS_DIR = SRC / "collections"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()

    total = missing = 0

    for path in sorted(COLLECTIONS_DIR.glob("*.md")):
        raw = path.read_text(encoding="utf-8")
        _, front, rest = raw.split("---", 2)
        data = yaml.safe_load(front)

        changed = False
        for work in data.get("works", []):
            total += 1
            image_path = SRC / work["image"]
            if not image_path.exists():
                print(f"!! {path.stem}: image not found: {work['image']}", file=sys.stderr)
                missing += 1
                continue
            with Image.open(image_path) as im:
                width, height = im.size
            if work.get("image_width") != width or work.get("image_height") != height:
                work["image_width"] = width
                work["image_height"] = height
                changed = True

        status = "  " if not any(
            "REVIEW" in str(w.get("image", "")) for w in data.get("works", [])
        ) else "!!"
        print(f"{status} {path.stem:<34} {len(data.get('works', []))} works")

        if args.write and changed:
            dumped = yaml.dump(data, sort_keys=False, allow_unicode=True,
                                default_flow_style=False, width=88)
            path.write_text(f"---\n{dumped}---{rest}", encoding="utf-8")

    print(f"\n{total} artworks checked, {missing} image file(s) not found", file=sys.stderr)


if __name__ == "__main__":
    main()
