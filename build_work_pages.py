#!/usr/bin/env python3
"""Generate the pages behind the nav links that still point at '#'.

The mega menu promises fourteen things the site cannot deliver. For external
user testing that is the biggest risk we have: people click, and nothing
happens. This fills eleven of them.

These are deliberately, visibly UNFINISHED pages, not dummy content. A
placeholder that looks like content is worse than no placeholder, because it
gets shipped by accident and because testers react to the invented prose
instead of to the navigation. Same reasoning as the .tbc chips on the
focus-area pages, and the same styling.

What is real on every page:
  - the title, taken from the nav
  - the lead sentence, which is the nav's own description, already agreed
  - every outbound link, which points at a page that exists today

What is marked as missing: the body. Nothing is invented.

Three links are deliberately NOT built here, because each sits on an open
committee decision:
  Impact stories, Policy & practice outcomes  - Michelle doubts Our Program
                                                has enough behind it to justify
                                                the section at all
  Health services                             - the seven focus areas are not
                                                confirmed final

Run:  python3 build_work_pages.py && python3 build_nav.py
      (build_nav.py second, so the new pages get the nav and the active state)
"""
import os, re, html

ROOT = os.path.dirname(os.path.abspath(__file__))
TEMPLATE = os.path.join(ROOT, "work-with-us.html")
SITE = "https://jo-wilkin-tc.github.io/tc-website-redesign"

# ---------------------------------------------------------------------------
# One entry per page. "lead" is copied from the mega-menu description in
# build_nav.py — it is the one piece of prose here that has been agreed.
# "related" may ONLY point at pages that exist; the whole point of these stubs
# is that every link on them works.
# ---------------------------------------------------------------------------
PAGES = [
  # ---- Our Work / Data & surveillance ----
  dict(slug="work-statewide-tracking", section="Data &amp; surveillance",
       title="Statewide tracking",
       lead="Environmental health surveillance across California.",
       related=[("data.html", "Our data"),
                ("data-explorer.html", "Data Explorer"),
                ("priority-areas.html", "Focus areas")]),
  dict(slug="work-sickle-cell-data-collection", section="Data &amp; surveillance",
       title="Sickle Cell Data Collection",
       lead="Twenty years of linked patient data.",
       related=[("projects.html", "Projects"),
                ("resources.html?filter=paper", "Articles &amp; reports"),
                ("data.html", "Our data")]),
  dict(slug="work-health-environment-indicators", section="Data &amp; surveillance",
       title="Health &amp; environment indicators",
       lead="The measures we maintain and publish.",
       related=[("data.html", "Our data"),
                ("topics.html", "Health topics"),
                ("data-and-tools.html", "Find your data")]),
  dict(slug="work-primary-data-collection", section="Data &amp; surveillance",
       title="Primary data collection",
       lead="Monitoring and sampling in the field.",
       related=[("projects.html#current", "Current projects"),
                ("communities.html", "Where we work")]),
  # ---- Our Work / Research & analysis ----
  dict(slug="work-community-based-research", section="Research &amp; analysis",
       title="Community-based research",
       lead="Questions set with the people they affect.",
       related=[("communities.html", "Where we work"),
                ("community-story.html", "Partner stories"),
                ("communities.html#involved", "Get involved")]),
  dict(slug="work-epidemiology", section="Research &amp; analysis",
       title="Epidemiology",
       lead="Who is affected, where, and how much.",
       related=[("resources.html?filter=paper", "Articles &amp; reports"),
                ("topics.html", "Health topics")]),
  dict(slug="work-spatial-analysis-mapping", section="Research &amp; analysis",
       title="Spatial analysis &amp; mapping",
       lead="Exposure, access and risk across place.",
       related=[("tools.html", "All our tools"),
                ("data-explorer.html", "Data Explorer"),
                ("communities.html", "Where we work")]),
  dict(slug="work-data-linkage", section="Research &amp; analysis",
       title="Data linkage",
       lead="Joining health, environmental and place data.",
       related=[("data.html", "Our data"),
                ("resources.html?filter=paper", "Articles &amp; reports")]),
  # ---- Our Work / Capacity building & support ----
  dict(slug="work-training-instruction", section="Capacity building &amp; support",
       title="Training &amp; instruction",
       lead="Teaching partners to work with their own data.",
       related=[("work-with-us.html", "Work with us"),
                ("resources.html?filter=video", "Videos"),
                ("communities.html#involved", "Get involved")]),
  # ---- Data & Tools / Data & open science ----
  dict(slug="data-insights", section="Data &amp; open science",
       title="Data insights",
       lead="What the numbers are telling us.",
       related=[("resources.html?filter=news", "Data briefs"),
                ("data-explorer.html", "Data Explorer"),
                ("topics.html", "Health topics")]),
]

# ---------------------------------------------------------------------------
# Code & repositories is the one page here with real structure rather than a
# stub body: we know which tools exist, because tools.html lists them.
#
# What we do NOT know is where the code lives. The nav description says "on
# GitHub", but the repo-hosting decision is still open — some team members are
# on health-department laptops that are not permitted to use GitHub as a code
# store. So every URL below is a marked gap, not a guess, and the note on the
# page says so. Fill REPOS in once that is settled.
# ---------------------------------------------------------------------------
REPOS = [
  ("Pesticide Mapping Tool",      "R / Shiny",     None),
  ("New Pesticide Mapping Tool",  "R / Shiny",     None),
  ("Pesticide Linkage Service",   "Python",        None),
  ("Water Quality Viewer",        "R / Shiny",     None),
  ("Healthcare Accessibility Map","R / Shiny",     None),
  ("Lithium Valley Data Explorer","R / Shiny",     None),
  ("PurpleAir Download Tool",     "R",             None),
  ("Traffic Tool",                "Python",        None),
  ("Hot &amp; Smoky Tool",        "R / Shiny",     None),
  ("Climate Tool &amp; Data Finder", "R / Shiny",  None),
]

TBC = '<span class="tbc">to confirm</span>'

# ------------------------------------------------------------------ body ----
def lead_and_note(lead, what):
    """Lead and the in-development marker share one section — as two they left
    a stranded band of white space between them."""
    return """
  <!-- LEAD + IN DEVELOPMENT -->
  <section class="section">
    <div class="wrap">
      <div class="prose" style="max-width:75%%;">
        <p class="lead">%s</p>
        <p><span class="tbc">page in development</span></p>
        <p class="tbc-note">%s This page exists so the navigation can be tested
        end to end &mdash; the route works, the content has not been written yet.
        Nothing on this page is placeholder prose standing in for real copy.</p>
      </div>
    </div>
  </section>
""" % (lead, what)

def related_block(related):
    items = "".join(
        '<li><a href="%s">%s</a></li>\n        ' % (h, l) for h, l in related)
    return """
  <!-- WHAT EXISTS TODAY -->
  <section class="section tint">
    <div class="wrap">
      <div class="section-head" style="max-width:75%%;">
        <h2 class="sec-title">In the meantime</h2>
        <p>Related pages that are built and working today.</p>
      </div>
      <ul class="news-list">
        %s</ul>
    </div>
  </section>
""" % items

def banner(section, title, lead):
    return """
  <!-- BANNER -->
  <section class="page-banner">
    <div class="wrap">
      <p class="eyebrow">%s</p>
      <h1>%s</h1>
      <p class="lead">%s</p>
    </div>
  </section>
""" % (section, title, lead)

def stub_body(p):
    return (banner(p["section"], p["title"], "")
            + lead_and_note(p["lead"],
                            "The line above is the description agreed in the "
                            "navigation; the rest is still to be written.")
            + related_block(p["related"]))

def repos_body():
    rows = "".join(
        '<li><strong>%s</strong> &mdash; %s &middot; %s</li>\n        '
        % (name, lang, ('<a href="%s">repository</a>' % url) if url else TBC)
        for name, lang, url in REPOS)
    return (banner("Data &amp; open science", "Code &amp; repositories",
                   "How we built it.")
            + """
  <!-- THE REPOS -->
  <section class="section">
    <div class="wrap">
      <div class="section-head" style="max-width:75%%;">
        <h2 class="sec-title">Our tools, and the code behind them</h2>
        <p>Every tool we publish is built from code we maintain. The list is real;
        the links are not set yet.</p>
      </div>
      <ul class="adv-list">
        %s</ul>
      <div class="prose" style="max-width:75%%;">
        <p class="tbc-note">Repository links are marked <em>to confirm</em> because
        where the code is hosted has not been decided. The navigation currently
        says &ldquo;on GitHub&rdquo;, but not everyone on the team can use GitHub
        as a code store &mdash; some work on health-department laptops that do not
        permit it. That decision has to come before these links can be filled in,
        and it may change the wording in the menu too.</p>
      </div>
    </div>
  </section>
"""     % rows
            + related_block([("tools.html", "All our tools"),
                             ("data.html", "Our data"),
                             ("data.html", "Datasets &amp; downloads")]))

# ----------------------------------------------------------------- build ----
def strip(s):
    return html.unescape(re.sub(r"<[^>]+>", "", s)).strip()

shell = open(TEMPLATE).read()
head, rest = shell.split('<main id="main" data-pagefind-body>', 1)
_, tail = rest.split("</main>", 1)

def write(slug, title, desc, body):
    s = head + '<main id="main" data-pagefind-body>\n' + body + "\n</main>" + tail
    s = re.sub(r"<title>.*?</title>",
               "<title>%s | Tracking California</title>" % title, s, count=1, flags=re.S)
    s = re.sub(r'(<meta name="description" content=")[^"]*(")',
               lambda m: m.group(1) + desc + m.group(2), s, count=1)
    s = re.sub(r'(<meta property="og:title" content=")[^"]*(")',
               lambda m: m.group(1) + title + m.group(2), s, count=1)
    s = re.sub(r'(<meta property="og:description" content=")[^"]*(")',
               lambda m: m.group(1) + desc + m.group(2), s, count=1)
    s = re.sub(r'(<meta property="og:url" content=")[^"]*(")',
               lambda m: m.group(1) + "%s/%s.html" % (SITE, slug) + m.group(2), s, count=1)
    open(os.path.join(ROOT, slug + ".html"), "w").write(s)
    print("  %s.html" % slug)

if __name__ == "__main__":
    print("pages behind the nav:")
    for p in PAGES:
        write(p["slug"], strip(p["title"]), strip(p["lead"]), stub_body(p))
    write("code-repositories", "Code & repositories",
          "The code behind the tools Tracking California publishes.", repos_body())
    print("\nnow run: python3 build_nav.py")
