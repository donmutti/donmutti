/* Blog article behaviour: copy buttons, code tabs and the image lightbox.
   No framework, no server. The chosen code language is kept in localStorage
   and shared by every tabbed block on every page of the site. */
(function () {
  var KEY = 'blog.codeLang';
  var MOVE = 8;

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

  function reducedMotion() {
    return window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  }

  /* ---- lightbox ---- */

  var lb = {
    root: null,
    thumb: null,
    prevFocus: null,
    lockY: 0,
    open: false,
    pinching: false,
    pointers: 0
  };

  function articleImages() {
    return document.querySelectorAll('.post-body img');
  }

  function captionOf(img) {
    var fig = img.closest('figure');
    var cap = fig && fig.querySelector('figcaption');
    return cap ? cap.textContent.trim() : '';
  }

  function lockScroll() {
    lb.lockY = window.scrollY || window.pageYOffset;
    document.body.style.position = 'fixed';
    document.body.style.top = '-' + lb.lockY + 'px';
    document.body.style.left = '0';
    document.body.style.right = '0';
    document.body.style.width = '100%';
  }

  function unlockScroll() {
    document.body.style.position = '';
    document.body.style.top = '';
    document.body.style.left = '';
    document.body.style.right = '';
    document.body.style.width = '';
    window.scrollTo(0, lb.lockY);
  }

  function setInert(on) {
    var kids = document.body.children;
    for (var i = 0; i < kids.length; i++) {
      if (kids[i] === lb.root) { continue; }
      if (on) { kids[i].setAttribute('inert', ''); }
      else { kids[i].removeAttribute('inert'); }
    }
  }

  function fitSize(natW, natH, capH, box) {
    var cs = window.getComputedStyle(box);
    var padX = (parseFloat(cs.paddingLeft) || 0) + (parseFloat(cs.paddingRight) || 0);
    var padY = (parseFloat(cs.paddingTop) || 0) + (parseFloat(cs.paddingBottom) || 0);
    var maxW = Math.max(40, box.clientWidth - padX);
    var maxH = Math.max(40, box.clientHeight - padY - capH);
    var scale = Math.min(maxW / natW, maxH / natH);
    return { w: Math.max(1, natW * scale), h: Math.max(1, natH * scale) };
  }

  function invertToThumb(img, thumbRect) {
    var r = img.getBoundingClientRect();
    var sx = thumbRect.width / r.width;
    var sy = thumbRect.height / r.height;
    var dx = thumbRect.left - r.left;
    var dy = thumbRect.top - r.top;
    img.style.transition = 'none';
    img.style.transform = 'translate(' + dx + 'px, ' + dy + 'px) scale(' + sx + ', ' + sy + ')';
  }

  function playTransform(img, value) {
    if (reducedMotion()) {
      img.style.transition = 'none';
      img.style.transform = value;
      return;
    }
    img.style.transition = '';
    img.style.transform = value;
  }

  function openLightbox(thumb) {
    if (lb.open) { return; }
    var cap = captionOf(thumb);
    var lang = (document.documentElement.lang || 'en').slice(0, 2);
    var label = cap || thumb.getAttribute('alt') || (lang === 'ru' ? 'Изображение' : 'Image');
    var root = document.createElement('div');
    root.className = 'lightbox';
    root.setAttribute('role', 'dialog');
    root.setAttribute('aria-modal', 'true');
    root.setAttribute('aria-label', label);
    root.tabIndex = -1;
    var backdrop = document.createElement('div');
    backdrop.className = 'lightbox-backdrop';
    var figure = document.createElement('figure');
    figure.className = 'lightbox-figure';
    var img = document.createElement('img');
    img.className = 'lightbox-img';
    img.src = thumb.currentSrc || thumb.src;
    img.alt = thumb.alt || '';
    img.draggable = false;
    img.width = thumb.naturalWidth || thumb.width;
    img.height = thumb.naturalHeight || thumb.height;
    figure.appendChild(img);
    var caption = null;
    if (cap) {
      caption = document.createElement('figcaption');
      caption.className = 'lightbox-caption';
      caption.textContent = cap;
      figure.appendChild(caption);
    }
    root.appendChild(backdrop);
    root.appendChild(figure);
    document.body.appendChild(root);
    lb.root = root;
    lb.thumb = thumb;
    lb.prevFocus = document.activeElement;
    lb.open = true;
    lb.pinching = false;

    var thumbRect = thumb.getBoundingClientRect();
    lockScroll();
    setInert(true);

    var capH = caption ? caption.getBoundingClientRect().height + 10 : 0;
    var size = fitSize(img.naturalWidth || img.width, img.naturalHeight || img.height, capH, root);
    img.style.width = size.w + 'px';
    img.style.height = size.h + 'px';

    invertToThumb(img, thumbRect);
    root.offsetWidth;
    requestAnimationFrame(function () {
      root.classList.add('is-on');
      playTransform(img, 'none');
    });

    history.pushState({ lightbox: true }, '', location.href);
    root.focus();
  }

  function closeLightbox() {
    if (!lb.open || !lb.root) { return; }
    var root = lb.root;
    var img = root.querySelector('.lightbox-img');
    var thumb = lb.thumb;
    var finish = function () {
      if (root.parentNode) { root.parentNode.removeChild(root); }
      setInert(false);
      unlockScroll();
      if (lb.prevFocus && typeof lb.prevFocus.focus === 'function') {
        try { lb.prevFocus.focus(); } catch (e) {}
      }
      lb.root = null;
      lb.thumb = null;
      lb.prevFocus = null;
      lb.open = false;
    };
    root.classList.remove('is-on');
    if (img && thumb && thumb.isConnected && !reducedMotion()) {
      invertToThumb(img, thumb.getBoundingClientRect());
      playTransform(img, img.style.transform);
      var done = false;
      var once = function () {
        if (done) { return; }
        done = true;
        finish();
      };
      img.addEventListener('transitionend', once);
      setTimeout(once, 400);
    } else {
      finish();
    }
  }

  function requestClose() {
    if (!lb.open) { return; }
    if (history.state && history.state.lightbox) {
      history.back();
    } else {
      closeLightbox();
    }
  }

  function initLightbox() {
    var imgs = articleImages();
    for (var i = 0; i < imgs.length; i++) {
      var img = imgs[i];
      img.draggable = false;
      img.setAttribute('tabindex', '0');
      img.setAttribute('role', 'button');
      img.setAttribute('aria-haspopup', 'dialog');
    }

    document.addEventListener('dragstart', function (event) {
      if (event.target && event.target.closest && event.target.closest('.post-body img, .post-body figure, .lightbox')) {
        event.preventDefault();
      }
    });

    var startX = 0, startY = 0, moved = false, startOnImg = null;

    document.addEventListener('pointerdown', function (event) {
      if (event.button && event.button !== 0) { return; }
      if (event.isPrimary === false) { return; }
      startX = event.clientX;
      startY = event.clientY;
      moved = false;
      startOnImg = event.target.closest ? event.target.closest('.post-body img') : null;
      if (lb.open) { lb.pointers += 1; }
    });

    document.addEventListener('pointermove', function (event) {
      if (Math.hypot(event.clientX - startX, event.clientY - startY) > MOVE) { moved = true; }
    });

    document.addEventListener('pointerup', function (event) {
      if (lb.open) { lb.pointers = Math.max(0, lb.pointers - 1); }
      if (event.button && event.button !== 0) { return; }
      if (moved || lb.pinching) { lb.pinching = lb.pointers > 1; return; }
      if (lb.open) {
        requestClose();
        return;
      }
      if (startOnImg && event.target === startOnImg) {
        event.preventDefault();
        openLightbox(startOnImg);
      }
    });

    document.addEventListener('pointercancel', function () {
      if (lb.open) { lb.pointers = Math.max(0, lb.pointers - 1); }
      startOnImg = null;
    });

    document.addEventListener('touchstart', function (event) {
      if (lb.open && event.touches && event.touches.length > 1) { lb.pinching = true; }
    }, { passive: true });

    document.addEventListener('keydown', function (event) {
      if (!lb.open) { return; }
      if (event.key === 'Escape') {
        event.preventDefault();
        requestClose();
        return;
      }
      if (event.key === 'Tab') {
        event.preventDefault();
        if (lb.root) { lb.root.focus(); }
      }
    });

    window.addEventListener('popstate', function () {
      if (lb.open) { closeLightbox(); }
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

    initLightbox();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
