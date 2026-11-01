<!-- Written by Kone Tshivhinda (Claude Sonnet 5.5) on 2026-10-15 - Branching and merge policy. -->

# Branching strategy

## Branch model

This is a small, single-site repository, so it uses **one long-lived branch: `main`**. Everything on `main` is what visitors see; merging to `main` deploys.

A separate `develop` branch is intentionally **not** used. It would add a second place to review and a second history to keep in sync, with no benefit for a site that deploys in under a minute and can be reverted with one click. If the project grows (several contributors, staged releases), revisit this under the Solution Evaluation Standard in `INSTRUCTIONS.md`.

## Branch names

| Type | Pattern | Example |
|------|---------|---------|
| New work for a phase | `feature/P<ID>-<slug>` | `feature/P2-music-links` |
| Fix for a phase | `bugfix/P<ID>-<slug>` | `bugfix/P1-gallery-caption` |
| Urgent fix to the live site | `hotfix/<slug>` | `hotfix/broken-cv-link` |
| Housekeeping, docs, tooling | `chore/<slug>` | `chore/update-readme` |

Use lower-case words separated by hyphens. Phase IDs come from `docs/PHASES_AND_TASKS.md`.

## Protection on `main`

- Changes arrive only through a pull request. No direct commits, no force-pushes, no deletion.
- The `PR checks` workflow must pass (compliance script, PR title convention).
- Branches are deleted automatically after merge.

## Merge policy

**Merge commit only.** Squash and rebase merges are switched off. A merge commit keeps each feature branch's history intact, which makes it easy to see why a change was made and to revert it as a unit.

Revert a bad release with GitHub's "Revert" button on the pull request, which opens a new pull request that undoes the merge.

## Who merges

A human merges. An AI assistant prepares the branch and the pull request description, then stops. It never merges, approves or enables auto-merge on anyone's behalf.

## Admin bypass

The repository owner is an administrator and could bypass branch protection in an emergency (for example, a broken deploy that blocks the normal path). Doing so is the owner's own decision and should be followed by a `WORKLOG.md` row explaining what happened. AI assistants are never authorised to use a bypass.

## Commit hygiene

- Commit with the GitHub `noreply` email so that no personal address is exposed in public history.
- Add a `WORKLOG.md` row before each commit.
- Keep commit messages short and in the imperative ("Add music links section").
