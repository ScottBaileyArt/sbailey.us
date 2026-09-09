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

**Four different numbering schemes, none of which agree.** The collections are
numbered inconsistently across page filenames, title graphics, and image
folders:

| Scheme | Example | Status |
|--------|---------|--------|
| Page filenames | `c14.htm` | **14/15/16 are scrambled** |
| Number badge graphic | `titleC16.gif` | correct (chronological) |
| Name graphic | `titleTextC14.jpg` | reversed for c1–c11, offset for 14–16 |
| Image folders | `images/c0/` | `c0` holds collection **11**'s images |

**Three page files are misnamed.** Cross-referencing the name graphics against
the exhibition years in the bio confirms a clean three-way swap:

| File | Collection | Actually is | Year |
|------|-----------|-------------|------|
| `c14.htm` | 16 | Anthropogenic Landscapes | 2015 |
| `c15.htm` | 14 | Manifest Destiny | 2010 |
| `c16.htm` | 15 | Topometry, Topology, Topography | 2012 |

The number badges and the navigation are both *correct*; only the filenames are
wrong, and the nav compensates (the link labelled "c16" points at `c14.htm`).
**The site works correctly today** and the rebuild preserves that behaviour.

**Resolved: `c11.htm` has no `images/c11` folder** because collection 11 is
*Infrared* (2007), whose images live in `images/c0/` and whose detail pages are
`c0_01.htm` … `c0_11.htm`. Not an orphan — just another instance of assets
numbered on a different scheme than pages. No action needed.

**None of this carries into the rebuild.** Collections are being rebuilt as data
files addressed by name (`/accretions/`), so all four numbering schemes are read
once during migration and then retired. No files are being renamed.

**[preserved] Two collection titles are Japanese and were transcribed from the
title graphics**, since the images carried text the `alt` attributes omitted:

| Collection | Transcribed as |
|-----------|----------------|
| c2 | 自然の魂 (shizen no tamashii) |
| c8 | 枠を超えて (waku wo koete) |

Read off low-resolution GIFs, so **Scott should confirm the characters** —
particularly c8. The romanised names match his bio exactly.

**[changed] Collection 17 now has a timeline node marker.** In the original, the
row of node markers had one for every collection except c17 (*Accretions*),
which had a text label but no clickable node above it. The rebuild generates
both rows from the same data, so c17 now gets one like the rest.

**[preserved] Several artworks have no medium or year in the original captions**
— 11 of 168. The rebuild leaves those fields blank rather than inventing them:
3 installation views in *Inside Looking Out*, 4 details in *Virtually Sublime*,
3 installation views in *Infrared*, and a studio view in *Earthly
Constellations*.

**[changed] Artwork `alt` text was regenerated.** The originals were placeholder
strings — `alt="IR1"`, `alt="IR2"`, and `alt="Inside Looking Out"` repeated on
pages of entirely unrelated collections. Each image now uses its own artwork
title, which is what a screen reader should announce.

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

---

## Collections index, contact, and home pages

**New per-collection fields, sourced from `collections.htm`.** The old
collections-index page (a card per collection: icon, location, exhibition
venue, and a short blurb) drew on text that exists nowhere else — not on the
collection's own page, not in the bio. That content is now `index_location`,
`index_venue`, `index_summary`, and `index_icon` in all 17 collection data
files. Nothing existing was changed; this is new data alongside it.

**[preserved] The index card for c15 titles it "Topology, Topometry,
Topography"** — word order swapped from "Topometry, Topology, Topography" on
the collection's own page and in the timeline nav. Kept the collection page's
order as the canonical title; the swapped index-card text was not carried
over as a second title, just noted here.

**[preserved] The index cards for c2 and c8 give English-only titles**
("Shizen No Tamashii", "Waku Wo Koete"), without the Japanese characters used
on those collections' own pages (自然の魂, 枠を超えて — see above). Both
transcriptions are used only internally to locate where the title ends in the
card's markup; the collection pages keep the characters as their title.

**[preserved] c13's index blurb sat in a bare `<span class="style3">` with no
surrounding `<p>` tag** — the same kind of broken markup already noted for
this collection above. Recovered by hand rather than automatically.

**[changed] Collections-index layout wraps into rows of 4** rather than the
original's single ~2700px-wide scrolling row. Confirmed with Aydan rather than
changed silently. The VIEW button is not yet pinned to the bottom of each
card — attempted with a CSS table-cell technique that turned out to be
unreliable across cards of different heights (visually confirmed not to work),
reverted rather than left half-working. Real fix is straightforward once the
layout moves to Grid/Flexbox in the mobile-first CSS pass (roadmap step 5);
tracked there rather than patched further blind.

**[preserved] Contact's email keeps the original's spam-obfuscated display
text** — the visible text reads "scott.j.bailey **at** hotmail.com" rather
than the real address, while the `mailto:` link itself is correct. Caught
after an initial draft flattened this to a plain `@` address; restored to
match the original's evident intent.

**Homepage's featured artwork is hardcoded**, matching the original
(`index.html`, *Accretion 3,871,914*). Update the image, caption, and link by
hand when a new collection goes up — see any collection file's `works` list
for the field shapes if this should become data-driven later.

---

## Lightbox (PhotoSwipe)

**Every artwork's real image dimensions were added.** `image_width`/
`image_height` on all 168 artwork records, computed directly from the actual
files via `tools/add-image-dimensions.py`. PhotoSwipe needs these upfront to
size its zoom/pan viewport without a layout jump on first open. All 168
resolved cleanly — no missing files.

**Lightbox captions reuse the same data as the on-page caption**, via a shared
Nunjucks macro in `collection.njk` (`workCaption`) — title, then venue or
medium+dimensions, then year. One definition, two call sites, so they can't
drift apart.

**Not independently verified in a browser.** Everything static — markup,
`data-pswp-*` attributes, asset resolution (CSS/JS all 200), JS syntax — was
checked, but the actual click/zoom/arrow-key/swipe behavior needs a human;
there's no browser automation available in this environment. Worth an actual
click-through on a few collections (including `/miscellaneous/`, only 4 works,
and one with genuinely missing medium/year like `/inside-looking-out/`) before
calling this done.
