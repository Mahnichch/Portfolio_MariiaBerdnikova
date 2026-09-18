# Mariia Berdnikova — portfolio

A standalone static portfolio site. Plain HTML, CSS and JavaScript — **no
build step, no framework, no dependencies**. Open a file, edit it, save,
refresh.

## Files

```
index.html              the hero + the project index
about.html
art.html                own visual work (placeholder slots)
contact.html
projects/
  moozeon.html          MoozeOn / Музон      — ultramarine
  shodka.html           Сходка               — hot pink
  dartfest.html         Dartfest 2025        — rust
  yummy-music.html      Yummy Music          — acid green
  short-film.html       Short film           — rust
  research.html         Music & liminality   — ultramarine
assets/
  css/site.css          all styling, commented by section
  js/sprite.js          the decorative SVG set (stars, scribbles, arrows…)
  js/site.js            entry stagger, hover underlines, scroll parallax
  img/placeholder/      stand-in art — replace with real images
.nojekyll               stops GitHub Pages running the files through Jekyll
```

## Editing

**Text** — edit the HTML directly. Anything still to be filled in is marked
with a `TODO` comment.

**Page accent colour** — each page picks one of four accents in its very
first tag: `<html lang="en" data-accent="pink">`. Valid values: `pink`,
`green`, `blue`, `rust`. That one attribute recolours the whole page.

**Photos** — drop real images into `assets/img/` and point the `src` at
them. They should be **cut-outs with a transparent background** (PNG or
WebP); the design places them flat on the cream with no frame, shadow or
rounded corner. Add `class="cutout cutout--bw"` for a black-and-white one,
`class="cutout"` for full colour. Delete `assets/img/placeholder/` once
nothing points at it.

**The front page** (`index.html`) — one full-bleed screen: the pink wordmark
(`.wordmark`) sits behind the cut-out figure (`.hero-figure`), with the
handwritten asides (`.scrawl`) and the corner labels around them. The
wordmark's vertical position is a tuned `translateY` in the CSS, because
Bagel Fat One's metrics put its ink well below its line box — if you swap
that font, retune that one value. Below the hero, `.work-list` is the
project index; add or reorder rows there.

**Collages** (project pages, `art.html`) — every item is placed with
`--x`, `--y`, `--w`, `--rot` and `--z` inline. Keep it uneven: vary the
widths, nudge the rotations a degree or two, and let items overlap by
giving neighbours close coordinates. Below 860px they stop being
absolutely positioned and stack automatically.

## Preview locally

The pages load a shared SVG sprite and use relative paths, so run a tiny
web server rather than opening the files straight off disk:

```bash
python3 -m http.server 8000
```

Then open <http://localhost:8000>.

## Deploy to GitHub Pages

1. Repository → **Settings** → **Pages**.
2. **Source**: *Deploy from a branch*.
3. **Branch**: `main`, folder `/ (root)` → **Save**.
4. Wait a minute; the URL appears at the top of the same page.

The site then lands at `https://mahnichch.github.io/Portfolio_MariiaBerdnikova/`.

Pages is free on public repositories. If you make this repo private, Pages
stops working unless you are on a paid GitHub plan.

Keep `.nojekyll`: without it GitHub ignores files and folders starting with
an underscore.

### Custom domain

Add a file named `CNAME` at the root containing just the domain
(`mariia.example`), then point the domain's DNS at GitHub Pages and set it
under Settings → Pages → Custom domain.

## Fonts

Loaded from Google Fonts over the network: **Bagel Fat One** (the fat pink
wordmark on the front page), **Shantell Sans** (hand-drawn display lettering
and the handwritten asides), **Inter** (tiny uppercase labels) and **Space
Grotesk** (body). If they fail to load the page still works and falls back
to system faces.

Cyrillic: Shantell Sans and Inter both ship Cyrillic, so display titles and
labels can be written in Russian directly (`СХОДКА`, `Музон`). Space Grotesk
does not, so Cyrillic body text falls through to Inter — which is why Inter
follows it in the stack. Bagel Fat One has no Cyrillic, so the front-page
wordmark stays Latin.

## Accessibility & graceful degradation

- Every decorative SVG is `aria-hidden`.
- With JavaScript off, all content is visible — only the entry animation
  and the hover underlines are skipped.
- `prefers-reduced-motion: reduce` turns off the animations and parallax.
- Below 860px the hero becomes an ordinary column and the collages stack.
