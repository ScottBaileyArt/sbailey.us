# Content notes — questions for Scott

Things found in the original site that look like mistakes rather than choices.
Nothing here has been changed without being listed. Anything marked **[changed]**
was altered in the rebuild; anything marked **[preserved]** was left exactly as-is
and is awaiting a decision.

---

## bio page

**[changed] Duplicate entry — 1999 Curatorial Practices Seminar**
Under *Positions, Residencies, Workshops*, this entry appears twice:

> 1999 — Contemporary International Curatorial Practices Seminar
> American University in Cairo, Cairo, Egypt

One copy sits out of chronological order between the 2009 and 2001 entries;
the other is correctly placed between 2000 and 1999. The markup around the
out-of-order copy is broken (a stray empty table row), which suggests a
copy-paste accident. **Kept one copy.** Restore the second if it was intentional.

**[preserved] "Wenatche, WA"** — missing final "e", under the 2016 Stanley
Lifetime Achievement Award. Presumably should be "Wenatchee, WA".

**[preserved] "R eport From Cairo"** — stray space, in the 2002 Marilu Knode
bibliography entry. Presumably "Report From Cairo".

**[preserved] "Pedigogy in Art Education"** — 1992 publication. Presumably
"Pedagogy".

**[preserved] "Ars Sine Scienctia Nihil"** — 2004 bibliography entry. The Latin
phrase is normally *"Ars sine scientia nihil est"* — likely "Scienctia" →
"Scientia".

**[preserved] "2 nd Al Nitaq Art Festival"** — stray space, 2001 group
exhibition. Presumably "2nd".

**[preserved] "Yasmeen Siddiqui , "** — space before the comma, 2001
bibliography entry.

**[preserved] Overlapping teaching entries** — *Teaching and Other Academic
Experience* lists "2003-present: Assistant Professor, Director of Art Program,
MAC Gallery Director" and separately "2012-present: MAC Gallery Director". The
gallery director role is named in both. May be deliberate (start dates differ),
but reads as redundant.

**[changed] Apostrophe in "Bailey's most recent paintings"** — was a corrupted
character (displayed as a black diamond or question mark in some browsers)
caused by an encoding mismatch. Replaced with a proper apostrophe. This is a
display bug fix, not a content change.

---

## Site-wide structural findings

**Collection files are misnamed (three of them).** The filename does not match
the collection the page actually contains:

| File | Collection it actually shows |
|------|------------------------------|
| `c14.htm` | collection **16** |
| `c15.htm` | collection **14** |
| `c16.htm` | collection **15** |

`c12`, `c13`, and `c17` are self-consistent. The navigation compensates for this
— the link labelled "c16" correctly points at `c14.htm` — so **the site works
correctly today** and the rebuild preserves that behaviour. But it is confusing
to maintain. When collections are converted to data files (roadmap step 3), the
URLs should be corrected so collection 14 lives at `/c14/`. Ideally collections
would be addressed by name (`/accretions/`) rather than number.

**Broken spacer image next to the "BIO" title, live site only.** `bio.htm`
references `images/common/spacer.gif` (lowercase), but the live server's real
folder is `images/Common/` (capital C) — confirmed by requesting both paths
directly (lowercase 404s, capital-C 200s). It's the only lowercase image
reference on the page; everything else already says `Common` and loads fine,
which is why this is the one broken image rather than the whole header.
Not something we can fix on the live server, and not a bug in our rebuild —
our own asset folder is genuinely lowercase (`src/images/common/`), so our
references are correct for our own build. Worth a final check across the other
legacy pages during porting in case the same slip appears elsewhere.

**The stylesheet link was broken site-wide.** 196 of 207 pages had
`<link href="" rel="stylesheet">` — an empty address, so no stylesheet loaded.
Comparison with an older copy of the bio page (`Xbio.htm`, ~2007) shows those
pages originally linked `css/sb.css` and carried no inline styles. The Microsoft
Office metadata in every page header suggests the files were round-tripped
through a Microsoft tool that stripped the addresses. Someone then pasted an
inline style block into each page to patch back the lost formatting.

The rebuild reconnects `sb.css`. Visible differences from the patched version:
- links are blue-grey and underlined, rather than plain grey without underline
- the background image sits in one position rather than repeating
- **[changed]** `sb.css` also drew a thin 1px border on the top/right of the
  content cells (`.mainTableTD`), fencing in the bio/title area. Scott's
  seen it and doesn't want it — removed from `src/css/sb.css`.

**Awaiting Scott's preference on the link color and background repeat.**
Either is a one-line change.

**A "c16" label in the year timeline points at collection 16 but sits under the
2016 year heading**, while c17 (2023, *Accretions*) has a text label but no
corresponding node marker in the row above it. Worth confirming the timeline
still reflects how he wants the collections grouped by year.
