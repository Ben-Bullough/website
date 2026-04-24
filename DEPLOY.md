# Deployment guide

One-time setup to get the site live at `https://benbullough.co.uk` via GitHub Pages, with DNS in Squarespace.

## 1. Push to GitHub

```bash
git add .
git commit -m "Initial site"
git push origin main
```

## 2. Turn on GitHub Pages

1. On GitHub, open the repository `Ben-Bullough/website`.
2. Go to **Settings → Pages**.
3. Under **Build and deployment**, set **Source** to **GitHub Actions**.
4. Under **Custom domain**, enter `benbullough.co.uk` and click **Save**. (The `CNAME` file in the repo already contains this; adding it here tells GitHub to provision an HTTPS certificate.)
5. Leave **Enforce HTTPS** unchecked for now &mdash; it can't be enabled until DNS resolves.

Push the current branch. The `.github/workflows/pages.yml` workflow will build and deploy the site on every push to `main`. First run takes 1–2 minutes; watch it under the **Actions** tab. After the first successful run, the site is available at `https://ben-bullough.github.io/website/` (while DNS is still propagating).

## 3. Configure DNS in Squarespace

Squarespace still manages the domain; we just change DNS so it points at GitHub's Pages servers.

Open Squarespace Domains → `benbullough.co.uk` → **DNS Settings** (or **Advanced DNS**). Remove any existing `A` records on `@` and any `CNAME` on `www` that conflict, then add the following.

**Apex (`benbullough.co.uk`) — four A records:**

| Type | Host | Value |
|------|------|-------|
| A | `@` | `185.199.108.153` |
| A | `@` | `185.199.109.153` |
| A | `@` | `185.199.110.153` |
| A | `@` | `185.199.111.153` |

(Optional but recommended IPv6 — four AAAA records on `@`:)

| Type | Host | Value |
|------|------|-------|
| AAAA | `@` | `2606:50c0:8000::153` |
| AAAA | `@` | `2606:50c0:8001::153` |
| AAAA | `@` | `2606:50c0:8002::153` |
| AAAA | `@` | `2606:50c0:8003::153` |

**`www` subdomain — one CNAME:**

| Type | Host | Value |
|------|------|-------|
| CNAME | `www` | `ben-bullough.github.io.` |

(Use your real GitHub username — `ben-bullough` — lowercased, with a trailing dot if Squarespace requires one. Squarespace typically adds it automatically.)

Save.

## 4. Verify

DNS usually propagates in a few minutes but can take up to 24 hours. You can check progress from the terminal:

```bash
dig +short benbullough.co.uk
dig +short www.benbullough.co.uk
```

You should see the four `185.199.x.153` addresses for the apex, and `ben-bullough.github.io` for `www`.

Back on GitHub → **Settings → Pages**, the **Custom domain** section will eventually show a green check ("DNS check successful"). GitHub will then issue a Let's Encrypt certificate automatically.

## 5. Enforce HTTPS

Once the DNS check is green and the certificate is issued (usually another few minutes), tick **Enforce HTTPS** on the same page. From that point on, `http://` requests redirect to `https://` automatically.

## 6. Canonical domain

GitHub Pages will automatically redirect `www.benbullough.co.uk` → `benbullough.co.uk` (apex) because the `CNAME` file contains the apex. Nothing to do.

## Troubleshooting

- **"Domain's DNS record could not be retrieved"** — DNS hasn't propagated yet. Wait, or run `dig` to confirm.
- **Certificate pending for hours** — remove the custom domain in GitHub Settings → Pages, save, re-add it, save again. This re-triggers cert issuance.
- **`CNAME` file disappears after a push** — the workflow uploads the whole repo including `CNAME`, so this shouldn't happen. If it does, re-add the file and make sure GitHub's **Custom domain** setting still shows `benbullough.co.uk`.
- **Old Squarespace parking page still showing** — an old `A` record is still cached. Double-check that every non-GitHub `A`/`CNAME` on `@` and `www` is removed.

## References

- GitHub Pages apex domains: <https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site>
- GitHub's apex IPs: <https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site#configuring-an-apex-domain>
