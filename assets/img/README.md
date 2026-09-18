# Images

Put real images straight in this folder and point the pages at them.

**What the design expects:** cut-outs with a **transparent background**
(PNG or WebP). They sit flat on the cream — no frame, no drop shadow, no
rounded corners. Mix black-and-white cut-outs with full-colour ones:

```html
<img class="cutout"        src="assets/img/kazan-stage.png" alt="">
<img class="cutout cutout--bw" src="assets/img/portrait.png"   alt="">
```

Keep files reasonably small (long edge ~1600px is plenty) — GitHub Pages
serves them as-is, and there is no build step to optimise them.

`placeholder/` holds the stand-in art the site ships with. Delete that
folder once nothing references it any more.
