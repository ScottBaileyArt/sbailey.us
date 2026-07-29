# Project Brief — sbailey.us rebuild

Handoff context for continuing this work in Claude Code. Read this first.

---

## Who and what

I'm helping my father modernize his painter portfolio site. He's an artist and
art professor — tech literate but not technical. I'm a CS PhD student, comfortable
with programming generally, but web development is not my specialty. Explain
web-specific things rather than assuming familiarity.

**The site:** currently live at `https://sbailey.wvc.edu/` (hosted by Wenatchee
Valley College). The domain `sbailey.us` is registered at DreamHost. There are also
stale copies floating around on college servers (`commons.wvc.edu/scottbailey/`,
`commonsv2.wvc.edu/scottbailey/`) — not our problem yet, but worth knowing they exist.

**The repo:** `github.com/ScottBaileyArt/sbailey.us` — this is a dump of the site
files, created as a starting point for the rewrite. **It is not part of the live
site's deployment pipeline.** The live site is served from the college's server
independently. Nothing we do in this repo can break the live site.

---

## What his goals are

From his own list:
- Keep the current aesthetic — clean, image-focused. Do not redesign it into
  something generic.
- Keep the timeline navigation at the top of all pages
- Fix broken links and icon images
- Larger type for readability
- Work properly on phones
- Full-screen lightbox gallery with arrow navigation between images
- Image zoom
- **Be able to update it himself going forward** — mainly adding a new collection
  once a year or so, not overhauling

Budget-conscious. Free hosting, cheap or free everything else.

---

## The plan we settled on

**Stack:** Eleventy (static site generator) → Cloudflare Pages or Netlify (free
hosting, builds from git) → Sveltia CMS (git-based CMS giving him a web form at
`/admin` to add collections without touching code).

**Why Eleventy over Hugo:** templates are close to plain HTML, less new syntax
to learn. **Why a CMS at all despite the once-a-year cadence:** precisely because
it's once a year — he'll forget any documented procedure, but a labeled form is
self-explanatory. **Why not Squarespace et al:** monthly cost, and the templates
would constrain the design he already has.

**Note on the CMS:** Netlify CMS is dead (now Decap CMS); Netlify Identity, the
thing that used to make it turnkey, is deprecated. Sveltia CMS with a GitHub OAuth
backend is the current path. This is a later phase — don't set it up yet.

---

## Repo structure decision

1. Snapshot the existing state on a branch called `legacy-site` and push it.
   That's the permanent record of the old site.
2. `main` becomes the new Eleventy site.
3. Prune cruft from `main`: the repo is ~1.2GB, most of it dead weight — a
   `for mark/` folder (217MB), `Old/` (7.5MB), `.fla`/`.swf` Flash files,
   `.zip` site backups, `Thumbs.db`. Keep `html/images/` and the `.htm` files
   as migration reference; those can go once content is ported.
4. Do the cleanup as its own commit so the diff is legible.

---

## What the old site actually is (findings from inspecting the repo)

Dreamweaver-era HTML, roughly 2008 vintage. Specifically:

- Nested `<table>` layouts with hardcoded pixel widths (`<table width="1444">`).
  This is why it doesn't work on phones — there's no responsive CSS at all.
- Inline `MM_preloadImages` / `MM_swapImage` Dreamweaver JavaScript. Dead weight;
  strip it.
- Microsoft Office XML junk in the `<head>` (`mso:CustomDocumentProperties`). Strip.
- Empty stylesheet links (`<link href="" ...>`) on some pages.
- Old Google Analytics (`ga.js`, `UA-10150590-1`) — long dead, remove.
- Page naming: `index.htm`, `bio.htm`, `contact.htm`, `collections.htm`,
  collection pages `c1.htm` … `c17.htm`, and per-image pages `c17_01.htm` etc.
- **The header nav and the year-timeline nav are hand-copied into every single
  page.** This is the core problem: adding a new collection means editing dozens
  of files. Making these into a single shared layout is the main structural win.

---

## Immediate task (start here)

Get a minimal Eleventy site building, then port **one page** — `bio.htm` — as a
proof of the pattern:

1. Set up the Eleventy project structure in `main` (`src/` input, `_site/` output).
2. `src/_includes/base.njk` — a layout containing the shared chrome: head,
   logo + `collections | bio | contact` nav, the year timeline row, closing tags.
   Page content goes in via `{{ content | safe }}`.
3. `src/bio.html` — front matter (`layout: base.njk`, `title: Bio`) plus only the
   bio-specific content from the original `bio.htm`.
4. Strip the Dreamweaver/MSO/analytics cruft as you go.
5. Verify it renders on localhost and matches the original visually.

**Scope discipline for this phase: replicate the old site's appearance first.**
No responsive rework, no lightbox, no redesign yet. Those come after the whole
site is ported into the templating structure. Getting the structure right is the
prerequisite for everything else.

---

## Roadmap after that

1. ✅ Eleventy running, `bio.htm` ported (current task)
2. Port `contact.htm`, `index.htm`, `collections.htm`
3. Restructure collections as **data** — a file per collection with title, year,
   statement, and image list — so one template generates all collection pages and
   the timeline nav is generated from that list rather than hand-copied
4. Image pipeline: `@11ty/eleventy-img` for automatic resizing + `srcset`.
   Important — he will upload 15MB studio photographs, and without this the site
   is unusable on mobile.
5. Mobile-first CSS rewrite, larger type, keeping his visual character
6. PhotoSwipe for the lightbox (full-screen, arrow keys, swipe, pinch-zoom,
   thumbnails — covers most of his wishlist in one library)
7. Deploy to Cloudflare Pages / Netlify on a temporary URL, test
8. Sveltia CMS + get him logged in and publishing a test change himself
9. Point `sbailey.us` DNS at the new host; ask WVC to retire the old copies

---

## Working preferences

- Explain the web-specific reasoning; I want to understand this well enough to
  maintain it, not just have it done.
- One step at a time, verify each before moving on.
- Preserve his design decisions. The restraint and image focus are the point.
