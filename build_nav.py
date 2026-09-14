#!/usr/bin/env python3
"""Apply the site navigation to every root page.

This is the mega menu that was trialled as variant D and adopted by the core
committee. The nav is duplicated verbatim into every *.html page (the repo has
no templating), so this script is how it gets changed: edit the panels below
and rerun.

resources.html matters more than the others — build_content.py and
build_projects.py take everything before <main> from it as their page chrome,
so a nav change that misses it is reverted the next time those run. Because
this script rewrites resources.html too, run it BEFORE them, not after.

Run:  python3 build_nav.py        (idempotent — rerun any time)
"""
import os, re, glob

ROOT = os.path.dirname(os.path.abspath(__file__))

def link(href, label, desc=None):
    d = '<span class="mm-desc">%s</span>' % desc if desc else ""
    return '<a class="mm-link" href="%s">%s%s</a>' % (href, label, d)

def col(title, links, tail=None):
    t = ('\n          <a class="link-arrow" href="%s">%s</a>' % tail) if tail else ""
    return ('        <div class="mm-col">\n          <p class="mm-title">%s</p>\n'
            '          %s%s\n        </div>\n' % (title, "\n          ".join(links), t))

def feature(title, blocks, tail=None):
    t = ('\n          <a class="link-arrow" href="%s">%s</a>' % tail) if tail else ""
    return ('        <div class="mm-col mm-feature">\n          <p class="mm-title">%s</p>\n'
            '          %s%s\n        </div>\n' % (title, "\n          ".join(blocks), t))

def stats(pairs):
    return ('<div class="mm-stats">\n            %s\n          </div>' % "\n            ".join(
        '<div><span class="n">%s</span><span class="l">%s</span></div>' % p for p in pairs))

def foot(title, areas, tail):
    pills = '<div class="mm-pills">%s</div>' % "".join(
        '<a href="%s">%s</a>' % (h, l) for l, h in areas)
    return ('        <div class="mm-foot">\n          <p class="mm-title">%s</p>\n'
            '          %s\n          <a class="link-arrow" href="%s">%s</a>\n'
            '        </div>\n' % (title, pills, tail[0], tail[1]))

AREAS = [("Air quality", "priority-area.html"), ("Climate resilience", "priority-area.html"),
         ("Extreme heat", "priority-area.html"), ("Pesticides", "area-pesticides.html"),
         ("Sickle cell disease", "priority-area.html"), ("Water quality", "priority-area.html"),
         ("Health services", "#")]

# ---------------------------------------------------------------- panels ----
# Our Work: capabilities, not possessions. Much of this has no page yet — that
# is the point of the mockup, and the gap the content build has to fill.
PANEL_WORK = col("Data &amp; surveillance", [
        link("#", "Statewide tracking", "Environmental health surveillance across California"),
        link("#", "Sickle Cell Data Collection", "Twenty years of linked patient data"),
        link("#", "Health &amp; environment indicators", "The measures we maintain and publish"),
        link("#", "Primary data collection", "Monitoring and sampling in the field"),
    ], ("data.html", "See the data")) + col("Research &amp; analysis", [
        link("#", "Community-based research", "Questions set with the people they affect"),
        link("#", "Epidemiology", "Who is affected, where, and how much"),
        link("#", "Spatial analysis &amp; mapping", "Exposure, access and risk across place"),
        link("#", "Data linkage", "Joining health, environmental and place data"),
    ], ("resources.html?filter=paper", "Read our research")) + col("Capacity building &amp; support", [
        link("#", "Training &amp; instruction", "Teaching partners to work with their own data"),
        link("work-with-us.html", "Technical assistance", "Hands-on help with a question you are stuck on"),
        link("work-with-us.html#contact", "Bespoke data &amp; analysis", "Commissioned work, costed and scoped"),
        link("tools.html", "Decision-support tools", "Built for the people who have to act"),
    ], ("work-with-us.html", "Work with us")) \
    + foot("Focus areas", AREAS, ("priority-areas.html", "All focus areas"))

PANEL_DATA = col("Start here", [
        link("data-and-tools.html", "Find your data", "Answer two questions, get the right dataset or tool"),
        link("data-explorer.html", "Data Explorer", "Air, water, heat and health, mapped to your community"),
    ], ("data-and-tools.html", "Not sure what you need?")) + col("Our tools", [
        link("tools.html", "All our tools", "Explorers, maps and viewers"),
        link("tools.html", "Pesticide Mapping Tool", "Agricultural pesticide use across California"),
        link("tools.html", "Water Quality Viewer", "Contaminant levels in water systems statewide"),
        link("tools.html", "Healthcare Accessibility Map", "Distance to emergency and maternity care"),
    ]) + col("Data &amp; open science", [
        link("data.html", "Our data", "What we collect, and how to get at it"),
        link("data.html", "Datasets &amp; downloads", "Open data, ready to use"),
        link("#", "Code &amp; repositories", "How we built it, on GitHub"),
        link("#", "Data insights", "What the numbers are telling us"),
    ], ("data.html", "All our data"))

PANEL_PROJECTS = col("Projects", [
        link("projects.html#current", "Current projects", "What we have running right now"),
        link("projects.html#previous", "Previous projects", "Completed work and what came of it"),
        link("priority-areas.html", "Projects by focus area", "Pesticides, heat, water, air and more"),
    ], ("projects.html", "All projects")) + col("Partnerships", [
        link("communities.html", "Where we work", "The map of who we work with, and on what"),
        link("community-story.html", "Partner stories", "The work described by the people in it"),
        link("communities.html#involved", "Get involved", "Bring us a question from your community"),
    ]) + feature("Latest", [
        link("projects.html#current", "FRESSCA", "Farmworker resilience to heat and pesticide exposure"),
        stats([("45+", "partner organizations"), ("24", "active &amp; recent projects")]),
    ], ("projects.html", "See what is running now"))

PANEL_PROGRAM = col("Who we are", [
        link("about.html", "About Tracking California", "Our mission and what sets us apart"),
        link("about.html", "Our approach", "How we work, from question to change"),
        link("about.html#team", "Our staff", "The people behind the program"),
        link("about.html#partners", "Our partners", "Community, agency and academic"),
        link("about.html#contact", "Contact us", "Get in touch with the team"),
    ]) + col("Our impact", [
        link("#", "Impact stories", "What changed for communities because of the work"),
        link("#", "Policy &amp; practice outcomes", "Decisions and regulations our data informed"),
        link("resources.html?filter=news", "In the press", "Coverage, announcements and releases"),
    ]) + col("Publications &amp; news", [
        link("resources.html?filter=paper", "Articles &amp; reports", "Peer-reviewed research and technical reports"),
        link("resources.html?filter=news", "Data briefs", "Short summaries for non-technical readers"),
        link("resources.html?filter=newsletter", "Newsletters", "Program highlights, a few times a year"),
        link("resources.html?filter=video", "Videos", "Webinars, partner stories and overviews"),
        link("topics.html", "Health topics", "Asthma, pesticides, water, heat and more"),
    ], ("resources.html", "The full library"))

# accent marks the item that is set apart on the bar
PANELS = [("work",     "Our Work",            PANEL_WORK,     " cols-3eq", False),
          ("data",     "Data &amp; Tools",    PANEL_DATA,     " cols-3eq", True),
          ("projects", "Projects &amp; Partners", PANEL_PROJECTS, " cols-2", False),
          ("program",  "Our Program",         PANEL_PROGRAM,  " cols-3eq", False)]


# Which top-level item each page belongs to, for the active state.
SECTION = {
    "index.html": "home",
    "data-and-tools.html": "data", "data.html": "data", "tools.html": "data",
    "data-explorer.html": "data",
    "projects.html": "projects", "communities.html": "projects",
    "community-story.html": "projects",
    "priority-areas.html": "work", "priority-area.html": "work",
    "work-with-us.html": "work",
    "about.html": "program", "resources.html": "program", "topics.html": "program",
    "topic.html": "program", "resource-article.html": "program",
}
for p in glob.glob(os.path.join(ROOT, "area-*.html")):
    SECTION[os.path.basename(p)] = "work"
for p in glob.glob(os.path.join(ROOT, "news-*.html")):
    SECTION[os.path.basename(p)] = "program"

def header_for(section):
    def cls(key):
        return " active" if section == key else ""
    parts = ['<header class="site-header">',
             '  <div class="wrap header-inner">',
             '    <a class="brand" href="index.html" aria-label="Tracking California home">',
             '      <img class="brand-logo" src="assets/tc-logo.svg" alt="Tracking California">',
             '    </a>',
             '    <button class="nav-toggle" aria-label="Menu">',
             '      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">'
             '<path d="M3 6h18M3 12h18M3 18h18"/></svg>',
             '    </button>',
             '    <nav class="nav mm-nav">']
    for key, label, body, extra, accent in PANELS:
        parts += ['      <div class="mm-item">',
                  '        <button class="mm-trigger%s%s" id="mm-t-%s" aria-expanded="false" '
                  'aria-controls="mm-p-%s">%s <span class="caret">\u25be</span></button>'
                  % (" mm-accent" if accent else "", cls(key), key, key, label),
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
              '      <a class="nav-lang" href="#" lang="es" hreflang="es">Espa&ntilde;ol</a>',
              '    </nav>',
              '  </div>',
              '</header>']
    return "\n".join(parts)

# ------------------------------------------------------------------ apply ---
changed = 0
for path in sorted(glob.glob(os.path.join(ROOT, "*.html"))):
    name = os.path.basename(path)
    s = open(path).read()
    before = s

    s, n = re.subn(r'<header class="site-header">.*?</header>',
                   lambda m: header_for(SECTION.get(name, "")), s, count=1, flags=re.S)
    if not n:
        print("  ! no header found in", name)
        continue

    # the nav's stylesheet and script, once each, right after the base ones
    if "assets/meganav.css" not in s:
        s = s.replace('<link rel="stylesheet" href="assets/styles.css">',
                      '<link rel="stylesheet" href="assets/styles.css">\n'
                      '<link rel="stylesheet" href="assets/meganav.css">', 1)
    if "assets/meganav.js" not in s:
        s = s.replace('<script src="assets/main.js"></script>',
                      '<script src="assets/main.js"></script>\n'
                      '<script src="assets/meganav.js"></script>', 1)

    if s != before:
        open(path, "w").write(s)
        changed += 1

print("navigation applied to %d pages" % changed)
