/* Theme toggle. Default is dark; the light palette is monochrome like a chessboard. */
(function () {
  const root = document.documentElement;
  const button = document.getElementById('theme-toggle');
  const icon = document.getElementById('theme-icon');
  const label = document.getElementById('theme-label');

  function refreshThemeButton() {
    if (!button) return;
    const isDark = root.dataset.theme !== 'light';
    const lang = (window.APP && window.APP.lang) || 'fa';
    const text = window.APP && window.APP.copy ? window.APP.copy[lang] : null;
    icon.textContent = isDark ? '☼' : '☾';
    label.textContent = text ? (isDark ? text.themeToLight : text.themeToDark) : (isDark ? 'Light' : 'Dark');
    button.setAttribute('aria-pressed', isDark ? 'false' : 'true');
    button.setAttribute('aria-label', lang === 'fa'
      ? (isDark ? 'تغییر به تم روشن' : 'تغییر به تم تیره')
      : (isDark ? 'Switch to light theme' : 'Switch to dark theme'));
    const themeMeta = document.querySelector('meta[name="theme-color"]');
    if (themeMeta) themeMeta.content = isDark ? '#09090b' : '#f4f4f1';
  }

  if (button) button.addEventListener('click', function () {
    root.dataset.theme = root.dataset.theme === 'light' ? 'dark' : 'light';
    refreshThemeButton();
  });
  window.addEventListener('site-language-change', refreshThemeButton);
  refreshThemeButton();
})();
