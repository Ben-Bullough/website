# website

My personal blog at [benbullough.co.uk](https://benbullough.co.uk).

Hand-written static HTML and CSS. No build step, no JavaScript, no tracking. Styled after [Bear Blog](https://bearblog.dev) (Verdana, #3273dc links, near-black headings on white).

## Structure

```text
index.html           home page with recent posts
about.html           about page
404.html             not-found page
blog/
  index.html         full post list
  *.html             individual posts
assets/css/styles.css
CNAME                custom domain for GitHub Pages
.nojekyll            disable Jekyll processing
.github/workflows/pages.yml
```

## Local preview

```bash
python3 -m http.server 8000
```

Open <http://localhost:8000>.

## Adding a post

1. Copy an existing file in `blog/` (e.g. `hello-world.html`) to a new filename.
2. Update `<title>`, `<h1>`, the date in `<p class="article-meta">`, and the body.
3. Add a new `<article class="entry">` block to `blog/index.html`.
4. Optionally add a link to the "recent posts" list on `index.html`.
5. Commit and push &mdash; GitHub Actions deploys automatically.

## Deployment

See [DEPLOY.md](DEPLOY.md) for the one-time GitHub Pages + Squarespace DNS setup.
