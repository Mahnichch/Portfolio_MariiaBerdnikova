/* =========================================================================
   Mariia Berdnikova — portfolio behaviour.

   No framework, no build step. Everything degrades: with JS off you still
   get the full page, just without the entry stagger, the thread draw-in and
   the scribbled link underlines.

     0. Hero film: reduced motion + pause control
     1. Entry stagger (~300ms total)
     2. Thread draw-in + hover focus (index.html)
     3. Scribbled link underlines
     4. Scroll parallax on scattered decoration
   ========================================================================= */

(function () {
  'use strict';

  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---------------------------------------------------------------------
     0. Hero film.

     The <video> carries `autoplay muted playsinline`, so it plays on its own
     with JavaScript off. All this adds is: stop it for anyone who asked for
     reduced motion, and give everyone a working pause control.
     ------------------------------------------------------------------ */

  function setupHeroVideo() {
    var wrap = document.querySelector('.hero-video');
    if (!wrap) return;
    var video = wrap.querySelector('video');
    var toggle = wrap.querySelector('.video-toggle');
    if (!video || !toggle) return;

    if (reduced) {
      video.autoplay = false;
      video.pause();
    }

    function label() {
      var playing = !video.paused && !video.ended;
      toggle.textContent = playing ? 'Pause' : 'Play';
      toggle.setAttribute('aria-label', playing ? 'Pause the film' : 'Play the film');
    }

    toggle.hidden = false;
    label();

    toggle.addEventListener('click', function () {
      if (video.paused) {
        var p = video.play();
        // play() rejects if the browser blocks it; keep the label honest.
        if (p && p.catch) p.catch(function () { label(); });
      } else {
        video.pause();
      }
    });

    video.addEventListener('play', label);
    video.addEventListener('pause', label);

    // Some browsers refuse autoplay until the file can play through; retry
    // once it can, unless reduced motion asked us not to.
    video.addEventListener('canplay', function () {
      if (!reduced && video.paused && video.autoplay) {
        var p = video.play();
        if (p && p.catch) p.catch(function () {});
      }
      label();
    });
  }

  /* ---------------------------------------------------------------------
     1. Entry stagger — quick and confident, not slow and precious.
     ------------------------------------------------------------------ */

  function stageEntry() {
    var items = document.querySelectorAll('[data-reveal]');
    for (var i = 0; i < items.length; i++) {
      // Cap the stagger so the whole entry lands inside ~300ms.
      var delay = Math.min(i * 45, 300);
      items[i].style.setProperty('--delay', delay + 'ms');
    }
  }

  /* ---------------------------------------------------------------------
     2. Thread map
     ------------------------------------------------------------------ */

  function setupThreads() {
    var map = document.querySelector('.map');
    if (!map) return;

    var threads = map.querySelectorAll('path[data-thread]');
    for (var i = 0; i < threads.length; i++) {
      var path = threads[i];
      var len = Math.ceil(path.getTotalLength());
      path.style.setProperty('--len', len);
      // Threads draw in after the photo and titles have arrived.
      path.style.setProperty('--delay', 220 + i * 90 + 'ms');
    }

    // Hovering a project lights its own thread and fades the rest back.
    var nodes = map.querySelectorAll('.node[data-thread-ref]');

    function lit(on, name) {
      map.classList.toggle('is-focused', on);
      for (var j = 0; j < threads.length; j++) {
        threads[j].classList.toggle(
          'is-lit',
          on && threads[j].getAttribute('data-thread') === name
        );
      }
    }

    nodes.forEach(function (node) {
      var name = node.getAttribute('data-thread-ref');
      node.addEventListener('mouseenter', function () { lit(true, name); });
      node.addEventListener('focus', function () { lit(true, name); });
      node.addEventListener('mouseleave', function () { lit(false, name); });
      node.addEventListener('blur', function () { lit(false, name); });
    });
  }

  /* ---------------------------------------------------------------------
     3. Scribbled link underlines — drawn on hover via stroke-dashoffset.
     ------------------------------------------------------------------ */

  var SQUIGGLE =
    '<svg class="scribble-line" viewBox="0 0 200 20" preserveAspectRatio="none"' +
    ' aria-hidden="true" focusable="false">' +
    '<path d="M3 13c24-9 38 5 62-2s36-7 62 1 42 5 70-5" fill="none"' +
    ' stroke="currentColor" stroke-width="5" stroke-linecap="round"/></svg>';

  function setupScribbles() {
    var links = document.querySelectorAll('.scribble');
    for (var i = 0; i < links.length; i++) {
      if (links[i].querySelector('.scribble-line')) continue;
      links[i].insertAdjacentHTML('beforeend', SQUIGGLE);
      var path = links[i].querySelector('.scribble-line path');
      links[i].style.setProperty('--len', Math.ceil(path.getTotalLength()));
    }
  }

  /* ---------------------------------------------------------------------
     4. Parallax — small elements drift very slightly on scroll.
     ------------------------------------------------------------------ */

  function setupParallax() {
    if (reduced) return;
    var bits = document.querySelectorAll('[data-parallax]');
    if (!bits.length) return;

    var ticking = false;

    function paint() {
      var y = window.pageYOffset;
      for (var i = 0; i < bits.length; i++) {
        var rate = parseFloat(bits[i].getAttribute('data-parallax')) || 0.05;
        bits[i].style.setProperty('--py', (-y * rate).toFixed(1) + 'px');
      }
      ticking = false;
    }

    window.addEventListener(
      'scroll',
      function () {
        if (ticking) return;
        ticking = true;
        window.requestAnimationFrame(paint);
      },
      { passive: true }
    );

    paint();
  }

  /* ------------------------------------------------------------------ */

  function init() {
    setupHeroVideo();
    stageEntry();
    setupThreads();
    setupScribbles();
    setupParallax();
    // One frame later, so the transitions actually run from their start state.
    window.requestAnimationFrame(function () {
      window.requestAnimationFrame(function () {
        document.documentElement.classList.add('is-ready');
      });
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
