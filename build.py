# -*- coding: utf-8 -*-
"""Static site generator for semperism.org.

Each entry has a one-page brief that
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
EMAIL = "shknudson@semperism.org"     # site contact (Semperism correspondence only)
AUTHOR = "S. Harrison Knudson, J.D."
SUBSTACK = "https://semperism.substack.com"
import json
# The author's other sites. Shown in every footer and listed as sameAs in the
# structured data, so search engines connect them to one person.
ELSEWHERE = [
    ("IFC-SiS", "https://ifcsis.org/"),
    ("Super Elements", "https://superelements.com/"),
    ("Son of God · theology library", "https://sonofgod.love/library"),
    ("Peachfire · a novel", "https://peachfire.ink/"),
]
PERSON = {
    "@type": "Person", "@id": "https://semperism.org/about.html#person",
    "name": "S. Harrison Knudson", "honorificSuffix": "J.D.",
    "alternateName": ["Steele Harrison Knudson", "S Harrison Knudson", "Steele H. Knudson", "Steele Knudson", "Harrison Knudson"],
    "givenName": "Steele", "additionalName": "Harrison", "familyName": "Knudson",
    "image": {"@type": "ImageObject", "@id": "https://semperism.org/img/knudson-with-ronald-reagan.jpg#image",
              "url": "https://semperism.org/img/knudson-with-ronald-reagan.jpg",
              "contentUrl": "https://semperism.org/img/knudson-with-ronald-reagan.jpg",
              "name": "S. Harrison Knudson with President Ronald Reagan",
              "caption": "S. Harrison Knudson (Steele Harrison Knudson, Steele Knudson) with President Ronald Reagan",
              "about": {"@id": "https://semperism.org/about.html#person"}},
    "url": "https://semperism.org/about.html",
    "jobTitle": "Attorney and independent scholar",
    "alumniOf": [{"@type": "CollegeOrUniversity", "name": "George Mason University Antonin Scalia Law School"},
                 {"@type": "CollegeOrUniversity", "name": "University of Utah"}],
    "sameAs": ["https://orcid.org/0009-0004-3600-4115", "https://ifcsis.org/director.html", "https://superelements.com/",
               "https://sonofgod.love/", "https://sonofgod.love/library", SUBSTACK, "https://peachfire.ink/"],
}
OG_IMAGE = "https://semperism.org/img/semperism-og.jpg"
LOGO = "https://semperism.org/img/semperism-logo.png"
# Home-page structured data: WebSite tells Google the site name ("Semperism");
# Organization.logo tells Google which image is the site's logo.
WEBSITE = {"@type": "WebSite", "@id": "https://semperism.org/#website", "name": "Semperism",
           "alternateName": ["Semperism.org", "Semper Virtus"], "url": "https://semperism.org/",
           "publisher": {"@id": "https://semperism.org/#org"}}
ORG = {"@type": "Organization", "@id": "https://semperism.org/#org", "name": "Semperism",
       "url": "https://semperism.org/", "slogan": "Semper Virtus",
       "logo": {"@type": "ImageObject", "url": LOGO, "width": 512, "height": 512},
       "image": "https://semperism.org/img/semper-virtus-medallion.webp",
       "founder": {"@id": "https://semperism.org/about.html#person"},
       "email": "shknudson@semperism.org",
       "sameAs": ["https://semperism.substack.com"]}
def ld(obj):
    return '<script type="application/ld+json">' + json.dumps(dict({"@context": "https://schema.org"}, **obj), ensure_ascii=False) + '</script>\n'
# Shorter essays published on the Semper Substack (newest first)
POSTS = [
    dict(title="The Fuel Left Out of Panem",
         sub="Panem's children inherit the guilt. Real tyranny also raises children to inherit the hate.",
         blurb="The Hunger Games shows a state that can make guilt hereditary, and leaves out the blood "
               "and faith that make hatred hereditary too. On Coin's last Games, the Nuremberg Laws, "
               "Barnette, Romeo and Juliet, and the inquisitor's chair.",
         url=SUBSTACK + "/p/the-fuel-left-out-of-panem", date="November 2026"),
]
# Full papers published on Semper (Substack). When a paper goes up, add its slug
# and post URL here, run build.py, and publish. Its brief page and library card
# then link to the full text instead of offering it by request.
FULL_TEXT = {
    "forum-shopping-for-the-apocalypse": SUBSTACK + "/p/forum-shopping-for-the-apocalypse",
    "the-key-of-the-constitution": SUBSTACK + "/p/the-key-of-the-constitution",
}
HERO = "Constitutions fail less often by usurpation than by consecration."

# ---------------------------------------------------------------- library data
# kind: "Essay", "Working paper", "Outline" ...   status line shows under title.
# brief: list of (heading, [paragraphs]) — the one-page brief, rendered on site.
ENTRIES = [
    dict(
        id="SE-07", slug="the-heretic-becomes-the-inquisitor", kind="Essay",
        title="The Heretic Becomes the Inquisitor",
        sub="Institutional mimicry under terminological displacement",
        meta="Essay · sixth version · August 2026",
        blurb="Confession, shunning, purity taboo and secondary punishment were never distinctively "
              "religious. They are the general architecture of closed institutions. When the heretic "
              "takes the inquisitor’s chair, the words change and the machinery does not.",
        description="Why institutions that repudiate religious authority reproduce its enforcement "
                    "machinery under new names, and why the renaming is functional rather than ironic.",
        brief=[
            ("The puzzle", [
                "The secular critique of religion was accurate: orthodoxy enforced by social pressure, "
                "dissent punished by excommunication and shunning, sacred objects that put power beyond "
                "challenge, belief performed as a loyalty test. The same inventory now describes "
                "enforcement in institutions that reject religious authority entirely, under different "
                "names. Why?",
            ]),
            ("Not a church, a closed institution", [
                "The usual answer is that the movement is a religion, or descends from one. This essay "
                "takes a third route. The mechanisms were never religious in origin. They are what any "
                "institution does when it must hold a boundary without recourse to evidence. Religion "
                "is the best-documented instance, which is why the mechanisms carry religious names.",
                "The unit is the institution — a department, a newsroom, a party committee, a "
                "licensing board — because only institutions can expel, decertify or dismiss. Six "
                "observable criteria mark how closed an institution is, by degree rather than kind.",
            ]),
            ("Why the words change", [
                "No committee replaced excommunication with cancellation. The cheaper descriptions "
                "displaced the expensive ones, and three pressures did the selecting: critique-insulation "
                "(the old words hand opponents a century of argument), legitimacy transfer (therapeutic "
                "language carries a presumption of evidence that theology does not), and participation "
                "cost (a recruit will join a process that holds people accountable who would never join "
                "an inquisition).",
            ]),
            ("The pattern repeats, and cuts both ways", [
                "The French Terror, Soviet show trials and Maoist struggle sessions each denounced "
                "orthodoxy and rebuilt its architecture. The essay applies the same test against the "
                "grain, to the Republican Party’s censure and non-recognition of its own dissenters "
                "after January 2021, and finds the same structure under a different lexicon.",
                "The vocabulary changes. The structure does not. And the new vocabulary is not a "
                "disguise applied afterward; it is the condition on which ordinary people keep taking part.",
            ]),
        ],
        ask="The full essay situates the argument against McWhorter, Bottum, Lifton, Durkheim, "
            "Garfinkel and Kuran, sets out the six criteria and the substitution table, and states "
            "three conditions that would count against it.",
    ),
    dict(
        id="SE-08", slug="informacionalisme", kind="Framework",
        title="Informacionalisme",
        sub="Knowledge, power, and the struggle for truth across civilizations",
        meta="Framework · book in progress · 2026",
        blurb="The oldest instrument of power is the management of what people are able to know. "
              "Informacionalisme names the systematic replacement of operative knowledge with managed "
              "ignorance — and the intelligence that institutions commission to sustain it.",
        description="Informacionalisme: the replacement of operative knowledge with managed ignorance, "
                    "from the scribal monopolies to commissioned intelligence.",
        brief=[
            ("An ancient pattern with a new name", [
                "Scholars of democratic backsliding have described authoritarian informationalism: the "
                "manipulation of information flows by modern regimes. The phenomenon is real, but it is "
                "not new. Informacionalisme — named in the French register for its aristocratic "
                "genealogy — is the systematic replacement of operative knowledge with managed "
                "ignorance, calibrated to a literacy ceiling.",
            ]),
            ("Three pressures, every era", [
                "Knowledge drifts and degrades without active preservation. Its custodians develop "
                "interests that diverge from truth. And power manufactures legitimating narratives. The "
                "pattern holds from the scribal monopolies of Mesopotamia and Egypt to Semmelweis, whose "
                "proof that handwashing saved mothers was rejected because accepting it was intolerable. "
                "What has always ended it, imperfectly and for a time, is the written record and the "
                "education that makes it legible.",
            ]),
            ("Gresham’s law applied to truth", [
                "The internet was supposed to collapse the literacy ceiling. Instead counterfeit signal, "
                "cheaper to produce and richer in emotion, drove out good. Flooding an epistemic economy "
                "is the same maneuver as flooding a currency: the aim is not to win a transaction but "
                "to destroy the medium of exchange.",
            ]),
            ("Commissioned intelligence", [
                "Artificial intelligence is a misnomer. Intelligence has always been commissioned: "
                "Augustus commissioned Virgil, the Church commissioned Michelangelo, crowns and popes "
                "founded the universities. What is new is the scale, the speed and the invisibility of "
                "the patron. The question is who commissioned the intelligence, toward what end, and "
                "what corrective signal it was built to suppress.",
                "The framework also explains what the study of ignorance usually misses: why people "
                "cling to their own misinformation. Ignorance is not only inflicted from above. It is "
                "cultivated from below, when an institution offers the security of managed ignorance in "
                "place of the discomfort of knowing. Once ignorance is known to be remediable, choosing "
                "to remain in it is a moral failure.",
            ]),
        ],
        ask="Informacionalisme is the subject of a book in progress. Working papers on the framework, "
            "including its relation to agnotology and to institutional mimicry, are available on request.",
    ),
    dict(
        id="SE-03", slug="the-key-of-the-constitution", kind="Article",
        title="The Key of the Constitution",
        sub="Purpose, oath, and the republic that may not be consecrated",
        meta="Article draft · November 2026",
        blurb="The Preamble states what the government is for, the oath states what officers swear "
              "to, and the Constitution refuses to say what any citizen must profess. One design: a "
              "purpose statement is as confining as a rights statement.",
        description="Every exercise of federal power must serve one of the Preamble’s six ends. "
                    "The oath binds officers to that text, not to the Republic it constrains.",
        brief=[
            ("Three vows", [
                "The Constitution speaks to three vows. Its Preamble says what the government is for. "
                "Its oath clauses say what officers must swear to. And by what it leaves out, and what "
                "its courts have struck down, it says what no citizen may be compelled to profess. "
                "The article argues that the three belong to a single design, and that we have them "
                "in the wrong order.",
            ]),
            ("The Preamble is law", [
                "The first sentence has a subject, a verb, an object and a purpose clause: “in Order "
                "to” names six ends, and the whole instrument is the means. The ratifiers voted on that "
                "sentence with everything beneath it. Story called a preamble the key to the minds of "
                "its makers. James Monroe, who voted against ratification in Virginia, called the "
                "Preamble the key of the Constitution, and said power exercised against it is "
                "unconstitutionally exercised.",
                "Jacobson v. Massachusetts (1905) holds that the Preamble grants no power, and that is "
                "correct. Its wider dismissal answered a question no party briefed. Every prohibition in "
                "the Story passage Jacobson relied on runs against enlargement. None runs against limits.",
            ]),
            ("The purpose test", [
                "Every act of the government must serve at least one of the six ends. If an act does "
                "not do one of these things, it should not be done. The test asks three questions: name "
                "the end, show the link, and count the cost to the other five.",
                "The qualifiers are the teeth. Not welfare but general welfare; not defence but common "
                "defence; liberty for ourselves and our Posterity. Maine’s highest court used exactly "
                "this reasoning in 1871 to refuse a tax for private manufacturers.",
            ]),
            ("The oath, not the Pledge", [
                "The only vow the Constitution prescribes binds officers to a text, and when federal law "
                "uses the word allegiance it names one object: the Constitution. The Pledge, written in "
                "1892, routes devotion through a symbol to the political order itself. The Court refused "
                "to compel it in Barnette and refused to consecrate the flag in Johnson.",
                "The Preamble limits the government’s ends; the Bill of Rights limits its means. Together "
                "they were the settlement of 1791, and they remain the two walls of the cage.",
            ]),
        ],
        ask="The full article sets out the remedy — no new cause of action, a burden to name the end, "
            "deferential review of means and de novo review of the qualifiers — and answers the "
            "objections, including that the test is Lochner by another name.",
    ),
    dict(
        id="SE-04", slug="the-caged-constitution", kind="Essay",
        title="The Caged Constitution",
        sub="Why the Semperists were right",
        meta="Essay · second version · October 2026",
        blurb="The men called Anti-Federalists were not against the Constitution. They were against "
              "trusting structure to hold without written prohibitions. Madison came to agree, and "
              "wrote the cage himself.",
        description="The Bill of Rights as the Federalist structure completed by the Semperist "
                    "program, and the ways the cage is being unscrewed by translation.",
        brief=[
            ("A better name", [
                "The label Anti-Federalist has misled since 1787. These men were not against "
                "federalism, and most of them served the Republic once the Bill of Rights was added. "
                "They were against the confidence that structural design alone, without explicit "
                "prohibition, would hold the powers being granted. I call them Semperists, from "
                "semper, always: the temptations of power are permanent, so the prohibitions must be too.",
            ]),
            ("Madison’s concession", [
                "Madison was the Semperists’ student before he was their opponent. Mason’s Virginia "
                "Declaration of Rights of 1776 is the direct ancestor of the amendments Madison drafted "
                "in 1789, and by the First Congress he had been persuaded. The Bill of Rights is not the "
                "dissenting half of a divided founding. It is the Federalist structure completed by the "
                "program its principal architect came to accept. The cage is not external to the "
                "building. The cage is the building.",
            ]),
            ("The heretic becomes the inquisitor", [
                "Movements that rise against an order in the name of conscience win, take the "
                "institutions, and within a generation turn the same techniques on new dissenters. "
                "Technique outlives content. That is why the grammar of the Bill of Rights is the "
                "grammar of distrust: not of the present rulers, but of every future generation, "
                "especially those who rise to correct the abuses of the past.",
            ]),
            ("Unscrewed by translation", [
                "Prohibitions are rarely repealed. More often their words are kept and refilled. The "
                "essay traces the technique through the fasces and the word socialist to the present "
                "use of equity, which borrows the weight of its Chancery, financial and Aristotelian "
                "senses while meaning none of them — and states what evidence would refute the claim.",
                "The same technique reads the Constitution as a permission structure and routes durable "
                "change around Article V. The American inheritance is cultural, not material, so it can "
                "be lost the same way: not by amendment, not by revolution, but by translation.",
            ]),
        ],
        ask="The full essay sets out the European and colonial history the Semperists drew on, the "
            "fragility of a constitutional inheritance that lives only in practice, and what recovery "
            "would require. It is the second of a pair; the companion essay on the Nordic welfare "
            "states is available on request with it.",
    ),
    dict(
        id="SE-05", slug="conscience-to-the-church", kind="Working draft",
        title="Conscience to the Church; Obligation to the State",
        sub="Marriage as incorporation",
        meta="Working draft · November 2026",
        blurb="The state has two powers over domestic life: to enforce obligations and to define "
              "relationships. It should keep the first and give up the second. Churches keep marriage; "
              "the state registers what people actually undertake.",
        description="A proposal to finish two centuries of unbundling marriage: registered domestic "
                    "associations with a protective floor, and no civil effect for a religious rite alone.",
        brief=[
            ("The wrong fight", [
                "For thirty years the American argument over marriage has been about who may enter the "
                "category. The prior question went unasked: why does the state keep the category at all? "
                "Taxes, benefits, housing, inheritance and support turn on one status, when the state "
                "could look directly at who has undertaken what and who depends on whom.",
                "This is not an argument against marriage. Churches, synagogues, mosques and families "
                "will go on marrying people. The word belongs to whoever uses it.",
            ]),
            ("Finish the unbundling", [
                "The law has been taking the bundle apart for nearly two centuries. The Married Women’s "
                "Property Acts ended coverture. Levy v. Louisiana attached children’s claims to children. "
                "Hospital visitation follows the patient’s designation, and HIPAA gives a spouse no "
                "special right. Each time, the state kept the protection and changed what triggered it — "
                "Maine’s movement from status to contract, carried out inside marriage itself.",
            ]),
            ("Two steps", [
                "First, a religious ceremony should have no civil effect on its own. Alabama already "
                "made formation a filing in 2019. Second, the state should let people register the "
                "household they are actually forming: a joint-estate association, a term association "
                "with renewal, or a separate-estate association that organizes property and liability "
                "much as an LLC does. Civil marriage remains one available form.",
                "Beneath every form sits a floor no agreement can waive: support for children, "
                "recognition of caregiving and lost earning capacity, full disclosure, and protection "
                "against coercion and abuse.",
            ]),
            ("Function, not status", [
                "Why should someone who cared for a disabled partner for twenty years have fewer rights "
                "than someone married for two? Why may a state forbid an employer to consider marital "
                "status, and then tax by it? The church answers for the soul. The state answers for what "
                "people owe.",
            ]),
        ],
        ask="The draft works through Obergefell and the Respect for Marriage Act, the three kinds of "
            "authority, taxation without marital status, five hard cases and a transition with "
            "grandfathering, and includes a fifty-state appendix.",
    ),
    dict(
        id="SE-06", slug="forum-shopping-for-the-apocalypse", kind="Essay",
        title="Forum Shopping for the Apocalypse",
        sub="AI eschatology as a jurisdictional maneuver",
        meta="Essay · October 2026",
        blurb="Whether it promises extinction or paradise, AI eschatology works as a forum-selection "
              "clause. It moves authority up to summits and licensing boards, and away from the "
              "ordinary law states and county courts already enforce.",
        description="The end of the world is not a jurisdiction. A reply to Michael Brendan "
                    "Dougherty on AI eschatology.",
        brief=[
            ("Who profits from the belief", [
                "Michael Brendan Dougherty asked in National Review why so many people decided the only "
                "two endings for artificial intelligence are extinction or abundance, and answered with "
                "the psychology of apocalypse. He is right about the believers. The question he leaves "
                "open is who profits from the belief. A cult has no lobbyists. An eschatology attached "
                "to trillions in capital has a great many.",
            ]),
            ("A forum-selection clause", [
                "Every lawyer learns that jurisdiction is half the case. If the technology decides the "
                "fate of the species, the only competent tribunal is civilizational — summits, security "
                "councils, frontier-model licensing — not the state attorney general, the school board "
                "or the plaintiff’s bar. The doom version ends in licensing only incumbents can afford. "
                "The paradise version ends in preemption.",
            ]),
            ("Watch the forum move", [
                "In 2023 OpenAI’s chief executive asked the Senate for a federal licensing agency. In "
                "2025 he told the Senate that requiring government approval would be disastrous. That "
                "year the House passed a ten-year bar on state AI laws; the Senate struck it 99 to 1. "
                "The prophecy changed. The venue it pointed to never came down to earth.",
            ]),
            ("Ordinary law looks petty", [
                "Next to the end of the world, ordinary law looks small, and that is the point. Contract, "
                "tort and the rules that already govern who may deal with whom are law a state "
                "legislature can enact in a single session and a county court can enforce, without "
                "waiting for a global framework. Those are exactly the rules an eschatology makes "
                "look like a rounding error.",
                "This is not an allegation of a con; the believers are sincere. But sincerity tells you "
                "what a man believes, not whose interests his proposal serves. The end of the world is "
                "not a jurisdiction.",
            ]),
        ],
        ask="The essay is short and was posted publicly in October 2026. It concedes that some AI "
            "risks are concrete and testable, and argues that those deserve plain rules too.",
    ),
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


# ---------------------------------------------------------------- helpers
e = lambda s: html.escape(s, quote=True)

def req_link(title, docid):
    subject = "Request: %s (%s)" % (title, docid)
    body = "\n".join(["Please send: %s (%s)" % (title, docid), "", "Name:", "Institution:",
                      "Role:", "The question you are working on:", ""])
    return "mailto:%s?subject=%s&body=%s" % (EMAIL, quote(subject, safe=""), quote(body, safe=""))

NAV = [("semperism.html", "Semperism"), ("library.html", "Library"), ("about.html", "About")]

def page(fname, title, body, current="", description="", head_extra="", og=None):
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
<meta property="og:type" content="{'article' if 'citation_title' in head_extra else 'website'}">
<meta property="og:site_name" content="Semperism">
<meta property="og:image" content="{(og or {}).get('url', OG_IMAGE)}">
<meta property="og:image:width" content="{(og or {}).get('w', 1200)}">
<meta property="og:image:height" content="{(og or {}).get('h', 630)}">
<meta property="og:image:alt" content="{e((og or {}).get('alt', 'The Semper Virtus medallion of Semperism'))}">
<meta name="twitter:card" content="summary_large_image">
<meta name="application-name" content="Semperism">
<meta name="apple-mobile-web-app-title" content="Semperism">
<meta name="theme-color" content="#1f3358">
{(ld(WEBSITE) + ld(ORG)) if fname == "index.html" else ""}{ld(PERSON) if fname in ("index.html", "about.html") else ""}{head_extra}<link rel="icon" href="/favicon.ico" sizes="48x48">
<link rel="icon" href="/favicon-48.png" sizes="48x48" type="image/png">
<link rel="icon" href="/favicon-96.png" sizes="96x96" type="image/png">
<link rel="icon" href="/favicon-192.png" sizes="192x192" type="image/png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<link rel="stylesheet" href="/style.css">
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="site">
  <a class="brand" href="/"><img class="mark" src="/img/semperism-mark.webp" width="48" height="48" alt="">Semperism</a>
  <nav><ul>{nav}</ul></nav>
  <a class="btn btn-sm" href="mailto:{EMAIL}">Write</a>
</header>
<main id="main">
{body}
</main>
<footer class="site">
  <span>{e(AUTHOR)}</span>
  <span>Correspondence: <a href="mailto:{EMAIL}">{EMAIL}</a></span>
  <span>Essays: <a href="{SUBSTACK}">Semper on Substack</a></span>
  <span>Also by the author: {" &middot; ".join('<a href="%s">%s</a>' % (u, l) for l, u in ELSEWHERE)}</span>
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
        {('<a class="req" href="%s">Read the full paper on Semper</a>' % e(FULL_TEXT[x['slug']])) if x['slug'] in FULL_TEXT else ('<a class="req" href="%s">Request the full paper</a>' % e(req_link(x['title'], x['id'])))}
      </p>
    </article>"""

def post_card(x):
    return f"""    <article class="card">
      <span class="eyebrow">Substack &middot; {e(x['date'])}</span>
      <h3><a href="{e(x['url'])}">{e(x['title'])}</a></h3>
      <p class="card-sub">{e(x['sub'])}</p>
      <p>{e(x['blurb'])}</p>
      <p class="card-actions">
        <a class="btn btn-sm btn-ghost" href="{e(x['url'])}">Read the essay &rarr;</a>
        <a class="req" href="{SUBSTACK}/subscribe">Subscribe free</a>
      </p>
    </article>"""

# ---------------------------------------------------------------- build
if os.path.isdir(OUT):
    shutil.rmtree(OUT)
os.makedirs(OUT)
shutil.copy(os.path.join(ROOT, "style.css"), OUT)
for f in ("favicon.svg", "favicon.ico", "favicon-48.png", "favicon-96.png", "favicon-192.png",
          "apple-touch-icon.png", "site.webmanifest"):
    if os.path.exists(os.path.join(ROOT, f)):
        shutil.copy(os.path.join(ROOT, f), OUT)
shutil.copytree(os.path.join(ROOT, "img"), os.path.join(OUT, "img"))

# Home
home = f"""<section class="hero wrap hero-emblem">
  <img class="emblem" src="/img/semper-virtus-medallion.webp" width="935" height="900" alt="Semper Virtus: Virtue holds the spear at rest, its point breaking a chain; a child holds the book Lex Aeterna; a cracked crown lies at her feet.">
  <div>
  <span class="eyebrow">From <em>sic semper tyrannis</em></span>
  <h1>{e(HERO)}</h1>
  <p class="lede">Semperism is a constitutional philosophy of permanent limits: the study of how institutions acquire a reverence they were never granted, and how a founding text is built to refuse it.</p>
  <p class="hero-actions"><a class="btn" href="/library.html">Enter the library</a> <a class="btn btn-ghost" href="/semperism.html">The framework</a></p>
  </div>
</section>
<section class="wrap">
  <h2 class="section-h">Recently added</h2>
  <div class="pubs">
{chr(10).join(card(x) for x in ENTRIES[:3])}
  </div>
  <p><a href="/library.html">All papers in the library &rarr;</a></p>
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
  <h2>The word</h2>
  <p>History calls them Anti-Federalists, a label their opponents gave them that says only what they were against. Mason, who refused to sign at Philadelphia; Henry, who fought ratification in Virginia; the essayist Brutus; Monroe, who voted no and later became President. What they shared was a conviction the old vocabulary never named: some things are always a threat. Consolidation, consecration, the marking of dissent as disloyalty — these are not accidents of bad rulers. They are the <em>always</em> of government, and they call for permanent, written prohibition.</p>
  <p>I call that disposition <em>Semperist</em>. It is an interpretive name, not a claimed historical identity. It comes from the motto George Wythe’s committee set on Virginia’s seal in 1776, <em>sic semper tyrannis</em>. John Wilkes Booth later turned the phrase into an assassin’s line. It deserves to be heard again as the founders heard it: not vengeance, but a permanent posture toward power. The seal shows it — Virtus standing over the fallen tyrant, spear grounded, sword sheathed.</p>
  <figure class="emblem-fig">
    <img src="/img/semper-virtus-medallion.webp" width="935" height="900" alt="The Semper Virtus emblem.">
    <figcaption><em>Semper Virtus.</em> Virtue holds the spear at rest, its point breaking the chain. The crown lies cracked at her feet, and the child holds <em>Lex Aeterna</em> — the law that outlasts every ruler, kept for posterity.</figcaption>
  </figure>
  <h2>Federalists and Semperists</h2>
  <p>The Federalists believed structure would suffice: ambition set against ambition, because men are not angels. Hamilton argued in Federalist No. 84 that a bill of rights was unnecessary. The Semperists answered that structure without written prohibition invites the very drift structure is meant to slow.</p>
  <p>Neither side simply won. Madison drafted the Bill of Rights himself — the Semperist program, enacted by its ablest opponent. Federalist architecture without Semperist prohibition would have been a machine without a cage. Semperist prohibition without Federalist architecture would have been a cage without a machine. The founding succeeded because two rival virtues corrected each other. It took 278 days to say yes to a government, and 1,550 days to say what it must not do.</p>
  <h2>Anti-consecration architecture</h2>
  <p>On this reading the Constitution fuses Federalist structural design with a Semperist permanent prohibition: no actor and no institution is placed beyond constraint. The officer’s oath under Article VI runs to the Constitution, not to a person, an office or a flag. The Preamble limits the government’s ends; the Bill of Rights limits its means. A purpose statement is as confining as a rights statement.</p>
  <h2>Where the work goes from here</h2>
  <p>The same question — how institutions come to exceed the terms on which they were founded — runs through the papers in the <a href="/library.html">library</a>: the Preamble and the oath, the Bill of Rights and the words it depends on, marriage and the state, displacement and the regimes that cause it, and the reach of institutions over lawful private life.</p>
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

  <h2 class="section-h">Essays on Substack</h2>
  <p class="muted">Shorter pieces are published in full on <a href="{SUBSTACK}">Semper</a>, free to read with no subscription needed. Subscribe there to get new essays by email.</p>
  <div class="pubs">
{chr(10).join(post_card(x) for x in POSTS)}
  </div>


  <div class="note">
    <h3>Why the full papers are sent rather than posted</h3>
    <p>Several of these papers are still moving, and some are written for a particular audience or jurisdiction. Rather than post a version written for nobody in particular, I send the current one with the question in view. Say what you are working on in the request and I will reply with the paper, usually within a few days. Requests are as welcome from critics as from allies.</p>
  </div>
  <div class="note">
    <h3>Not everything is listed here</h3>
    <p>Further work — on the Constitution, the Pledge and the oath, and scripture — is under submission to journals and so is not posted. It is available on request for review purposes. Write to <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
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
             f'<meta name="citation_author_orcid" content="https://orcid.org/0009-0004-3600-4115">\n'
             f'<meta name="citation_publication_date" content="{year}">\n'
             f'<meta name="citation_public_url" content="{url}">\n'
             + ld({"@type": "ScholarlyArticle", "headline": x["title"],
                   "alternativeHeadline": x.get("sub", ""), "description": x["description"],
                   "author": {"@id": PERSON["@id"], "@type": "Person", "name": PERSON["name"],
                              "url": PERSON["url"]},
                   "datePublished": str(year), "url": url, "inLanguage": "en",
                   **({"sameAs": FULL_TEXT[x["slug"]]} if x["slug"] in FULL_TEXT else {}),
                   "isPartOf": {"@type": "WebSite", "name": "Semperism", "url": DOMAIN + "/"}}))
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
    <p>{e("The full paper is published on Semper, free to read." if x['slug'] in FULL_TEXT else x['ask'])}</p>
    <p class="card-actions">
      {('<a class="btn btn-sm" href="%s">Read the full paper &rarr;</a>' % e(FULL_TEXT[x['slug']])) if x['slug'] in FULL_TEXT else ('<a class="btn btn-sm" href="%s">Request the full paper</a>' % e(req_link(x['title'], x['id'])))}
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
  <figure style="margin:8px 0 28px">
    <img src="img/knudson-with-ronald-reagan.jpg" alt="S. Harrison Knudson (Steele Harrison Knudson, Steele Knudson) with President Ronald Reagan" width="448" height="364" style="width:100%;max-width:448px;height:auto;display:block">
    <figcaption style="font-size:13px;opacity:.7;margin-top:8px">S. Harrison Knudson (Steele Harrison Knudson, Steele Knudson) with President Ronald Reagan.</figcaption>
  </figure>
  <p>Steele Knudson has some two decades of practice across federal regulatory compliance, export controls and anti-corruption, antitrust, land use and internet governance. He holds a J.D. from George Mason University’s Antonin Scalia Law School and a B.S. in Urban Planning from the University of Utah.</p>
  <p>His work runs on several tracks that share one question — how institutions come to exceed the terms on which they were founded. This site collects the constitutional side of that work: Semperism.</p>
  <p>Correspondence: <a href="mailto:{EMAIL}">{EMAIL}</a></p>
  <p class="aka" style="font-size:13px;opacity:.6;margin-top:40px;padding-top:12px;border-top:1px solid currentColor">S. Harrison Knudson is also known as Steele Knudson and Steele Harrison Knudson.</p>
</article>"""
page("about.html", "About — S. Harrison Knudson (Steele Harrison Knudson)", about, current="about.html",
     og={"url": "https://semperism.org/img/knudson-with-ronald-reagan.jpg", "w": 448, "h": 364,
         "alt": "S. Harrison Knudson (Steele Harrison Knudson, Steele Knudson) with President Ronald Reagan"},
     description="S. Harrison Knudson, J.D. (Steele Harrison Knudson) — American lawyer and scholar, Arlington, Virginia.")

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
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">\n'
            + "".join(f"  <url><loc>{DOMAIN}{u}</loc>"
                      + (f"<image:image><image:loc>{DOMAIN}/img/knudson-with-ronald-reagan.jpg</image:loc></image:image>" if u.endswith("about.html") else "")
                      + "</url>\n" for u in urls) + "</urlset>\n")
shutil.copy(os.path.join(ROOT, "README.md"), OUT)
os.makedirs(os.path.join(OUT, "docs"), exist_ok=True)
print("built", len(ENTRIES), "briefs ->", OUT)
