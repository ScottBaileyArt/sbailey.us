# Running the site on your own computer

This is a one-time setup so you can preview the new site on your own machine
as it comes together — before anything is live on the internet. Once it's set
up, running it again takes about 10 seconds.

A few terms, since some of this is new:

- **Terminal**: a text-based way to run programs on your Mac, instead of
  clicking icons. Everything below happens here — search for it with
  Spotlight (Cmd+Space, then type "Terminal").
- **Repository ("repo")**: the project folder, tracked by a tool called Git so
  changes are saved with history. Ours lives at
  `github.com/ScottBaileyArt/sbailey.us`. Git is already installed on your
  computer.
- **Node.js**: a program that lets your computer run the site-building tool
  (Eleventy). You only install this once.
- **`localhost`**: a web address that only your own computer can see. When the
  site is "running," it's visible at a `localhost` address in your browser —
  not on the real internet, and not visible to anyone else.

---

## 1. Install Node.js (one time only)

Download the **LTS** version (LTS = "Long Term Support," the stable one) from
[nodejs.org](https://nodejs.org/) and run the installer, accepting the
defaults.

To check it worked, open Terminal and type:

```
node -v
```

You should see a version number like `v22.x.x`. If you see "command not
found," restart Terminal (or your computer) and try again.

---

## 2. Get the project files

In Terminal, navigate to wherever you'd like the project folder to live (for
example, your Desktop), then run:

```
cd Desktop
git clone https://github.com/ScottBaileyArt/sbailey.us.git
cd sbailey.us
```

The `cd` command means "go into this folder." After this, you'll have a
`sbailey.us` folder on your Desktop, and your Terminal will be "inside" it —
which matters, because every command below assumes you're there.

**Later on**, to get whatever's changed since last time, run this from inside
the `sbailey.us` folder:

```
git pull
```

---

## 3. Install the site's tools (one time only)

Still inside the `sbailey.us` folder, run:

```
npm install
```

This reads a list of tools the project needs (mainly Eleventy, the program
that turns our template files into a website) and downloads them into a
folder called `node_modules`. It'll print a lot of text — that's normal. This
only needs to be run once, or again later if the list of tools changes (I'll
let you know if that happens).

---

## 4. Run the site

```
npx @11ty/eleventy --serve
```

You'll see something like:

```
[11ty] Server at http://localhost:8080/
```

(The number might not be 8080 — if that port's busy, Eleventy just picks the
next one and tells you.)

---

## 5. View it

Open that `http://localhost:...` address in your web browser. You're now
looking at the site running live off your own computer.

While this is running, any file changes get picked up automatically — the
page in your browser refreshes itself. You don't need to restart anything.

To stop the site, click back into Terminal and press **Ctrl+C**.

---

## Quick reference, once it's all installed

Every time after the first, running the site is just:

```
cd Desktop/sbailey.us
git pull
npx @11ty/eleventy --serve
```

---

## What you'll actually see right now

Only the **bio page** exists so far — this is a first test to get the tools
working and make sure the approach looks right before building out the rest.
Visit `http://localhost:.../bio/`. The homepage and collection pages aren't
built yet, so most links will 404 (a "page not found" message) — that's
expected, not broken.

I also left a running list of small oddities I found in the old page content
(typos, a duplicated line, a couple of mismatched file names) in
`CONTENT-NOTES.md`, in the same folder — worth a look whenever you have a
minute, no rush.

---

## If something goes wrong

- **"command not found: npm" or "npx"** — these come bundled with Node.js, so
  this usually means Node didn't install correctly. Reinstall from
  [nodejs.org](https://nodejs.org/).
- **Nothing happens when you visit the localhost address** — check the
  Terminal window for the exact address it printed; the port number
  (the part after the colon) can change.
- **Anything else** — take a screenshot of the Terminal and send it my way.
