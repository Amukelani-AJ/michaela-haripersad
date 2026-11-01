<!-- Written by Kone Tshivhinda (Claude Sonnet 5.5) on 2026-10-15 - Project overview and editing guide. -->
<!-- Written by Kone Tshivhinda (Claude Sonnet 5.5) on 2026-10-15 - P4: photo workflow now covers retiring photos and full-width tiles. -->

# Michaela Haripersad: portfolio

The online portfolio of **Michaela Haripersad**, a Johannesburg singer and Business Development Intern: her story, experience, skills, credentials, photos and a way to get in touch.

**Live site:** https://amukelani-aj.github.io/michaela-haripersad/

It is a single, fast, accessible page built with plain HTML, CSS and JavaScript. There is nothing to install and no build step; the folder `site/` is exactly what is published.

## Preview it on your computer

From the repository root, start any static file server and open the address it prints. With Python:

```
python3 -m http.server 8000 --directory site
```

Then open http://localhost:8000. (Opening `site/index.html` by double-clicking also works for a quick look, but a server is closer to the real thing.)

## What is where

```
site/                    Everything that is published
  index.html             The whole page: all text lives here
  404.html               "Page not found" screen
  assets/css/styles.css  Design: colours, layout, responsive rules
  assets/js/main.js      Small interactions: menu, lightbox, accordions, email link
  assets/img/            Optimised photos (WebP) and the link-preview image
  assets/fonts/          Self-hosted Inter and Playfair Display (SIL OFL licences included)
  assets/docs/           The downloadable CV (web edition)
  favicon.*, apple-touch-icon.png, robots.txt, sitemap.xml
scripts/                 Helpers for images, icons, the share image and the safety checks
docs/                    Architecture, phases, branching rules, hand-off ledger
.github/workflows/       Automatic checks and publishing
INSTRUCTIONS.md          The rules for anyone (or any AI assistant) editing this repo
WORKLOG.md               Running log of changes
```

## Editing the content

All wording is in `site/index.html`. Search for the section id you want:

| Section | id | Notes |
|---------|----|-------|
| Hero | `top` | Name, roles, short introduction, quote |
| My story | `story` | Her autobiography, word for word |
| Two stages, one voice | `sides` | Stage and boardroom cards |
| Experience | `experience` | Timeline; each group of duties is a `<details>` block |
| Skills | `skills` | Nine skill cards |
| Credentials | `credentials` | Education (with a small graduation photo), earlier certificates, 2026 certificates and training |
| Gallery | `gallery` | Six photo tiles in two rows that open in a viewer |
| Interests | `interests` | Interests and languages |
| Contact | `contact` | Email button, CV download, roles she is exploring |

### Add or change a photo

1. Keep the original file outside the repository (the `originals/` folder is git-ignored).
2. Add a line for it in `PHOTOS` at the top of `scripts/optimize-images.py`. The path is relative to the folder you pass as `--src`.
3. Run `python3 scripts/optimize-images.py --src <folder with originals> --out site/assets/img` (needs Pillow: `pip install pillow`). This writes WebP versions at several sizes and removes all hidden photo data such as location and camera details.
4. Copy an existing `<button class="tile" ...>` block in the gallery, and change the image names, the `--ar` (width divided by height), the placeholder colour from `site/assets/img/manifest.json`, the caption and, importantly, the `alt` text that describes the photo. Use `tile lead-tile` or `tile feature` only for a photo that should span the full width on phones.
5. To retire a photo, remove its line from `PHOTOS`, delete its tile, and remove its files with `git rm site/assets/img/<name>-*.webp`.

The photos arrived in two batches that share the file names `Media.jpg`, `Media (1).jpg`, and so on. The script therefore reads the first batch from a `Mickys` sub-folder of `--src` and the second batch from the folder itself (see the note at the top of the script).

### Add music, video or social links

Add them as plain links in the contact section, after the CV button:

```html
<a class="btn btn-ghost" href="https://example.com/her-profile" rel="noopener">Listen on ...</a>
```

Then list the same addresses under `"sameAs": [ ... ]` in the JSON-LD block near the top of `index.html` so search engines can connect them to her name. Prefer plain links over embedded players: embeds add trackers and slow the page.

### Update the CV download

The CV on the site is a web edition. It keeps her public email address and leaves out her phone number, date of birth, gender, licence details and referees. Replace `site/assets/docs/Michaela_Haripersad_CV.pdf` whenever the CV changes and keep those details out.

### Change the email address

In `index.html`, change `data-mail="name|domain.com"` (it appears twice in the contact section). The address is deliberately written in two parts; do not write it out in full anywhere in the HTML.

### Regenerate icons and the share image

- Icons: `python3 scripts/make-icons.py` (needs `fonttools`, `brotli`, `playwright`).
- Link-preview image (the picture shown when the link is shared): edit `scripts/og-image/template.html`, then `python3 scripts/make-og-image.py` (needs `playwright`, `pillow`).

## Publishing

Changes reach the live site through a pull request:

1. Create a branch, for example `feature/P2-music-links`, and make your changes.
2. Add a row to `WORKLOG.md` and run `python3 scripts/validate-compliance.py`.
3. Open a pull request into `main`. The **PR checks** workflow runs automatically.
4. A person reviews and merges it (merge commit). The **Deploy to GitHub Pages** workflow then publishes `site/` within a minute or two.

GitHub Pages must be set to **Build and deployment → Source: GitHub Actions** (Settings → Pages). A free GitHub account needs the repository to be public for Pages.

## Quality checks

The site was checked for accessibility (axe-core, plus a pixel-level contrast check on text over gradients), keyboard use, the mobile menu, no-JavaScript viewing, and layout from 390 px phones to 1920 px desktops. It respects "reduce motion" settings and has print and high-contrast styles.

## Privacy

- No analytics, cookies, trackers or third-party requests. Fonts are served from this repository.
- No phone number, date of birth, gender, licence or referee details anywhere on the site or in the CV download.
- The contact email is built in the browser so it is not sitting in the page source as plain text.
- Photos have all embedded metadata removed.

`scripts/validate-compliance.py` enforces the key rules automatically on every pull request and every deploy.

## Rights and credits

- The text, CV and photographs are personal content about Michaela Haripersad. All rights reserved: this repository grants no licence to copy or reuse them. Photo credits are still to be confirmed (see `docs/AI_COMMUNICATION.md`).
- Fonts: [Inter](https://rsms.me/inter/) and [Playfair Display](https://fonts.google.com/specimen/Playfair+Display), both under the SIL Open Font License 1.1 (licence texts are in `site/assets/fonts/`).
- Site design and code prepared with Claude (Anthropic) for Kone Tshivhinda.

## Working on this repository

Read `INSTRUCTIONS.md` first. The short version: work on a branch, one phase per pull request, log your change in `WORKLOG.md`, never commit private details, and let a human merge.
