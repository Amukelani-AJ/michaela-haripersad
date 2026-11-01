<!-- Written by Kone Tshivhinda (Claude Sonnet 5.5) on 2026-10-15 - How the portfolio is built and why. -->
<!-- Written by Kone Tshivhinda (Claude Sonnet 5.5) on 2026-10-15 - P4: updated the image and performance notes for the photo refresh. -->

# Architecture

## Summary

A single-page, static website. There is no framework, no bundler and no server code. The folder `site/` is exactly what is published.

```
Visitor's browser
      │  HTTPS
      ▼
GitHub Pages (static files from site/)
      ▲
      │  deploy workflow on every merge to main
GitHub Actions  ◄──  pull request  ◄──  feature branch
```

## Layers

| Layer | Files | Responsibility |
|-------|-------|----------------|
| Content and structure | `site/index.html`, `site/404.html` | Semantic HTML: one `h1`, landmarks, a skip link, native `<details>` accordions and a native `<dialog>` lightbox. All text lives here so it can be edited without tooling. |
| Presentation | `site/assets/css/styles.css` | Design tokens (colours, spacing, radii), light, sand and dark section themes, responsive breakpoints (1100, 960, 700, 560 px), reduced-motion, forced-colours and print styles. |
| Behaviour | `site/assets/js/main.js` | Small, dependency-free enhancements: mobile menu, scroll progress, reveal-on-scroll, current-section highlight, expand/collapse all accordions, lightbox, email assembly. |
| Assets | `site/assets/img`, `site/assets/fonts`, `site/assets/docs` | Optimised WebP photos, self-hosted fonts, the downloadable CV. |
| Tooling | `scripts/` | Image optimiser, icon builder, share-image builder, compliance validator. Only needed when you change assets or run checks. |
| Delivery | `.github/workflows/` | `pr-checks.yml` (validator on every PR) and `deploy.yml` (publish to Pages on merge). |

## Progressive enhancement

The page is fully readable with JavaScript off. The `js` class is added to `<html>` by `main.js`; reveal animations and the mobile menu only activate when it is present. Without JavaScript the navigation is a plain list of anchor links, the accordions are native `<details>`, gallery photos are visible (without the larger viewer), and the email address appears in an obfuscated spelled-out form.

## Images

Original photos are never stored in the repository. `scripts/optimize-images.py` re-encodes each photo to WebP at several widths (for `srcset`), strips all embedded metadata (EXIF, GPS, camera data) by re-encoding from pixels, and records an average colour per photo that is used as the placeholder while the image loads. The gallery is a justified-rows layout driven by each photo's aspect ratio (`--ar`) and becomes a two-column grid on phones, where the `lead-tile` and `feature` tiles span the full width. One photo, the graduation portrait, is only 360 px wide at source, so it is shown as a small thumbnail beside the first credential card and is not part of the gallery or the viewer.

## Accessibility

Targets WCAG 2.2 AA. Verified with axe-core, a pixel-sampled contrast check for text on gradients, and scripted keyboard tests: skip link, focus order and visible focus, accordions with Enter and Space, a lightbox that traps focus, closes on Escape and returns focus to the photo that opened it, a mobile menu that closes on Escape, no horizontal scroll at 390 px, and honouring `prefers-reduced-motion`.

## Privacy by design

- No analytics, cookies, trackers or third-party requests. Fonts are self-hosted.
- The contact email is assembled in the browser from `data-mail="user|domain"`; the page source holds no plain-text address.
- The downloadable CV is a web edition without phone number, date of birth, gender, licence details or referees.
- `scripts/validate-compliance.py` blocks phone-like numbers, personal-detail labels, literal email addresses in the site, and non-`noreply` commit emails.

## Decisions (Solution Evaluation Standard)

### D1. Site technology

| Candidate | Verdict |
|-----------|---------|
| Plain HTML, CSS and JS | **Chosen.** No build step to break, trivially editable, fastest possible load, and nothing to maintain or upgrade for years. |
| Static site generator (Jekyll, Hugo, Astro) | Rejected for v1: adds tooling and a learning curve for what is one page of content. Reconsider if the site grows past a few pages. |
| React/Next.js | Rejected: heavy for a brochure site, build and dependency churn, worse default accessibility and weight. |

### D2. Hosting

| Candidate | Verdict |
|-----------|---------|
| GitHub Pages via Actions workflow | **Chosen.** Free, same place as the code, HTTPS included, revert by reverting the merge. Requires a public repository on the free plan. |
| Netlify or Vercel | Good alternatives, but add another account and dashboard for no extra capability here. |
| Own server | Rejected: cost and maintenance. |

### D3. Fonts

| Candidate | Verdict |
|-----------|---------|
| Self-hosted Inter and Playfair Display (SIL OFL, licences included) | **Chosen.** No third-party requests, faster first paint, consistent rendering, no visitor IP shared with a font CDN. |
| Google Fonts link | Rejected: third-party request and privacy trade-off. |
| System fonts only | Rejected: loses the editorial character of the design. |

### D4. Deploy method

| Candidate | Verdict |
|-----------|---------|
| Actions workflow publishing the `site/` folder | **Chosen.** Publishes only the site, keeps scripts and docs out of the live output, and runs the validator before every release. |
| "Deploy from branch" (root or `/docs`) | Rejected: would publish the whole repository root, or force the site into `/docs`. |

### D5. Contact method

| Candidate | Verdict |
|-----------|---------|
| `mailto:` assembled by JavaScript, with an obfuscated visible fallback | **Chosen.** No server needed and limits simple scraping. |
| Contact form service | Rejected for v1: third-party data processor and spam handling. Revisit if volume justifies it. |
| Plain `mailto:` in the HTML | Rejected: trivially harvested by bots. |

## Performance budget

Roughly 1.7 MB of WebP photos across all sizes (each visitor downloads only the sizes their screen needs), about 115 KB of fonts, 41 KB of CSS (about 9 KB compressed), 7 KB of JavaScript and a 57 KB HTML document (about 14 KB compressed). The two main fonts are preloaded and the first-screen photo is marked `fetchpriority="high"`; photos below the fold use `loading="lazy"`.

## Browser support

Current versions of Chrome, Edge, Firefox and Safari, plus iOS and Android browsers. Modern CSS (grid, `clamp()`, `aspect-ratio`, `dialog`) is used with graceful fallbacks where practical.

## When you change the domain

If the site moves to a custom domain, update: `<link rel="canonical">`, `og:url`, `og:image` and the JSON-LD `url` and `image` in `site/index.html`; `site/sitemap.xml`; the `Sitemap:` line in `site/robots.txt`; and the link in `site/404.html`. Add a `CNAME` file to `site/` if GitHub Pages asks for one.
