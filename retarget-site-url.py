#!/usr/bin/env python3
"""Point the portfolio at its new web address (Python 3, standard library only).

Run it once, before the first push to the new GitHub account:

    python3 retarget-site-url.py https://NEW-ACCOUNT.github.io/NEW-REPO/

It looks for the old address, https://konethegreatest.github.io/michaela-haripersad/, in the project
folder that sits next to this script (michaela-haripersad/) and swaps in the new one. That address is
written into the canonical link, the link-preview (Open Graph) tags, the search-engine data block,
robots.txt, sitemap.xml, the 404 page and the README. Nothing else is touched and line endings are kept.

Options:
    --project PATH   project folder to change (default: the michaela-haripersad folder next to this script)
    --old URL        the address to replace (default: the original live address)
    --dry-run        show what would change and write nothing

If the repository is called <account>.github.io, the address is simply https://<account>.github.io/
"""
import argparse
import sys
from pathlib import Path

OLD_DEFAULT = "https://konethegreatest.github.io/michaela-haripersad/"
SKIP_DIRS = {".git", "node_modules", "__pycache__"}
TEXT_SUFFIXES = {".html", ".xml", ".txt", ".md", ".json", ".svg", ".webmanifest", ".js", ".css", ".yml", ".yaml", ".py"}


def with_slash(url):
    return url if url.endswith("/") else url + "/"


def text_files(project):
    for path in sorted(project.rglob("*")):
        rel = path.relative_to(project)
        if not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        if any(part in SKIP_DIRS for part in rel.parts):
            continue
        try:
            with open(path, "r", encoding="utf-8", newline="") as fh:
                yield path, rel, fh.read()
        except UnicodeDecodeError:
            continue


def plural(n):
    return f"{n} place" + ("" if n == 1 else "s")


def main():
    ap = argparse.ArgumentParser(description="Point the portfolio at its new web address.")
    ap.add_argument("new_url", help="the new address, for example https://account.github.io/repo/")
    ap.add_argument("--project", help="project folder (default: michaela-haripersad next to this script)")
    ap.add_argument("--old", default=OLD_DEFAULT, help="address to replace (default: the original live address)")
    ap.add_argument("--dry-run", action="store_true", help="show the changes without writing them")
    args = ap.parse_args()

    new = with_slash(args.new_url.strip())
    old = with_slash(args.old.strip())
    if not new.startswith("https://") or any(ch.isspace() for ch in new):
        print("The new address must start with https:// and contain no spaces, for example https://account.github.io/repo/")
        return 2
    project = Path(args.project) if args.project else Path(__file__).resolve().parent / "michaela-haripersad"
    if not (project / "site" / "index.html").is_file():
        print(f"Cannot find site/index.html in {project}. Use --project to point at the project folder.")
        return 2
    if new == old:
        print("The new address is the same as the old one. Nothing to do.")
        return 0

    total = 0
    for path, rel, text in list(text_files(project)):
        count = text.count(old)
        if not count:
            continue
        total += count
        print(f"{'would change' if args.dry_run else 'changed':>12}  {rel.as_posix()}  ({plural(count)})")
        if not args.dry_run:
            with open(path, "w", encoding="utf-8", newline="") as fh:
                fh.write(text.replace(old, new))

    if not total:
        print("The old address was not found. It may already have been changed.")
        return 0
    print(f"\n{plural(total)} {'would be ' if args.dry_run else ''}updated.")

    if not args.dry_run:
        host = old.split("/")[2]
        left = [rel.as_posix() for _, rel, text in text_files(project) if host in text]
        if left:
            print(f"Heads up: {host} is still mentioned in: {', '.join(left)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
