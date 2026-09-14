# Tracking California — website redesign prototype

A **static, hi-fidelity design prototype** for the new trackingcalifornia.org. This is a
direction to react to — not the production build. It exists to make the redesign concrete:
real TC brand, real layout, clickable navigation.

> ⚠️ **This is not the live site.** Content is illustrative placeholder copy. The live site
> remains at <https://trackingcalifornia.org>.

## What's here

Plain HTML + CSS (no framework, no build step) so it publishes instantly to GitHub Pages and
is easy for anyone to open, read, and tweak.

| Page | File | Purpose |
|------|------|---------|
| Home | `index.html` | Hero + Data & Tools / Our Communities pillars, latest work, Uncover → Translate → Partner → Transform framework, priority areas, community-partner map, publications |
| Our priority areas | `priority-areas.html` | The six areas of concentrated effort, and how they relate to Health Topics |
| ↳ Priority area | `priority-area.html` | Per-area template (Extreme heat) pulling data + communities + projects together |
| Our Data & Tools | `data-and-tools.html` | Landing = the "find the data or tool for you" finder, then links out to Our Data / Our Tools |
| ↳ Our Data | `data.html` | The data page |
| ↳ Our Tools | `tools.html` | Data Explorer embed, other/future tool cards, custom-tool CTA |
| ↳ Data explorer | `data-explorer.html` | Single-tool "inner page" template |
| Our Communities | `communities.html` | Front door surfacing community work |
| ↳ Community story | `community-story.html` | Single-story "inner page" template |
| Our Projects | `projects.html` | Current and previous projects |
| Our Library | `resources.html` | Filterable publications/newsletters/videos/news library (Resources dropdown, no landing) |
| Health Topics | `topics.html` | Browsable index of all health topics (Resources dropdown) |
| ↳ Topic | `topic.html` | Deep-content template (sidebar layout) |
| ↳ Article | `resource-article.html` | Single article/commentary read view |
| About Us | `about.html` | Who we are: mission (+ "what sets us apart" callout), stats, staff, Our Partners, contact |
| Work with us | `work-with-us.html` | Funder/partner pathway (in the About dropdown): why partner, what makes a good fit, get in touch |

Shared assets in `assets/`: `styles.css` (the design system), `main.js` (mobile nav +
resources filter), the TC logo/symbol, and the hero image.

## Design decisions baked in

- **Priority areas are a lens across the work, not a sibling of it** — the six areas each pull together data, community partnerships and projects, so they lead the Our Work mega-menu panel rather than taking a fourth top-level slot. They are distinct from the 22 Health Topics under Resources: priority areas are where staff and funding concentrate, health topics are everything we publish data on.
- **Data & Communities lead the home page** — the Data & Tools / Our Communities pillars open the page, followed by the Uncover → Translate → Partner → Transform positioning framework.
- **A funder/partner pathway** is its own page (`work-with-us.html`, in the About dropdown): reasons to partner (community partnerships, data know-how, public-health networks, agency & academic record) and what makes a good fit.
- **Nav dropdowns list standalone pages only** — no anchor links into a page. Dropdowns are Data & Tools (→ Our Data, Our Tools), Resources (→ Our Library, Health Topics), and About (→ About Us, Work with us); Communities and Projects are plain links. "Data" leads "Tools" throughout.
- **The Data & Tools landing is the interactive finder**; the tool catalogue lives on its own `tools.html` ("Our Tools").
- **"Our Communities"** is a top-level front door that *surfaces* work currently buried inside project pages — it links out, it doesn't duplicate.
- **Resources has no landing page** — the dropdown goes straight to Our Library (publications/news) or Health Topics.
- TC brand palette, Open Sans, US spellings, clean and text-forward.

## Navigation — the mega menu

The site navigation is a full-width mega menu with four top-level items:

**Our Work** · **Data & Tools** · **Projects & Partners** · **Our Program**

The structural idea is that *Our Work* describes what we do rather than listing what we own —
**Data & surveillance**, **Research & analysis**, **Capacity building & support** — with focus
areas as a strip across the foot of the panel. That is what settles the long-running "are we a
data program that works with communities, or a community program that makes data?" question:
data leads the work without communities being demoted, because the panel is about capability,
not property.

Deliberately absent: *Resources* as a word (data and tools are resources too), *Communities* as a
top-level label (it named a virtue, not the work), *Impacts* as a top-level slot (folded into Our
Program), and a standalone *Work with us* page, whose substance is a capability under Our Work.
Data & Tools sits second and is set apart in colour so it is not buried.

Two details worth knowing:

- **Column labels use `--tc-orange-text` (`#A06403`), not TC Orange.** `#FBB036` on white is
  1.85:1 — far short of the 4.5:1 WCAG AA needs at label size. `#A06403` is the same hue and
  saturation darkened to 4.86:1. `#FBB036` remains correct for large type and non-text accents.
  Note the same problem still applies to the site's orange `.eyebrow` labels, which have not been
  changed — that is a brand decision, not a build one.
- **Phones drill in rather than scroll.** `styles.css` turns `.nav` into a fixed sheet below
  1100px but never gave it a height or an overflow, so a tall menu ran off the screen and the page
  behind scrolled. The sheet now scrolls, and each panel slides in over it with a back button and
  swipe-right to return.

### Changing the nav

The repo has no templating — the header is duplicated verbatim into every page — so the nav is
applied by a script. Edit the panel definitions at the top of `build_nav.py` and rerun it:

```bash
python3 build_nav.py          # apply the nav to every root page (idempotent)
python3 build_focus_areas.py  # regenerate the focus-area landing pages
```

**Order matters.** `build_nav.py` rewrites `resources.html`, which `build_content.py` and
`build_projects.py` take their page chrome from — so it must run *before* them, never after, or a
content rebuild reverts the nav.

Styling lives in `assets/meganav.css` and behaviour in `assets/meganav.js`, both loaded by every
page alongside `styles.css` and `main.js`.

### History

The menu was chosen by trialling four variants side by side (A: three sections; B: a port of the
committee's own mockup; C: a data-first hybrid; D: the consolidation). The core committee adopted
D on 2026-09-14, and the variants were retired once it was promoted to the main site. They are in
git history if the comparison is ever needed again — see the commits around `feature/megamenu-d`.

## Viewing locally

Just open `index.html` in a browser, or serve the folder:

```bash
python3 -m http.server 8000   # then visit http://localhost:8000
```

## How this feeds the real rebuild

This prototype is the **visual spec** for the production rebuild (Next.js or Astro + TinaCMS,
git-backed content). The HTML/CSS here translates directly into components; the content model
already exists as structured JSON in the current site.

---
*Design prototype · TC brand · for internal review.*
