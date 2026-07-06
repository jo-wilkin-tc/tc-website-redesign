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

- **Data & Communities lead the home page** — the Data & Tools / Our Communities pillars open the page, followed by the Uncover → Translate → Partner → Transform positioning framework.
- **A funder/partner pathway** is its own page (`work-with-us.html`, in the About dropdown): reasons to partner (community partnerships, data know-how, public-health networks, agency & academic record) and what makes a good fit.
- **Nav dropdowns list standalone pages only** — no anchor links into a page. Dropdowns are Data & Tools (→ Our Data, Our Tools), Resources (→ Our Library, Health Topics), and About (→ About Us, Work with us); Communities and Projects are plain links. "Data" leads "Tools" throughout.
- **The Data & Tools landing is the interactive finder**; the tool catalogue lives on its own `tools.html` ("Our Tools").
- **"Our Communities"** is a top-level front door that *surfaces* work currently buried inside project pages — it links out, it doesn't duplicate.
- **Resources has no landing page** — the dropdown goes straight to Our Library (publications/news) or Health Topics.
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
