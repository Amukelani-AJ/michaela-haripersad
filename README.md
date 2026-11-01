<!-- Written by Claude Opus 5.5 on 2026-11-01 - Repository overview for the hosted portfolio. -->

# Michaela Haripersad: portfolio

[![Deploy to GitHub Pages](https://github.com/Amukelani-AJ/michaela-haripersad/actions/workflows/deploy.yml/badge.svg)](https://github.com/Amukelani-AJ/michaela-haripersad/actions/workflows/deploy.yml)

The online portfolio of **Michaela Haripersad**, a Johannesburg singer and performer and a Business Development Intern at Motsoeneng Bill Incorporated.

**Live site:** https://amukelani-aj.github.io/michaela-haripersad/

## About

A single-page site that tells her story and presents both sides of her work, the stage and the boardroom:

- **My story**: her biography, in her own words
- **Two stages, one voice**: singing, performing and modelling alongside business development, executive support, tenders and events
- **Experience**: her internship, set out as a timeline
- **Skills, credentials and interests**: education, certificates, training and languages (English and Afrikaans)
- **Gallery**: a selection of photos in a full-screen viewer
- **Contact**: an email button and a downloadable CV

It is built with plain HTML, CSS and JavaScript. There are no frameworks, dependencies or build step, and the `site/` folder is published exactly as it is.

## Features

- Fast and lightweight: optimised WebP images in several sizes, and fonts served from the repository
- Accessible: checked with axe-core, works with a keyboard and without JavaScript, respects reduced-motion settings, and includes print and high-contrast styles
- Responsive from 390 px phones to 1920 px desktops
- Private by design: no analytics, cookies or trackers, the email address is assembled in the browser, and photo metadata is removed

## Repository layout

```
.github/workflows/deploy.yml   Publishes the site to GitHub Pages on every push to main
michaela-haripersad/           The website project
  site/                        Everything that is published (index.html holds all the text)
  scripts/                     Image, icon and share-image helpers, and the compliance validator
  docs/                        Architecture, phases and branching notes
  README.md                    Detailed editing guide
  INSTRUCTIONS.md              Working rules for anyone editing the project
  WORKLOG.md                   Change log
HOSTING.md                     Guide to moving the site to another GitHub account
retarget-site-url.py           Changes the site's web address after a move
```

## Run it locally

You need Python 3, or any other static file server.

```
python -m http.server 8000 --directory michaela-haripersad/site
```

Then open http://localhost:8000.

## Editing

All the wording is in `michaela-haripersad/site/index.html`. The [project README](michaela-haripersad/README.md) explains how to change each section, add or retire photos, update the CV and add music or social links.

Before you commit, run the validator:

```
python michaela-haripersad/scripts/validate-compliance.py --no-git
```

It checks for privacy problems (phone numbers, literal email addresses and personal details), broken links, missing alt text and other site-integrity issues.

## Deployment

The site is hosted on GitHub Pages, with Settings → Pages → Source set to **GitHub Actions**. Every push to `main` runs [`deploy.yml`](.github/workflows/deploy.yml). The workflow runs the validator, then publishes `michaela-haripersad/site/`. If the validator fails, nothing is published. A change is usually live a minute or two after the push.

## Rights and credits

- The text, CV and photographs are personal content about Michaela Haripersad. **All rights reserved**: this repository grants no licence to copy or reuse them. Photo credits have not been confirmed yet.
- Fonts: [Inter](https://rsms.me/inter/) and [Playfair Display](https://fonts.google.com/specimen/Playfair+Display). Both are under the SIL Open Font License 1.1, and the licence texts are in `michaela-haripersad/site/assets/fonts/`.
- Site design and code were prepared with Claude (Anthropic).
