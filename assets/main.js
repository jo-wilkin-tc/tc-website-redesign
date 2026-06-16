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
  document.querySelectorAll('[data-type]').forEach(item => {
    const show = want === 'all' || item.dataset.type === want;
    item.classList.toggle('is-hidden', !show);
  });
});

// "Our latest work" carousel arrows
document.addEventListener('click', function (e) {
  const btn = e.target.closest('.car-btn');
  if (!btn) return;
  const car = btn.closest('.section').querySelector('.carousel');
  if (!car) return;
  car.scrollBy({ left: btn.dataset.car === 'prev' ? -644 : 644, behavior: 'smooth' });
});

// Interactive datasets & tools explorer
(function () {
  var EX = {
    air:        { tag: 'Data Explorer', title: 'Air quality', img: 'assets/tools/data-explorer.png', link: 'https://data.trackingcalifornia.org', label: 'Open the Data Explorer', desc: 'Map annual PM2.5 and ozone concentrations' },
    asthma:     { tag: 'Data Explorer', title: 'Asthma', img: 'assets/tools/data-explorer.png', link: 'https://data.trackingcalifornia.org', label: 'Open the Data Explorer', desc: 'Explore asthma emergency-department and hospitalization rates' },
    traffic:    { tag: 'Traffic Tool', title: 'Traffic & roads', img: 'assets/tools/traffic.jpg', link: 'https://ext.trackingcalifornia.org/traffic', label: 'Open the Traffic Tool', desc: 'View modeled traffic volumes across California roads' },
    water:      { tag: 'Water Quality Viewer', title: 'Drinking water', img: 'assets/tools/water.png', link: '#', label: 'Open the Water Quality Viewer', desc: 'Check drinking-water system boundaries and quality' },
    pesticides: { tag: 'Pesticide Mapping Tool', title: 'Pesticides', img: 'assets/tools/pesticide.png', link: '#', label: 'Open the Pesticide Mapping Tool', desc: 'Map agricultural pesticide use' }
  };
  function render() {
    var topic = document.getElementById('ex-topic');
    if (!topic) return;
    var d = EX[topic.value];
    var scope = document.getElementById('ex-scope').value;
    document.getElementById('ex-img').src = d.img;
    document.getElementById('ex-tag').textContent = d.tag;
    document.getElementById('ex-title').textContent = d.title;
    document.getElementById('ex-desc').textContent = d.desc + ' for ' + scope + '.';
    var a = document.getElementById('ex-link');
    a.href = d.link;
    a.innerHTML = d.label + ' <span class="arrow"></span>';
    if (d.link.indexOf('http') === 0) { a.target = '_blank'; a.rel = 'noopener'; } else { a.removeAttribute('target'); }
  }
  document.addEventListener('change', function (e) {
    if (e.target.id === 'ex-topic' || e.target.id === 'ex-scope') render();
  });
  if (document.getElementById('ex-topic')) render();
})();
