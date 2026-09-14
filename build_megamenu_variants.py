#!/usr/bin/env python3
"""Generate two further mega-menu variants, for the core-committee comparison.

  megamenu-b/   Variant B — a faithful port of the colleague's revised_4 mockup
                (docs/TC_MegaMenu_revised_4.html) into TC brand and content:
                Our Work · Impacts · Data & Tools · Resources · About.
                Data & Tools stands alone, third.

  megamenu-c/   Variant C — the data-first hybrid: Data & Tools is folded INTO
                Our Work and leads it, so public health data sits at the same
                level as Communities and Projects rather than below them.
                Our Work · Impacts · Resources · About.

Both follow the /megamenu/ pattern exactly: root pages copied into the variant
folder with the header swapped, asset paths rewritten to ../ so the 29MB
assets/ and pagefind/ are SHARED, and the trial CSS/JS layered on top. The
root prototype and /megamenu/ are never touched.

These are navigation mockups. Links to pages that do not exist yet (the
surveillance programs, impacts, fee-for-service, Espanol) are href="#" and
carry class="todo", which is a marker for the build only — no visual treatment.

Run:  python3 build_megamenu_variants.py     (idempotent — rerun any time)
Bin:  rm -rf megamenu-b/ megamenu-c/
"""
import os, re, glob, shutil

ROOT = os.path.dirname(os.path.abspath(__file__))

# --------------------------------------------------------------- helpers ---
def link(href, label, desc=None, todo=False):
    d = '<span class="mm-desc">%s</span>' % desc if desc else ""
    # todo = no page behind it yet. Marked in the markup for the build's sake,
    # but deliberately given no visual treatment.
    c = "mm-link todo" if todo else "mm-link"
    return '<a class="%s" href="%s">%s%s</a>' % (c, href, label, d)

def sub(links):
    """A nested list under the link above it, with a light blue rule."""
    return '<div class="mm-sub">\n            %s\n          </div>' % "\n            ".join(links)

def col(title, links, tail=None, extra=""):
    t = ('\n          <a class="link-arrow" href="%s">%s</a>' % tail) if tail else ""
    return ('        <div class="mm-col%s">\n          <p class="mm-title">%s</p>\n'
            '          %s%s\n        </div>\n' % (extra, title, "\n          ".join(links), t))

def pills(areas, todo=False):
    c = ' class="todo"' if todo else ""
    return '<div class="mm-pills">%s</div>' % "".join(
        '<a href="%s"%s>%s</a>' % (h, c, l) for l, h in areas)

def feature(title, blocks, tail=None):
    t = ('\n          <a class="link-arrow" href="%s">%s</a>' % tail) if tail else ""
    return ('        <div class="mm-col mm-feature">\n          <p class="mm-title">%s</p>\n'
            '          %s%s\n        </div>\n' % (title, "\n          ".join(blocks), t))

def stats(pairs):
    return ('<div class="mm-stats">\n            %s\n          </div>' % "\n            ".join(
        '<div><span class="n">%s</span><span class="l">%s</span></div>' % p for p in pairs))

def foot(title, body, tail):
    return ('        <div class="mm-foot">\n          <p class="mm-title">%s</p>\n'
            '          %s\n          <a class="link-arrow" href="%s">%s</a>\n'
            '        </div>\n' % (title, body, tail[0], tail[1]))

# ------------------------------------------------------- shared ingredients --
# The seven focus areas. Six have a page; "Health services" is new in the
# colleague's mockup and has nothing behind it yet.
AREAS = [("Air quality", "priority-area.html"), ("Climate resilience", "priority-area.html"),
         ("Extreme heat", "priority-area.html"), ("Pesticides", "priority-area.html"),
         ("Sickle cell disease", "priority-area.html"), ("Water quality", "priority-area.html")]
AREAS_PLUS = AREAS + [("Health services", "#")]

COMMUNITIES = [
    link("communities.html", "Where we work", "Map of Tracking's community partnerships"),
    link("community-story.html", "Community stories", "Partnerships in their own words"),
    link("communities.html#involved", "Get involved", "Bring us a question from your community"),
    link("work-with-us.html", "Work with us", "Fee-for-service and technical assistance"),
]
PROJECTS = [
    link("projects.html#current", "Current projects", "What we have running right now"),
    link("projects.html#previous", "Previous projects", "Completed work and what came of it"),
]

# Impacts — a new content area in the colleague's version. Kept in the nav so
# the shape can be judged, but nothing is written behind it yet.
PANEL_IMPACTS = col("What changed", [
        link("#", "Impact stories", "What shifted for communities because of our work", todo=True),
        link("#", "Policy outcomes", "Regulations and decisions our data informed", todo=True),
        link("#", "Community outcomes", "Capacity built, practices changed, local action taken", todo=True),
        link("#", "Tools adopted", "Where our data is being used beyond Tracking", todo=True),
    ]) + col("In the press", [
        link("resources.html?filter=news", "News &amp; press releases", "Announcements, data releases, program updates"),
        link("#", "Media coverage", "How our work has been covered and cited", todo=True),
        link("#", "Awards &amp; recognition", "External recognition of Tracking's work", todo=True),
    ]) + feature("In practice", [
        link("#", "Agricultural pesticides near schools", "Policy outcome — new state regulations followed our research", todo=True),
        link("#", "FRESSCA: farmworkers breathing cleaner air", "Community outcome — heat and pesticide resilience", todo=True),
    ])

PANEL_RESOURCES = col("Read", [
        link("resources.html?filter=paper", "Articles &amp; reports", "Peer-reviewed research and technical reports"),
        link("resources.html?filter=news", "Data briefs", "Accessible summaries for non-technical audiences"),
        link("resources.html?filter=newsletter", "Newsletters", "Program highlights, a few times a year"),
    ]) + col("Watch &amp; explore", [
        link("resources.html?filter=video", "Videos", "Webinars, community stories, project overviews"),
        link("topics.html", "Health topics", "Asthma, pesticides, water, heat and more"),
        link("resources.html", "Full library", "Everything, filterable by topic and type"),
    ]) + feature("Recent", [
        link("resources.html?filter=paper", "Temporal trends of agricultural organophosphate pesticide use in California", "Peer-reviewed · 2025"),
        stats([("120+", "publications")]),
    ], ("resources.html?filter=paper", "See all publications"))

PANEL_ABOUT = col("Who we are", [
        link("about.html", "About Tracking", "Our mission and what sets us apart"),
        link("about.html#team", "Our staff", "The people behind the program"),
        link("about.html#partners", "Our partners", "Community, agency, and academic partners"),
        link("#", "Funding", "How our work is supported", todo=True),
        link("about.html#contact", "Contact us", "Get in touch with the team"),
    ]) + col("Work with us", [
        link("work-with-us.html", "Why partner with us", "Community reach, data expertise, a 25-year record"),
        link("#", "Fee-for-service", "Bespoke data, analysis, and technical assistance", todo=True),
        link("work-with-us.html#contact", "Start a conversation", "Tell us what you're trying to find out"),
    ]) + feature("In numbers", [
        stats([("25+", "years active"), ("45+", "community partners"), ("120+", "publications")]),
    ], ("about.html", "More about us"))

# Tools, listed individually — the colleague's "tools by focus area" column.
TOOLS_BY_AREA = [
    link("tools.html", "Pesticide Mapping Tool", "Agricultural pesticide use across California"),
    link("tools.html", "Water Quality Viewer", "Contaminant levels in water systems statewide"),
    link("tools.html", "PFAS Maps", "PFAS in California drinking water"),
    link("tools.html", "Hot &amp; Smoky Tool", "Heat and wildfire smoke exposure"),
    link("tools.html", "Traffic Exposure Dataset", "Statewide traffic volumes for research"),
    link("tools.html", "Healthcare Accessibility Map", "Distance to ER and maternity care"),
]
FIND_WHAT_YOU_NEED = [
    link("data-and-tools.html", "Find your data", "Answer two questions, get the right dataset or tool"),
    link("data-explorer.html", "Data Explorer", "Air, water, heat, health — mapped to your community"),
    link("tools.html", "All our tools", "Explorers, maps, and viewers"),
    link("data.html", "Datasets &amp; repositories", "Download our open data and code"),
]

# ------------------------------------------------------------- variant B ---
# Faithful port: five sections, Data & Tools standing alone in third place.
B_WORK = col("Focus areas", [pills(AREAS_PLUS)], ("priority-areas.html", "All focus areas")) \
       + col("Communities", COMMUNITIES) \
       + col("Projects", PROJECTS, ("projects.html", "All projects")) \
       + feature("Latest work", [
            link("projects.html#current", "FRESSCA: farmworker resilience to heat and pesticide exposure", "Impact story"),
            stats([("45+", "community partners"), ("24", "active &amp; recent projects")]),
         ])

B_DATA = col("Find what you need", FIND_WHAT_YOU_NEED) \
       + col("Tools by focus area", TOOLS_BY_AREA) \
       + feature("Start here", [
            link("data-and-tools.html", "Not sure which tool or dataset you need?", "Find your data"),
            stats([("8+", "tools and data products"), ("120+", "open datasets")]),
         ])

# ------------------------------------------------------------- variant C ---
# Data-first hybrid: Data & Tools folded into Our Work and leading it, so the
# menu answers "data shop or community organisation?" with "data, in service of
# communities" rather than leaving data in third place outside the work.
C_WORK = col("Public health data", [
        link("#", "Surveillance", "Long-running statewide data programs", todo=True),
        sub([
            link("#", "Environmental Health Tracking (EHTP)", todo=True),
            link("#", "Sickle Cell Data Collection (SCDC)", todo=True),
        ]),
        link("data.html", "Our data", "What we collect, and how to get at it"),
        link("data-and-tools.html", "Find your data", "Answer two questions, get the right dataset"),
    ], ("data.html", "All our data")) \
    + col("Tools", [
        link("data-explorer.html", "Data Explorer", "Air, water, heat, health — mapped to your community"),
        link("tools.html", "Our tools", "Explorers, maps, and viewers"),
        link("tools.html", "Pesticide Mapping Tool", "Agricultural pesticide use across California"),
        link("tools.html", "Water Quality Viewer", "Contaminant levels statewide"),
    ], ("tools.html", "All our tools")) \
    + col("Communities", COMMUNITIES) \
    + col("Projects", PROJECTS, ("projects.html", "All projects")) \
    + foot("Focus areas", pills(AREAS_PLUS), ("priority-areas.html", "All focus areas"))

# --------------------------------------------------------------- variants --
VARIANTS = {
  "megamenu-b": dict(
    css="megamenu-b", home=None,
    ribbon=('<div class="proto-ribbon"><strong>Mega-menu variant B</strong> — five sections, '
            'Data &amp; Tools standing on its own. '
            '<a href="../megamenu-c/index.html">Variant C: data-first →</a> · '
            '<a href="../megamenu/index.html">Variant A →</a> · '
            '<a href="../index.html">Standard version →</a></div>'),
    panels=[("work", "Our Work", B_WORK, " cols-4"),
            ("impacts", "Impacts", PANEL_IMPACTS, " cols-2"),
            ("data", "Data &amp; Tools", B_DATA, " cols-2"),
            ("resources", "Resources", PANEL_RESOURCES, " cols-2"),
            ("about", "About", PANEL_ABOUT, " cols-2")],
    section={"data-and-tools.html": "data", "data.html": "data", "tools.html": "data",
             "data-explorer.html": "data",
             "communities.html": "work", "community-story.html": "work",
             "projects.html": "work", "priority-areas.html": "work", "priority-area.html": "work",
             "resources.html": "resources", "topics.html": "resources",
             "topic.html": "resources", "resource-article.html": "resources",
             "about.html": "about", "work-with-us.html": "about"},
    news="resources"),

  "megamenu-c": dict(
    css="megamenu-c", home=None,
    ribbon=('<div class="proto-ribbon"><strong>Mega-menu variant C</strong> — data-first: '
            'Data &amp; Tools folded into Our Work, and leading it. '
            '<a href="../megamenu-b/index.html">Variant B: data alongside →</a> · '
            '<a href="../megamenu/index.html">Variant A →</a> · '
            '<a href="../index.html">Standard version →</a></div>'),
    panels=[("work", "Our Work", C_WORK, " cols-4"),
            ("impacts", "Impacts", PANEL_IMPACTS, " cols-2"),
            ("resources", "Resources", PANEL_RESOURCES, " cols-2"),
            ("about", "About", PANEL_ABOUT, " cols-2")],
    section={"data-and-tools.html": "work", "data.html": "work", "tools.html": "work",
             "data-explorer.html": "work",
             "communities.html": "work", "community-story.html": "work",
             "projects.html": "work", "priority-areas.html": "work", "priority-area.html": "work",
             "resources.html": "resources", "topics.html": "resources",
             "topic.html": "resources", "resource-article.html": "resources",
             "about.html": "about", "work-with-us.html": "about"},
    news="resources"),
}

# ---------------------------------------------------------------- header ---
def header_for(v, section):
    def cls(key):
        return " active" if section == key else ""
    parts = ['<header class="site-header">',
             '  <div class="wrap header-inner">',
             '    <a class="brand" href="index.html" aria-label="Tracking California home">',
             '      <img class="brand-logo" src="../assets/tc-logo.svg" alt="Tracking California">',
             '    </a>',
             '    <button class="nav-toggle" aria-label="Menu">',
             '      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">'
             '<path d="M3 6h18M3 12h18M3 18h18"/></svg>',
             '    </button>',
             '    <nav class="nav mm-nav">']
    for key, label, body, extra in v["panels"]:
        parts += ['      <div class="mm-item">',
                  '        <button class="mm-trigger%s" id="mm-t-%s" aria-expanded="false" '
                  'aria-controls="mm-p-%s">%s <span class="caret">▾</span></button>'
                  % (cls(key), key, key, label),
                  '        <div class="mm-panel" id="mm-p-%s" role="region" aria-labelledby="mm-t-%s">'
                  % (key, key),
                  '      <div class="wrap mm-inner%s">' % extra,
                  body.rstrip("\n"),
                  '      </div>',
                  '        </div>',
                  '      </div>']
    parts += ['      <a class="nav-search" href="search.html" aria-label="Search">',
              '        <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
              'stroke-width="2"><circle cx="11" cy="11" r="7"/><path d="m21 21-4.3-4.3"/></svg>',
              '        Search',
              '      </a>',
              '      <a class="nav-lang" href="#">Espa&ntilde;ol</a>',
              '    </nav>',
              '  </div>',
              '</header>']
    return "\n".join(parts)

# ------------------------------------------------------------------ build ---
pages = sorted(os.path.basename(p) for p in glob.glob(os.path.join(ROOT, "*.html")))

for folder, v in VARIANTS.items():
    out = os.path.join(ROOT, folder)
    if os.path.isdir(out):
        shutil.rmtree(out)
    os.makedirs(out)

    section = dict(v["section"])
    for p in glob.glob(os.path.join(ROOT, "news-*.html")):
        section[os.path.basename(p)] = v["news"]

    for name in pages:
        s = open(os.path.join(ROOT, name)).read()

        # share the root assets/ and pagefind/ rather than copying 29MB
        s = re.sub(r'(?<=["\'(])(assets|pagefind)/', r'../\1/', s)

        # swap the whole header block wholesale (never line-level — see CLAUDE.md)
        s, n = re.subn(r'<header class="site-header">.*?</header>',
                       lambda m: header_for(v, section.get(name, "")), s, count=1, flags=re.S)
        if not n:
            print("  ! no header found in", name)

        # reuse the existing prototype ribbon slot for the variant notice
        s = re.sub(r'<div class="proto-ribbon">.*?</div>', lambda m: v["ribbon"], s, count=1, flags=re.S)

        # layer the mega-menu CSS/JS, then the variant add-ons, on top
        s = s.replace('<link rel="stylesheet" href="../assets/styles.css">',
                      '<link rel="stylesheet" href="../assets/styles.css">\n'
                      '<link rel="stylesheet" href="../assets/megamenu.css">\n'
                      '<link rel="stylesheet" href="../assets/megamenu-variants.css">', 1)
        s = s.replace('<script src="../assets/main.js"></script>',
                      '<script src="../assets/main.js"></script>\n'
                      '<script src="../assets/megamenu.js"></script>', 1)

        open(os.path.join(out, name), "w").write(s)

    print("%s built: %d pages" % (folder, len(pages)))
