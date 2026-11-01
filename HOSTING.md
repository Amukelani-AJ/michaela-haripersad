# Hosting the portfolio on another GitHub account

`michaela-haripersad/` is the complete project as it stood after the last merge (PR #2, the photo refresh): the website in `site/`, the publishing workflow in `.github/workflows/`, the helper scripts and the project docs. It has no git history, so the new account starts with a clean history of its own.

You need a GitHub account to host it and Git on your computer. Python 3 is needed only for step 1 and for the optional local preview.

## 1. Point the site at its new address

Work out the final address first.

- A project site, the usual case: `https://<account>.github.io/<repo>/`, where `<repo>` is any name you choose, for example `https://newaccount.github.io/michaela-haripersad/`.
- A user site: if the repository is called `<account>.github.io`, the address is just `https://<account>.github.io/`.

Then run this once, from the folder that holds this file:

```
python retarget-site-url.py https://<account>.github.io/<repo>/
```

(Use `python3` on a Mac or Linux.) It changes the old address in 9 places across 5 files: the canonical link, the link-preview tags (what LinkedIn or WhatsApp show when the link is shared), the search-engine data block, `robots.txt`, `sitemap.xml`, the 404 page and the project README. Add `--dry-run` to see what it would change without changing anything. The site also works if you skip this step, but search engines and link previews would still point at the old address.

## 2. Create the repository

On the account that will host the site, create a new empty repository: no README, no licence, no `.gitignore`. It has to be public, because a free account cannot publish a private repository with GitHub Pages.

With the GitHub CLI, signed in as the right account (`gh auth status` shows which one, `gh auth switch` changes it):

```
gh repo create <repo> --public
```

For an organisation, use `<org>/<repo>`.

## 3. Switch on GitHub Pages

In the new repository open Settings, then Pages, then Build and deployment, and set Source to **GitHub Actions**. Do this before the first push so the first publish works straight away.

## 4. Push the project

Run these from inside the `michaela-haripersad` folder:

```
git init -b main
git config user.name "Your Name"
git config user.email "<id>+<account>@users.noreply.github.com"
git add .
git commit -m "chore: import the portfolio"
git remote add origin https://github.com/<account>/<repo>.git
git push -u origin main
```

For `user.email` use the account's private GitHub address (Settings, then Emails, shows it as `<id>+<account>@users.noreply.github.com`), not a personal email address. Commits are public, and the project's pull-request check rejects commits that use any other address.

The push starts the **Deploy to GitHub Pages** workflow (Actions tab). The site is live after a minute or two at the address from step 1. If that first run failed because Pages was not switched on yet, switch it on and then run the workflow again from the Actions tab (Deploy to GitHub Pages, Run workflow).

## Good to know

- The workflow runs `scripts/validate-compliance.py` before it publishes and stops if it finds a phone number, a literal email address or similar in the site files. Keep that script in place.
- If you only want the website, the minimum is `site/`, `scripts/validate-compliance.py` and `.github/workflows/deploy.yml` (this set was tested and passes the checks). `docs/`, `INSTRUCTIONS.md` and `WORKLOG.md` are working notes; in a public repository they are public too.
- Do not copy the original photos or any `.zip` file into the project folder. The web copies of the photos are already in `site/assets/img/`, and a folder called `originals/` and `.zip` files are git-ignored on purpose.
- If you are moving the site rather than copying it, unpublish the old one (old repository, Settings, Pages) so only one live copy exists.
- Later edits follow the rules in `README.md` and `INSTRUCTIONS.md`: a pull request into `main`, with a row added to `WORKLOG.md`. Branch protection is a GitHub setting (Settings, then Branches), not part of the files.
- Photo credits and usage rights are still unconfirmed (see `docs/AI_COMMUNICATION.md`). The README says all rights reserved.
- A quick preview on your own computer: `python -m http.server 8000 --directory site` from the project folder, then open http://localhost:8000.
