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

    /* --- hand-drawn heart ------------------------------------------------ */
    '<symbol id="heart" viewBox="0 0 100 92">',
    '  <path fill="currentColor" filter="url(#rough)"',
    '        d="M50 88C20 66 4 48 4 30 4 14 16 4 30 4c10 0 17 6 20 13 3-7 10-13 20-13',
    '           14 0 26 10 26 26 0 18-16 36-46 58z"/>',
    '</symbol>',

    /* --- outlined heart, drawn rather than filled ------------------------ */
    '<symbol id="heart-line" viewBox="0 0 100 92">',
    '  <path fill="none" stroke="currentColor" stroke-width="6" stroke-linejoin="round"',
    '        filter="url(#rough)"',
    '        d="M50 86C22 65 7 48 7 31 7 16 18 7 30 7c10 0 17 6 20 13 3-7 10-13 20-13',
    '           12 0 23 9 23 24 0 17-15 34-43 55z"/>',
    '</symbol>',

    /* --- outlined 5-point star ------------------------------------------- */
    '<symbol id="star-line" viewBox="0 0 100 100">',
    '  <path fill="none" stroke="currentColor" stroke-width="5" stroke-linejoin="round"',
    '        filter="url(#rough)"',
    '        d="M50 4 61.3 34.4 93.8 35.8 68.4 56 77 87.2 50 69.3 23 87.2 31.6 56',
    '           6.2 35.8 38.7 34.4Z"/>',
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
