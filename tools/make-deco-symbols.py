#!/usr/bin/env python3
"""Generate the star and heart path data for assets/js/sprite.js.

Drawn in the manner of the reference sheet: solid shapes with confident,
smooth outlines and deeply concave sides, so each point tapers to a needle.
They are NOT scratchy. An earlier version jittered every vertex and ran the
result through a turbulence filter, which made the shapes wobble rather than
look drawn — the irregularity here is slight and in the silhouette, and the
filter is off for these symbols.

Run it and paste the printed block into sprite.js. It is a one-off author
tool, not a build step — the site ships the literal path data.
"""
import math
import random


def fmt(v):
    s = '%.1f' % v
    return s.rstrip('0').rstrip('.') if '.' in s else s


def pt(p):
    return '%s %s' % (fmt(p[0]), fmt(p[1]))


def star_path(cx=50, cy=50, r=48, points=5, inner=0.38, rot=0.0,
              seed=1, jitter=0.03, bow=0.30):
    """A star whose sides curve IN towards the middle. That concave taper is
    what makes a drawn star read as drawn; a straight-sided one reads as
    plotted however much its vertices are nudged about."""
    rnd = random.Random(seed)
    verts = []
    for i in range(points * 2):
        ang = rot + i * math.pi / points - math.pi / 2
        rad = r if i % 2 == 0 else r * inner
        rad *= 1 + rnd.uniform(-jitter, jitter)
        ang += rnd.uniform(-jitter, jitter) * 0.5
        verts.append((cx + rad * math.cos(ang), cy + rad * math.sin(ang)))

    d = ['M' + pt(verts[0])]
    for i in range(1, len(verts) + 1):
        a, b = verts[i - 1], verts[i % len(verts)]
        mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
        k = bow * rnd.uniform(0.82, 1.18)
        ctrl = (mx + (cx - mx) * k, my + (cy - my) * k)
        d.append('Q%s %s' % (pt(ctrl), pt(b)))
    return ' '.join(d) + 'Z'


def heart_path(seed=1, jitter=1.4, lean=0.0):
    """Lopsided by a little, smooth everywhere — a heart someone drew in one
    confident pass, not one sketched over and over."""
    rnd = random.Random(seed)

    def j(p, amt=1.0):
        return (p[0] + rnd.uniform(-jitter, jitter) * amt,
                p[1] + rnd.uniform(-jitter, jitter) * amt)

    tip = j((50 + lean, 88), 0.4)
    left = j((4, 30))
    lobe_l = j((28, 3))
    notch = j((50, 19), 0.5)
    lobe_r = j((71, 4))
    right = j((96, 31))

    seg = [
        (j((22, 68)), j((5, 49)), left),
        (j((3, 13)), j((15, 3)), lobe_l),
        (j((39, 3), 0.6), j((46, 12), 0.6), notch),
        (j((55, 11), 0.6), j((62, 3), 0.6), lobe_r),
        (j((84, 3)), j((97, 14)), right),
        (j((95, 50)), j((79, 68)), tip),
    ]
    d = ['M' + pt(tip)]
    for c1, c2, end in seg:
        d.append('C%s %s %s' % (pt(c1), pt(c2), pt(end)))
    return ' '.join(d) + 'Z'


if __name__ == '__main__':
    out = [
        ('star-5',      star_path(seed=4, points=5, inner=0.42, bow=0.17)),
        ('star-line',   star_path(seed=11, r=45, points=5, inner=0.42, bow=0.17)),
        ('star-line-b', star_path(seed=23, r=45, points=5, inner=0.43,
                                  rot=0.16, bow=0.16)),
        ('star-6',      star_path(seed=7, points=6, inner=0.46, bow=0.30)),
        ('star-8',      star_path(seed=9, points=8, inner=0.40, bow=0.34)),
        # The four-point sparkle from the sheet: almost no body, all taper.
        ('star-4',      star_path(seed=13, points=4, inner=0.20, bow=0.52)),
        ('star-4-b',    star_path(seed=31, points=4, inner=0.17, rot=0.40,
                                  bow=0.56)),
        ('heart',       heart_path(seed=3, lean=-1.2)),
        ('heart-line',  heart_path(seed=5)),
        ('heart-line-b', heart_path(seed=17, lean=-1.8)),
    ]
    for name, d in out:
        print('--- %s ---' % name)
        print(d)
