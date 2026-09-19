"""Build the about-page collage from a photograph.

Cuts the person out, turns them black and white, gives them a sticker
outline, and sets them on a flat colour ground with hand-drawn stars and
dashed circles.

This is NOT part of the site build — the site itself has no build step. It is
a one-off tool for regenerating assets/img/about-collage.jpg from a new
photo. See the README.

    pip install pillow numpy "rembg[cpu]"
    python3 tools/make-about-collage.py photo.jpg

The first run downloads a ~176MB segmentation model. Everything is drawn at
2x and downscaled, which is what keeps the star points and the sticker edge
clean.
"""
import math
import random
import sys

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageOps

S = 2                      # supersample factor
W, H = 900, 1600           # final size (9:16, same shape as the reference)
CW, CH = W * S, H * S
CUTOUT = 'cut-raw.png'


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


def cut_out(photo_path, cache='cut-raw.png'):
    """Remove the background. u2net_human_seg is the person-specific model;
    it holds hair edges far better than the general one."""
    import os
    if os.path.exists(cache):
        return cache
    from rembg import new_session, remove
    im = Image.open(photo_path).convert('RGB')
    out = remove(im, session=new_session('u2net_human_seg'), post_process_mask=True)
    out.save(cache)
    return cache


def build(bg_rgb, star_rgb, outline_rgb, ring_rgb, out_path):
    canvas = Image.new('RGB', (CW, CH), bg_rgb)
    draw = ImageDraw.Draw(canvas, 'RGBA')

    # --- dashed rings, sitting quietly in the ground -----------------------
    for (x, y, r, w) in [(0.10, 0.07, 0.10, 3), (0.86, 0.20, 0.13, 3),
                         (0.05, 0.62, 0.09, 3), (0.93, 0.74, 0.16, 3)]:
        dashed_circle(draw, x * CW, y * CH, r * CW, ring_rgb + (150,),
                      w * S, dash=16 * S, gap=14 * S, rot=x * 3)

    # --- a thin rule, as in the reference ---------------------------------
    draw.line([(0.965 * CW, 0), (0.965 * CW, 0.30 * CH)],
              fill=ring_rgb + (120,), width=2 * S)

    # --- stars behind the figure ------------------------------------------
    behind = [(0.13, 0.17, 0.115, 0.20, 1), (0.90, 0.47, 0.145, -0.30, 2),
              (0.78, 0.10, 0.052, 0.60, 3), (0.055, 0.42, 0.040, 0.2, 8)]
    for i, (x, y, r, rot, seed) in enumerate(behind):
        star(draw, x * CW, y * CH, r * CW, star_rgb, rot=rot, seed=seed)

    # --- the figure --------------------------------------------------------
    cut = Image.open(CUTOUT).convert('RGBA')
    box = cut.split()[-1].getbbox()
    cut = cut.crop(box)

    # Black and white, pushed for contrast, the way the reference reads.
    rgb = ImageOps.grayscale(cut.convert('RGB'))
    rgb = ImageOps.autocontrast(rgb, cutoff=1)
    rgb = ImageEnhance.Contrast(rgb).enhance(1.22)
    rgb = ImageEnhance.Brightness(rgb).enhance(1.06)
    fig = Image.merge('RGBA', (rgb, rgb, rgb, cut.split()[-1]))

    target_h = int(CH * 0.80)
    scale = target_h / fig.height
    fig = fig.resize((int(fig.width * scale), target_h), Image.LANCZOS)

    fx = (CW - fig.width) // 2
    fy = CH - fig.height          # stand her on the bottom edge, so the
                                  # photo's own crop is not read as a cut
    border = sticker(fig, outline_rgb, 13 * S)
    canvas.paste(border, (fx, fy), border)
    canvas.paste(fig, (fx, fy), fig)

    # --- stars in front, overlapping her and the edges ---------------------
    front = [(0.06, 0.88, 0.135, 0.15, 4), (0.72, 0.84, 0.100, -0.5, 5),
             (0.86, 0.22, 0.045, 0.3, 6)]
    draw2 = ImageDraw.Draw(canvas, 'RGBA')
    for (x, y, r, rot, seed) in front:
        star(draw2, x * CW, y * CH, r * CW, star_rgb, rot=rot, seed=seed)

    canvas.resize((W, H), Image.LANCZOS).save(out_path, quality=90,
                                              subsampling=1, optimize=True)
    print('wrote', out_path)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit('usage: python3 tools/make-about-collage.py PHOTO.jpg [cream]')

    CUTOUT = cut_out(sys.argv[1])
    cream = len(sys.argv) > 2 and sys.argv[2] == 'cream'

    if cream:
        # The site's own palette: ultramarine ground, cream stars and edge.
        build((34, 51, 221), (247, 242, 233), (247, 242, 233),
              (150, 165, 255), 'assets/img/about-collage.jpg')
    else:
        # Electric blue with yellow stars, as used on the site.
        build((47, 67, 252), (245, 228, 106), (245, 228, 106),
              (150, 170, 255), 'assets/img/about-collage.jpg')
