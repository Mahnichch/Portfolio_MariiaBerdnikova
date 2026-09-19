"""Build the two photographic pieces the About collage is made of.

From ONE photograph it produces both large elements in the reference layout:

  assets/img/about-cutout.png   the figure cut out, black and white, with a
                                thick cream sticker edge, transparent around
  assets/img/about-duotone.jpg  a blown-up crop of the same photograph,
                                flattened into two tones of the accent

This is NOT part of the site build — the site has no build step.

    pip install pillow numpy "rembg[cpu]"
    python3 tools/make-about-photos.py photo.jpg

The first run downloads a ~176MB segmentation model; after that it is
offline. Delete the cut-raw.png it caches before running on a new photo.
"""
import os
import sys

import numpy as np
from PIL import Image, ImageEnhance, ImageFilter, ImageOps

CUTOUT = 'cut-raw.png'
OUT_CUT = 'assets/img/about-cutout.png'
OUT_DUO = 'assets/img/about-duotone.jpg'

# Two tones the duotone maps onto: shadows and highlights.
DUO_DARK = (176, 74, 122)
DUO_LIGHT = (246, 206, 224)

EDGE = (247, 242, 233)      # cream, same as the page
CUT_W = 900                 # delivered width of the cut-out
DUO_W = 1100                # delivered width of the duotone panel


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


def sticker(fig, colour, thickness):
    """The cut-out's border: the silhouette grown outwards and filled."""
    grown = fig.split()[-1]
    step = 9
    for _ in range(max(1, thickness // (step // 2))):
        grown = grown.filter(ImageFilter.MaxFilter(step))
    grown = grown.filter(ImageFilter.GaussianBlur(thickness * 0.35))
    grown = grown.point(lambda v: 255 if v > 110 else 0)
    layer = Image.new('RGBA', fig.size, colour + (0,))
    layer.putalpha(grown)
    return layer


def build_cutout(scale=2):
    cut = Image.open(CUTOUT).convert('RGBA')
    cut = cut.crop(cut.split()[-1].getbbox())

    w = CUT_W * scale
    cut = cut.resize((w, round(cut.height * w / cut.width)), Image.LANCZOS)

    grey = ImageOps.grayscale(cut.convert('RGB'))
    grey = ImageOps.autocontrast(grey, cutoff=1)
    grey = ImageEnhance.Contrast(grey).enhance(1.25)
    fig = Image.merge('RGBA', (grey, grey, grey, cut.split()[-1]))

    edge = sticker(fig, EDGE, 16 * scale)
    # Room for the border, which grows outside the figure's own bounds.
    pad = 20 * scale
    canvas = Image.new('RGBA', (fig.width + pad * 2, fig.height + pad * 2),
                       (0, 0, 0, 0))
    canvas.paste(edge, (pad, pad), edge)
    canvas.paste(fig, (pad, pad), fig)

    canvas = canvas.crop(canvas.split()[-1].getbbox())

    # The photograph is cropped mid-skirt, so the figure ends on a straight
    # cut across fabric. Fade the last stretch out so it dissolves into the
    # page instead of stopping on a ruled line.
    h = canvas.height
    fade_from = int(h * 0.86)
    rows = np.arange(h)[:, None].astype(np.float32)
    ramp = np.clip((h - rows) / (h - fade_from), 0.0, 1.0)
    ramp = np.where(rows < fade_from, 1.0, ramp)
    alpha = np.asarray(canvas.split()[-1], dtype=np.float32)
    canvas.putalpha(Image.fromarray((alpha * ramp).astype(np.uint8)))

    out = canvas.resize((CUT_W, round(CUT_W * canvas.height / canvas.width)),
                        Image.LANCZOS)
    out.save(OUT_CUT, optimize=True)
    print('wrote', OUT_CUT, out.size, os.path.getsize(OUT_CUT) // 1024, 'KB')


def build_duotone(photo_path, crop=(0.18, 0.22, 0.98, 0.78)):
    """A blown-up crop of the same photograph, flattened to two tones. The
    reference does exactly this — its pink panel is the same person as the
    cut-out, enlarged until the picture goes soft."""
    im = Image.open(photo_path).convert('RGB')
    l, t, r, b = crop
    im = im.crop((int(l * im.width), int(t * im.height),
                  int(r * im.width), int(b * im.height)))
    im = im.resize((DUO_W, round(DUO_W * im.height / im.width)), Image.LANCZOS)

    grey = ImageOps.autocontrast(ImageOps.grayscale(im), cutoff=2)
    # Flatten the midtones so it reads as a printed panel, not a photograph.
    grey = ImageEnhance.Contrast(grey).enhance(0.72)

    g = np.asarray(grey, dtype=np.float32)[..., None] / 255.0
    dark = np.array(DUO_DARK, dtype=np.float32)
    light = np.array(DUO_LIGHT, dtype=np.float32)
    duo = dark + (light - dark) * g

    Image.fromarray(duo.astype(np.uint8)).save(OUT_DUO, quality=86,
                                               subsampling=1, optimize=True)
    print('wrote', OUT_DUO, os.path.getsize(OUT_DUO) // 1024, 'KB')


if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit('usage: python3 tools/make-about-photos.py PHOTO.jpg')
    photo = sys.argv[1]
    CUTOUT = cut_out(photo)
    build_cutout()
    build_duotone(photo)
