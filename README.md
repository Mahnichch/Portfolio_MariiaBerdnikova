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
  moozeon.html          MoozeOn              — ultramarine
  shodka.html           Shodka               — hot pink
  dartfest.html         Dartfest 2025        — rust
  yummy-music.html      Yummy Music          — acid green
  short-film.html       Short film           — rust
  research.html         Music & liminality   — ultramarine
tools/
  make-about-photos.py   rebuilds the two About photo pieces
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
the film fills the viewport and the only things over it are the nav, the two
corner labels, the scroll cue and the pause control — all cream label boxes,
so they stay readable on any frame. Nothing else sits on the film: the
handwritten greeting lives below it, at the head of the project list, where
it can lie straight on the cream. That is not decoration-shyness — behind
that corner the film swings from near-white plaid to dark sky to plum, so no
single text colour stays legible and anything placed there needs a backing
box, which looked like a dialog.

The film fills the screen from 16:10 up, which covers every common laptop
and monitor. That threshold is measured rather than guessed: the handwritten
name on the closing card leaves a 5.69% margin to the frame edge, and
cropping to 16:10 takes 5.0% off each side — inside it. Squarer windows fall
back to fitting the full width with thin cream bands, because cropping them
further would cut the first and last letters off the name. **If you replace
the film with one whose content is not tight to the frame edges**, drop the
`min-aspect-ratio` rule in `site.css` and let it always `cover`.

On a phone the hero is deliberately **not** a full screen. The film is 16:9,
so on a tall narrow screen it can only ever be a band across the middle, and
stretching the hero to 100vh just adds empty cream above and below it. It is
sized to its contents instead, the film runs edge to edge, and the greeting
and the first project rows land inside the first screen.

Below the hero, `.work-list` is the project index; add or reorder rows.

**Collages** (project pages, `art.html`) — every item is placed with
`--x`, `--y`, `--w`, `--rot` and `--z` inline. Keep it uneven: vary the
widths, nudge the rotations a degree or two, and let items overlap by
giving neighbours close coordinates. Below 860px they stop being
absolutely positioned and stack automatically.

## The About page

About is a pinned-up collage rather than a column: notes with torn edges,
taped photographs at varied sizes and angles, and the cut-out collage as its
anchor. Every piece is a `.scrap` placed with `--x`, `--y`, `--w` and
`--rot` inline, the same system the project collages use, so rearranging it
means editing those four numbers. Below 860px they stop being positioned and
stack.

It borrows the *arrangement* of a scrapbook but not its finish — no sepia,
no ageing, no vintage. The ground is warm cream carrying a fine paper fibre:
`--paper` in `site.css`, a seamlessly tiling `feTurbulence` written inline as
a data URI, so it costs no extra request. It sits about eight levels below
the flat cream and can be dialled with the `amplitude` in its `feFuncA` — or
removed entirely by deleting `background-image` from `body`.

Every photograph on it is **torn rather than cropped square**, and they come
from four different shots — the same thing the reference does. Rebuild them
all from new photographs with:

```bash
pip install pillow numpy "rembg[cpu]"
python3 tools/make-about-photos.py path/to/photos
```

Which photo plays which part is the `PHOTOS` dict at the top of that script:

- **figure** — cut out and given a cream sticker edge. Give it a
  **full-length** shot: one cropped mid-body ends on a straight cut across
  fabric. If the background was erased by hand and saved as a JPEG (so the
  transparency arrived as flat black), leave `FIGURE_IS_KEYED = True` and
  the black is removed by filling the figure's enclosed holes — a plain
  brightness threshold punches straight through dark shoes.
- **duotone** — a different shot, blown up until it goes soft and flattened
  to two tones. It runs off the top and right of the page, so only its left
  and bottom edges are torn.
- **snap1 / snap2** — torn photographs; `crop` in each `build_snap` call
  frames them, and `bw=True` drops them to black and white. The page sets a
  pink star behind snap1.

Small blank scraps of torn paper are scattered between the pieces:
`<div class="scrap note paper-bit">` with a `--h`, reusing the note's tear.

The tear itself is `torn_edge()`: sine waves of falling amplitude around
each side, so the low frequencies drift and the high ones roughen. A thin
cream lip is grown just outside the tear — the pale fibre you get along a
real rip, and what stops a photograph dissolving into the page.

Two details worth knowing before you edit it:

- **Notes are `#fffdf7`, slightly lighter than the page.** They have to be:
  cream on cream makes the torn edge invisible and the note reads as a plain
  block of text.
- **The tear is a `clip-path` polygon**, not an image. There are two of them
  (`.note` and `.note--b`) so notes side by side do not repeat the same
  edge.

The photo slots are marked `TODO` in `about.html`. Drop real images in and
delete the comment.

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

Three voices, named once at the top of `site.css` as `--font-display`,
`--font-label` and `--font-body`, so swapping one is a single line:

- **Rock Salt** — the rough handwritten display face, for big lettering and
  the handwritten asides.
- **Inter** — tiny uppercase labels.
- **Space Grotesk** — body copy.

Nothing else should introduce a fourth face. If they fail to load the page
still works and falls back to system faces.

The site is written in Latin throughout: the projects are called **MoozeOn**
and **Shodka**, not by their Russian names, because the Russian reads as
noise to anyone who cannot decode it. That means the display face needs no
Cyrillic — Rock Salt has none — and carries no fallback for it.

Rock Salt sets much wider and taller than a normal face. If you swap it,
expect to retune the display sizes.

If you ever do need Russian on a page, note that Rock Salt and Space Grotesk
have no Cyrillic; Inter does, which is why it follows Space Grotesk in the
body stack.

## Accessibility & graceful degradation

- Every decorative SVG is `aria-hidden`.
- With JavaScript off, all content is visible — only the entry animation
  and the hover underlines are skipped.
- `prefers-reduced-motion: reduce` turns off the animations and parallax.
- Below 860px the hero becomes an ordinary column and the collages stack.
