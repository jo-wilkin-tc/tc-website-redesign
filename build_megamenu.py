#!/usr/bin/env python3
"""Generate the mega-menu trial site into megamenu/.

Copies every root *.html into megamenu/, swaps the standard header for a
full-width mega menu, and rewrites asset paths to ../ so the 29MB assets/
and pagefind/ folders are SHARED rather than duplicated.

The root prototype is never touched: megamenu/ pages load styles.css plus
assets/megamenu.css, and main.js plus assets/megamenu.js.

Run:  python3 build_megamenu.py        (idempotent — rerun any time)
Bin:  rm -rf megamenu/
"""
import os, re, glob, shutil

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT  = os.path.join(ROOT, "megamenu")

# Which top-level mega-menu item each page belongs to, for the active state.
SECTION = {
    "index.html": "home",
    "data-and-tools.html": "work", "data.html": "work", "tools.html": "work",
    "data-explorer.html": "work", "communities.html": "work",
    "community-story.html": "work", "projects.html": "work",
    "resources.html": "resources", "topics.html": "resources",
    "topic.html": "resources", "resource-article.html": "resources",
    "about.html": "who", "work-with-us.html": "who",
}
for p in glob.glob(os.path.join(ROOT, "news-*.html")):
    SECTION[os.path.basename(p)] = "resources"

def link(href, label, desc=None):
    d = '<span class="mm-desc">%s</span>' % desc if desc else ""
    return '<a class="mm-link" href="%s">%s%s</a>' % (href, label, d)

def col(title, links):
    return ('        <div class="mm-col">\n          <p class="mm-title">%s</p>\n'
            '          %s\n        </div>\n' % (title, "\n          ".join(links)))

def feature(img, title, text, href, cta):
    return ('        <div class="mm-col mm-feature">\n'
            '          <p class="mm-title">Featured</p>\n'
            '          <a href="%s"><img src="%s" alt="" loading="lazy">'
            '<span class="mm-feature-title">%s</span></a>\n'
            '          <p>%s</p>\n'
            '          <a class="link-arrow" href="%s">%s</a>\n'
            '        </div>\n' % (href, img, title, text, href, cta))

# ---------------------------------------------------------------- panels ----
PANEL_WORK = col("Data &amp; Tools", [
        link("data-and-tools.html", "Find your data", "Answer two questions, get the right dataset or tool"),
        link("data.html", "Our Data", "What we collect, and how to get at it"),
        link("tools.html", "Our Tools", "Explorers, maps and viewers"),
        link("data-explorer.html", "Data Explorer", "Air quality, asthma and more, mapped"),
    ]) + col("Communities", [
        link("communities.html", "Our Communities", "Where we work and who we work with"),
        link("community-story.html", "Community stories", "Partnerships in their own words"),
        link("communities.html#involved", "Get involved", "Bring us a question from your community"),
    ]) + col("Projects", [
        link("projects.html#current", "Current projects", "What we have running right now"),
        link("projects.html#previous", "Previous projects", "Completed work and what came of it"),
        link("projects.html", "All projects", "The full portfolio"),
    ]) + feature("../assets/tools/data-explorer.png", "Explore California health data",
        "Map annual PM2.5, ozone and asthma rates down to the census tract.",
        "data-explorer.html", "Open the Data Explorer")

PANEL_RESOURCES = col("Read", [
        link("resources.html?filter=news", "News &amp; press releases", "Announcements and data briefs"),
        link("resources.html?filter=paper", "Articles &amp; reports", "Peer-reviewed publications"),
        link("resources.html?filter=newsletter", "Newsletters", "Project highlights, straight to your inbox"),
    ]) + col("Browse", [
        link("resources.html?filter=video", "Videos", "Webinars and community-made films"),
        link("topics.html", "Health Topics", "Asthma, pesticides, water, heat and more"),
        link("resources.html", "The full library", "Everything, filterable"),
    ]) + feature("../assets/img/infographic.png", "Our latest publications",
        "Peer-reviewed research on pesticides, PFAS, air quality and sickle cell disease.",
        "resources.html?filter=paper", "See all publications")

PANEL_WHO = ('        <div class="mm-col">\n          <p class="mm-title">Who we are</p>\n          '
    + "\n          ".join([
        link("about.html", "About Us", "Our mission and what sets us apart"),
        link("about.html#team", "Our staff", "The people behind the program"),
        link("about.html#partners", "Our partners", "Community, agency and academic"),
    ]) + '\n        </div>\n') + col("Work with us", [
        link("work-with-us.html", "Why partner with us", "Community reach, data know-how, a 20-year record"),
        link("work-with-us.html#contact", "Start a conversation", "Tell us what you are trying to find out"),
        link("about.html#contact", "Contact", "Get in touch with the team"),
    ]) + ('        <div class="mm-col mm-feature">\n'
          '          <p class="mm-title">Tracking California in numbers</p>\n'
          '          <div class="mm-stats">\n'
          '            <div><span class="n">20+</span><span class="l">Years active</span></div>\n'
          '            <div><span class="n">45</span><span class="l">Community partners</span></div>\n'
          '            <div><span class="n">120+</span><span class="l">Publications</span></div>\n'
          '          </div>\n'
          '          <a class="link-arrow" href="about.html">More about us</a>\n'
          '        </div>\n')

PANELS = [("work", "Our Work", PANEL_WORK, ""),
          ("resources", "Our Resources", PANEL_RESOURCES, " cols-2"),
          ("who", "Who We Are", PANEL_WHO, " cols-2")]

# The root prototype already carries an orange "Design prototype" ribbon; rather
# than stack a second bar, the trial notice replaces its text in place.
TRIAL_RIBBON = ('<div class="proto-ribbon"><strong>Mega-menu trial</strong> — a navigation '
  'experiment, same content restructured into three sections. '
  '<a href="../index.html">View the standard version →</a></div>')

def header_for(section):
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
             '    <nav class="nav mm-nav">',
             '      <a href="index.html" class="mm-top%s">Home</a>' % cls("home")]
    for key, label, body, extra in PANELS:
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
              '    </nav>',
              '  </div>',
              '</header>']
    return "\n".join(parts)

# ------------------------------------------------------------------ build ---
if os.path.isdir(OUT):
    shutil.rmtree(OUT)
os.makedirs(OUT)

pages = sorted(os.path.basename(p) for p in glob.glob(os.path.join(ROOT, "*.html")))
for name in pages:
    s = open(os.path.join(ROOT, name)).read()

    # share the root assets/ and pagefind/ rather than copying 29MB
    s = re.sub(r'(?<=["\'(])(assets|pagefind)/', r'../\1/', s)

    # swap the whole header block wholesale (never line-level — see CLAUDE.md)
    s, n = re.subn(r'<header class="site-header">.*?</header>',
                   lambda m: header_for(SECTION.get(name, "")), s, count=1, flags=re.S)
    if not n:
        print("  ! no header found in", name)

    # reuse the existing prototype ribbon slot for the trial notice
    s = re.sub(r'<div class="proto-ribbon">.*?</div>', lambda m: TRIAL_RIBBON, s, count=1, flags=re.S)

    # layer the trial CSS/JS on top of the shared ones
    s = s.replace('<link rel="stylesheet" href="../assets/styles.css">',
                  '<link rel="stylesheet" href="../assets/styles.css">\n'
                  '<link rel="stylesheet" href="../assets/megamenu.css">', 1)
    s = s.replace('<script src="../assets/main.js"></script>',
                  '<script src="../assets/main.js"></script>\n'
                  '<script src="../assets/megamenu.js"></script>', 1)

    open(os.path.join(OUT, name), "w").write(s)

print("mega-menu trial built: %d pages -> megamenu/" % len(pages))
