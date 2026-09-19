#!/usr/bin/env python3
"""Generate the hand-drawn star and heart path data for assets/js/sprite.js.

The old shapes were mathematically perfect polygons with a turbulence filter
laid over the top, which still reads as "even" — the arms are all the same
length and every edge is dead straight. These are built the way a hand draws
them instead: uneven arms, angles that miss, edges that bow, and a pen that
overshoots where the stroke closes.

Run it and paste the printed block into sprite.js. It is a one-off author
tool, not a build step — the site ships the literal path data.
"""
import math
import random


def fmt(v):
    """Trim coordinates to one decimal; keeps the sprite readable and small."""
    s = '%.1f' % v
    return s.rstrip('0').rstrip('.') if '.' in s else s


def pt(p):
    return '%s %s' % (fmt(p[0]), fmt(p[1]))


def bowed(a, b, bow, rnd):
    """A quadratic control point for the chord a->b, pushed off to one side so
    the edge bows the way a drawn line does rather than ruling straight."""
    mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
    dx, dy = b[0] - a[0], b[1] - a[1]
    n = math.hypot(dx, dy) or 1
    k = bow * n * rnd.uniform(0.55, 1.45)
    return (mx - dy / n * k, my + dx / n * k)


def star_path(cx=50, cy=50, r=47, points=5, inner=0.4, rot=-0.06,
              seed=1, jitter=0.075, bow=0.05, overshoot=True):
    rnd = random.Random(seed)
    pts = []
    for i in range(points * 2):
        ang = rot + i * math.pi / points - math.pi / 2
        rad = r if i % 2 == 0 else r * inner
        rad *= 1 + rnd.uniform(-jitter, jitter)
        ang += rnd.uniform(-jitter, jitter) * 0.55
        pts.append((cx + rad * math.cos(ang), cy + rad * math.sin(ang)))

    d = ['M' + pt(pts[0])]
    for i in range(1, len(pts) + 1):
        a, b = pts[i - 1], pts[i % len(pts)]
        d.append('Q%s %s' % (pt(bowed(a, b, bow, rnd)), pt(b)))
    if overshoot:
        # Carry the stroke a little past its own start, the way a pen does
        # when it comes back round to where it began.
        a, b = pts[0], pts[1]
        t = 0.3
        end = (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)
        d.append('Q%s %s' % (pt(bowed(a, end, bow, rnd)), pt(end)))
    return ' '.join(d)


def heart_path(seed=1, jitter=2.6, lean=1.0, overshoot=True):
    """A heart with two lobes that do not match — which is the whole point.
    The left one is drawn bigger and higher, as an unpractised hand does."""
    rnd = random.Random(seed)

    def j(p, amt=1.0):
        return (p[0] + rnd.uniform(-jitter, jitter) * amt,
                p[1] + rnd.uniform(-jitter, jitter) * amt)

    tip = j((50 + lean, 87), 0.5)
    left = j((5, 29))
    lobe_l = j((29, 4))
    notch = j((50, 18), 0.6)
    lobe_r = j((69, 7))
    right = j((94, 32))

    seg = [
        (tip, j((21, 67)), j((5, 48)), left),
        (left, j((4, 13)), j((16, 3)), lobe_l),
        (lobe_l, j((40, 4), 0.7), j((46, 11), 0.7), notch),
        (notch, j((54, 10), 0.7), j((61, 4), 0.7), lobe_r),
        (lobe_r, j((83, 4)), j((95, 15)), right),
        (right, j((93, 49)), j((78, 67)), tip),
    ]
    d = ['M' + pt(seg[0][0])]
    for _, c1, c2, end in seg:
        d.append('C%s %s %s' % (pt(c1), pt(c2), pt(end)))
    if overshoot:
        d.append('C%s %s %s' % (pt(j((36, 76), 0.4)), pt(j((28, 70), 0.4)),
                                pt(j((22, 63), 0.4))))
    return ' '.join(d)


if __name__ == '__main__':
    print('--- star-5 (filled) ---')
    print(star_path(seed=4, overshoot=False))
    print('--- star-line ---')
    print(star_path(seed=11, r=45))
    print('--- star-line-b ---')
    print(star_path(seed=23, r=45, inner=0.44, rot=0.12))
    print('--- star-6 ---')
    print(star_path(seed=7, points=6, inner=0.52, r=47, overshoot=False))
    print('--- star-8 ---')
    print(star_path(seed=9, points=8, inner=0.44, r=47, overshoot=False))
    print('--- heart (filled) ---')
    print(heart_path(seed=3, jitter=3.6, lean=-2.0, overshoot=False))
    print('--- heart-line ---')
    print(heart_path(seed=5))
    print('--- heart-line-b ---')
    print(heart_path(seed=17, lean=-1.5))
