/* Small, dependency-free interactions: scroll reveals and mouse parallax. */
(function () {
  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const revealItems = document.querySelectorAll('.reveal');

  if (reducedMotion || !('IntersectionObserver' in window)) {
    revealItems.forEach(function (item) { item.classList.add('visible'); });
  } else {
    const observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('visible');
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.08 });
    revealItems.forEach(function (item) { observer.observe(item); });
  }

  const finePointer = window.matchMedia('(hover: hover) and (pointer: fine)').matches;
  if (!finePointer || reducedMotion) return;

  document.querySelectorAll('[data-tilt]').forEach(function (card) {
    card.addEventListener('pointermove', function (event) {
      const rect = card.getBoundingClientRect();
      const x = (event.clientX - rect.left) / rect.width - 0.5;
      const y = (event.clientY - rect.top) / rect.height - 0.5;
      card.style.setProperty('--rx', (-y * 7).toFixed(2) + 'deg');
      card.style.setProperty('--ry', (x * 8).toFixed(2) + 'deg');

      if (card.classList.contains('hero-scene')) {
        card.style.setProperty('--poster-x', (-x * 8).toFixed(1) + 'px');
        card.style.setProperty('--poster-y', (-y * 6).toFixed(1) + 'px');
        card.style.setProperty('--frame-x', (x * 4).toFixed(1) + 'px');
        card.style.setProperty('--frame-y', (y * 4).toFixed(1) + 'px');
        card.style.setProperty('--stamp-x', (x * 16).toFixed(1) + 'px');
        card.style.setProperty('--stamp-y', (y * 10).toFixed(1) + 'px');
        card.style.setProperty('--title-x', (x * 6).toFixed(1) + 'px');
        card.style.setProperty('--title-y', (y * 4).toFixed(1) + 'px');
        card.style.setProperty('--piece-x', (-x * 22).toFixed(1) + 'px');
        card.style.setProperty('--piece-y', (-y * 16).toFixed(1) + 'px');
        card.style.setProperty('--chip-x', (x * 14).toFixed(1) + 'px');
        card.style.setProperty('--chip-y', (y * 8).toFixed(1) + 'px');
        card.style.setProperty('--board-x', (-x * 18).toFixed(1) + 'px');
        card.style.setProperty('--board-y', (-y * 10).toFixed(1) + 'px');
      }
    });

    card.addEventListener('pointerleave', function () {
      card.style.setProperty('--rx', '0deg');
      card.style.setProperty('--ry', '0deg');
      ['poster-x','poster-y','frame-x','frame-y','stamp-x','stamp-y','title-x','title-y','piece-x','piece-y','chip-x','chip-y','board-x','board-y'].forEach(function (key) {
        card.style.setProperty('--' + key, '0px');
      });
    });
  });
})();
