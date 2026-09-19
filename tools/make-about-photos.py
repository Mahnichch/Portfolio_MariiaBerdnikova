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
    'figure':  '7.jpg',     # already cut out by hand, exported on black
    'duotone': '1.jpg',
    'snap1':   '10.jpg',
    'snap2':   '6.jpg',
}

# Set for a photograph whose background was erased by hand and exported as a
# JPEG, so the transparency arrived as flat black.
FIGURE_IS_KEYED = True

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


def key_black(path, cutoff=16):
    """Drop a flat black background that came from a hand-made cut-out saved
    as JPEG.

    A plain brightness threshold will not do: parts of her trainers are pure
    black too, so thresholding punches holes straight through them. Instead
    the non-black pixels are taken as the figure and its *enclosed* holes are
    filled back in, which recovers the dark shoe without bringing back the
    background — only black connected to the outside is dropped.

    (Not ImageDraw.floodfill: it still exists in Pillow 12 but does nothing,
    filling zero pixels and silently leaving the background opaque.)"""
    from scipy import ndimage

    im = Image.open(path).convert('RGB')
    arr = np.asarray(im).max(axis=2)

    figure = ndimage.binary_fill_holes(arr > cutoff)
    alpha = np.where(figure, 255, 0).astype(np.uint8)
    alpha = Image.fromarray(alpha, 'L')
    # Pull the edge in a touch to lose the dark JPEG fringe, then soften it.
    alpha = alpha.filter(ImageFilter.MinFilter(5))
    alpha = alpha.filter(ImageFilter.GaussianBlur(1.2))

    out = im.convert('RGBA')
    out.putalpha(alpha)
    return out.crop(out.split()[-1].getbbox())


def build_figure(path, out, width=760, scale=2, keyed=False):
    """Cut the person out and give them a cream sticker edge."""
    if keyed:
        cut = key_black(path)
    else:
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


def drawn_star(size, colour, points=5, inner=0.33, rot=-0.12, seed=5,
               bow=0.16):
    """A star that looks drawn with a marker rather than plotted: the sides
    of each point bow inwards, every vertex is nudged off its true position,
    and the whole thing is drawn at 4x and scaled down so the curves stay
    smooth."""
    S = 4
    n = size * S
    rnd = random.Random(seed)
    cx = cy = n / 2
    R = n * 0.49

    verts = []
    for i in range(points * 2):
        ang = rot + i * math.pi / points - math.pi / 2
        rad = R * (1 if i % 2 == 0 else inner)
        rad *= 1 + rnd.uniform(-0.085, 0.085)
        ang += rnd.uniform(-0.055, 0.055)
        verts.append((cx + rad * math.cos(ang), cy + rad * math.sin(ang)))

    # Walk each edge as a quadratic curve whose control point is pulled back
    # towards the middle, which is what gives the points their concave taper.
    path = []
    for i in range(len(verts)):
        p0 = verts[i]
        p1 = verts[(i + 1) % len(verts)]
        mx, my = (p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2
        # Each edge bows by a different amount, and some of them bow the
        # wrong way — an evenly tapered star is the thing that gives a
        # generated shape away.
        b = bow * rnd.uniform(0.35, 1.5)
        ctrl = (mx + (cx - mx) * b, my + (cy - my) * b)
        dx, dy = p1[0] - p0[0], p1[1] - p0[1]
        ln = math.hypot(dx, dy) or 1
        k = ln * rnd.uniform(-0.05, 0.05)
        ctrl = (ctrl[0] - dy / ln * k, ctrl[1] + dx / ln * k)
        for s in range(9):
            t = s / 9
            u = 1 - t
            path.append((u * u * p0[0] + 2 * u * t * ctrl[0] + t * t * p1[0],
                         u * u * p0[1] + 2 * u * t * ctrl[1] + t * t * p1[1]))

    layer = Image.new('RGBA', (n, n), (0, 0, 0, 0))
    ImageDraw.Draw(layer).polygon(path, fill=colour + (255,))
    return layer.resize((size, size), Image.LANCZOS)


def build_star_snap(path, out, seed, width=560, crop=None, star_scale=0.78,
                    star_dx=0.08, star_dy=-0.20, star_rot=9,
                    star_colour=(244, 132, 178)):
    """A torn photograph with a drawn star set BEHIND the person — inside the
    frame, between her and the background, the way the reference has it. That
    needs her segmented out of her own photograph so the star can go in
    between."""
    im = Image.open(path).convert('RGB')
    if crop:
        l, t, r, b = crop
        im = im.crop((int(l * im.width), int(t * im.height),
                      int(r * im.width), int(b * im.height)))
    im = im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)

    g = ImageOps.autocontrast(ImageOps.grayscale(im), cutoff=1)
    flat = Image.merge('RGB', (g, g, g)).convert('RGBA')

    # The mask belongs to one particular crop, so the crop is part of its
    # name — reusing a mask cut from a different framing silently misplaces
    # her, and the star then goes in front of an edge it should be behind.
    tag = '-'.join('%.2f' % c for c in crop) if crop else 'full'
    cache = 'cut-snapstar-%s-%s.png' % (os.path.basename(path), tag)
    if not os.path.exists(cache):
        from rembg import new_session, remove
        remove(im, session=new_session('u2net_human_seg'),
               post_process_mask=True).save(cache)
    person_alpha = Image.open(cache).convert('RGBA').split()[-1]
    person = flat.copy()
    person.putalpha(person_alpha)

    star_size = int(min(flat.size) * star_scale)
    star = drawn_star(star_size, star_colour, seed=seed,
                      rot=math.radians(star_rot))
    # Tilted, and set high and slightly right, so that all five points clear
    # her outline. A star centred behind her cannot work at any size: its two
    # lower points land on her chest, which is why only three of them used to
    # show. Up here her head crosses one point instead of swallowing two, so
    # the star still reads as being behind her.
    sx = int(flat.width * (0.5 + star_dx)) - star_size // 2
    sy = int(flat.height * (0.5 + star_dy)) - star_size // 2

    composed = flat.copy()
    composed.alpha_composite(star, (sx, sy))
    composed.alpha_composite(person)
    im = composed.convert('RGB')

    mask = torn_mask(im.width, im.height, seed=seed, amp=im.width * 0.032)
    res = with_paper_lip(im, mask, im.width * 0.013)
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


if __name__ == '__main__':
    base = sys.argv[1] if len(sys.argv) > 1 else '.'
    p = {k: os.path.join(base, os.path.basename(v)) for k, v in PHOTOS.items()}

    build_figure(p['figure'], 'assets/img/about-figure.png',
                 keyed=FIGURE_IS_KEYED)
    build_duotone(p['duotone'], 'assets/img/about-duotone.png')
    # Black and white, with a drawn star behind her inside the frame.
    # The full frame, not a tight crop: she has to sit small enough in it to
    # leave the star somewhere to put its points.
    build_star_snap(p['snap1'], 'assets/img/about-snap-1.png', seed=7)
    build_snap(p['snap2'], 'assets/img/about-snap-2.png', seed=23, bw=True,
               crop=(0.12, 0.46, 0.88, 1.0))
