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

## Mega-menu variants

Three alternative navigations are published alongside the standard prototype so they can be
compared side by side. Same content throughout — the question each one answers differently is
**where public health data sits in the hierarchy**.

| | URL |
|---|---|
| Standard nav | `…github.io/tc-website-redesign/` |
| Variant A — three sections | `…github.io/tc-website-redesign/megamenu/` |
| Variant B — five sections | `…github.io/tc-website-redesign/megamenu-b/` |
| Variant C — data-first | `…github.io/tc-website-redesign/megamenu-c/` |
| **Variant D — post-committee** | `…github.io/tc-website-redesign/megamenu-d/` |

### Variant A — three sections

Restructures five top-level items into three, each opening a full-width panel:

- **Our Work** — Priority areas · Data & Tools · Communities · Projects
- **Our Resources** — Read (news, articles & reports, newsletters) · Browse (videos, health
  topics, full library)
- **Who We Are** — About Us, staff, partners · Work with us · TC in numbers

Same content throughout — nothing is added or removed, only regrouped. The Resources links use
`resources.html?filter=news|paper|newsletter|video` deep links into the existing library filter,
so no pages were split.

### Variant B — five sections, data standing alone

A port of the core-committee mockup (`docs/TC_MegaMenu_revised_4.html`) into TC brand and
content: **Our Work** (focus areas · communities · projects) · **Impacts** · **Data & Tools** ·
**Resources** · **About**. Data & Tools keeps its own top-level slot, third in the order.

### Variant C — data-first hybrid

Folds Data & Tools back *into* Our Work and puts it first, so public health data sits at the same
level as communities and projects rather than below them: **Our Work** (public health data ·
tools · communities · projects, with focus areas as a strip across the foot of the panel) ·
**Impacts** · **Resources** · **About**.

The trade-off between B and C is the open positioning question — *are we a data program that
works with communities, or a community-based program that also makes data?* B says data is a
peer of the work; C says data leads it.

Both B and C are **navigation mockups**: links to pages that do not exist yet (the surveillance
programs EHTP / SCDC, the Impacts section, fee-for-service, funding, Español) go to `#`. They
carry `class="todo"` in the markup as a marker for the build, but no visual treatment.

### Variant D — the consolidation (current proposal)

Built from the core-committee meeting of 2026-09-14, which asked for the three earlier variants to
be reduced to one. Four top-level items, three columns per panel:

**Our Work** · **Data & Tools** · **Projects & Partners** · **Our Program**

The structural move is that *Our Work* stops listing the things we own and starts describing what
we do — **Data & surveillance**, **Research & analysis**, **Capacity building & support** — with
focus areas as a strip across the foot. That is what settles the long-running "are we a data
program that works with communities, or a community program that makes data?" question: data leads
the work without communities being demoted, because the panel is about capability, not property.

Dropped along the way: *Resources* as a word (data and tools are resources too), *Communities* as a
top-level label (it named a virtue, not the work), *Impacts* as a top-level slot (folded into Our
Program), and the standalone *Work with us* page, whose substance is now a capability under Our
Work. Data & Tools is second on the bar and set apart in colour so it is not buried.

Variant D also carries two fixes that the earlier variants do not:

- **Accessible column labels.** TC Orange on white is 1.85:1 — far short of the 4.5:1 WCAG AA needs
  at that size, and the labels were set at 11.8px. They now use `--tc-orange-text` (`#A06403`), the
  same hue and saturation darkened to 4.86:1, at 12.8px. `#FBB036` remains correct for large type
  and non-text accents.
- **Drill-down navigation on phones.** `styles.css` turns `.nav` into a fixed sheet below 1100px but
  never gave it a height or an overflow, so a tall menu ran off the screen and the page behind
  scrolled instead. The sheet now scrolls, and each panel slides in over it with a back button and
  swipe-right to return.

```bash
python3 build_megamenu.py             # regenerate megamenu/            (idempotent)
python3 build_megamenu_variants.py    # regenerate megamenu-b/ and -c/  (idempotent)
python3 build_megamenu_d.py           # regenerate megamenu-d/          (idempotent)
rm -rf megamenu/ megamenu-b/ megamenu-c/ megamenu-d/   # bin them
```

Both scripts work the same way: each root page is copied into the variant folder, the header
block is swapped wholesale, and asset paths are rewritten to `../` so `assets/` (29 MB) and
`pagefind/` are **shared, not duplicated** — each variant adds roughly 560 KB. Styling lives in
`assets/megamenu.css` (all variants) plus `assets/megamenu-variants.css` (B and C) and
`assets/megamenu-d.css` / `assets/megamenu-d.js` (D only), loaded
only by the variant pages, so `styles.css` and `main.js` are untouched and neither the standard
prototype nor the other variants can regress. Edit the panel content in the build script and
rerun.

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
