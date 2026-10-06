/* Tracking California — MEGA MENU
   Site navigation behaviour. Three jobs:
     1. open/close the full-width panels (hover, click, keyboard)
     2. ?filter= deep links into the library filter pills on resources.html
     3. on phones, drill-down sheets — back button, swipe right, scroll lock
   main.js still handles the hamburger, the carousel and the explorer.

   Consolidated from megamenu.js and megamenu-d.js when variant D was adopted.
   The explorer image-path patch that used to live here is gone: it existed
   only because the variant pages sat one folder below the assets they used. */


(function () {
  var DESKTOP = window.matchMedia('(min-width: 1081px)');
  var items = [].slice.call(document.querySelectorAll('.mm-item'));
  if (!items.length) return;
  var hoverTimer;

  function close(item) {
    item.classList.remove('open');
    var t = item.querySelector('.mm-trigger');
    if (t) t.setAttribute('aria-expanded', 'false');
  }
  function closeAll(except) {
    items.forEach(function (i) { if (i !== except) close(i); });
  }
  function open(item) {
    closeAll(item);
    item.classList.add('open');
    var t = item.querySelector('.mm-trigger');
    if (t) t.setAttribute('aria-expanded', 'true');
  }

  items.forEach(function (item) {
    var trigger = item.querySelector('.mm-trigger');
    if (!trigger) return;

    // click works everywhere: it's the only interaction on touch and mobile
    trigger.addEventListener('click', function (e) {
      e.preventDefault();
      item.classList.contains('open') ? close(item) : open(item);
    });

    // hover only on desktop, with a small close delay so the diagonal
    // trip from the trigger down into the panel doesn't dismiss it
    item.addEventListener('mouseenter', function () {
      if (!DESKTOP.matches) return;
      clearTimeout(hoverTimer);
      open(item);
    });
    item.addEventListener('mouseleave', function () {
      if (!DESKTOP.matches) return;
      hoverTimer = setTimeout(function () { close(item); }, 180);
    });
  });

  // click outside closes; Escape closes and returns focus to the trigger
  document.addEventListener('click', function (e) {
    if (!e.target.closest('.mm-item')) closeAll(null);
  });
  document.addEventListener('keydown', function (e) {
    if (e.key !== 'Escape') return;
    var openItem = document.querySelector('.mm-item.open');
    if (!openItem) return;
    close(openItem);
    var t = openItem.querySelector('.mm-trigger');
    if (t) t.focus();
  });
  // tabbing out of a panel closes it
  document.addEventListener('focusin', function (e) {
    if (!e.target.closest('.mm-item')) closeAll(null);
  });
})();

/* Deep links into the library filter: resources.html?filter=news
   Lets the mega menu point at News / Articles & reports / Newsletters / Videos
   without splitting the library into separate pages. */
(function () {
  var want = new URLSearchParams(location.search).get('filter');
  if (!want) return;
  var pill = document.querySelector('.pill[data-filter="' + want.replace(/"/g, '') + '"]');
  if (pill) pill.click();
})();


/* ======================= adopted from variant D ======================= */


(function () {
  var MOBILE = window.matchMedia('(max-width: 1100px)');
  var items = [].slice.call(document.querySelectorAll('.mm-item'));
  if (!items.length) return;

  var ARROW = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" ' +
              'stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">' +
              '<path d="M15 18l-6-6 6-6"/></svg>';

  function close(item) {
    item.classList.remove('open');
    var t = item.querySelector('.mm-trigger');
    if (t) { t.setAttribute('aria-expanded', 'false'); t.focus(); }
    lock();
  }

  /* lock the page only while a sheet is actually covering it */
  function lock() {
    var anyOpen = items.some(function (i) { return i.classList.contains('open'); });
    document.body.classList.toggle('mm-locked', anyOpen && MOBILE.matches);
  }

  items.forEach(function (item) {
    var panel = item.querySelector('.mm-panel');
    var trigger = item.querySelector('.mm-trigger');
    if (!panel || !trigger) return;

    /* the back button sits above the panel content and is styled away on
       desktop, so the same markup serves both layouts */
    var wrap = document.createElement('div');
    wrap.className = 'wrap';
    var back = document.createElement('button');
    back.className = 'mm-back';
    back.type = 'button';
    back.innerHTML = ARROW + '<span>' + (trigger.textContent || 'Menu').trim().replace(/\s*▾$/, '') + '</span>';
    back.setAttribute('aria-label', 'Back to the main menu');
    back.addEventListener('click', function (e) { e.stopPropagation(); close(item); });
    wrap.appendChild(back);
    panel.insertBefore(wrap, panel.firstChild);

    /* swipe right anywhere on the sheet goes back. Only a mostly-horizontal
       gesture counts, so vertical scrolling inside the panel still works. */
    var x0 = null, y0 = null;
    panel.addEventListener('touchstart', function (e) {
      if (!MOBILE.matches || e.touches.length !== 1) { x0 = null; return; }
      x0 = e.touches[0].clientX; y0 = e.touches[0].clientY;
    }, { passive: true });
    panel.addEventListener('touchend', function (e) {
      if (x0 === null) return;
      var t = e.changedTouches[0];
      var dx = t.clientX - x0, dy = t.clientY - y0;
      if (dx > 60 && Math.abs(dx) > Math.abs(dy) * 1.6) close(item);
      x0 = null;
    }, { passive: true });

    /* keep the lock honest however the panel was opened or closed */
    new MutationObserver(lock).observe(item, { attributes: true, attributeFilter: ['class'] });
  });

  /* closing the hamburger must not leave a sheet stranded over the page */
  var toggle = document.querySelector('.nav-toggle');
  if (toggle) toggle.addEventListener('click', function () {
    items.forEach(function (i) { i.classList.remove('open'); });
    lock();
  });

  MOBILE.addEventListener('change', lock);
})();
