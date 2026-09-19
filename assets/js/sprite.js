/* =========================================================================
   Decorative SVG sprite.

   Loaded as the FIRST element inside <body> so every <use href="#..."> that
   comes after it resolves immediately — including over file:// (no fetch).

   Everything here is decoration: mark each <svg class="deco"> aria-hidden.

   Pieces:
     #scribble  #spiral  #arrow  #arrow-curve  #circle-rough  #underline
     #strike  #thread-seg
     #star-4  #star-4-b  #star-5  #star-6  #star-8
     #star-line  #star-line-b  #heart  #heart-line  #heart-line-b

   Edges are roughened by the feTurbulence/feDisplacementMap filter #rough,
   so strokes read as brush/crayon rather than clean vector lines.

   The stars and hearts do NOT use that filter, and they are not regular
   polygons either. They are drawn: solid shapes with smooth outlines and
   deeply concave sides, so each point tapers to a needle. That taper is what
   makes a star read as drawn — a straight-sided one reads as plotted however
   much its vertices are nudged about, and roughening its edges only makes it
   look wobbly. tools/make-deco-symbols.py generates the path data; the shapes
   ship as literal paths, not as code. The -b variants exist so a shape
   repeated on one page is never identical to itself.
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

    /* --- 6-point star  ---------------------------------------------------*/
    '<symbol id="star-6" viewBox="0 0 100 100">',
    '  <path fill="currentColor"',
    '        d="M49.5 2.5 Q53.8 25.3 60.9 30.6 Q69.4 33.8 91.6 25.8 Q72.7 41.3',
    '           71.5 50 Q70.6 57.7 90.5 73.3 Q68.9 65.3 61 68.5 Q53.6 72.9 49.5',
    '           97.8 Q46.2 72.8 39.4 68.8 Q31.1 65.1 7.8 73.6 Q27.6 58.2 27.8 50.1',
    '           Q25.6 41 6.9 25.9 Q29.6 33.7 38.6 30.5 Q45.6 25.5 49.5 2.5Z"/>',
    '</symbol>',

    /* --- 8-point star  ---------------------------------------------------*/
    '<symbol id="star-8" viewBox="0 0 100 100">',
    '  <path fill="currentColor"',
    '        d="M49.8 2.1 Q52.5 27.6 57.4 32.7 Q62.5 34.4 82.9 17.1 Q67.8 35.8',
    '           68.1 42.2 Q70.3 47.7 98.2 50.2 Q70.1 52.2 67.3 57.1 Q68.5 64.8',
    '           84.4 84.3 Q64.2 67.6 57.6 67.9 Q52.7 71.5 50.6 97.2 Q47.5 73.3',
    '           42.4 67.7 Q36 67.2 15.6 83.8 Q34.1 62.5 32.3 57.2 Q27.2 52.6 3.1',
    '           50.3 Q29 47.6 32.1 42.5 Q31.6 35.6 15.8 16.6 Q36.5 33.5 42.6 32.6',
    '           Q47.7 30 49.8 2.1Z"/>',
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

    /* --- filled heart, lopsided on purpose  ------------------------------*/
    '<symbol id="heart" viewBox="0 0 100 92">',
    '  <path fill="currentColor"',
    '        d="M48.5 88 C22.9 67.9 5.4 48 3.6 30.3 C3.4 14 15.1 3.7 28.4 1.8',
    '           C39.3 2.3 46.4 12.2 49.3 19.5 C54.7 10.2 62.6 3 70.3 3.3 C84.6 4.1',
    '           97.6 15.2 97.4 30.9 C94.7 50.8 78.8 69.2 48.5 88Z"/>',
    '</symbol>',


    /* --- outlined heart  -------------------------------------------------*/
    '<symbol id="heart-line" viewBox="0 0 100 92">',
    '  <path fill="none" stroke="currentColor" stroke-width="6"',
    '        stroke-linejoin="round" stroke-linecap="round"',
    '        d="M50.1 88.3 C21.9 67.3 5.1 49.2 4.8 31.2 C1.6 12.2 14.4 4.2 28.7',
    '           4.2 C39.4 2.4 46.5 11.4 49.3 19 C55.2 10.4 61.2 3.6 72.2 4.4 C83.2',
    '           2.2 98.4 15 97.1 29.9 C94.4 51.3 79.1 68.5 50.1 88.3Z"/>',
    '</symbol>',

    /* --- filled 5-point star  --------------------------------------------*/
    '<symbol id="star-5" viewBox="0 0 100 100">',
    '  <path fill="currentColor"',
    '        d="M49.4 2.8 Q54.6 23.3 61.6 33.7 Q73 37.3 94.4 35.4 Q76.1 46.7 69.6',
    '           56.6 Q69.6 68.5 79 89.2 Q61.7 74 50.1 70.2 Q38.4 75.1 22.8 88.4',
    '           Q31 68.2 31.1 55.9 Q23.2 46 3.6 34.4 Q25.7 36.7 37.8 33.5 Q44.6',
    '           22.9 49.4 2.8Z"/>',
    '</symbol>',

    /* --- outlined 5-point star  ------------------------------------------*/
    '<symbol id="star-line" viewBox="0 0 100 100">',
    '  <path fill="none" stroke="currentColor" stroke-width="5"',
    '        stroke-linejoin="round" stroke-linecap="round"',
    '        d="M50.1 5.1 Q54.9 24.2 61.4 34.3 Q73.3 37.3 92.9 36.2 Q75 46.7 67.6',
    '           55.7 Q68.8 68.3 76.3 86.9 Q61.2 73.5 50.1 68.4 Q39 72.7 23.9 85.3',
    '           Q31 67.8 31.9 56.2 Q24.2 46.4 6.2 35.1 Q27.1 37.3 38.8 34.5 Q45.5',
    '           25.6 50.1 5.1Z"/>',
    '</symbol>',

    /* --- outlined star, second hand  -------------------------------------*/
    '<symbol id="star-line-b" viewBox="0 0 100 100">',
    '  <path fill="none" stroke="currentColor" stroke-width="5"',
    '        stroke-linejoin="round" stroke-linecap="round"',
    '        d="M58 4.5 Q59 25.5 63.9 35.9 Q74.4 41.2 94.7 42.9 Q75.8 50.7 67.3',
    '           58.7 Q65.6 70 70 89.4 Q56.9 73.6 47 68.8 Q35.7 71.2 19.4 81.2',
    '           Q29.4 64.1 30.6 53.1 Q24.9 42.5 10.1 29.2 Q29.6 34.2 41.1 33 Q49.6',
    '           24.1 58 4.5Z"/>',
    '</symbol>',

    /* --- outlined heart, second hand  ------------------------------------*/
    '<symbol id="heart-line-b" viewBox="0 0 100 92">',
    '  <path fill="none" stroke="currentColor" stroke-width="6"',
    '        stroke-linejoin="round" stroke-linecap="round"',
    '        d="M48.2 88.3 C22 67.5 6 50.2 5.3 29.4 C2.7 14.4 13.8 3.9 28.7 3.6',
    '           C39.6 2.4 46.3 12.1 50.2 18.5 C55.8 10.5 62.1 3.6 69.7 3.7 C84.4',
    '           2.5 95.8 15.2 96.7 30.3 C94.9 51.4 78 68.9 48.2 88.3Z"/>',
    '</symbol>',

    /* --- four-point sparkle  ---------------------------------------------*/
    '<symbol id="star-4" viewBox="0 0 100 100">',
    '  <path fill="currentColor"',
    '        d="M50.3 2.7 Q52.1 34.6 56.9 43.2 Q64.1 48.1 97.1 49.6 Q64.7 51.7',
    '           56.7 56.6 Q51.5 61.3 50.5 98.7 Q48.7 61.7 43.3 56.9 Q38.6 51.5 2.6',
    '           50.1 Q38.6 48.6 43.1 43.1 Q48.6 38.2 50.3 2.7Z"/>',
    '</symbol>',

    /* --- four-point sparkle, second hand  --------------------------------*/
    '<symbol id="star-4-b" viewBox="0 0 100 100">',
    '  <path fill="currentColor"',
    '        d="M67.6 6.9 Q56.6 38 57.5 47 Q63.7 54 93.5 67.8 Q58.2 54.4 53 57.5',
    '           Q46.4 61.6 31.4 93.1 Q43.4 61.6 42.4 53.2 Q37.7 46.3 5.7 31.3 Q39',
    '           43.9 47.1 42.4 Q52.6 41.2 67.6 6.9Z"/>',
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
