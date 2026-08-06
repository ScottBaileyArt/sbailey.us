#!/usr/bin/env python3
"""
Pull the collections-index card content (collections.htm) into each
collection's data file: a location line, an exhibition venue line, a short
index blurb (distinct wording from the collection page's own intro), and the
small icon thumbnail.

The panel hrefs in collections.htm are scrambled the same way the page
filenames are (c14.htm points at two different panels). Panel *position* is
reliable though -- they run c17 down to c1, the same true chronological order
as roster.json -- so panels are matched to collections positionally, not by
href.

    python3 tools/extract-collections-index.py           # report
    python3 tools/extract-collections-index.py --write    # update the .md files
"""

import argparse
import html
import json
import re
import sys
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parent.parent
LEGACY = REPO / "html"
COLLECTIONS_DIR = REPO / "src" / "collections"

# One collection's title got visually wrapped across two links in the legacy
# markup ("MANIFEST DESTIN" + "Y"), which the tag-stripped text reproduces as
# "MANIFEST DESTIN Y". Documented here rather than guessed at generically.
TEXT_FIXUPS = {
    "manifest-destiny": [("DESTIN Y", "DESTINY")],
}

# The two Japanese-titled collections are romanised only on the index card,
# without the characters used on their own pages -- a legitimate alternate
# form, used here only to locate where the title ends.
ALTERNATE_TITLES = {
    "waku-wo-koete": "Waku Wo Koete",
    "shizen-no-tamashii": "Shizen No Tamashii",
}

# c15's index card swaps the title's word order ("Topology, Topometry,
# Topography" vs "Topometry, Topology, Topography" on the collection's own
# page -- see CONTENT-NOTES.md). That's a real discrepancy, not an equivalent
# name, so it is not treated as an alternate title; the location text is
# taken from the same card by hand instead of stripped automatically.
MANUAL_LOCATIONS = {
    "topometry-topology-topography": "Washington State, USA, 2013",
}

# c13's blurb sits in a bare <span class="style3"> with no surrounding <p> --
# the same broken markup already logged for this collection in
# CONTENT-NOTES.md. The <p>-based parser below cannot see it.
MANUAL_SUMMARIES = {
    "earthly-constellations": (
        "Through a process of controlled accident, countless splatters of "
        "(primarily of transparent drops of cyan, magenta, and yellow) "
        "acrylic paint express the night views from space of various cities."
    ),
}


def clean(fragment: str) -> str:
    text = re.sub(r"<[^>]+>", " ", fragment)
    text = html.unescape(text).replace("\xa0", " ")
    return re.sub(r"\s+", " ", text).strip(" ,;")


def strip_title(text: str, title: str) -> str:
    """Remove a known title from the front of a cleaned paragraph, loosely."""
    pattern = r"^\s*" + re.escape(title).replace(r"\ ", r"\s+") + r"\s*"
    return re.sub(pattern, "", text, flags=re.IGNORECASE).strip(" ,;")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()

    source = (LEGACY / "collections.htm").read_text(encoding="latin-1")
    panels = re.split(r'<th[^>]*scope="col">', source)[1:]
    roster = json.loads((REPO / "tools" / "roster.json").read_text())
    roster_desc = sorted(roster, key=lambda r: -r["number"])

    if len(panels) != len(roster_desc):
        sys.exit(f"error: {len(panels)} panels but {len(roster_desc)} collections "
                  f"in roster -- positional matching would be wrong, stopping")

    for panel, entry in zip(panels, roster_desc):
        body = panel[: panel.find("</th>")]
        icon_match = re.search(r'<img src="(images/[^"]+)"', body)
        icon = icon_match.group(1) if icon_match else None

        # Venue and blurb are sometimes two <p> tags, sometimes one <p> with
        # the two separated by a blank line (<br><br>) inside it -- split on
        # both so the two don't end up merged into a single field.
        raw_paragraphs = re.findall(r"<p[^>]*>(.*?)</p>", body, re.S)
        paragraphs = []
        for raw in raw_paragraphs:
            for chunk in re.split(r"(?:<br\s*/?>\s*){2,}", raw):
                cleaned = clean(chunk)
                if cleaned and cleaned.upper() != "VIEW":
                    paragraphs.append(cleaned)

        for find, replace in TEXT_FIXUPS.get(entry["slug"], []):
            paragraphs = [p.replace(find, replace) for p in paragraphs]

        # First paragraph is just the number badge ("c17"); drop it.
        if paragraphs and re.fullmatch(r"c\d+", paragraphs[0], re.IGNORECASE):
            paragraphs = paragraphs[1:]

        location = venue = summary = None
        if paragraphs:
            if entry["slug"] in MANUAL_LOCATIONS:
                location = MANUAL_LOCATIONS[entry["slug"]]
            else:
                title_variant = ALTERNATE_TITLES.get(entry["slug"], entry["title"])
                stripped = strip_title(paragraphs[0], title_variant)
                if stripped == paragraphs[0]:
                    # Stripping changed nothing -- the title text genuinely
                    # was not found, a real failure worth flagging.
                    print(f"!! {entry['slug']}: could not strip title from "
                          f"{paragraphs[0]!r}", file=sys.stderr)
                    location = paragraphs[0]
                else:
                    # An empty result is valid -- e.g. Miscellaneous's card
                    # has no location text at all, just the title.
                    location = stripped or None
        if len(paragraphs) > 1:
            venue = paragraphs[1]
        if len(paragraphs) > 2:
            summary = paragraphs[2]
        if not summary and entry["slug"] in MANUAL_SUMMARIES:
            summary = MANUAL_SUMMARIES[entry["slug"]]

        status = "  " if (location and venue and summary) else "!!"
        print(f"{status} {entry['slug']:<34} "
              f"location={'y' if location else '-'} "
              f"venue={'y' if venue else '-'} "
              f"summary={'y' if summary else '-'} "
              f"icon={'y' if icon else '-'}")

        if args.write:
            path = COLLECTIONS_DIR / f"{entry['slug']}.md"
            raw = path.read_text(encoding="utf-8")
            _, front, rest = raw.split("---", 2)
            data = yaml.safe_load(front)
            # Insert before the (long) works list rather than after it.
            works = data.pop("works", None)
            if location:
                data["index_location"] = location
            if venue:
                data["index_venue"] = venue
            if summary:
                data["index_summary"] = summary
            if icon:
                data["index_icon"] = icon
            if works is not None:
                data["works"] = works
            dumped = yaml.dump(data, sort_keys=False, allow_unicode=True,
                                default_flow_style=False, width=88)
            path.write_text(f"---\n{dumped}---{rest}", encoding="utf-8")


if __name__ == "__main__":
    main()
