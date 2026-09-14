# Website redesign — working to-do

Live list for the navigation phase. Dates anchor to the two fixed points:
**staff retreat ~30 Sep 2026** and **external user testing by ~15 Oct 2026**.

Key: **[JW]** Joanna · **[TC]** team/committee decision · **[BUILD]** code work

---

## 1. Retreat kit — due before 30 Sep  ⬅ the hard deadline

- [ ] **[BUILD]** Card-sort stimulus: the four column headers *only*, no links
      beneath them — Michelle's exercise ("what would you expect to find here?
      where would your stuff be?"). Needs to work **on paper**, since she
      explicitly wants to avoid people needing a laptop.
- [ ] **[BUILD]** Scenario cards — walk-throughs for: a funder, a local health
      department, a community partner, a researcher after a dataset, a staff
      member looking for their own project.
- [ ] **[BUILD]** Printable one-page handout of Variant D's structure.
- [ ] **[JW]** Agree the session shape with Diane (she is pitching it to Susan
      as the day-two impacts slot; Shubhayu wants it moved earlier in day two).
- [ ] **[TC]** Decide what "community" means — community / community-engaged /
      community-based. Blocks the final name of the third nav item.

## 2. Pesticides landing page — proves the focus-area model

Diane's scenario: *someone wants to know about pesticide use and what Tracking
does about it — where do they land?* Today every focus area links to the same
generic `priority-area.html`, which is hard-coded to Extreme heat.

- [x] **[BUILD]** Generalize `priority-area.html` into per-area pages driven by
      one content block per area (`build_focus_areas.py`), so adding an area is a
      data edit. Variant build scripts now link Pesticides to the real page.
- [x] **[BUILD]** Wire the pesticides page from content that already exists:
      - Tools — Pesticide Mapping Tool · Pesticide Linkage Service ·
        New Pesticide Mapping Tool (forthcoming)
      - Data & code — Pesticide Field-Level Mapping
      - Project — Agricultural Pesticides Near Public Schools
      - Library — "Temporal trends of agricultural organophosphate pesticide
        use in California" · Pesticide Mapping Tool video tutorial
      - News — EU Plans to Ban Chlorothalonil · Tracking Awareness Week 2020
      - Topic page — Pesticides
- [ ] **[JW]** Supply the things that are not on the site and cannot be invented
      — `area-pesticides.html` is built and linked, with these marked in place:
      - three "why it matters" figures, with sources — currently rendered as
        conspicuous **FIGURE TO CONFIRM** chips rather than invented numbers
      - the framing paragraphs — a draft is in `build_focus_areas.py`, written
        to be replaced with the program's own words
      - which two partner stories belong under "In communities" (none of the
        existing stories are pesticide-specific)
      - whether the hero image is right: there is no pesticide photograph in
        `assets/`, so it currently uses the school-field image
- [ ] **[BUILD]** The other five focus areas still point at `priority-area.html`
      (hard-coded to Extreme heat). Each needs a block in `build_focus_areas.py`
      once its content exists — porting Extreme heat over is the easy first one.
- [ ] **[TC]** Confirm the seven focus areas are final — "Health services" is
      new in the committee mockup and has nothing behind it.

## 3. Navigation follow-ups

- [ ] **[TC]** Library placement: four top-level items puts the full library
      under Our Program. Fallback is five items with Publications & News
      standing alone. Michelle said either works.
- [ ] **[TC]** Is the Impacts content worth building? Michelle doubts awards &
      recognition would have more than two entries.
- [ ] **[TC]** How to categorize projects — Michelle has not settled a scheme,
      so it is deliberately not in the nav yet.
- [ ] **[BUILD]** Retire variants A/B/C once D is agreed, or keep them behind a
      comparison link. Three live variants will confuse external testers.

## 4. Accessibility — partly done

- [x] **[BUILD]** Mega-menu column labels: TC Orange on white is 1.85:1 and
      fails WCAG AA. Variant D uses `--tc-orange-text` `#A06403` (4.86:1) at
      12.8px. *(done — variant D only)*
- [ ] **[TC]** Brand-wide: the same orange is used for `.eyebrow` labels across
      the whole site, with the same failure. **TC Green `#8CA083` is 2.81:1 and
      fails too.** Changing a brand colour is a committee call, not a build one.
- [ ] **[BUILD]** Keyboard and screen-reader pass over the mega menu before
      external testing.
- [ ] **[BUILD]** Apply the phone drill-down and the nav-sheet scroll fix to
      whichever variant survives — it currently lives in `megamenu-d.css` only.

## 5. Known issues

- [x] Horizontal overflow and off-screen hamburger below 385px. *(fixed)*
- [ ] **[BUILD]** `priority-area.html` is one page serving six areas — every
      focus-area link in every variant goes to the Extreme heat page.
- [ ] **[BUILD]** Variant A still shows a "Home" item; B, C and D do not. Pick
      one convention before testing.

## Later — after the navigation settles

- [ ] Content build. Diane's note: this is the biggest piece of work, and it
      cannot start until the nav is agreed.
- [ ] Design directions — colourways, type, layout — for the retreat. Next
      committee meeting is just before the retreat and is meant to cover design.
