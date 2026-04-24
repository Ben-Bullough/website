# website

Ben Bullough's personal blog at [benbullough.co.uk](https://benbullough.co.uk).

Hand-written static HTML and CSS. No build step, no JavaScript, no tracking. Styled after [Bear Blog](https://bearblog.dev) (Verdana, `#3273dc` links, near-black headings on white, dark-mode variant via `prefers-color-scheme`).

## Run locally

From the repo root:

```bash
uv run website
```

That's it. uv sets up a virtual environment on first run (takes a second or two) and starts a preview server at <http://localhost:8000>, opening your default browser at it. Ctrl-C stops the server.

Options:

```bash
uv run website --port 8001   # serve on a different port
uv run website --no-open     # don't open a browser
```

The command is backed by `website.py` at the repo root and wired up via `[project.scripts]` in `pyproject.toml`. uv reads these and makes `website` a runnable command for this project.

**Why a server and not just double-clicking `index.html`?** Opening files via `file://` breaks relative links (`/assets/...`) and the 404 page. Always preview through a local server.

**Fallback if uv isn't available** (ships with [`uv`](https://docs.astral.sh/uv/) itself, or `brew install uv`):

```bash
python3 -m http.server 8000
```

Live-reload is not built in. After editing, save the file and refresh the browser (⌘R). Hard-refresh (⌘⇧R) if CSS changes don't show up — the browser is caching `styles.css`.

## Structure

```text
index.html              home + recent posts list
about.html              about page
404.html                not-found page
blog/
  index.html            full post list
  hello-world.html      starter post
  why-this-blog.html    starter post
  on-writing-to-think.html  starter post
assets/css/styles.css   all styles (single file)
CNAME                   benbullough.co.uk (tells GitHub Pages the custom domain)
.nojekyll               disables Jekyll processing on Pages
.github/workflows/pages.yml  auto-deploys on push to main
website.py              local preview server (launched by `uv run website`)
pyproject.toml          uv project config; defines the `website` command
DEPLOY.md               one-time DNS + Pages setup
```

## Adding a new post

1. Copy an existing post in `blog/` to a new filename. `hello-world.html` is the simplest template:
   ```bash
   cp blog/hello-world.html blog/my-new-post.html
   ```
2. Edit the new file:
   - `<title>` — `my new post | Ben Bullough`
   - `<meta name="description">` — one-line summary (used by search engines and link previews)
   - `<h1>` — post title
   - `<p class="article-meta">` — date in `YYYY-MM-DD`
   - The `<article class="prose">` body
3. Add an `<article class="entry">` block to `blog/index.html` (newest at the top):
   ```html
   <article class="entry">
     <p class="post-date">2026-04-26</p>
     <h2><a class="interactive-link" href="my-new-post.html">my new post</a></h2>
     <p>One-line summary.</p>
   </article>
   ```
4. Optionally add a `<li>` to the "recent posts" list on `index.html`.
5. Commit and push — GitHub Actions deploys automatically (~1–2 min).

```bash
git add blog/my-new-post.html blog/index.html index.html
git commit -m "Post: my new post"
git push
```

## Editing the site look

All styles live in `assets/css/styles.css`. Key variables sit at the top of the file in `:root`:

```css
--width: 720px;       /* content column width */
--font-main: Verdana, Geneva, sans-serif;
--bg: #ffffff;
--heading: #222222;
--text: #444444;
--link: #3273dc;
--visited: #8b6fcb;
```

Dark-mode equivalents are under a `@media (prefers-color-scheme: dark)` block just below. Change the values in one place and the whole site updates.

The hover-underline link effect lives in `.interactive-link`.

## Things to know

- **Dates** — use `YYYY-MM-DD`. The CSS renders them with `font-variant-numeric: tabular-nums` so they align in lists.
- **Links inside post bodies** — a plain `<a href="...">Text</a>` is fine; it'll get the blue link colour automatically. Use `class="interactive-link"` only for nav-style links where you want the hover-underline effect instead of persistent colour.
- **Images** — drop them in `assets/` (e.g. `assets/img/foo.png`) and reference with `<img src="../assets/img/foo.png" alt="…">` from inside `blog/`. `max-width: 100%` is already set globally.
- **The `CNAME` file must contain exactly `benbullough.co.uk`** — no `https://`, no trailing slash. GitHub Pages reads it on every build and rebinds the custom domain.
- **`.nojekyll` must stay** — without it, GitHub tries to run Jekyll on the repo and silently drops files that start with `_`.
- **404.html uses absolute paths** (`/assets/...`) because GitHub serves it from the root regardless of the requested URL. The other pages use relative paths so local preview works.
- **No feed yet** — if you want RSS later, `feed.xml` at the root is enough (no tooling needed).

## Deployment

See [DEPLOY.md](DEPLOY.md) for the one-time GitHub Pages + Squarespace DNS setup.

Day-to-day: `git push` to `main`. The workflow at `.github/workflows/pages.yml` publishes within a couple of minutes.
