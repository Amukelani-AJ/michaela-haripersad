// Written by Kone Tshivhinda (Claude Sonnet 5.5) on 2026-10-15 - Small, dependency-free interactions for the portfolio.
(() => {
  'use strict';

  const root = document.documentElement;
  root.classList.add('js');

  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
  const $ = (selector, ctx = document) => ctx.querySelector(selector);
  const $$ = (selector, ctx = document) => Array.from(ctx.querySelectorAll(selector));

  /* 1. Email links - the address is assembled here so it does not sit in the page source as plain text. */
  $$('[data-mail]').forEach((el) => {
    const [user, domain] = el.dataset.mail.split('|');
    const address = `${user}@${domain}`;
    if (el.tagName === 'A') {
      const subject = el.dataset.subject ? `?subject=${encodeURIComponent(el.dataset.subject)}` : '';
      el.setAttribute('href', `mailto:${address}${subject}`);
    }
    if (el.hasAttribute('data-mail-text')) el.textContent = address;
  });

  /* 2. Header state, scroll progress bar and back-to-top button */
  const header = $('#siteHeader');
  const progress = $('.progress span');
  const toTop = $('.to-top');
  let ticking = false;

  const onScroll = () => {
    ticking = false;
    const y = window.scrollY;
    const max = root.scrollHeight - window.innerHeight;
    header.classList.toggle('is-scrolled', y > 24);
    toTop.classList.toggle('is-shown', y > 900);
    if (progress && max > 0) progress.style.setProperty('--p', Math.min(1, y / max).toFixed(4));
  };
  const requestTick = () => {
    if (!ticking) {
      ticking = true;
      window.requestAnimationFrame(onScroll);
    }
  };
  window.addEventListener('scroll', requestTick, { passive: true });
  window.addEventListener('resize', requestTick, { passive: true });
  onScroll();
  toTop.addEventListener('click', () => {
    window.scrollTo({ top: 0, behavior: reduceMotion.matches ? 'auto' : 'smooth' });
  });

  /* 3. Mobile navigation */
  const toggle = $('.nav-toggle');
  const navList = $('#navList');
  const setNav = (open) => {
    toggle.setAttribute('aria-expanded', String(open));
    toggle.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
    navList.classList.toggle('is-open', open);
    document.body.classList.toggle('nav-open', open);
  };
  toggle.addEventListener('click', () => setNav(toggle.getAttribute('aria-expanded') !== 'true'));
  navList.addEventListener('click', (event) => {
    if (event.target.closest('a')) setNav(false);
  });
  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape' && navList.classList.contains('is-open')) {
      setNav(false);
      toggle.focus();
    }
  });
  window.matchMedia('(min-width: 961px)').addEventListener('change', (event) => {
    if (event.matches) setNav(false);
  });

  /* 4. Reveal on scroll (content stays visible if JavaScript, IntersectionObserver or motion is unavailable) */
  const revealEls = $$('.reveal');
  if ('IntersectionObserver' in window && !reduceMotion.matches) {
    const revealer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add('is-visible');
            revealer.unobserve(entry.target);
          }
        });
      },
      { rootMargin: '0px 0px -8% 0px', threshold: 0.08 }
    );
    revealEls.forEach((el) => revealer.observe(el));
  } else {
    revealEls.forEach((el) => el.classList.add('is-visible'));
  }

  /* 5. Mark the section in view in the navigation */
  const navLinks = new Map($$('.nav-list a[href^="#"]').map((a) => [a.getAttribute('href').slice(1), a]));
  const sectionEls = $$('main > section[id]');
  if ('IntersectionObserver' in window) {
    const spy = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (!entry.isIntersecting) return;
          navLinks.forEach((a) => a.removeAttribute('aria-current'));
          const link = navLinks.get(entry.target.id);
          if (link) link.setAttribute('aria-current', 'location');
        });
      },
      { rootMargin: '-45% 0px -50% 0px' }
    );
    sectionEls.forEach((section) => spy.observe(section));
  }

  /* 6. Experience: expand or collapse every duty group at once */
  const expandBtn = $('#expandAll');
  const duties = $$('details.duty');
  if (expandBtn && duties.length) {
    const sync = () => {
      expandBtn.textContent = duties.every((d) => d.open) ? 'Collapse all details' : 'Expand all details';
    };
    expandBtn.addEventListener('click', () => {
      const open = !duties.every((d) => d.open);
      duties.forEach((d) => { d.open = open; });
      sync();
    });
    duties.forEach((d) => d.addEventListener('toggle', sync));
    sync();
  }

  /* 7. Gallery lightbox (native <dialog>: Escape closes, focus is trapped, focus returns to the photo) */
  const dialog = $('#lightbox');
  const tiles = $$('[data-lightbox]');
  if (dialog && typeof dialog.showModal === 'function' && tiles.length) {
    const image = $('img', dialog);
    const caption = $('figcaption', dialog);
    let index = 0;
    let opener = null;

    const show = (i) => {
      index = (i + tiles.length) % tiles.length;
      const tile = tiles[index];
      const thumb = $('img', tile);
      image.src = tile.dataset.full;
      image.alt = thumb ? thumb.alt : '';
      caption.textContent = `${tile.dataset.caption} (${index + 1} of ${tiles.length})`;
    };

    tiles.forEach((tile, i) => {
      tile.addEventListener('click', () => {
        opener = tile;
        show(i);
        dialog.showModal();
        document.body.classList.add('lb-open');
      });
    });
    $('.lb-close', dialog).addEventListener('click', () => dialog.close());
    $('.lb-prev', dialog).addEventListener('click', () => show(index - 1));
    $('.lb-next', dialog).addEventListener('click', () => show(index + 1));
    dialog.addEventListener('click', (event) => {
      if (event.target === dialog) dialog.close();
    });
    dialog.addEventListener('keydown', (event) => {
      if (event.key === 'ArrowLeft') show(index - 1);
      if (event.key === 'ArrowRight') show(index + 1);
    });
    let touchStartX = null;
    dialog.addEventListener('touchstart', (event) => { touchStartX = event.changedTouches[0].clientX; }, { passive: true });
    dialog.addEventListener('touchend', (event) => {
      if (touchStartX === null) return;
      const dx = event.changedTouches[0].clientX - touchStartX;
      touchStartX = null;
      if (Math.abs(dx) > 50) show(index + (dx < 0 ? 1 : -1));
    }, { passive: true });
    dialog.addEventListener('close', () => {
      document.body.classList.remove('lb-open');
      if (opener) opener.focus();
    });
  } else {
    tiles.forEach((tile) => { tile.style.cursor = 'default'; });
  }

  /* 8. Printing: load every photo first so lazy-loaded gallery pictures are not left blank on paper */
  window.addEventListener('beforeprint', () => {
    $$('img[loading="lazy"]').forEach((img) => { img.loading = 'eager'; });
  });
})();
