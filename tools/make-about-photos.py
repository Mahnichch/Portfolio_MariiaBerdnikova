"""Build the photographic pieces the About collage is made of.

Every piece is torn rather than cropped square, the way the reference is:
each photograph is masked with an irregular edge and given a thin paper lip
just outside it, so it reads as something ripped out and laid down.

    pip install pillow numpy "rembg[cpu]"
    python3 tools/make-about-photos.py

Photographs are read from PHOTOS below — edit those paths to use different
ones. The figure is cut out with a segmentation model (a ~176MB download on
first run, offline after that); everything else is a torn rectangle.

Outputs, all PNG because they all carry transparency:

  assets/img/about-figure.png    full-height cut-out, cream sticker edge
  assets/img/about-duotone.png   a different shot, blown up and flattened
                                 into two tones, torn on the two edges that
                                 do not run off the page
  assets/img/about-snap-1.png    torn photograph
  assets/img/about-snap-2.png    torn photograph
"""
import math
import os
import random
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageOps

# Which photograph plays which part. The figure wants a full-length shot —
# one cropped mid-body ends on a straight cut across fabric.
PHOTOS = {
    'figure':  'photos/4.jpg',
    'duotone': 'photos/1.jpg',
    'snap1':   'photos/5.jpg',
    'snap2':   'photos/6.jpg',
}

PAPER = (247, 242, 233)     # cream, same as the page
DUO_DARK = (176, 74, 122)
DUO_LIGHT = (246, 206, 224)


def torn_edge(length, amp, seed, steps=90):
    """A 1-D wandering edge: sine waves of falling amplitude, plus a little
    jitter. Low frequencies give the tear its overall drift, high ones the
    roughness."""
    rnd = random.Random(seed)
    waves = [(1, 0.45), (2, 0.28), (3, 0.18), (5, 0.12), (9, 0.08), (17, 0.05)]
    phases = [rnd.uniform(0, 2 * math.pi) for _ in waves]
    out = []
    for i in range(steps + 1):
        t = i / steps
        v = 0.0
        for (freq, a), ph in zip(waves, phases):
            v += a * math.sin(2 * math.pi * freq * t + ph)
        v = (v + 1.1) / 2.2                      # roughly 0..1
        v += rnd.uniform(-0.06, 0.06)
        out.append((t * length, max(0.0, min(1.0, v)) * amp))
    return out


def torn_mask(w, h, seed, amp=None, sides='trbl'):
    """A rectangle whose chosen sides are torn instead of straight."""
    amp = amp if amp is not None else min(w, h) * 0.035
    top = torn_edge(w, amp, seed + 1)
    right = torn_edge(h, amp, seed + 2)
    bottom = torn_edge(w, amp, seed + 3)
    left = torn_edge(h, amp, seed + 4)

    pts = []
    pts += [(x, v if 't' in sides else 0) for x, v in top]
    pts += [(w - (v if 'r' in sides else 0), y) for y, v in right]
    # reversed() already walks these edges back the way the outline needs to
    # go (right-to-left along the bottom, bottom-to-top up the left). Flipping
    # the coordinate as well sends them the wrong way and the polygon crosses
    # itself, which slices the picture corner to corner.
    pts += [(x, h - (v if 'b' in sides else 0)) for x, v in reversed(bottom)]
    pts += [(v if 'l' in sides else 0, y) for y, v in reversed(left)]

    mask = Image.new('L', (w, h), 0)
    ImageDraw.Draw(mask).polygon(pts, fill=255)
    return mask


def with_paper_lip(img, mask, lip):
    """Put a thin cream border just outside the torn edge — the pale fibre
    you get along a real tear, and what stops the photo dissolving into the
    page."""
    grown = mask
    step = 7
    for _ in range(max(1, int(lip) // (step // 2))):
        grown = grown.filter(ImageFilter.MaxFilter(step))

    out = Image.new('RGBA', img.size, PAPER + (0,))
    out.putalpha(grown)
    photo = img.convert('RGBA')
    photo.putalpha(mask)
    return Image.alpha_composite(out, photo)


def fit(path, width):
    im = Image.open(path).convert('RGB')
    return im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)


def build_figure(path, out, width=760, scale=2):
    """Cut the person out and give them a cream sticker edge."""
    cache = 'cut-' + os.path.basename(path) + '.png'
    if not os.path.exists(cache):
        from rembg import new_session, remove
        remove(Image.open(path).convert('RGB'),
               session=new_session('u2net_human_seg'),
               post_process_mask=True).save(cache)
    cut = Image.open(cache).convert('RGBA')
    cut = cut.crop(cut.split()[-1].getbbox())

    w = width * scale
    cut = cut.resize((w, round(cut.height * w / cut.width)), Image.LANCZOS)

    grey = ImageOps.grayscale(cut.convert('RGB'))
    grey = ImageOps.autocontrast(grey, cutoff=1)
    grey = ImageEnhance.Contrast(grey).enhance(1.22)
    fig = Image.merge('RGBA', (grey, grey, grey, cut.split()[-1]))

    grown = fig.split()[-1]
    step = 9
    for _ in range(max(1, (15 * scale) // (step // 2))):
        grown = grown.filter(ImageFilter.MaxFilter(step))
    grown = grown.filter(ImageFilter.GaussianBlur(15 * scale * 0.35))
    grown = grown.point(lambda v: 255 if v > 110 else 0)

    pad = 22 * scale
    canvas = Image.new('RGBA', (fig.width + pad * 2, fig.height + pad * 2),
                       (0, 0, 0, 0))
    edge = Image.new('RGBA', fig.size, PAPER + (0,))
    edge.putalpha(grown)
    canvas.paste(edge, (pad, pad), edge)
    canvas.paste(fig, (pad, pad), fig)

    canvas = canvas.crop(canvas.split()[-1].getbbox())
    res = canvas.resize((width, round(width * canvas.height / canvas.width)),
                        Image.LANCZOS)
    res.save(out, optimize=True)
    print('wrote', out, res.size, os.path.getsize(out) // 1024, 'KB')


def build_duotone(path, out, width=900, crop=(0.16, 0.20, 1.0, 0.82)):
    """A different shot, enlarged until it goes soft and flattened to two
    tones. It runs off the top and right of the page, so only the left and
    bottom edges are torn."""
    im = Image.open(path).convert('RGB')
    l, t, r, b = crop
    im = im.crop((int(l * im.width), int(t * im.height),
                  int(r * im.width), int(b * im.height)))
    im = im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)

    grey = ImageOps.autocontrast(ImageOps.grayscale(im), cutoff=2)
    grey = ImageEnhance.Contrast(grey).enhance(0.72)
    g = np.asarray(grey, dtype=np.float32)[..., None] / 255.0
    duo = np.array(DUO_DARK, np.float32) + \
        (np.array(DUO_LIGHT, np.float32) - np.array(DUO_DARK, np.float32)) * g
    duo = Image.fromarray(duo.astype(np.uint8))

    mask = torn_mask(duo.width, duo.height, seed=41,
                     amp=duo.width * 0.030, sides='lb')
    res = with_paper_lip(duo, mask, duo.width * 0.010)
    res.save(out, optimize=True)
    print('wrote', out, res.size, os.path.getsize(out) // 1024, 'KB')


def build_snap(path, out, seed, width=560, bw=False, crop=None):
    im = Image.open(path).convert('RGB')
    if crop:
        l, t, r, b = crop
        im = im.crop((int(l * im.width), int(t * im.height),
                      int(r * im.width), int(b * im.height)))
    im = im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)
    if bw:
        g = ImageOps.autocontrast(ImageOps.grayscale(im), cutoff=1)
        im = Image.merge('RGB', (g, g, g))

    mask = torn_mask(im.width, im.height, seed=seed, amp=im.width * 0.032)
    res = with_paper_lip(im, mask, im.width * 0.013)
    res.save(out, optimize=True)
    print('wrote', out, res.size, os.path.getsize(out) // 1024, 'KB')


if __name__ == '__main__':
    base = sys.argv[1] if len(sys.argv) > 1 else '.'
    p = {k: os.path.join(base, os.path.basename(v)) for k, v in PHOTOS.items()}

    build_figure(p['figure'], 'assets/img/about-figure.png')
    build_duotone(p['duotone'], 'assets/img/about-duotone.png')
    build_snap(p['snap1'], 'assets/img/about-snap-1.png', seed=7,
               crop=(0.20, 0.40, 0.82, 1.0))
    build_snap(p['snap2'], 'assets/img/about-snap-2.png', seed=23, bw=True,
               crop=(0.12, 0.46, 0.88, 1.0))
