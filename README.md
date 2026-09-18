# Mariia Berdnikova — portfolio

A standalone static portfolio site. Plain HTML, CSS and JavaScript — **no
build step, no framework, no dependencies**. Open a file, edit it, save,
refresh.

## Files

```
index.html              the hero film + the project index
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
  video/hero.mp4        the front-page film (H.264)
  video/hero.webm       the same film (VP9)
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

**The front-page film** — `assets/video/hero.mp4` and `hero.webm` are the
same film in two formats; `index.html` lists both and the browser picks one,
so **replace both** or the swap only reaches some visitors. `.mov` files
straight off a phone usually will not work: they are often HEVC, which
Chrome and Firefox refuse to play. Convert with
[ffmpeg](https://ffmpeg.org) — from a source at `in.mov`:

```bash
ffmpeg -i in.mov -an -vf scale=1600:-2 -c:v libx264 -pix_fmt yuv420p \
  -crf 27 -preset slower -movflags +faststart assets/video/hero.mp4
ffmpeg -i in.mov -an -vf scale=1600:-2 -c:v libvpx-vp9 -crf 40 -b:v 0 \
  -row-mt 1 assets/video/hero.webm
ffmpeg -ss 0.2 -i in.mov -frames:v 1 -q:v 4 assets/img/hero-poster.jpg
```

`-an` drops the audio: browsers only autoplay muted video, and it keeps the
files small. The poster is what shows before the film loads and for anyone
who has asked their system for reduced motion — the film does not autoplay
for them, and a Play control appears instead.

**The front page** (`index.html`) — one full screen. From laptop width up
the film fills the viewport and everything over it (nav, corner labels,
scroll cue, pause control) is a cream label box so it stays readable on any
frame; the handwritten asides and scattered decoration are ink meant for a
cream page, so they show only on mobile, where the hero is a normal column.

The film is fitted, not cropped, unless the screen is 16:9 or wider. That is
deliberate: the closing card sets the handwritten name almost edge to edge,
so a horizontal crop cuts the first and last letters off. On a 16:10 laptop
you get the full width plus two thin cream bands, which is where the corner
labels sit. **If you replace the film with one whose content is not tight to
the frame edges**, you can drop that rule in `site.css` and let it always
`cover`.

Below the hero, `.work-list` is the project index; add or reorder rows.

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

Loaded from Google Fonts over the network: **Shantell Sans** (hand-drawn
display lettering and the handwritten asides), **Inter** (tiny uppercase
labels) and **Space Grotesk** (body). If they fail to load the page still
works and falls back to system faces.

Cyrillic: Shantell Sans and Inter both ship Cyrillic, so display titles and
labels can be written in Russian directly (`СХОДКА`, `Музон`). Space Grotesk
does not, so Cyrillic body text falls through to Inter — which is why Inter
follows it in the stack.

## Accessibility & graceful degradation

- Every decorative SVG is `aria-hidden`.
- With JavaScript off, all content is visible — only the entry animation
  and the hover underlines are skipped.
- `prefers-reduced-motion: reduce` turns off the animations and parallax.
- Below 860px the hero becomes an ordinary column and the collages stack.
