"""Build the about-page collage from a photograph.

Cuts the person out, turns them black and white, gives them a sticker
outline, and sets them on a torn organic patch of flat colour with
hand-drawn stars and dashed rings. The patch is deliberately NOT a
rectangle: on the page it lies flat on the cream like the site's other
cut-outs, so it is saved as a PNG with a transparent surround.

This is NOT part of the site build — the site itself has no build step. It is
a one-off tool for regenerating assets/img/about-collage.png from a new
photo. See the README.

    pip install pillow numpy "rembg[cpu]"
    python3 tools/make-about-collage.py photo.jpg

The first run downloads a ~176MB segmentation model. Everything is drawn at
2x and downscaled, which is what keeps the star points and the torn edge
clean.
"""
import math
import os
import random
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageOps

S = 2                      # supersample factor
# The image never displays wider than ~360 CSS px, so 760 is already 2x
# for a retina screen; larger would only cost bytes.
W, H = 760, 1351           # final size
CW, CH = W * S, H * S
CUTOUT = 'cut-raw.png'
OUT = 'assets/img/about-collage.png'


def cut_out(photo_path, cache=CUTOUT):
    """Remove the background. u2net_human_seg is the person-specific model;
    it holds hair edges far better than the general one."""
    if os.path.exists(cache):
        return cache
    from rembg import new_session, remove
    im = Image.open(photo_path).convert('RGB')
    out = remove(im, session=new_session('u2net_human_seg'),
                 post_process_mask=True)
    out.save(cache)
    return cache


def star(draw, cx, cy, r, colour, rot=0.0, inner=0.44, jitter=0.05, seed=0):
    """A five-point star with slightly uneven points, so it reads as drawn
    rather than generated."""
    rnd = random.Random(seed)
    pts = []
    for i in range(10):
        ang = rot + i * math.pi / 5 - math.pi / 2
        rad = r if i % 2 == 0 else r * inner
        rad *= 1 + rnd.uniform(-jitter, jitter)
        ang += rnd.uniform(-jitter, jitter) * 0.5
        pts.append((cx + rad * math.cos(ang), cy + rad * math.sin(ang)))
    draw.polygon(pts, fill=colour)


def dashed_circle(draw, cx, cy, r, colour, width, dash=14, gap=12, rot=0.0):
    step = (dash + gap) / r          # radians per dash+gap
    a = rot
    while a < rot + 2 * math.pi:
        b = min(a + dash / r, rot + 2 * math.pi)
        draw.arc([cx - r, cy - r, cx + r, cy + r],
                 math.degrees(a), math.degrees(b), fill=colour, width=width)
        a += step


def torn_patch(seed=11):
    """The organic ground the collage sits on: an off-round shape whose edge
    wanders, built by summing sine waves around the radius. The low
    frequencies give it its lopsided overall shape, the high ones the torn
    edge — without the high ones it reads as a blob, without the low ones as
    a wobbly circle."""
    rnd = random.Random(seed)
    waves = [(2, 0.070), (3, 0.055), (5, 0.030), (8, 0.020),
             (13, 0.013), (21, 0.009), (34, 0.006)]
    phases = [rnd.uniform(0, 2 * math.pi) for _ in waves]

    # The wave amplitudes sum to ~0.20, so the radius can swell to 1.2x. The
    # base radii have to leave room for that, or the frame slices the edge
    # flat — which is the straight edge this whole shape exists to avoid.
    # The surplus margin costs nothing: the image is cropped to the shape at
    # the end.
    cx, cy = CW * 0.50, CH * 0.50
    rx, ry = CW * 0.400, CH * 0.400

    pts = []
    steps = 1440
    for i in range(steps):
        t = 2 * math.pi * i / steps
        k = 1.0
        for (freq, amp), ph in zip(waves, phases):
            k += amp * math.sin(freq * t + ph)
        pts.append((cx + rx * k * math.cos(t), cy + ry * k * math.sin(t)))

    mask = Image.new('L', (CW, CH), 0)
    ImageDraw.Draw(mask).polygon(pts, fill=255)
    # Soften then re-threshold: rounds off the sharpest spikes without
    # straightening the wander.
    mask = mask.filter(ImageFilter.GaussianBlur(3 * S))
    mask = mask.point(lambda v: 255 if v > 128 else 0)
    return mask


def sticker(cut, colour, thickness):
    """Return a layer holding the figure's silhouette, grown by `thickness`,
    filled with `colour` — the cut-out's border."""
    alpha = cut.split()[-1]
    grown = alpha
    step = 9
    for _ in range(max(1, thickness // (step // 2))):
        grown = grown.filter(ImageFilter.MaxFilter(step))
    # Smooth the square-kernel staircase into a cut edge.
    grown = grown.filter(ImageFilter.GaussianBlur(thickness * 0.35))
    grown = grown.point(lambda v: 255 if v > 110 else 0)
    layer = Image.new('RGBA', cut.size, colour + (0,))
    layer.putalpha(grown)
    return layer


def build(bg_rgb, star_rgb, outline_rgb, ring_rgb, out_path):
    patch = torn_patch()

    # --- the coloured ground, clipped to the torn patch --------------------
    ground = Image.new('RGBA', (CW, CH), bg_rgb + (255,))
    draw = ImageDraw.Draw(ground, 'RGBA')

    for (x, y, r, w) in [(0.24, 0.12, 0.10, 3), (0.78, 0.22, 0.12, 3),
                         (0.18, 0.62, 0.09, 3), (0.82, 0.72, 0.14, 3)]:
        dashed_circle(draw, x * CW, y * CH, r * CW, ring_rgb + (150,),
                      w * S, dash=16 * S, gap=14 * S, rot=x * 3)

    for (x, y, r, rot, seed) in [(0.25, 0.17, 0.100, 0.20, 1),
                                 (0.82, 0.46, 0.125, -0.30, 2),
                                 (0.72, 0.12, 0.046, 0.60, 3),
                                 (0.17, 0.44, 0.036, 0.20, 8)]:
        star(draw, x * CW, y * CH, r * CW, star_rgb, rot=rot, seed=seed)

    ground.putalpha(patch)

    # --- the figure --------------------------------------------------------
    cut = Image.open(CUTOUT).convert('RGBA')
    cut = cut.crop(cut.split()[-1].getbbox())

    rgb = ImageOps.grayscale(cut.convert('RGB'))
    rgb = ImageOps.autocontrast(rgb, cutoff=1)
    rgb = ImageEnhance.Contrast(rgb).enhance(1.22)
    rgb = ImageEnhance.Brightness(rgb).enhance(1.06)
    fig = Image.merge('RGBA', (rgb, rgb, rgb, cut.split()[-1]))

    target_h = int(CH * 0.62)
    scale = target_h / fig.height
    fig = fig.resize((int(fig.width * scale), target_h), Image.LANCZOS)

    fx = (CW - fig.width) // 2
    fy = int(CH * 0.860) - fig.height

    # Outline under the figure, both on one layer so they clip together.
    person = Image.new('RGBA', (CW, CH), (0, 0, 0, 0))
    border = sticker(fig, outline_rgb, 13 * S)
    person.paste(border, (fx, fy), border)
    person.paste(fig, (fx, fy), fig)

    # The photograph is cropped at her skirt, so her lower edge is a straight
    # cut across the fabric. Two things hide it. First the hem is faded out
    # over the lower fifth of the figure, so it dissolves into the ground
    # instead of stopping on a ruled line. Second, below that same point the
    # figure is clipped to the patch, so it can never hang outside the torn
    # edge. Above it nothing is touched, and hair and shoulders still
    # overhang the patch.
    fade_top = fy + fig.height * 0.84
    hem = fy + fig.height
    rows = np.arange(CH)[:, None].astype(np.float32)
    ramp = np.clip((hem - rows) / (hem - fade_top), 0.0, 1.0)
    ramp = np.where(rows < fade_top, 1.0, ramp)

    pa = np.array(person.split()[-1], dtype=np.float32)
    pm = np.array(patch, dtype=np.float32) / 255.0
    inside = np.where(rows < fade_top, 1.0, pm)
    person.putalpha(Image.fromarray((pa * ramp * inside).astype(np.uint8)))

    canvas = Image.alpha_composite(ground, person)

    # --- stars in front, a couple spilling off the patch onto the page -----
    front = Image.new('RGBA', (CW, CH), (0, 0, 0, 0))
    d2 = ImageDraw.Draw(front, 'RGBA')
    for (x, y, r, rot, seed) in [(0.13, 0.83, 0.105, 0.15, 4),
                                 (0.70, 0.79, 0.085, -0.5, 5),
                                 (0.79, 0.26, 0.040, 0.3, 6),
                                 (0.06, 0.33, 0.052, 0.1, 9)]:
        star(d2, x * CW, y * CH, r * CW, star_rgb, rot=rot, seed=seed)
    canvas = Image.alpha_composite(canvas, front)

    # Crop away the transparent surround so the file is the shape and not a
    # mostly-empty rectangle, then scale to the delivered width.
    canvas = canvas.crop(canvas.split()[-1].getbbox())
    out_h = round(W * canvas.height / canvas.width)
    canvas.resize((W, out_h), Image.LANCZOS).save(out_path, optimize=True)
    print('wrote', out_path, f'{W}x{out_h}', os.path.getsize(out_path) // 1024, 'KB')


if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit('usage: python3 tools/make-about-collage.py PHOTO.jpg [cream]')

    CUTOUT = cut_out(sys.argv[1])
    cream = len(sys.argv) > 2 and sys.argv[2] == 'cream'

    if cream:
        # The site's own palette: ultramarine ground, cream stars and edge.
        build((34, 51, 221), (247, 242, 233), (247, 242, 233),
              (150, 165, 255), OUT)
    else:
        # Electric blue with yellow stars, as used on the site.
        build((47, 67, 252), (245, 228, 106), (245, 228, 106),
              (150, 170, 255), OUT)
