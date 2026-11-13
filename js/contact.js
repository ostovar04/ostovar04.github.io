/* Static contact form: opens the visitor's own email application (no server required). */
(function () {
  const form = document.getElementById('contact-form');
  const status = document.getElementById('form-status');
  if (!form) return;

  form.addEventListener('submit', function (event) {
    event.preventDefault();
    const recipient = form.dataset.recipient || 'benjaminbigbang24@gmail.com';
    const name = document.getElementById('sender-name').value.trim();
    const senderEmail = document.getElementById('sender-email').value.trim();
    const message = document.getElementById('sender-message').value.trim();
    const copy = (window.APP && window.APP.copy[window.APP.lang]) || {};
    const subject = (copy.formSubject || 'Message from the portfolio') + ' — ' + name;
    const body = [
      (copy.mailName || 'Name') + ': ' + name,
      (copy.mailAddress || 'Email') + ': ' + senderEmail,
      '',
      (copy.mailMessage || 'Message') + ':',
      message
    ].join('\n');
    const safeRecipient = recipient.replace(/[^a-zA-Z0-9._+@-]/g, '');
    const mailto = 'mailto:' + safeRecipient
      + '?subject=' + encodeURIComponent(subject)
      + '&body=' + encodeURIComponent(body);

    if (status) status.textContent = copy.formOpened || 'Opening your email application…';
    window.location.href = mailto;
  });
})();
