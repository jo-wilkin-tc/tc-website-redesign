/* Tracking California — MEGA MENU VARIANT D
   Layered on megamenu.js, which already handles opening and closing the
   panels. This adds only what the phone drill-down needs:
     1. a back button at the top of every panel
     2. swipe right to go back, the gesture people already use
     3. a scroll lock so the page behind a sheet stays put
   All of it is inert on desktop, where the panels are hover dropdowns. */

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
