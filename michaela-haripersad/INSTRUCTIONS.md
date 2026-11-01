<!-- Written by Kone Tshivhinda (Claude Sonnet 5.5) on 2026-10-15 - Master compliance contract for this repository. -->

# INSTRUCTIONS: read this before you change anything

This file is the contract for every person and every AI assistant who works in this repository. Read it in full at the start of each session. If anything here conflicts with a request, stop and ask the repository owner.

## 1. What this repository is

The public portfolio website of Michaela Haripersad: a static site (plain HTML, CSS and JavaScript, no build step) in `site/`, published with GitHub Pages. **The repository and the site are public, so everything committed here is public.**

The framework here is deliberately lighter than a full application: one protected branch, two workflows, a handful of documents. Keep it that way unless the project grows.

## 2. Reading order

1. This file.
2. `docs/PHASES_AND_TASKS.md` (what is in flight and which files each phase owns).
3. `docs/ARCHITECTURE.md` (how the site is built and why).
4. `docs/AI_COMMUNICATION.md` (open messages between engineers and assistants).
5. The latest rows of `WORKLOG.md`.

## 3. Identity protocol

At the start of a session, ask the human engineer for their **name** and which **AI model** is being used. Then create or update `docs/engineers/<name>.md` with the role, the onboarding date, the preferred branch prefix and a session log table. That folder is git-ignored on purpose: it holds local context only and is never committed.

Use the same name and model in file attribution headers (section 6) and in `WORKLOG.md`.

## 4. Branches, pull requests and merging

| Rule | Detail |
|------|--------|
| Protected branch | `main` is protected. No direct commits and no force-pushes. |
| Branch names | `feature/P<ID>-<slug>`, `bugfix/P<ID>-<slug>`, `hotfix/<slug>`, `chore/<slug>`. See `docs/BRANCHING_STRATEGY.md`. |
| Scope | One phase per pull request. |
| PR title | `P<ID>: <summary>` or `chore: <summary>` / `fix: <summary>` / `docs: <summary>`. |
| Merging | Merge commit only (no squash, no rebase-merge), so the branch history stays readable. **A human merges. An AI assistant never merges, approves or enables auto-merge.** |
| Going live | Merging to `main` publishes the site automatically (`.github/workflows/deploy.yml`). Treat every merge as a release. |

## 5. Section 4.1: Solution Evaluation Standard

For any non-trivial decision (adding a library, a build step, an embed, a hosting change, a new page structure), the author must:

1. Identify at least two or three realistic candidate approaches, including "do nothing" and "reuse what exists".
2. Evaluate each against this project's constraints: privacy of the person featured, accessibility (WCAG 2.2 AA), page weight, longevity (no build tooling to rot), and ease of editing by a non-specialist.
3. Check whether the decision is already settled in `docs/ARCHITECTURE.md`.
4. Record the reasoning in the pull request description (and in `docs/ARCHITECTURE.md` if it changes the architecture) **before** writing the code.

## 6. Cumulative code attribution

Every source file starts with a one-line header naming the author and date, in the file's own comment style:

```
Written by <Engineer name> (<AI model>) on <YYYY-MM-DD> - <one-line purpose>
```

When you modify an existing file, **add** your own line below the existing one(s). Never delete or rewrite another author's attribution or explanatory comments.

## 7. Privacy and safety rules (public repository)

Never commit or publish any of the following:

- Date of birth, age-revealing documents, gender markers, identity or driver's licence details.
- Phone numbers, home address, or the names and contact details of referees or other private individuals.
- Original (full-size) photographs. Originals stay outside the repository; the site only carries web-optimised copies with all embedded metadata (EXIF, GPS, camera data) removed. Use `scripts/optimize-images.py`.
- Secrets, tokens, `.env` files or credentials.
- A personal email address in commit metadata. Commits to this repository use the GitHub `noreply` address (`<id>+<username>@users.noreply.github.com`). `scripts/validate-compliance.py` checks this.

The only contact detail on the site is Michaela's public email address. It is assembled in the browser by `site/assets/js/main.js` from a `data-mail` attribute so that it does not appear as plain text in the page source. Do not paste it into HTML, Markdown or JSON as ordinary text.

No trackers, analytics, advertising scripts, remote fonts or third-party embeds without a recorded decision under section 5. Every asset the page needs is served from this repository.

## 8. Content and writing rules

- Facts about Michaela come from her CV and her own autobiography. Do not invent employers, dates, qualifications, awards, releases or quotes. If something is missing, leave a note in `docs/AI_COMMUNICATION.md` instead of guessing.
- Text that was written by an assistant rather than by Michaela (for example connective headings and short descriptions) must be listed in `docs/AI_COMMUNICATION.md` so she can review it.
- Tone: warm, plain, first person for her own story. Avoid stock phrases; the words "diligent" and "hardworking" are banned (the validator checks).
- Client, tender and vendor names are kept general. Do not add names that her CV does not already show.
- Every image needs meaningful `alt` text that describes what is in the photo.

## 9. Prohibited actions

| Do not | Why |
|--------|-----|
| Commit directly to `main`, force-push, or delete `main` | History and the live site must stay recoverable. |
| Merge a pull request as an AI assistant, or turn on auto-merge | A human owns every release. |
| Commit secrets, `.env`, `node_modules/`, `__pycache__/`, original photos or `docs/engineers/*.md` | Privacy and repository hygiene. |
| Publish any item listed in section 7 | The site is public and permanent once indexed. |
| Add third-party scripts, trackers or remote fonts without a recorded decision | Privacy, speed and longevity. |
| Delete another author's attribution or comments | Cumulative attribution (section 6). |
| Start work without reading this file and the documents in section 2 | Prevents drift and duplicated effort. |
| Merge several phases in one pull request | Reviewability and clean rollback. |

## 10. Pre-commit checklist

Before every commit, confirm:

1. You read this file and are on a correctly named branch (not `main`).
2. The change belongs to one phase and only touches files that phase owns (`docs/PHASES_AND_TASKS.md`).
3. New or changed files carry an attribution header (section 6).
4. `WORKLOG.md` has a new row for this change.
5. `python3 scripts/validate-compliance.py` passes.
6. No private data from section 7 is present, and the commit email is the GitHub `noreply` address.
7. New images were produced by `scripts/optimize-images.py` and have `alt` text.
8. The page still works without JavaScript, with the keyboard only, and at phone width (open `site/index.html` through a local server and check).
9. Text changes were checked for spelling, facts and tone (section 8).
10. The PR description records any section 5 decision, and the PR title follows the convention.
11. Open items were added to `docs/AI_COMMUNICATION.md` instead of being left in your head.
12. You are not merging your own pull request.
