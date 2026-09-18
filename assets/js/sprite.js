/* =========================================================================
   Decorative SVG sprite.

   Loaded as the FIRST element inside <body> so every <use href="#..."> that
   comes after it resolves immediately — including over file:// (no fetch).

   Everything here is decoration: mark each <svg class="deco"> aria-hidden.

   Pieces:
     #scribble  #spiral  #arrow  #arrow-curve  #star-6  #star-8
     #circle-rough  #underline  #strike  #thread-seg

   Edges are roughened by the feTurbulence/feDisplacementMap filter #rough,
   so strokes read as brush/crayon rather than clean vector lines.
   ========================================================================= */

(function () {
  var SPRITE = [
    '<svg xmlns="http://www.w3.org/2000/svg" aria-hidden="true" focusable="false"',
    '     style="position:absolute;width:0;height:0;overflow:hidden" id="deco-sprite">',
    '<defs>',
    '  <filter id="rough" x="-25%" y="-25%" width="150%" height="150%"',
    '          filterUnits="objectBoundingBox">',
    '    <feTurbulence type="fractalNoise" baseFrequency="0.045" numOctaves="3"',
    '                  seed="7" result="noise"/>',
    '    <feDisplacementMap in="SourceGraphic" in2="noise" scale="3.4"',
    '                       xChannelSelector="R" yChannelSelector="G"/>',
    '  </filter>',
    '</defs>',

    /* --- loose scribble ------------------------------------------------ */
    '<symbol id="scribble" viewBox="0 0 120 60">',
    '  <g fill="none" stroke="currentColor" stroke-width="4" stroke-linecap="round"',
    '     filter="url(#rough)">',
    '    <path d="M6 44c14-26 24 6 36-14S72 6 80 26s14 22 34 6"/>',
    '    <path d="M14 54c18-10 34 4 52-8"/>',
    '  </g>',
    '</symbol>',

    /* --- spiral scrawl -------------------------------------------------- */
    '<symbol id="spiral" viewBox="0 0 100 100">',
    '  <path fill="none" stroke="currentColor" stroke-width="4.5" stroke-linecap="round"',
    '        filter="url(#rough)"',
    '        d="M52 50c-6-2-9 6-3 9s14-3 12-12-13-13-22-7-11 22-2 31 28 9 38-4 9-33-6-43"/>',
    '</symbol>',

    /* --- straight hand-drawn arrow -------------------------------------- */
    '<symbol id="arrow" viewBox="0 0 100 40">',
    '  <g fill="none" stroke="currentColor" stroke-width="4" stroke-linecap="round"',
    '     filter="url(#rough)">',
    '    <path d="M4 21c22-3 44-2 90-2"/>',
    '    <path d="M74 7l20 12-20 13"/>',
    '  </g>',
    '</symbol>',

    /* --- curved hand-drawn arrow ---------------------------------------- */
    '<symbol id="arrow-curve" viewBox="0 0 100 70">',
    '  <g fill="none" stroke="currentColor" stroke-width="4" stroke-linecap="round"',
    '     filter="url(#rough)">',
    '    <path d="M6 10c34-8 66 6 78 44"/>',
    '    <path d="M66 50l19 6 2-21"/>',
    '  </g>',
    '</symbol>',

    /* --- 6-point crayon star -------------------------------------------- */
    '<symbol id="star-6" viewBox="0 0 100 100">',
    '  <path fill="currentColor" filter="url(#rough)"',
    '        d="M98 50 61.3 56.5 74 91.6 50 63 26 91.6 38.7 56.5 2 50 38.7 43.5',
    '           26 8.4 50 37 74 8.4 61.3 43.5Z"/>',
    '</symbol>',

    /* --- 8-point crayon star -------------------------------------------- */
    '<symbol id="star-8" viewBox="0 0 100 100">',
    '  <path fill="currentColor" filter="url(#rough)"',
    '        d="M98 50 62.9 55.4 83.9 83.9 55.4 62.9 50 98 44.6 62.9 16.1 83.9',
    '           37.1 55.4 2 50 37.1 44.6 16.1 16.1 44.6 37.1 50 2 55.4 37.1',
    '           83.9 16.1 62.9 44.6Z"/>',
    '</symbol>',

    /* --- rough circle (overshoots itself, drawn twice) ------------------- */
    '<symbol id="circle-rough" viewBox="0 0 120 100">',
    '  <g fill="none" stroke="currentColor" stroke-width="4" stroke-linecap="round"',
    '     filter="url(#rough)">',
    '    <path d="M92 20C74 4 36 4 18 24S10 78 40 90s66-2 72-24-6-38-24-44"/>',
    '  </g>',
    '</symbol>',

    /* --- squiggle underline --------------------------------------------- */
    '<symbol id="underline" viewBox="0 0 200 20" preserveAspectRatio="none">',
    '  <path fill="none" stroke="currentColor" stroke-width="5" stroke-linecap="round"',
    '        filter="url(#rough)"',
    '        d="M4 13c26-8 38 6 62-1s36-8 62 0 40 6 68-4"/>',
    '</symbol>',

    /* --- strike-through -------------------------------------------------- */
    '<symbol id="strike" viewBox="0 0 200 20" preserveAspectRatio="none">',
    '  <path fill="none" stroke="currentColor" stroke-width="5" stroke-linecap="round"',
    '        filter="url(#rough)" d="M4 12c52-6 104-4 192-5"/>',
    '</symbol>',

    /* --- short connecting thread (mobile card stack) --------------------- */
    '<symbol id="thread-seg" viewBox="0 0 40 56">',
    '  <path fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"',
    '        d="M20 2C6 16 34 30 20 54"/>',
    '</symbol>',

    '</svg>'
  ].join('\n');

  function inject() {
    if (document.getElementById('deco-sprite')) return;
    document.body.insertAdjacentHTML('afterbegin', SPRITE);
  }

  if (document.body) inject();
  else document.addEventListener('DOMContentLoaded', inject);
})();
