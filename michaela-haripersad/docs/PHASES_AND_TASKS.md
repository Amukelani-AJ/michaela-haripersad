<!-- Written by Kone Tshivhinda (Claude Sonnet 5.5) on 2026-10-15 - Roadmap, phase cards and file ownership. -->
<!-- Written by Kone Tshivhinda (Claude Sonnet 5.5) on 2026-10-15 - P4: P1 marked complete, P4 started, gallery ownership passes to P4. -->

# Phases and tasks

Work is split into numbered phases. Each phase owns a set of files so that parallel work does not collide. One phase per pull request.

## Tier 1: Foundation (sequential)

## P0: Repository and governance baseline

**Status**: ✅ Complete: Kone Tshivhinda (Claude Sonnet 5.5) | 2026-10-15
**Depends On**: none
**Blocks**: P1
**Complexity**: Low
**File Ownership**: `INSTRUCTIONS.md`, `WORKLOG.md`, `.gitignore`, `docs/BRANCHING_STRATEGY.md`, `docs/AI_COMMUNICATION.md`
**Exclusion Zone**: `site/` (belongs to P1 and later)

### Tasks

| # | Task | Description |
|---|------|-------------|
| 0.1 | Create repository | Public repository under the owner's personal account, `main` as the only long-lived branch |
| 0.2 | Governance documents | Contract, worklog, branching policy and communication ledger |
| 0.3 | Branch protection | Pull requests required, no force-push, no deletion, merge commits only, delete branch on merge |

## P1: Portfolio site v1

**Status**: ✅ Complete: Kone Tshivhinda (Claude Sonnet 5.5) | 2026-10-15 (merged in pull request #1; the site is live on GitHub Pages)
**Depends On**: P0
**Blocks**: P2, P3, P4
**Complexity**: Medium
**File Ownership**: `site/**`, `scripts/optimize-images.py`, `scripts/make-icons.py`, `scripts/make-og-image.py`, `scripts/og-image/**`, `scripts/validate-compliance.py`, `.github/workflows/**`, `docs/ARCHITECTURE.md`, `docs/PHASES_AND_TASKS.md`, `README.md`
**Exclusion Zone**: `INSTRUCTIONS.md` (change only through a separate `chore/` or `docs/` pull request)

### Tasks

| # | Task | Description |
|---|------|-------------|
| 1.1 | Content model | Autobiography, experience, skills, credentials, interests and roles drawn from the CV and the autobiography |
| 1.2 | Design system | Tokens, three section themes, responsive layout, reduced-motion, forced-colours and print styles |
| 1.3 | Sections | Hero, story, "two stages", experience timeline, skills, credentials, gallery with lightbox, interests, contact |
| 1.4 | Image pipeline | WebP at several widths, metadata stripped, placeholder colours, alt text for every photo |
| 1.5 | Web CV | Downloadable CV without phone, date of birth, gender, licence details or referees |
| 1.6 | Identity assets | Monogram favicon set, 1200 x 630 share image, 404 page, robots.txt, sitemap.xml |
| 1.7 | Quality gates | axe-core audit, pixel-sampled contrast check, keyboard and no-JavaScript tests, privacy scan |
| 1.8 | Delivery | Validator script, PR checks workflow, Pages deploy workflow |

## Tier 2: Content and reach (parallel, after P1)

## P2: Music and social links

**Status**: ⏳ Not started
**Depends On**: P1
**Blocks**: none
**Complexity**: Low
**File Ownership**: `site/index.html` (contact section, a new "Listen" section if wanted), `site/assets/css/styles.css` (only for that section)
**Exclusion Zone**: experience and credentials sections (P4)

### Tasks

| # | Task | Description |
|---|------|-------------|
| 2.1 | Collect links | Streaming profile, video clips, Instagram, TikTok, YouTube, LinkedIn: whichever Michaela wants public |
| 2.2 | Add links | Icon buttons in the contact section, plus `sameAs` in the JSON-LD block |
| 2.3 | Optional "Listen" section | Embed policy: prefer plain links over third-party embeds (privacy); record any embed decision under Section 4.1 |

## P3: Reach and polish

**Status**: ⏳ Not started
**Depends On**: P1
**Blocks**: none
**Complexity**: Low
**File Ownership**: `site/robots.txt`, `site/sitemap.xml`, `site/404.html`, `site/assets/img/og-image.jpg`, `scripts/og-image/**`
**Exclusion Zone**: page content

### Tasks

| # | Task | Description |
|---|------|-------------|
| 3.1 | Custom domain (optional) | Follow "When you change the domain" in `docs/ARCHITECTURE.md` |
| 3.2 | Search presence | Verify the site in Google Search Console and Bing Webmaster Tools (no tracking code needed) |
| 3.3 | Share image refresh | Re-render the share image when the headline, roles or main photo change |

## P4: Content upkeep

**Status**: 🚀 In Progress | Kone Tshivhinda (Claude Sonnet 5.5) | Started: 2026-10-15 (photo refresh done; open items are tracked in the ledger)
**Depends On**: P1
**Blocks**: none
**Complexity**: Low
**File Ownership**: `site/index.html` (story, experience, skills, credentials, gallery, interests), `site/assets/css/styles.css` (only the gallery and credential-photo rules), `scripts/optimize-images.py`, `site/assets/docs/Michaela_Haripersad_CV.pdf`, `site/assets/img/**`
**Exclusion Zone**: contact section (P2)

### Tasks

| # | Task | Description |
|---|------|-------------|
| 4.1 | Keep facts current | Update experience, certificates and the age mentioned in the autobiography when they change |
| 4.2 | Refresh the CV download | Replace the PDF whenever the CV changes (keep the web edition free of private details) |
| 4.3 | New photos | Run `scripts/optimize-images.py`, add the tiles and `alt` text. Done on 2026-10-15 for the second batch: three new gallery photos, a graduation thumbnail in Credentials, two look-alike photos retired |
| 4.4 | Graduation year | Waiting for Michaela: the graduation photo shows a certificate dated 2025 while the Higher Certificate is listed as 2023 (see MSG-009 in `docs/AI_COMMUNICATION.md`) |
| 4.5 | Television appearance line | Waiting for Michaela: year, her role and wording; do not name the programme or channel until she confirms (see MSG-010) |

## File Ownership Master Index

| Path | Owning phase |
|------|--------------|
| `INSTRUCTIONS.md`, `WORKLOG.md`, `.gitignore`, `docs/BRANCHING_STRATEGY.md`, `docs/AI_COMMUNICATION.md` | P0 (shared files are append-only where noted below) |
| `site/index.html`: structure, hero, story, sides | P1 |
| `site/index.html`: gallery | P1, then P4 |
| `site/index.html`: contact section | P2 |
| `site/index.html`: experience, skills, credentials, interests | P4 |
| `site/assets/css/styles.css`, `site/assets/js/main.js` | P1 (P2 and P4 may add rules for their own sections; P4 owns the gallery and credential-photo rules) |
| `site/assets/img/**`, `site/assets/docs/**` | P1, then P4 |
| `site/404.html`, `site/robots.txt`, `site/sitemap.xml`, `site/favicon*`, `site/apple-touch-icon.png` | P1, then P3 |
| `scripts/optimize-images.py` | P1, then P4 |
| other `scripts/**`, `.github/workflows/**` | P1 |
| `docs/ARCHITECTURE.md`, `docs/PHASES_AND_TASKS.md`, `README.md` | P1, then whichever phase changes the behaviour described |

## Conflict prevention rules

1. **One phase, one territory.** Touch only the files your phase owns. If you need a change elsewhere, leave a message in `docs/AI_COMMUNICATION.md`.
2. **Shared files are append-only.** `WORKLOG.md` and `docs/AI_COMMUNICATION.md` only grow downwards; earlier rows are never edited or deleted (except to update a message's status).
3. **One phase per pull request.** Never combine phases.
4. **Section isolation.** Keep edits inside the HTML section the phase owns, and add new CSS rules in a clearly commented block for that section.
5. **Mock rather than reach.** If a phase needs something an unfinished phase will provide, add a clearly marked placeholder and record it in the ledger instead of building the other phase's feature.
