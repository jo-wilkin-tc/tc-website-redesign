#!/usr/bin/env python3
"""Generate a curated landing page per focus area.

Diane's test scenario at the 2026-09-14 committee meeting: someone wants to
know about pesticide use and what Tracking does about it — where do they land?
Today every focus area links to priority-area.html, which is hard-coded to
Extreme heat, so they land on a page about heat.

This turns that one page into a template driven by a content block per area.
Adding an area is a dict entry here, not a copy of the HTML. priority-area.html
stays as the shell: its header, footer, styles and sidebar are reused verbatim,
so nav changes still flow through the usual sitewide edit.

Only the areas defined in AREAS get a real page; the rest keep pointing at
priority-area.html until someone writes their content.

Run:  python3 build_focus_areas.py      (idempotent — rerun any time)
"""
import os, re, html

ROOT = os.path.dirname(os.path.abspath(__file__))
TEMPLATE = os.path.join(ROOT, "priority-area.html")
SITE = "https://jo-wilkin-tc.github.io/tc-website-redesign"

# Every focus area, in the order the sidebar lists them. "page" is filled in
# below for the ones that have a generated page.
ALL_AREAS = ["Air quality", "Climate resilience", "Extreme heat", "Pesticides",
             "Sickle cell disease", "Water quality"]

# ---------------------------------------------------------------------------
# TO FILL IN: the figures and framing are the only things not already on the
# site. Everything else below links to pages that exist today.
#   - "findings" wants three figures with sources
#   - "intro" wants roughly sixty words of framing
# Placeholders are written as visible markers rather than invented numbers.
# ---------------------------------------------------------------------------
TBC = '<span class="tbc">figure to confirm</span>'

AREAS = {
  "pesticides": {
    "title": "Pesticides",
    "meta": "Pesticides as a Tracking California focus area — mapping agricultural "
            "pesticide use and proximity to homes, schools and pregnant residents.",
    # Image choice is an editorial call, not a build one — there is no
    # pesticide-specific photograph in assets/. This one is a school field,
    # which pairs with the schools project without implying anything about
    # the children in it.
    "hero": "assets/img/ej-kids.jpg",
    "hero_alt": "Children outdoors at a California school",
    "related": [("Pesticides", "topic.html"), ("Air Quality", "topic.html"),
                ("Maternal &amp; Infant Health", "topic.html")],

    # DRAFT framing — to be replaced with the program's own words.
    "intro": [
      "California applies more agricultural pesticide than any other state, and the "
      "people living closest to it are rarely the people deciding how it is used. "
      "Homes, schools and workplaces sit alongside treated fields, and until use is "
      "mapped at the scale people actually live at, proximity is impossible to "
      "discuss with any precision.",
      "We turn the state&rsquo;s pesticide-use reporting into something usable: mapped "
      "to the field, linked to the places that matter, and open to anyone who needs "
      "it. That work underpins research on exposure near schools and during "
      "pregnancy, and it gives community advocates and local agencies the same "
      "evidence base the state has.",
    ],
    "callout":
      "Pesticides show why the data and the partnerships belong together. The "
      "mapping makes exposure legible; the community work establishes which "
      "questions are worth asking; and the research turns both into evidence that "
      "regulators and school districts can act on.",

    "findings": [
      ("Fields mapped", "Agricultural pesticide use mapped at field level across California.", TBC),
      ("Near schools", "Share of public schools within a quarter mile of reported application.", TBC),
      ("Years of data", "Pesticide-use reporting processed into a consistent statewide series.", TBC),
    ],

    "data_text":
      "Field-level agricultural pesticide use, derived from California&rsquo;s "
      "Pesticide Use Reporting system and mapped to the land it was applied to — "
      "plus a linkage service that joins it to study locations, and the open code "
      "behind both.",
    "data_buttons": [
      ("tools.html", "fa-solid fa-map-location-dot", "Pesticide Mapping Tool"),
      ("tools.html", "fa-solid fa-link", "Pesticide Linkage Service"),
      ("data.html", "fa-brands fa-github", "Field-Level Mapping code"),
      ("data-and-tools.html", "fa-solid fa-compass", "Find your data"),
    ],

    # No pesticide-specific partner stories exist on the site yet — which two
    # belong here is a content decision, not a build one.
    "communities": [
      ("communities.html", "assets/img/community-partnership.jpg", "green", "Communities",
       "All our community work", "Where we work, who we work with, and how to bring us a question."),
    ],
    "communities_note":
      "Partner stories for this area are still to be chosen — two would sit here.",

    "projects": [
      ("projects.html", "assets/img/ej-kids.jpg", "", "Current project",
       "Agricultural Pesticides Near Public Schools",
       "Which schools sit closest to reported application, and who attends them."),
      ("resources.html?filter=paper", "assets/img/infographic.png", "orange", "Publication",
       "Temporal trends of organophosphate use",
       "Peer-reviewed analysis of agricultural organophosphate use and proximity across California."),
      ("resources.html?filter=video", "assets/img/data-insight-1.png", "", "Video",
       "Using the Pesticide Mapping Tool",
       "A walkthrough of the tool, from a first question to a mapped answer."),
    ],

    "news": [
      ("news-eu-plans-to-ban-cholorothalonil.html", "EU Plans to Ban Chlorothalonil"),
      ("news-unique-data.html", "Tracking Awareness Week: Unique Data"),
    ],

    "work_text":
      "If you are researching pesticide exposure, planning around application near "
      "schools or housing, or need use data linked to your own study locations, we "
      "can help you find it and build the partnership around it.",
  },
}

# ------------------------------------------------------------------ render ---
def card(href, img, tag_class, tag, title, text):
    t = ' %s' % tag_class if tag_class else ''
    return ('<a class="card" href="%s"><div class="thumb"><img src="%s" alt=""></div>'
            '<div class="pad"><span class="tag%s">%s</span><h3>%s</h3><p>%s</p></div></a>'
            % (href, img, t, tag, title, text))

def sidebar(slug, area):
    rows = []
    for name in ALL_AREAS:
        s = name.lower().replace(" ", "-")
        href = "area-%s.html" % s if s in AREAS else "priority-area.html"
        on = ' class="on"' if s == slug else ''
        rows.append('        <a href="%s"%s>%s</a>' % (href, on, name))
    rel = "\n".join('        <a href="%s">%s</a>' % (h, n) for n, h in area["related"])
    return ('      <aside class="sidenav">\n'
            '        <p class="grouptitle">Focus areas</p>\n%s\n'
            '        <p class="grouptitle">On this page</p>\n'
            '        <a href="#data">Our data &amp; tools</a>\n'
            '        <a href="#communities">In communities</a>\n'
            '        <a href="#projects">Projects &amp; research</a>\n'
            '        <a href="#news">In the news</a>\n'
            '        <p class="grouptitle">Related topics</p>\n%s\n'
            '      </aside>' % ("\n".join(rows), rel))

def main_block(slug, area):
    findings = "\n          ".join(
        '<div class="finding"><div class="fbig">%s</div><h4>%s</h4><p>%s</p></div>'
        % (fig, head, text) for head, text, fig in area["findings"])
    buttons = "\n          ".join(
        '<a class="btn btn-ghost" href="%s"><i class="%s"></i> %s</a>' % b
        for b in area["data_buttons"])
    communities = "\n          ".join(card(*c) for c in area["communities"])
    note = ('\n        <p class="prose tbc-note">%s</p>' % area["communities_note"]
            if area.get("communities_note") else "")
    projects = "\n          ".join(card(*c) for c in area["projects"])
    news = "\n          ".join(
        '<a class="link-arrow" href="%s">%s</a>' % n for n in area["news"])
    intro = "\n          ".join("<p>%s</p>" % p for p in area["intro"])

    return """
  <div class="wrap">

    <p class="breadcrumb"><a href="index.html">Home</a> / <a href="priority-areas.html">Focus areas</a> / %(title)s</p>

    <div class="split">

%(sidebar)s

      <!-- CONTENT -->
      <div>
        <p class="eyebrow">Focus area</p>
        <h2 class="sec-title">%(title)s</h2>

        <img src="%(hero)s" alt="%(hero_alt)s" style="width:100%%; border-radius:10px; margin:0 0 24px;">

        <div class="prose">
          %(intro)s

          <div class="callout">
            <p>%(callout)s</p>
          </div>
        </div>

        <h3 style="margin-top:2.6em;">Why it matters</h3>
        <div class="grid g3">
          %(findings)s
        </div>

        <h3 id="data" style="margin-top:2.6em;">Our data &amp; tools</h3>
        <div class="prose">
          <p>%(data_text)s</p>
        </div>
        <div class="btn-row">
          %(buttons)s
        </div>

        <h3 id="communities" style="margin-top:2.6em;">In communities</h3>
        <div class="grid g3">
          %(communities)s
        </div>%(note)s

        <h3 id="projects" style="margin-top:2.6em;">Projects &amp; research</h3>
        <div class="grid g3">
          %(projects)s
        </div>

        <h3 id="news" style="margin-top:2.6em;">In the news</h3>
        <div class="prose news-list">
          %(news)s
        </div>

        <h3 style="margin-top:2.6em;">Work with us on %(lower)s</h3>
        <div class="prose">
          <p>%(work_text)s</p>
        </div>
        <div class="btn-row">
          <a class="btn btn-primary" href="work-with-us.html">Start a conversation</a>
          <a class="btn btn-ghost" href="priority-areas.html">All focus areas</a>
        </div>

      </div>

    </div>
  </div>
""" % dict(title=area["title"], lower=area["title"].lower(), sidebar=sidebar(slug, area),
           hero=area["hero"], hero_alt=area["hero_alt"], intro=intro,
           callout=area["callout"], findings=findings, data_text=area["data_text"],
           buttons=buttons, communities=communities, note=note, projects=projects,
           news=news, work_text=area["work_text"])

# ------------------------------------------------------------------- build ---
shell = open(TEMPLATE).read()
head, rest = shell.split("<main id=\"main\" data-pagefind-body>", 1)
_, tail = rest.split("</main>", 1)

for slug, area in AREAS.items():
    out = "area-%s.html" % slug
    title = "%s — Tracking California" % area["title"]
    s = head
    s = re.sub(r"<title>.*?</title>", "<title>%s</title>" % title, s, count=1, flags=re.S)
    s = re.sub(r'(<meta name="description" content=")[^"]*(")',
               lambda m: m.group(1) + area["meta"] + m.group(2), s, count=1)
    s = re.sub(r'(<meta property="og:title" content=")[^"]*(")',
               lambda m: m.group(1) + html.escape(title) + m.group(2), s, count=1)
    s = re.sub(r'(<meta property="og:description" content=")[^"]*(")',
               lambda m: m.group(1) + area["meta"] + m.group(2), s, count=1)
    s = re.sub(r'(<meta property="og:url" content=")[^"]*(")',
               lambda m: m.group(1) + "%s/%s" % (SITE, out) + m.group(2), s, count=1)
    s += '<main id="main" data-pagefind-body>' + main_block(slug, area) + "</main>" + tail
    open(os.path.join(ROOT, out), "w").write(s)
    print("built %s" % out)

print("%d of %d focus areas have a page; the rest still use priority-area.html"
      % (len(AREAS), len(ALL_AREAS)))
