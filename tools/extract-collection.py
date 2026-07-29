#!/usr/bin/env python3
"""
Extract a collection's artwork list from a legacy Dreamweaver-era page into a
data file for the Eleventy rebuild.

    python3 tools/extract-collection.py c17 --slug accretions --title Accretions \
        --year 2022 --number 17

This is a migration aid, not part of the build. The old pages are messy but
regular: each artwork is a thumbnail cell (class="DetailLeftTD") holding a link
to a per-image detail page, followed by a caption cell (class="style3") whose
lines are title / medium+dimensions / year.

It gets most of the way there. Anything it is unsure about is written into the
output prefixed with "REVIEW:" so it fails loudly rather than silently guessing.
Always diff the result against the original page.
"""

import argparse
import html
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
LEGACY = REPO / "html"

# Dimensions look like: 64" X 36"  |  7' X 4'  |  36” X 40”  |  5’ X 4’ x 2’
UNIT = r"""(?:['"‘’“”]|\s*(?:in|ft)\b)?"""
DIMENSION_RE = re.compile(
    rf"(\d+\s*{UNIT}(?:\s*[xX×]\s*\d+\s*{UNIT}){{1,2}})"
)

# A caption line is a venue rather than a medium when it names a place. Matched
# on word boundaries so "Projection" does not read as "project".
VENUE_RE = re.compile(
    r"\b(gallery|museum|center|centre|institute|project|biennale|hotel)\b", re.I
)

YEAR_RE = re.compile(r"^(19|20)\d{2}$")


def clean(fragment: str) -> str:
    """Strip tags and entities from an HTML fragment, normalising whitespace."""
    text = re.sub(r"<[^>]+>", "", fragment)
    text = html.unescape(text)
    text = text.replace("\xa0", " ")
    return re.sub(r"\s+", " ", text).strip(" ,;")


def split_medium(line: str):
    """
    Split a caption's detail line into (medium, dimensions).

    Both orders occur in the legacy pages:
        'Acrylic on panel, 64" X 36"'   -> medium first
        "53' X 16' Acrylic on Canvas"   -> dimensions first
    so whatever surrounds the dimensions is treated as the medium.
    """
    match = DIMENSION_RE.search(line)
    if not match:
        return line.strip(" ,;"), None
    dimensions = match.group(1).strip()
    before = line[: match.start()].strip(" ,;")
    after = line[match.end():].strip(" ,;")
    medium = " ".join(part for part in (before, after) if part).strip(" ,;")
    return medium, dimensions


def looks_like_venue(line: str) -> bool:
    return not DIMENSION_RE.search(line) and bool(VENUE_RE.search(line))


def body_after_title(source: str) -> str:
    """
    Return everything after the page's title graphic.

    Seeking to "titleText" lands inside the <img> tag, leaving a fragment like
    'titleTextC17.jpg" alt="..." width="475">' with no opening bracket for the
    tag-stripper to match — which then leaks into the extracted prose. Skip to
    the end of that tag instead.
    """
    marker = source.find("titleText")
    if marker == -1:
        return source
    tag_end = source.find(">", marker)
    return source[tag_end + 1:] if tag_end != -1 else source[marker:]


def extract(prefix: str):
    page = LEGACY / f"{prefix}.htm"
    if not page.exists():
        sys.exit(f"error: {page} not found")

    source = page.read_text(encoding="latin-1")

    # Skip the shared nav chrome; the content starts after the title graphic.
    body = body_after_title(source)

    # Parse row by row rather than matching on CSS classes: the caption cell is
    # class="style3" on some pages and class="DetailRightTD" on others, and the
    # thumbnail cell varies too.
    thumb_re = re.compile(
        r'<a href="([^"]+\.htm)"[^>]*>\s*<img src="([^"]+)"([^>]*)>', re.S
    )

    works = []
    for row in re.split(r"<tr[^>]*>", body, flags=re.I):
        found = thumb_re.search(row)
        if not found:
            continue
        detail_page, thumb, img_attrs = found.groups()
        detail_page, thumb = detail_page.strip(), thumb.strip()

        # Skip the shared nav images (logo, timeline nodes, spacers).
        if re.search(r"/(common|titles)/", thumb, re.I):
            continue

        caption_match = re.search(r"<p>(.*?)</p>", row, re.S)
        if not caption_match:
            continue
        caption = caption_match.group(1)

        # The old pages declared display sizes that differ slightly from the
        # files' natural dimensions; keep them so the layout is unchanged.
        size = {}
        for dim in ("width", "height"):
            found = re.search(rf'{dim}="(\d+)"', img_attrs)
            if found:
                size[f"thumb_{dim}"] = int(found.group(1))
        lines = [clean(p) for p in re.split(r"<br\s*/?>", caption)]
        lines = [ln for ln in lines if ln]

        work = {"thumbnail": thumb, **size, "_detail_page": detail_page}

        work["title"] = lines[0] if lines else None

        # The year's position varies between pages: some list title / medium /
        # year, others title / year / medium, and on some it is buried in the
        # medium or venue text ("Acrylic on Wood Panel 2008").
        rest = lines[1:]
        year = None
        for index, line in enumerate(rest):
            if YEAR_RE.match(line.strip()):
                year = int(line.strip())
                rest = rest[:index] + rest[index + 1:]
                break

        detail_line = " ".join(rest).strip()

        if year is None:
            embedded = re.search(r"\b(19[89]\d|20[0-2]\d)\b", detail_line)
            if embedded:
                year = int(embedded.group(1))
                detail_line = (
                    detail_line[: embedded.start()] + detail_line[embedded.end():]
                )
                detail_line = re.sub(r"\s{2,}", " ", detail_line).strip(" ,;")

        if year is not None:
            work["year"] = year
        if detail_line:
            if looks_like_venue(detail_line):
                work["venue"] = detail_line
            else:
                medium, dimensions = split_medium(detail_line)
                if medium:
                    work["medium"] = medium
                if dimensions:
                    work["dimensions"] = dimensions
                elif not looks_like_venue(detail_line):
                    work["medium"] = detail_line

        # The full-size image lives on the per-image detail page. Asset folders
        # follow the title-graphic numbering rather than the page numbering
        # (c1.htm draws from images/c10/), so take whatever the page points at
        # rather than assuming a folder name.
        full = LEGACY / detail_page
        if full.exists():
            detail_src = full.read_text(encoding="latin-1")
            candidates = [
                c for c in re.findall(r'<img src="(images/[^"]+)"', detail_src)
                if not re.search(r"/(common|titles)/", c, re.I)
            ]
            larger = [c for c in candidates if c != thumb]
            work["image"] = larger[0] if larger else thumb
        else:
            work["image"] = f"REVIEW: detail page {detail_page} missing"

        works.append(work)

    return works


def extract_statement(prefix: str):
    """Pull the collection's short intro paragraph from the page."""
    source = (LEGACY / f"{prefix}.htm").read_text(encoding="latin-1")
    match = re.search(r'class="bioCopy">\s*<p[^>]*>(.*?)</p>', source, re.S)
    return clean(match.group(1)) if match else None


def extract_long_statement(prefix: str):
    """
    Pull the full exhibition statement from the linked 'b' page, if there is one.

    Only 8 of the 17 collections have these. They range from 283 to 3,303 words
    and are kept as paragraphs so the rebuild can render them as real prose.
    """
    source = (LEGACY / f"{prefix}.htm").read_text(encoding="latin-1")
    link = re.search(r'href="(c\d+b\.htm)"', source)
    if not link:
        return None, None

    b_page = LEGACY / link.group(1)
    if not b_page.exists():
        return link.group(1), ["REVIEW: statement page missing"]

    b_source = b_page.read_text(encoding="latin-1")
    body = body_after_title(b_source)
    # Drop the trailing nav/analytics, then take paragraph-ish blocks.
    body = re.sub(r"(?is)<script.*?</script>", " ", body)
    chunks = re.split(r"(?i)</p>|<br\s*/?>\s*<br\s*/?>", body)
    paragraphs = []
    for chunk in chunks:
        text = clean(chunk)
        if len(text.split()) >= 5:
            paragraphs.append(text)
    return link.group(1), paragraphs or ["REVIEW: no statement text extracted"]


def write_collection_file(data, works, path: Path):
    """Write an Eleventy collection page: YAML front matter, no body."""
    import yaml

    front = dict(data)
    front["works"] = [
        {k: v for k, v in w.items() if not k.startswith("_")} for w in works
    ]
    body = yaml.dump(
        front, sort_keys=False, allow_unicode=True, default_flow_style=False, width=88
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(f"---\n{body}---\n", encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("prefix", help="legacy page prefix, e.g. c17")
    parser.add_argument("--slug", required=True, help="URL slug, e.g. accretions")
    parser.add_argument("--title", required=True, help="collection title")
    parser.add_argument("--year", required=True, type=int)
    parser.add_argument("--number", required=True, type=int,
                        help="true collection number (from the badge graphic)")
    parser.add_argument("--write", action="store_true",
                        help="write src/collections/<slug>.md instead of printing JSON")
    args = parser.parse_args()

    works = extract(args.prefix)
    statement = extract_statement(args.prefix)
    b_page, long_statement = extract_long_statement(args.prefix)

    data = {
        "title": args.title,
        "number": args.number,
        "year": args.year,
        "legacy_prefix": args.prefix,
    }
    if statement:
        data["statement"] = statement
    if long_statement:
        data["legacy_statement_page"] = b_page
        data["exhibition_statement"] = long_statement

    if args.write:
        out = REPO / "src" / "collections" / f"{args.slug}.md"
        write_collection_file(data, works, out)
        print(f"wrote {out.relative_to(REPO)}", file=sys.stderr)
    else:
        print(json.dumps({**data, "slug": args.slug, "works": works},
                         indent=2, ensure_ascii=False))

    gaps = []
    for index, work in enumerate(works, 1):
        missing = [
            field for field in ("title", "year") if not work.get(field)
        ]
        if not work.get("medium") and not work.get("venue"):
            missing.append("medium/venue")
        if isinstance(work.get("image"), str) and work["image"].startswith("REVIEW"):
            missing.append("image")
        if missing:
            gaps.append(f"    work {index} ({work.get('title') or '?'}): "
                        f"no {', '.join(missing)}")

    print(f"{len(works)} works extracted, {len(gaps)} incomplete", file=sys.stderr)
    for gap in gaps:
        print(gap, file=sys.stderr)


if __name__ == "__main__":
    main()
