# semperism.org

Static site for GitHub Pages — same arrangement as ifcsis.org. No build step needed to publish: upload the files in this folder to the root of the repository.

## Library model (matches ifcsis.org)
- Each entry has a one-page brief readable on the site (`/<slug>.html`) and a one-page PDF (`/docs/<slug>.pdf`).
- The full paper is sent on request — the "Request the full paper" link opens a pre-filled email.
- Work under submission to journals is not listed.
- IFC-SiS papers are linked out to ifcsis.org, not duplicated.

## Publish (first time)
1. On GitHub, under your own account, create a new public repository (e.g. `semperism-site`). Upload every file in this folder to the repository root.
2. Repository → Settings → Pages → Source: "Deploy from a branch", branch `main`, folder `/ (root)`. Custom domain: `semperism.org` (the CNAME file is already included). Save.
3. GoDaddy → semperism.org: unpublish/disconnect the Websites + Marketing "Launching Soon" site, and turn OFF any domain forwarding (forwarding locked the @ records on ifcsis.org).
4. GoDaddy DNS for semperism.org: four A records on `@` — 185.199.108.153, 185.199.109.153, 185.199.110.153, 185.199.111.153 — and a CNAME `www` → `<your-github-username>.github.io`. Leave any email (MX, TXT/SPF) records alone.
5. When GitHub's DNS check passes and the certificate is issued (can take up to a day), tick "Enforce HTTPS".

## Add or change a paper
Edit `ENTRIES` (or `RELATED`) in `build.py`, run `python3 build.py`, then `python3 make_pdfs.py`, and upload the changed files from `site/`.
