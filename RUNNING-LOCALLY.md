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

We'll install Node.js through a small helper called **nvm** ("Node Version
Manager") rather than downloading it directly — it makes future updates
painless. Open Terminal and paste these one at a time, pressing Enter after
each:

```
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.6/install.sh | bash
```

```
\. "$HOME/.nvm/nvm.sh"
```

```
nvm install 24
```

That last one downloads and installs Node.js itself — give it a moment.

To check it worked:

```
node -v
```

should print something like `v24.18.0`, and

```
npm -v
```

should print something like `11.16.0`. If you see "command not found"
instead, quit Terminal fully and reopen it, then try the two `-v` commands
again.

---

## 2. Get the project files

In Terminal, run:

```
git clone git@github.com:ScottBaileyArt/sbailey.us.git
cd sbailey.us
```

This puts a `sbailey.us` folder in your home folder (the one with your
username, where Terminal starts by default), and `cd` — meaning "go into this
folder" — leaves your Terminal "inside" it, which matters because every
command below assumes you're there.

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
cd ~/sbailey.us
git pull
npx @11ty/eleventy --serve
```

---

## If something goes wrong

- **"command not found: npm" or "npx"** — these come bundled with Node.js, so
  this usually means step 1 didn't finish. Quit Terminal fully, reopen it, and
  try the `nvm install 24` step again.
- **Nothing happens when you visit the localhost address** — check the
  Terminal window for the exact address it printed; the port number
  (the part after the colon) can change.
- **Anything else** — take a screenshot of the Terminal and send it my way.
