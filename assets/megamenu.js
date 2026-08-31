/* Tracking California — MEGA MENU TRIAL
   Loaded only by pages under /megamenu/. Two jobs:
     1. open/close behaviour for the full-width panels (hover, click, keyboard)
     2. ?filter= deep links into the library filter pills on resources.html
   main.js still handles the mobile toggle, carousel and explorer. */

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

/* main.js is shared with the root prototype, so the datasets-and-tools explorer
   sets image paths like "assets/tools/x.png" — correct at the root, one level
   short inside megamenu/. Patch the src as it is written. */
(function () {
  var img = document.getElementById('ex-img');
  if (!img) return;
  function fix() {
    if (/^assets\//.test(img.getAttribute('src') || '')) {
      img.setAttribute('src', '../' + img.getAttribute('src'));
    }
  }
  new MutationObserver(fix).observe(img, { attributes: true, attributeFilter: ['src'] });
  fix();
})();
