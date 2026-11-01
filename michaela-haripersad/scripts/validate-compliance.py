#!/usr/bin/env python3
# Written by Kone Tshivhinda (Claude Sonnet 5.5) on 2026-10-15 - Compliance and site-hygiene validator (Python standard library only).
# Written by Kone Tshivhinda (Claude Sonnet 5.5) on 2026-10-15 - Skip GitHub's temporary test-merge commit in the commit-email check.
"""Repository compliance and site-hygiene validator.

Checks (each prints PASS, WARN or FAIL):
  1. Branch      - not main/master and follows the naming convention (skipped with --no-git).
  2. WORKLOG     - WORKLOG.md changed on this branch compared with the base branch.
  3. Hygiene     - no forbidden files are tracked (.env, engineer profiles, originals, caches ...).
  4. Privacy     - no phone-like numbers, personal-detail labels or literal email addresses in
                   publishable files, and commit emails are GitHub noreply addresses
                   (GitHub's own temporary test-merge commit on pull requests is skipped).
  5. Writing     - banned words are absent from the public text.
  6. Site        - required files exist, every local link and image resolves, every <img> has alt,
                   one <h1>, <html lang> set, attribution headers present.

Usage (run from the repository root):
  python3 scripts/validate-compliance.py                 # local run before committing
  python3 scripts/validate-compliance.py --ci --base origin/main
  python3 scripts/validate-compliance.py --no-git        # content checks only (used by the deploy workflow)

Exit code 0 = no failures, 1 = at least one FAIL.
"""
from __future__ import annotations

import argparse
import fnmatch
import os
import re
import subprocess
import sys
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "site"

BRANCH_PREFIXES = ("feature/", "bugfix/", "hotfix/", "release/", "fix/", "chore/", "docs/")
PROTECTED = {"main", "master", "develop"}

FORBIDDEN_TRACKED = [
    ".env", ".env.*", "*.pem", "*.key",
    "docs/engineers/*.md",
    "node_modules/*", "*/node_modules/*", "__pycache__/*", "*/__pycache__/*", "*.pyc", ".venv/*",
    "originals/*", "*.zip", ".DS_Store", "*/.DS_Store", "Thumbs.db", "*/Thumbs.db",
]

REQUIRED_SITE_FILES = [
    "index.html", "404.html", "favicon.svg", "favicon-32.png", "apple-touch-icon.png",
    "robots.txt", "sitemap.xml", "assets/css/styles.css", "assets/js/main.js",
    "assets/img/og-image.jpg", "assets/docs/Michaela_Haripersad_CV.pdf",
]

TEXT_SUFFIXES = {".html", ".css", ".js", ".json", ".txt", ".xml", ".svg", ".webmanifest", ".md", ".py", ".yml", ".yaml"}

# Privacy patterns (generic: no personal values are stored in this repository).
PHONE_RE = re.compile(r"(?<!\d)(?:\+27|0027|0)[\s.\-]?[1-9]\d[\s.\-]?\d{3}[\s.\-]?\d{4}(?!\d)")
LONG_NUMBER_RE = re.compile(r"(?<![\d.#/-])\d{10,13}(?![\d])")  # 10-13 digits: phone or ID number shaped
EMAIL_RE = re.compile(r"[A-Za-z0-9._%+\-]+@[A-Za-z0-9\-]+(?:\.[A-Za-z0-9\-]+)+")
LABEL_RE = re.compile(
    r"date of birth|\bDOB\b|\bgender\b|driver['’]?s?\s+licen[cs]e|\bID number\b|identity number|\breferees?\b",
    re.I,
)
BANNED_WORDS_RE = re.compile(r"\b(diligent|hard[\s\-]?working)\b", re.I)

ATTRIBUTION_RE = re.compile(r"Written by .+ \(.+\) on \d{4}-\d{2}-\d{2}")

results: list[tuple[str, str, str]] = []


def record(level: str, name: str, detail: str = "") -> None:
    results.append((level, name, detail))
    tag = {"PASS": "[ ok ]", "WARN": "[warn]", "FAIL": "[FAIL]"}[level]
    print(f"{tag} {name}" + (f": {detail}" if detail else ""))


def git(*args: str, check: bool = True) -> str:
    done = subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True)
    if check and done.returncode != 0:
        raise RuntimeError(done.stderr.strip() or f"git {' '.join(args)} failed")
    return done.stdout.strip()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


# --------------------------------------------------------------------------- 1. branch
def check_branch() -> None:
    branch = os.environ.get("GITHUB_HEAD_REF") or git("rev-parse", "--abbrev-ref", "HEAD", check=False)
    if not branch or branch == "HEAD":
        record("WARN", "Branch", "detached HEAD, name not checked")
        return
    if branch in PROTECTED:
        record("FAIL", "Branch", f"direct work on '{branch}' is not allowed; create a feature branch")
    elif not branch.startswith(BRANCH_PREFIXES):
        record("FAIL", "Branch", f"'{branch}' does not follow the convention (feature/P<ID>-slug, bugfix/..., hotfix/..., chore/...)")
    else:
        record("PASS", "Branch", branch)


# --------------------------------------------------------------------------- 2. worklog
def check_worklog(base: str, strict: bool) -> None:
    if not git("rev-parse", "--verify", "--quiet", base, check=False):
        record("WARN", "WORKLOG", f"base '{base}' not found locally; skipped")
        return
    changed = set(git("diff", "--name-only", f"{base}...HEAD", check=False).splitlines())
    changed |= set(git("diff", "--name-only", check=False).splitlines())
    changed |= set(git("diff", "--cached", "--name-only", check=False).splitlines())
    if "WORKLOG.md" in changed:
        record("PASS", "WORKLOG", "updated on this branch")
    else:
        record("FAIL" if strict else "WARN", "WORKLOG", "WORKLOG.md has no new row on this branch")


# --------------------------------------------------------------------------- 3. hygiene
def tracked_files() -> list[str]:
    return git("ls-files", check=False).splitlines()


def check_hygiene() -> None:
    bad = []
    for name in tracked_files():
        for pattern in FORBIDDEN_TRACKED:
            if fnmatch.fnmatch(name, pattern):
                bad.append(name)
                break
    if bad:
        record("FAIL", "Hygiene", "forbidden files are tracked: " + ", ".join(sorted(set(bad))))
    else:
        record("PASS", "Hygiene", "no forbidden files tracked")


# --------------------------------------------------------------------------- 4. privacy
def publishable_files() -> list[Path]:
    return [p for p in SITE.rglob("*") if p.is_file() and p.suffix.lower() in TEXT_SUFFIXES]


def check_privacy() -> None:
    problems: list[str] = []
    for path in publishable_files():
        text = read_text(path)
        rel = path.relative_to(ROOT)
        for rx, label in ((PHONE_RE, "phone-like number"), (LONG_NUMBER_RE, "10-13 digit number"), (EMAIL_RE, "literal email address"), (LABEL_RE, "personal-detail label")):
            for m in rx.finditer(text):
                line = text.count("\n", 0, m.start()) + 1
                problems.append(f"{rel}:{line} {label}")
    # Root documents: numbers only (the documents legitimately discuss what must not be published).
    for name in ("README.md", "INSTRUCTIONS.md", "WORKLOG.md"):
        path = ROOT / name
        if path.exists():
            text = read_text(path)
            for rx, label in ((PHONE_RE, "phone-like number"), (LONG_NUMBER_RE, "10-13 digit number"), (EMAIL_RE, "literal email address")):
                for m in rx.finditer(text):
                    line = text.count("\n", 0, m.start()) + 1
                    problems.append(f"{name}:{line} {label}")
    if problems:
        record("FAIL", "Privacy (content)", "; ".join(problems[:12]) + (" ..." if len(problems) > 12 else ""))
    else:
        record("PASS", "Privacy (content)", "no phone numbers, ID-like numbers, personal-detail labels or literal emails")


SYNTHETIC_MERGE_SUBJECT_RE = re.compile(r"^Merge [0-9a-f]{40} into [0-9a-f]{40}$")


def commits_head() -> str:
    """Return the newest commit whose email counts: the branch tip, not GitHub's test merge.

    On pull_request events the Actions checkout is a temporary "test merge" commit
    (refs/pull/N/merge) that GitHub creates itself and authors with the pull request
    author's account email. It is not part of the branch history and cannot be changed,
    so it is skipped; the real commits are its second parent and are still checked.
    """
    parents = git("rev-list", "--parents", "-n", "1", "HEAD", check=False).split()
    subject = git("log", "-1", "--format=%s", "HEAD", check=False)
    committer = git("log", "-1", "--format=%cn|%ce", "HEAD", check=False).lower()
    if len(parents) == 3 and SYNTHETIC_MERGE_SUBJECT_RE.match(subject) and committer == "github|noreply@github.com":
        return parents[2]
    return "HEAD"


def check_commit_emails(base: str) -> None:
    ok_email = re.compile(r"(@users\.noreply\.github\.com|^noreply@github\.com)$", re.I)
    have_base = bool(git("rev-parse", "--verify", "--quiet", base, check=False))
    head = commits_head()
    rev_range = f"{base}..{head}" if have_base else head
    log = git("log", "--format=%h|%ae|%ce", "-n", "200", rev_range, check=False)
    flagged = []
    for line in log.splitlines():
        short, author, committer = line.split("|")
        if not ok_email.search(author) or not ok_email.search(committer):
            flagged.append(short)  # the address itself is deliberately not printed (public CI logs)
    if flagged:
        record("FAIL", "Privacy (commit emails)", "commits not using a GitHub noreply address: " + ", ".join(flagged[:10]))
    else:
        record("PASS", "Privacy (commit emails)", "all commits use GitHub noreply addresses")


# --------------------------------------------------------------------------- 5. writing
def check_writing() -> None:
    problems = []
    for path in publishable_files() + [ROOT / "README.md"]:
        if not path.exists() or path.suffix.lower() in {".js", ".css"}:
            continue
        text = read_text(path)
        for m in BANNED_WORDS_RE.finditer(text):
            line = text.count("\n", 0, m.start()) + 1
            problems.append(f"{path.relative_to(ROOT)}:{line} '{m.group(0)}'")
    if problems:
        record("FAIL", "Writing", "banned words: " + "; ".join(problems[:10]))
    else:
        record("PASS", "Writing", "no banned words")


# --------------------------------------------------------------------------- 6. site integrity
class PageScan(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.refs: list[tuple[str, str]] = []
        self.imgs_without_alt = 0
        self.h1 = 0
        self.lang = None
        self.ids: dict[str, int] = {}

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        a = {k: (v or "") for k, v in attrs}
        if tag == "html":
            self.lang = a.get("lang")
        if tag == "h1":
            self.h1 += 1
        if tag == "img" and "alt" not in a:
            self.imgs_without_alt += 1
        if "id" in a:
            self.ids[a["id"]] = self.ids.get(a["id"], 0) + 1
        for key in ("src", "href", "poster", "data-full"):
            if a.get(key):
                self.refs.append((tag, a[key]))
        if a.get("srcset"):
            for part in a["srcset"].split(","):
                token = part.strip().split(" ")[0]
                if token:
                    self.refs.append((tag, token))


def is_local(ref: str) -> bool:
    return not (ref.startswith(("#", "mailto:", "tel:", "data:", "javascript:", "http://", "https://", "//")))


def check_site() -> None:
    missing_required = [f for f in REQUIRED_SITE_FILES if not (SITE / f).exists()]
    if missing_required:
        record("FAIL", "Site files", "missing: " + ", ".join(missing_required))
    else:
        record("PASS", "Site files", f"{len(REQUIRED_SITE_FILES)} required files present")

    failures: list[str] = []
    for page in ("index.html", "404.html"):
        path = SITE / page
        if not path.exists():
            continue
        scan = PageScan()
        scan.feed(read_text(path))
        if not scan.lang:
            failures.append(f"{page}: <html> has no lang")
        if scan.h1 != 1:
            failures.append(f"{page}: expected exactly one <h1>, found {scan.h1}")
        if scan.imgs_without_alt:
            failures.append(f"{page}: {scan.imgs_without_alt} <img> without alt")
        dupes = [k for k, v in scan.ids.items() if v > 1]
        if dupes:
            failures.append(f"{page}: duplicate ids {dupes}")
        for tag, ref in scan.refs:
            if is_local(ref):
                target = (path.parent / ref.split("#")[0].split("?")[0]).resolve()
                if not target.exists():
                    failures.append(f"{page}: <{tag}> points to missing file '{ref}'")
    css = SITE / "assets" / "css" / "styles.css"
    if css.exists():
        for ref in re.findall(r"url\(\s*['\"]?([^'\")]+)['\"]?\s*\)", read_text(css)):
            if is_local(ref) and not (css.parent / ref.split("#")[0].split("?")[0]).resolve().exists():
                failures.append(f"styles.css: url() points to missing file '{ref}'")
    # In-page anchors must resolve.
    index = SITE / "index.html"
    if index.exists():
        html = read_text(index)
        ids = set(re.findall(r'\sid="([^"]+)"', html))
        for anchor in set(re.findall(r'href="#([^"]+)"', html)):
            if anchor and anchor not in ids:
                failures.append(f"index.html: in-page link '#{anchor}' has no target")
    if failures:
        record("FAIL", "Site integrity", "; ".join(failures[:12]) + (" ..." if len(failures) > 12 else ""))
    else:
        record("PASS", "Site integrity", "links, images, alt text, headings and ids are consistent")


def check_attribution() -> None:
    candidates = [
        *SITE.glob("*.html"), *SITE.glob("assets/css/*.css"), *SITE.glob("assets/js/*.js"),
        *ROOT.glob("scripts/*.py"), *ROOT.glob("scripts/og-image/*.html"), *ROOT.glob(".github/workflows/*.yml"),
        *ROOT.glob("docs/*.md"), ROOT / "INSTRUCTIONS.md", ROOT / "WORKLOG.md", ROOT / "README.md", ROOT / ".gitignore",
    ]
    missing = []
    for path in candidates:
        if path.exists():
            head = "\n".join(read_text(path).splitlines()[:6])
            if not ATTRIBUTION_RE.search(head):
                missing.append(str(path.relative_to(ROOT)))
    if missing:
        record("FAIL", "Attribution headers", "missing in: " + ", ".join(missing))
    else:
        record("PASS", "Attribution headers", "present in all source and document files")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--ci", action="store_true", help="strict mode: a missing WORKLOG update fails")
    ap.add_argument("--base", default="origin/main", help="base ref for diff and commit checks (default origin/main)")
    ap.add_argument("--no-git", action="store_true", help="skip every check that needs git history")
    args = ap.parse_args()

    print(f"Validating {ROOT}\n")
    if not args.no_git:
        check_branch()
        check_worklog(args.base, strict=args.ci)
        check_hygiene()
        check_commit_emails(args.base)
    check_privacy()
    check_writing()
    check_site()
    check_attribution()

    fails = [r for r in results if r[0] == "FAIL"]
    warns = [r for r in results if r[0] == "WARN"]
    print(f"\n{len(results) - len(fails) - len(warns)} passed, {len(warns)} warnings, {len(fails)} failed")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
