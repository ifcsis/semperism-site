"""Render each brief page to a one-page PDF in site/docs, and take review screenshots."""
import os, sys, threading, http.server, functools
from playwright.sync_api import sync_playwright
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(ROOT, "site")
slugs = [f[:-5] for f in os.listdir(SITE) if f.endswith(".html")
         and f not in ("index.html", "library.html", "semperism.html", "about.html", "404.html")]
H = functools.partial(http.server.SimpleHTTPRequestHandler, directory=SITE)
srv = http.server.ThreadingHTTPServer(("127.0.0.1", 8799), H)
threading.Thread(target=srv.serve_forever, daemon=True).start()
shots = sys.argv[1] if len(sys.argv) > 1 else None
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page()
    for s in slugs:
        pg.goto(f"http://127.0.0.1:8799/{s}.html")
        pg.pdf(path=os.path.join(SITE, "docs", f"{s}.pdf"), format="Letter", print_background=False)
    if shots:
        for name, url, w in [("home", "/", 1200), ("library", "/library.html", 1200),
                             ("brief", f"/{slugs[0]}.html", 1200), ("mobile", "/library.html", 390)]:
            q = b.new_page(viewport={"width": w, "height": 900})
            q.goto("http://127.0.0.1:8799" + url)
            q.screenshot(path=os.path.join(shots, f"{name}.png"), full_page=True)
    b.close()
srv.shutdown()
print("pdfs:", slugs)
