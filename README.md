# semperism.org

Static site for GitHub Pages. No build step needed to publish: upload the files in this folder to the root of the repository.

## Library model
- Each entry has a one-page brief readable on the site (`/<slug>.html`) and a one-page PDF (`/docs/<slug>.pdf`).
- The full paper is sent on request — the "Request the full paper" link opens a pre-filled email.
- Work under submission to journals is not listed.
- Semperism work only; the contact address is the semperism.org one.

## Publish (first time)
1. On GitHub, under your own account, create a new public repository (e.g. `semperism-site`). Upload every file in this folder to the repository root.
2. Repository → Settings → Pages → Source: "Deploy from a branch", branch `main`, folder `/ (root)`. Custom domain: `semperism.org` (the CNAME file is already included). Save.
3. GoDaddy → semperism.org: unpublish/disconnect the Websites + Marketing "Launching Soon" site, and turn OFF any domain forwarding.
4. GoDaddy DNS for semperism.org: four A records on `@` — 185.199.108.153, 185.199.109.153, 185.199.110.153, 185.199.111.153 — and a CNAME `www` → `<your-github-username>.github.io`. Leave any email (MX, TXT/SPF) records alone.
5. When GitHub's DNS check passes and the certificate is issued (can take up to a day), tick "Enforce HTTPS".

## Add or change a paper
Edit `ENTRIES` (or `RELATED`) in `build.py`, run `python3 build.py`, then `python3 make_pdfs.py`, and upload the changed files from `site/`.
 

## When a full paper goes up on Semper (Substack)
Add a line to `FULL_TEXT` in `build.py` — the paper's slug and the Substack post URL — then run
`python3 build.py`, copy `site/` to the repository root, and push. The paper's brief page and library
card switch from "Request the full paper" to a link to the full text, and its structured data points
search engines to the post.

## Logo, site name and search engines
- Emblem: `img/semper-virtus-medallion.webp` (hero, about page). Logo for search: `img/semperism-logo.png` (512×512).
- Favicons: `favicon.ico`, `favicon-48/96/192.png`, `apple-touch-icon.png`, `site.webmanifest`. Google shows the favicon beside the site name in results.
- Home page carries `WebSite` (name "Semperism") and `Organization` (logo) structured data; every page links the favicons and a 1200×630 share image (`img/semperism-og.jpg`).
- To replace the logo, regenerate those image files from the new artwork, keep the file names, and run `python3 build.py`.
