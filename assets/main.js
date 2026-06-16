/* Tracking California redesign prototype — small UI helpers */

// Mobile nav toggle
document.addEventListener('click', function (e) {
  const toggle = e.target.closest('.nav-toggle');
  if (toggle) {
    const nav = document.querySelector('.nav');
    if (nav) nav.classList.toggle('open');
  }
});

// Resources filter (by data-type)
document.addEventListener('click', function (e) {
  const pill = e.target.closest('.pill[data-filter]');
  if (!pill) return;
  const bar = pill.closest('.filters');
  bar.querySelectorAll('.pill').forEach(p => p.classList.remove('on'));
  pill.classList.add('on');
  const want = pill.dataset.filter;
  document.querySelectorAll('.res-item').forEach(item => {
    const show = want === 'all' || item.dataset.type === want;
    item.classList.toggle('is-hidden', !show);
  });
});
