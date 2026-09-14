# Website redesign — working to-do

Last updated 14 Sep 2026. Two fixed points ahead:
**staff retreat ~30 Sep 2026** and **external user testing by ~15 Oct 2026**.

Key: **[JW]** Joanna · **[TC]** team/committee decision · **[BUILD]** code work

---

## Where things stand

The navigation is **settled and live**. The core committee adopted the mega menu
on 14 Sep; it was promoted to the main URL the same day and the four trial
variants were retired.

**Our Work** · **Data & Tools** · **Projects & Partners** · **Our Program**

<https://jo-wilkin-tc.github.io/tc-website-redesign/>

To change it: edit the panel definitions at the top of `build_nav.py` and rerun.
**`build_nav.py` must run BEFORE `build_content.py` / `build_projects.py`** — it
rewrites `resources.html`, which those two take their page chrome from, so
running it after silently reverts the nav.

---

## 1. Retreat kit — due before 30 Sep  ⬅ the only dated work

- [ ] **[BUILD]** Card-sort stimulus: the four column headers *only*, no links
      beneath them — Michelle's exercise ("what would you expect to find here?
      where would your stuff be?"). Must work **on paper**; she explicitly wants
      to avoid people needing a laptop.
- [ ] **[BUILD]** Scenario cards — a funder, a local health department, a
      community partner, a researcher after a dataset, a staff member looking
      for their own project.
- [ ] **[BUILD]** Printable one-page handout of the nav structure.
- [ ] **[JW]** Agree the session shape with Diane — she is pitching it to Susan
      as the day-two impacts slot; Shubhayu wants it earlier in day two.
- [ ] **[TC]** Decide what "community" means — community / community-engaged /
      community-based. Still blocks the final name of "Projects & Partners".

## 2. The nav is ahead of the content

Fourteen nav links point at `#`. This is the gap the content build has to fill,
and it is the main risk for external testing — people click, and nothing happens.

- [ ] **[TC]** **Our Work** — Statewide tracking · Sickle Cell Data Collection ·
      Health & environment indicators · Primary data collection ·
      Community-based research · Epidemiology · Spatial analysis & mapping ·
      Data linkage · Training & instruction
- [ ] **[TC]** **Data & Tools** — Code & repositories · Data insights
- [ ] **[TC]** **Our Program** — Impact stories · Policy & practice outcomes.
      Michelle doubts there is enough here to justify the section; decide before
      building it.
- [ ] **[TC]** **Español** — the toggle exists but points at `#`. There is no
      Spanish content in the prototype at all. For a program working with
      farmworker and Spanish-speaking communities this is a real gap, not a nav
      detail. Check what the live site does today: the library already has a
      tool tutorial marked "[English]".

## 3. Focus-area landing pages

`build_focus_areas.py` generates a curated page per area from one content block.
Only **pesticides** exists (`area-pesticides.html`); the other five still fall
back to `priority-area.html`, which is hard-coded to Extreme heat.

- [ ] **[JW]** Finish the pesticides page — three "why it matters" figures with
      sources (currently visible **FIGURE TO CONFIRM** chips, not invented
      numbers), the framing paragraphs (a draft is in the script, written to be
      replaced), which two partner stories belong under "In communities", and
      whether the hero image is right (there is no pesticide photograph in
      `assets/`, so it borrows the school-field one).
- [ ] **[BUILD]** Port Extreme heat into the script — the cheap next one, its
      content is already written in `priority-area.html`.
- [ ] **[TC]** Confirm the seven focus areas are final. "Health services" is new
      and has nothing behind it — its nav pill currently goes to `#`.

## 4. Accessibility

- [x] **[BUILD]** Mega-menu column labels now use `--tc-orange-text` `#A06403`
      (4.86:1) at 12.8px. TC Orange on white was 1.85:1 and failed WCAG AA.
- [x] **[BUILD]** Phone drill-down and the nav-sheet scroll fix, sitewide.
- [x] **[BUILD]** Horizontal overflow / off-screen hamburger below 385px.
- [ ] **[TC]** **Brand-wide colour problem.** The same orange is used for
      `.eyebrow` labels across the whole site, with the same failure. **TC Green
      `#8CA083` is 2.81:1 and fails too.** Changing a brand colour is a
      committee call, not a build one — worth putting to them.
- [ ] **[BUILD]** Keyboard and screen-reader pass over the mega menu before
      external testing.

## 5. Later — after the content settles

- [ ] **Content build.** Diane's note: the biggest piece of work, and it could
      not start until the nav was agreed. It is agreed now.
- [ ] **Design directions** — colourways, type, layout — for the retreat. The
      next committee meeting is just before the retreat and is meant to cover
      design.
- [ ] Pre-existing broken links inherited from the live CMS: absolute paths like
      `/topics/pfas/`, `/projects/imperial-air`, `/about/advisory-group`.
