/* Rees Performance — theme controller.
   Monochrome dark/light. Loaded synchronously in <head> so the stored theme is
   applied before first paint (no flash). Default follows the OS; an explicit
   choice is remembered in localStorage and wins over the OS thereafter. */
(function () {
  var KEY = 'rpx-theme';
  var root = document.documentElement;
  var mql = window.matchMedia('(prefers-color-scheme: light)');

  function stored() {
    try { return localStorage.getItem(KEY); } catch (e) { return null; }
  }
  function resolve() {
    var s = stored();
    if (s === 'light' || s === 'dark') return s;
    return mql.matches ? 'light' : 'dark';
  }
  function apply(theme) {
    root.setAttribute('data-theme', theme);
  }

  // Run immediately — before the body paints.
  apply(resolve());

  // Follow the OS only while the user hasn't made an explicit choice.
  mql.addEventListener('change', function () {
    if (!stored()) apply(mql.matches ? 'light' : 'dark');
  });

  var SUN = '<svg class="i-sun" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><circle cx="12" cy="12" r="4.5"/><path d="M12 1.5v2.5M12 20v2.5M4.2 4.2l1.8 1.8M18 18l1.8 1.8M1.5 12h2.5M20 12h2.5M4.2 19.8l1.8-1.8M18 6l1.8-1.8"/></svg>';
  var MOON = '<svg class="i-moon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M20 14.5A8 8 0 0 1 9.5 4a6.5 6.5 0 1 0 10.5 10.5z"/></svg>';

  function mount() {
    if (document.querySelector('.theme-toggle')) return;
    var host = document.querySelector('.nav .nav-links')
            || document.querySelector('.nav .wrap')
            || document.querySelector('.nav');
    if (!host) return;

    var btn = document.createElement('button');
    btn.className = 'theme-toggle';
    btn.type = 'button';
    btn.setAttribute('aria-label', 'Toggle light and dark theme');
    btn.title = 'Toggle theme';
    btn.innerHTML = SUN + MOON;
    btn.addEventListener('click', function () {
      var next = root.getAttribute('data-theme') === 'light' ? 'dark' : 'light';
      apply(next);
      try { localStorage.setItem(KEY, next); } catch (e) {}
    });
    host.appendChild(btn);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', mount);
  } else {
    mount();
  }
})();
