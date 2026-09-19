/* =========================================================================
   Decorative SVG sprite.

   Loaded as the FIRST element inside <body> so every <use href="#..."> that
   comes after it resolves immediately — including over file:// (no fetch).

   Everything here is decoration: mark each <svg class="deco"> aria-hidden.

   Pieces:
     #scribble  #spiral  #arrow  #arrow-curve  #circle-rough  #underline
     #strike  #thread-seg
     #star-5  #star-6  #star-8  #star-line  #star-line-b
     #heart  #heart-line  #heart-line-b

   Edges are roughened by the feTurbulence/feDisplacementMap filter #rough,
   so strokes read as brush/crayon rather than clean vector lines.

   The stars and hearts are NOT regular polygons with that filter laid over
   the top — that still reads as even, because every arm is the same length
   and every edge is straight. Their arms differ, their edges bow and the
   outlined ones overshoot where the stroke closes. tools/make-deco-symbols.py
   generates the path data; the shapes ship as literal paths, not as code.
   The -b variants exist so a shape repeated on one page is never identical
   to itself.
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

    /* --- 6-point star, drawn  ----------------------------------------------*/
    '<symbol id="star-6" viewBox="0 0 100 100">',
    '  <path fill="currentColor" filter="url(#rough)"',
    '        d="M45.9 4.4 Q52.4 16.3 60.4 27.3 Q74.9 26.3 89.1 23.5 Q79.9 35.4 72.8',
    '           48.6 Q79.7 60.1 89.2 69.3 Q76.3 68.1 63.2 68.6 Q55.9 81.9 51.5 96.4',
    '           Q47.3 83 40.2 70.9 Q24.4 71.5 9.1 74.9 Q18.4 64.1 25.3 51.7 Q15.4',
    '           39.8 4.1 29.2 Q19.8 29.9 35.4 28.8 Q41.6 17 45.9 4.4Z"/>',
    '</symbol>',

    /* --- 8-point star, drawn  ----------------------------------------------*/
    '<symbol id="star-8" viewBox="0 0 100 100">',
    '  <path fill="currentColor" filter="url(#rough)"',
    '        d="M46.7 3.4 Q50.7 18 56.9 31.7 Q68.8 26 78.9 17.4 Q73.3 28.2 69.4 39.7',
    '           Q82.8 45.6 97.3 47.6 Q82.2 49.9 68.3 56.1 Q76.5 69.6 86.4 82 Q73.7',
    '           74.3 59.9 69 Q55.7 81.7 54.2 95 Q49.1 81.8 42.6 69.3 Q29.4 76 17.6',
    '           84.9 Q26.4 72.7 31.6 58.5 Q18.9 55.1 5.9 53.4 Q18.6 49.4 30.1 42.7',
    '           Q22.9 31 14.2 20.4 Q26.9 27.8 40.8 32.3 Q45.7 18.2 46.7 3.4Z"/>',
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

    /* --- filled heart, lopsided on purpose  --------------------------------*/
    '<symbol id="heart" viewBox="0 0 100 92">',
    '  <path fill="currentColor" filter="url(#rough)"',
    '        d="M47.1 87.2 C23.4 66.8 6 45.5 4.1 29.7 C5 15.6 16.2 4.7 29.9 0.9',
    '           C40.9 1.8 47.3 11.5 47.9 19.5 C53 7.6 62.8 3.9 67.3 5.1 C84.6 6.7',
    '           96.5 18 97.6 31.8 C92.2 51.2 77.6 70.1 47.1 87.2Z"/>',
    '</symbol>',


    /* --- outlined heart  ---------------------------------------------------*/
    '<symbol id="heart-line" viewBox="0 0 100 92">',
    '  <path fill="none" stroke="currentColor" stroke-width="6"',
    '        stroke-linecap="round" stroke-linejoin="round" filter="url(#rough)"',
    '        d="M51.3 87.6 C20.8 65.7 5.2 48.4 6.5 31.3 C1.5 11.5 14.9 5.2 30.2 6.2',
    '           C41 2.8 47.1 9.7 48.5 17.9 C54.4 8.6 59.2 5.4 71.3 7.8 C81.5 2.5',
    '           97.5 16.9 96.1 30 C91.9 51.4 78.2 67.9 51.3 87.6 C35.4 76.9 28.4 71',
    '           22.8 62.6"/>',
    '</symbol>',

    /* --- filled 5-point star, for sitting behind a photograph  -------------*/
    '<symbol id="star-5" viewBox="0 0 100 100">',
    '  <path fill="currentColor" filter="url(#rough)"',
    '        d="M45.8 5.1 Q51.5 20.2 59.5 34.1 Q75.2 35.6 90.8 33.6 Q78.7 43.3 69.2',
    '           55.5 Q73.5 72.1 81.9 87 Q67.9 75.9 51.5 68.8 Q38.7 77.9 27.2 88.4',
    '           Q31.9 72.5 33 56 Q18.9 44.4 2.6 36.4 Q19.9 37.5 37.1 35.1 Q42.5 20.4',
    '           45.8 5.1Z"/>',
    '</symbol>',

    /* --- outlined 5-point star  --------------------------------------------*/
    '<symbol id="star-line" viewBox="0 0 100 100">',
    '  <path fill="none" stroke="currentColor" stroke-width="5"',
    '        stroke-linecap="round" stroke-linejoin="round" filter="url(#rough)"',
    '        d="M47.5 5.4 Q52.9 20.1 60.3 33.8 Q76.2 34.7 92.1 33.8 Q78.3 42.8 66.6',
    '           54.3 Q71.5 70.6 78.3 86.1 Q65.5 75.5 51.3 66.9 Q38.1 75 26.4 85',
    '           Q30.5 71.4 33 57.4 Q19.4 45.3 3.8 36.1 Q21.1 37.5 38.4 35.7 Q45 21.1',
    '           47.5 5.4 Q49 9.9 51.4 13.9"/>',
    '</symbol>',

    /* --- outlined star, second hand  ---------------------------------------*/
    '<symbol id="star-line-b" viewBox="0 0 100 100">',
    '  <path fill="none" stroke="currentColor" stroke-width="5"',
    '        stroke-linecap="round" stroke-linejoin="round" filter="url(#rough)"',
    '        d="M57.5 2.7 Q58.6 18.8 63.7 34.2 Q78.9 39.2 94.7 40.9 Q80.5 47.9 68.3',
    '           57.8 Q68 72.8 71.1 87.4 Q60.8 76.5 47.8 68.8 Q34.7 74.1 22.6 81.6',
    '           Q28 68.3 30 54.1 Q20.8 41.3 9.5 30.2 Q24.5 33.5 40 33.4 Q50.5 19.1',
    '           57.5 2.7 Q58 7.5 59.4 12.2"/>',
    '</symbol>',

    /* --- outlined heart, second hand  --------------------------------------*/
    '<symbol id="heart-line-b" viewBox="0 0 100 92">',
    '  <path fill="none" stroke="currentColor" stroke-width="6"',
    '        stroke-linecap="round" stroke-linejoin="round" filter="url(#rough)"',
    '        d="M48.6 87.8 C21 66.1 6.8 50.3 7.4 27.9 C3.5 15.6 13.7 4.6 30.4 5.1',
    '           C41.4 2.7 46.7 11.2 50.5 16.8 C55.7 8.9 61.1 5.4 66.5 6.4 C83.7 3',
    '           92.8 17.3 95.3 30.7 C92.9 51.6 76.1 68.6 48.6 87.8 C36.7 76.9 27',
    '           69.7 21.1 63.5"/>',
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
