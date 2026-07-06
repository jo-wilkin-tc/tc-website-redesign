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
| Home | `index.html` | Hero + Data & Tools / Our Communities pillars, Uncover → Translate → Partner → Transform framework, priority areas |
| Our Data & Tools | `data-and-tools.html` | Landing for data explorers & tools |
| ↳ Data explorer | `data-explorer.html` | Single-tool "inner page" template |
| Our Communities | `communities.html` | Front door surfacing community work |
| ↳ Community story | `community-story.html` | Single-story "inner page" template |
| Topics | `topics.html` | Browsable index of all topics |
| ↳ Topic | `topic.html` | Deep-content template (sidebar layout) |
| Resources | `resources.html` | Unified, filterable library (newsletters, commentaries, papers, reports, fact sheets) |
| ↳ Article | `resource-article.html` | Single article/commentary read view |
| About | `about.html` | Mission, "Work with us" partner pathway, team, partners, contact |

Shared assets in `assets/`: `styles.css` (the design system), `main.js` (mobile nav +
resources filter), the TC logo/symbol, and the hero image.

## Design decisions baked in

- **Data & Communities lead the home page** — the Data & Tools / Our Communities pillars open the page, followed by the Uncover → Translate → Partner → Transform positioning framework.
- **A funder/partner pathway** lives on the About page (`about.html#partner`): distinctive value prop (technical expertise + community trust), reasons to partner (community partnerships, data know-how, public-health networks, agency & academic record), and what makes a good fit.
- **"Our Communities"** is a top-level front door that *surfaces* work currently buried inside project pages — it links out, it doesn't duplicate.
- **Resources** is one modern, filterable hub rather than separate Newsletters / Publications silos.
- TC brand palette, Open Sans, US spellings, clean and text-forward.

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
