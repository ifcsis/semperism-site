# -*- coding: utf-8 -*-
"""Static site generator for semperism.org.

Same library arrangement as ifcsis.org: each entry has a one-page brief that
can be read on the site, and the full paper is sent on request by email.
Work under submission to journals is not listed.

Edit ENTRIES / RELATED below, then:  python3 build.py
Output goes to ./site — commit the contents of that folder to the repo root.
"""
import html, os, shutil
from urllib.parse import quote

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "site")
DOMAIN = "https://semperism.org"
EMAIL = "steele@knucode.com"          # site contact — confirm before publishing
AUTHOR = "S. Harrison Knudson, J.D."
HERO = "Constitutions fail less often by usurpation than by consecration."

# ---------------------------------------------------------------- library data
# kind: "Essay", "Working paper", "Outline" ...   status line shows under title.
# brief: list of (heading, [paragraphs]) — the one-page brief, rendered on site.
ENTRIES = [
    dict(
        id="SE-01", slug="who-pays-the-bill", kind="Essay",
        title="Who Pays the Bill?",
        sub="A Semperist reading of the European Return Regulation",
        meta="Second version · September 2026",
        blurb="Europe’s return debate asks who must leave. It does not ask who owes for the "
              "displacement in the first place. The receiving state has already answered that "
              "question in its own recognition decisions, and the answer names a regime.",
        description="Every grant of protection is the receiving state’s own finding of cause "
                    "against a named regime. An essay on why the invoice follows the grant.",
        brief=[
            ("The question the vote did not ask", [
                "The European Parliament’s June 2026 vote on the Return Regulation settled a "
                "question about who must leave. It left untouched the prior question: who owes for "
                "the displacement that put people on the move in the first place.",
                "The essay does not argue for exiling refugees. It argues that the cost of forced "
                "displacement has a debtor, and that the debtor is neither the displaced person nor "
                "the state that received them.",
            ]),
            ("The invoice follows the grant", [
                "A recognition decision is not only an act of protection. It is the receiving "
                "state’s own adjudication of cause: this person was persecuted, and this regime "
                "did it. Aggregated by country of origin, those decisions form a ledger — an "
                "adjudicated ledger — of displacement the receiving state has already attributed "
                "to a named regime by its own procedures.",
                "The bill therefore needs no new finding. It follows the grant.",
            ]),
            ("Return is not accountability", [
                "Return reaches the failed claim. Removing a person whose claim was refused says "
                "nothing about the persons whose claims succeeded, and recovers nothing from the "
                "regime that drove them out. Return may be lawful and still settle no account.",
            ]),
            ("The debtor is the regime, not the country", [
                "A regime that displaces its people has usually robbed the country as well. To bill "
                "the plundered state would be to collect twice from the same victims. The claim runs "
                "against the regime — its persons and its assets — and never against the "
                "successor state that inherits the damage.",
            ]),
            ("Unbilled relief is a subsidy", [
                "Relief that is never invoiced is not neutral. It absorbs the cost of the regime’s "
                "conduct and quietly solves its dissident problem for it. The humanitarian act is "
                "right; leaving the account unsent is what subsidises the tyrant.",
                "The essay claims no new doctrine. Home-state responsibility for wrongful acts is "
                "general law. What it adds is the instrument: decisions that already exist, already "
                "name the regime, and already state the cause.",
            ]),
        ],
        ask="The full essay works through the European instruments that could carry the claim "
            "— immobilised sovereign assets, the EU Global Human Rights Sanctions Regime, and "
            "universal-jurisdiction proceedings — and answers the objection that the "
            "Regulation reaches failed claimants rather than the persecuted.",
    ),
    dict(
        id="SE-02", slug="jurisprudence-of-voluntary-risk", kind="Outline",
        title="The Jurisprudence of Voluntary Risk",
        sub="When institutions may penalise lawful private conduct",
        meta="Outline · October 2026",
        blurb="Smoking, cannabis, motorcycles, firearms: employers, insurers, civil services and "
              "the military each treat lawful risk-taking differently, and no one designed the "
              "pattern. A test for when an institution may reach conduct the law permits.",
        description="Liberty follows the person; liability follows the risk. An outline of when "
                    "institutions may penalise lawful private conduct.",
        brief=[
            ("Liberty follows the person; liability follows the risk", [
                "Lawful private conduct that carries risk — smoking, cannabis use, motorcycling, "
                "firearm ownership — is treated one way by an insurer, another by an employer, "
                "another by a civil service, and another again by the military. The variation is "
                "large, and it has no author.",
            ]),
            ("An accidental jurisprudence", [
                "Insurance regulation, employment law, civil-service rules and military policy each "
                "settled their own corner of the question. Taken together they amount to a body of "
                "law no one set out to write, and it does not answer to a single principle.",
            ]),
            ("The test", [
                "The outline proposes that an institution may act on lawful private conduct only "
                "where it can show an institutional interest, a nexus between the conduct and that "
                "interest, and a response proportionate to the risk — and it separates inquiry "
                "from action, since asking about conduct and penalising it are different acts.",
                "A further distinction does much of the work: between risk a person creates and "
                "carries, and risk a person externalises onto others.",
            ]),
            ("The revenue trap", [
                "A state that licenses and taxes a vice acquires a fiscal interest in its "
                "consumption. Legalisation therefore changes the institution’s position as well "
                "as the citizen’s, and the outline treats that shift as part of the question.",
            ]),
        ],
        ask="The full outline works through the paired hard cases, risk pooling, the objections, "
            "and an open research checklist.",
    ),
]

# Related work hosted elsewhere — linked, not duplicated.
RELATED = [
    ("WP-05", "The Geography of Zero", "Interacting frictions and institutional design after distance",
     "https://ifcsis.org/the-geography-of-zero.html"),
    ("WP-03", "The Misallocated Burden", "Cost allocation and regulatory path dependence in children’s online safety",
     "https://ifcsis.org/the-misallocated-burden.html"),
    ("WP-04", "The Demand Side", "Identification error in child-safety markets",
     "https://ifcsis.org/the-demand-side.html"),
    ("WP-02", "Refusal Is Not Referral", "Scope, escalation, and institutional duty for AI in children’s spaces",
     "https://ifcsis.org/refusal-is-not-referral.html"),
    ("NB-04", "No Free Pass", "Parental enrollment and liability for child-facing AI",
     "https://ifcsis.org/no-free-pass.html"),
]

# ---------------------------------------------------------------- helpers
e = lambda s: html.escape(s, quote=True)

def req_link(title, docid):
    subject = "Request: %s (%s)" % (title, docid)
    body = "\n".join(["Please send: %s (%s)" % (title, docid), "", "Name:", "Institution:",
                      "Role:", "The question you are working on:", ""])
    return "mailto:%s?subject=%s&body=%s" % (EMAIL, quote(subject, safe=""), quote(body, safe=""))

NAV = [("semperism.html", "Semperism"), ("library.html", "Library"), ("about.html", "About")]

def page(fname, title, body, current="", description="", head_extra=""):
    nav = "".join('<li><a href="/%s"%s>%s</a></li>' % (h, ' aria-current="page"' if h == current else "", l)
                  for h, l in NAV)
    canon = DOMAIN + ("/" if fname == "index.html" else "/" + fname)
    doc = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(description)}">
<meta name="author" content="{e(AUTHOR)}">
<link rel="canonical" href="{canon}">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(description)}">
<meta property="og:url" content="{canon}">
{head_extra}<link rel="stylesheet" href="/style.css">
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="site">
  <a class="brand" href="/">Semperism</a>
  <nav><ul>{nav}</ul></nav>
  <a class="btn btn-sm" href="mailto:{EMAIL}">Write</a>
</header>
<main id="main">
{body}
</main>
<footer class="site">
  <span>{e(AUTHOR)}</span>
  <span>Correspondence: <a href="mailto:{EMAIL}">{EMAIL}</a></span>
  <span>This site sets no cookies and loads no third-party resources.</span>
</footer>
</body>
</html>
"""
    path = os.path.join(OUT, fname)
    with open(path, "w", encoding="utf-8") as f:
        f.write(doc)

def card(x):
    return f"""    <article class="card">
      <span class="eyebrow">{x['id']} &middot; {e(x['kind'])}</span>
      <h3><a href="/{x['slug']}.html">{e(x['title'])}</a></h3>
      <p class="card-sub">{e(x['sub'])}</p>
      <p>{e(x['blurb'])}</p>
      <p class="card-actions">
        <a class="btn btn-sm btn-ghost" href="/{x['slug']}.html">Read the brief &rarr;</a>
        <a class="req" href="{e(req_link(x['title'], x['id']))}">Request the full paper</a>
      </p>
    </article>"""

# ---------------------------------------------------------------- build
if os.path.isdir(OUT):
    shutil.rmtree(OUT)
os.makedirs(OUT)
shutil.copy(os.path.join(ROOT, "style.css"), OUT)

# Home
home = f"""<section class="hero wrap">
  <span class="eyebrow">From <em>sic semper tyrannis</em></span>
  <h1>{e(HERO)}</h1>
  <p class="lede">Semperism is a constitutional philosophy of permanent limits: the study of how institutions acquire a reverence they were never granted, and how a founding text is built to refuse it.</p>
  <p class="hero-actions"><a class="btn" href="/library.html">Enter the library</a> <a class="btn btn-ghost" href="/semperism.html">The framework</a></p>
</section>
<section class="wrap">
  <h2 class="section-h">Recently added</h2>
  <div class="pubs">
{chr(10).join(card(x) for x in ENTRIES)}
  </div>
</section>"""
page("index.html", "Semperism — S. Harrison Knudson", home,
     description="Semperism: a constitutional philosophy of permanent limits. Papers and briefs by S. Harrison Knudson, J.D.")

# Framework
fw = f"""<article class="wrap wrap-narrow prose">
  <span class="eyebrow">The framework</span>
  <h1>Semperism</h1>
  <p class="lede">The name is taken from Virginia’s motto, <em>sic semper tyrannis</em> — thus always to tyrants. The word that matters is <em>semper</em>. The founding settlement was not a truce with power, to be renegotiated each generation. It was a permanent textual prohibition on power exceeding its grant.</p>
  <h2>The claim</h2>
  <p>{e(HERO)} An office, a symbol or an institution is first marked out by a sign, then individuated, then revered, and finally consecrated — placed beyond the ordinary reach of the text that created it. Each step feels like respect. The last step is the failure.</p>
  <blockquote>Idolatry binds you to the actor through its symbol; the oath binds you to the law that binds the actor. The first you worship. The second you defend. A republic survives on the second and dies of the first.</blockquote>
  <h2>Anti-consecration architecture</h2>
  <p>On this reading the Constitution fuses Federalist structural design with a Semperist permanent prohibition: no actor and no institution is placed beyond constraint. The officer’s oath under Article VI runs to the Constitution, not to a person, an office or a flag.</p>
  <h2>Where the work goes from here</h2>
  <p>The same question — how institutions come to exceed the terms on which they were founded — runs through the papers in the <a href="/library.html">library</a>: displacement and the regimes that cause it, the reach of institutions over lawful private life, and the design of protected spaces online.</p>
</article>"""
page("semperism.html", "Semperism — the framework", fw, current="semperism.html",
     description="Semperism: constitutions fail less often by usurpation than by consecration.")

# Library
lib = f"""<section class="wrap page-top">
  <span class="eyebrow">Published work</span>
  <h1 class="page-h">Read the argument, then take it apart.</h1>
  <p>Everything here is released for comment. Objections — legal, historical, philosophical or empirical — are more useful than agreement.</p>
  <p class="muted">Each entry has a one-page brief you can read here. The full paper is sent on request, so that it can go to a reader with the question in view. Work under submission to journals is not listed.</p>

  <h2 class="section-h">Essays and papers</h2>
  <p class="muted">One page now; the paper on request.</p>
  <div class="pubs">
{chr(10).join(card(x) for x in ENTRIES)}
  </div>

  <h2 class="section-h">Related work at IFC-SiS</h2>
  <p class="muted">Papers on institutional design and children’s online safety, published by the International Foundation for Child-Safe internet Standards. Linked here, hosted there.</p>
  <ul class="related">
{chr(10).join(f'    <li><span class="eyebrow">{i}</span><a href="{u}">{e(t)}</a><span class="card-sub">{e(s)}</span></li>' for i, t, s, u in RELATED)}
  </ul>

  <div class="note">
    <h3>Why the full papers are sent rather than posted</h3>
    <p>Several of these papers are still moving, and some are written for a particular audience or jurisdiction. Rather than post a version written for nobody in particular, I send the current one with the question in view. Say what you are working on in the request and I will reply with the paper, usually within a few days. Requests are as welcome from critics as from allies.</p>
  </div>
  <div class="note">
    <h3>Not everything is listed here</h3>
    <p>Further work — on the Constitution, on oaths and symbols, and on scripture — is under submission to journals and so is not posted. It is available on request for review purposes. Write to <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
  </div>
</section>"""
page("library.html", "Library — Semperism", lib, current="library.html",
     description="Essays and papers by S. Harrison Knudson, J.D. One-page briefs on the site; full papers on request.")

# Brief pages
for x in ENTRIES:
    url = f"{DOMAIN}/{x['slug']}.html"
    year = "2026"
    headx = (f'<meta name="citation_title" content="{e(x["title"])}">\n'
             f'<meta name="citation_author" content="Knudson, S. Harrison">\n'
             f'<meta name="citation_publication_date" content="{year}">\n'
             f'<meta name="citation_public_url" content="{url}">\n')
    secs = "\n".join(f"  <h2>{e(h)}</h2>\n" + "\n".join(f"  <p>{e(p)}</p>" for p in ps) for h, ps in x["brief"])
    sep = " " if x["title"][-1] in "?!" else ": "
    cite = f"Knudson, S. Harrison. “{x['title']}{sep}{x['sub']}.” {x['kind']}, {year}. {url}"
    body = f"""<article class="wrap wrap-narrow paper">
  <p class="paper-back"><a href="/library.html">&larr; Library</a></p>
  <span class="eyebrow">{x['id']} &middot; {e(x['kind'])}</span>
  <h1>{e(x['title'])}</h1>
  <p class="paper-sub">{e(x['sub'])}</p>
  <p class="paper-meta">{e(x['meta'])} &middot; {e(AUTHOR)}</p>
{secs}
  <div class="note paper-ask">
    <p>{e(x['ask'])}</p>
    <p class="card-actions">
      <a class="btn btn-sm" href="{e(req_link(x['title'], x['id']))}">Request the full paper</a>
      <a class="req" href="/docs/{x['slug']}.pdf">Download this page as PDF</a>
    </p>
  </div>
  <h3>Cite this brief</h3>
  <p class="cite">{e(cite)}</p>
</article>"""
    page(f"{x['slug']}.html", f"{x['title']} — Semperism", body, current="library.html",
         description=x["description"], head_extra=headx)

# About
about = f"""<article class="wrap wrap-narrow prose">
  <span class="eyebrow">The author</span>
  <h1>{e(AUTHOR)}</h1>
  <p class="lede">American lawyer and scholar, Arlington, Virginia.</p>
  <p>Steele Knudson has some two decades of practice across federal regulatory compliance, export controls and anti-corruption, antitrust, land use and internet governance. He holds a J.D. from George Mason University’s Antonin Scalia Law School and a B.S. in Urban Planning from the University of Utah.</p>
  <p>His work runs on several tracks that share one question — how institutions come to exceed the terms on which they were founded. On the constitutional side that is Semperism. On the technical side it is the design of a protected namespace for children, pursued through the <a href="https://ifcsis.org/">International Foundation for Child-Safe internet Standards</a>, where he is Director.</p>
  <p>Correspondence: <a href="mailto:{EMAIL}">{EMAIL}</a></p>
</article>"""
page("about.html", "About — S. Harrison Knudson", about, current="about.html",
     description="S. Harrison Knudson, J.D. — American lawyer and scholar, Arlington, Virginia.")

# 404
page("404.html", "Not found — Semperism", """<section class="wrap wrap-narrow prose">
  <span class="eyebrow">404</span>
  <h1>That page isn’t here.</h1>
  <p>It may have moved. The <a href="/library.html">library</a> lists everything currently posted.</p>
</section>""", description="Page not found.")

# Housekeeping files
with open(os.path.join(OUT, "CNAME"), "w") as f: f.write("semperism.org\n")
open(os.path.join(OUT, ".nojekyll"), "w").close()
with open(os.path.join(OUT, "robots.txt"), "w") as f:
    f.write(f"User-agent: *\nAllow: /\nSitemap: {DOMAIN}/sitemap.xml\n")
urls = ["/", "/semperism.html", "/library.html", "/about.html"] + [f"/{x['slug']}.html" for x in ENTRIES]
with open(os.path.join(OUT, "sitemap.xml"), "w") as f:
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
            + "".join(f"  <url><loc>{DOMAIN}{u}</loc></url>\n" for u in urls) + "</urlset>\n")
shutil.copy(os.path.join(ROOT, "README.md"), OUT)
os.makedirs(os.path.join(OUT, "docs"), exist_ok=True)
print("built", len(ENTRIES), "briefs ->", OUT)
