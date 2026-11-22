/* Blog article behaviour: copy buttons and code tabs. No framework, no server.
   The chosen code language is kept in localStorage and shared by every
   tabbed block on every page of the site. */
(function () {
  var KEY = 'blog.codeLang';

  function stored() {
    try { return localStorage.getItem(KEY); } catch (e) { return null; }
  }

  function store(lang) {
    try { localStorage.setItem(KEY, lang); } catch (e) {}
  }

  function select(block, lang) {
    var tabs = block.querySelectorAll('.code-tab');
    var panels = block.querySelectorAll('.code-panel');
    var found = false;
    for (var i = 0; i < tabs.length; i++) {
      if (tabs[i].getAttribute('data-lang') === lang) { found = true; }
    }
    if (!found) { return false; }
    for (var j = 0; j < tabs.length; j++) {
      var on = tabs[j].getAttribute('data-lang') === lang;
      tabs[j].setAttribute('aria-selected', on ? 'true' : 'false');
      tabs[j].tabIndex = on ? 0 : -1;
      panels[j].classList.toggle('is-active', on);
    }
    return true;
  }

  function selectAll(lang) {
    var blocks = document.querySelectorAll('.code-tabs');
    for (var i = 0; i < blocks.length; i++) { select(blocks[i], lang); }
  }

  function activeText(block) {
    var code = block.querySelector('.code-panel.is-active code') || block.querySelector('code');
    return code ? code.textContent : '';
  }

  function copy(text) {
    if (navigator.clipboard && navigator.clipboard.writeText) {
      return navigator.clipboard.writeText(text);
    }
    return new Promise(function (resolve, reject) {
      var area = document.createElement('textarea');
      area.value = text;
      area.setAttribute('readonly', '');
      area.style.position = 'fixed';
      area.style.opacity = '0';
      document.body.appendChild(area);
      area.select();
      var ok = false;
      try { ok = document.execCommand('copy'); } catch (e) {}
      document.body.removeChild(area);
      if (ok) { resolve(); } else { reject(); }
    });
  }

  function init() {
    var saved = stored();
    var blocks = document.querySelectorAll('.code-tabs');
    for (var i = 0; i < blocks.length; i++) {
      var block = blocks[i];
      var first = block.querySelector('.code-tab');
      var done = saved && select(block, saved);
      if (!done && first) { select(block, first.getAttribute('data-lang')); }
    }

    document.addEventListener('click', function (event) {
      var tab = event.target.closest ? event.target.closest('.code-tab') : null;
      if (tab) {
        var lang = tab.getAttribute('data-lang');
        store(lang);
        selectAll(lang);
        return;
      }
      var btn = event.target.closest ? event.target.closest('.code-copy') : null;
      if (btn) {
        var block = btn.closest('.code');
        copy(activeText(block)).then(function () {
          btn.textContent = btn.getAttribute('data-copied');
          btn.setAttribute('data-state', 'copied');
          setTimeout(function () {
            btn.textContent = btn.getAttribute('data-label');
            btn.removeAttribute('data-state');
          }, 1600);
        }, function () {});
      }
    });

    document.addEventListener('keydown', function (event) {
      var tab = event.target.closest ? event.target.closest('.code-tab') : null;
      if (!tab || (event.key !== 'ArrowRight' && event.key !== 'ArrowLeft')) { return; }
      var tabs = Array.prototype.slice.call(tab.parentNode.querySelectorAll('.code-tab'));
      var at = tabs.indexOf(tab);
      var next = tabs[(at + (event.key === 'ArrowRight' ? 1 : tabs.length - 1)) % tabs.length];
      next.focus();
      next.click();
      event.preventDefault();
    });

    window.addEventListener('storage', function (event) {
      if (event.key === KEY && event.newValue) { selectAll(event.newValue); }
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
