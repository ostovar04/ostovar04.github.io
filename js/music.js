/* Local, offline soundtrack. Autoplay is attempted; browsers can still require a user gesture. */
(function () {
  const audio = document.getElementById('background-audio');
  const button = document.getElementById('music-toggle');
  const state = document.getElementById('music-state');
  const icon = document.getElementById('music-icon');
  if (!audio || !button || !state) return;

  audio.loop = true;
  audio.volume = 0.22;
  let messageKey = '';

  function refreshControls() {
    const playing = !audio.paused;
    const label = button.querySelector('[data-i18n]');
    const key = playing ? 'musicPause' : 'musicPlay';
    if (label) {
      label.setAttribute('data-i18n', key);
      label.textContent = window.APP ? window.APP.t(key) : (playing ? 'Pause music' : 'Play music');
    }
    button.setAttribute('aria-pressed', playing ? 'true' : 'false');
    if (icon) icon.textContent = playing ? 'Ⅱ' : '▶';
    if (messageKey) {
      state.setAttribute('data-i18n', messageKey);
      state.textContent = window.APP ? window.APP.t(messageKey) : '';
    } else {
      state.removeAttribute('data-i18n');
      state.textContent = '';
    }
  }

  function startMusic() {
    const attempt = audio.play();
    if (attempt && typeof attempt.then === 'function') {
      attempt.then(function () {
        messageKey = 'musicPlaying';
        refreshControls();
      }).catch(function () {
        messageKey = '';
        refreshControls();
      });
    } else {
      messageKey = audio.paused ? '' : 'musicPlaying';
      refreshControls();
    }
  }

  button.addEventListener('click', function () {
    if (audio.paused) startMusic();
    else {
      audio.pause();
      messageKey = 'musicPaused';
      refreshControls();
    }
  });

  audio.addEventListener('play', function () { messageKey = 'musicPlaying'; refreshControls(); });
  audio.addEventListener('pause', function () {
    if (messageKey === 'musicPlaying') messageKey = 'musicPaused';
    refreshControls();
  });
  window.addEventListener('site-language-change', refreshControls);

  /* If autoplay is blocked, a first click elsewhere also retries playback. */
  document.addEventListener('pointerdown', function (event) {
    if (event.target.closest('#music-toggle')) return;
    if (audio.paused) startMusic();
  }, { once: true, capture: true });

  refreshControls();
  startMusic();
})();
