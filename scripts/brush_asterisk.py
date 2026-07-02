# /// script
# requires-python = ">=3.11"
# ///
"""Generate a calligraphic brush-stroke asterisk as an SVG with tapered filled strokes."""
import math

def bezier(p0, p1, p2, p3, t):
    mt = 1 - t
    x = mt**3*p0[0] + 3*mt**2*t*p1[0] + 3*mt*t**2*p2[0] + t**3*p3[0]
    y = mt**3*p0[1] + 3*mt**2*t*p1[1] + 3*mt*t**2*p2[1] + t**3*p3[1]
    return x, y

def bezier_tangent(p0, p1, p2, p3, t):
    mt = 1 - t
    x = 3*mt**2*(p1[0]-p0[0]) + 6*mt*t*(p2[0]-p1[0]) + 3*t**2*(p3[0]-p2[0])
    y = 3*mt**2*(p1[1]-p0[1]) + 6*mt*t*(p2[1]-p1[1]) + 3*t**2*(p3[1]-p2[1])
    n = math.hypot(x, y) or 1
    return x/n, y/n

def stroke_outline(p0, p1, p2, p3, w_entry, w_exit, samples=48):
    """Filled outline of a tapered brush stroke: rounded entry, fine pointed exit."""
    side_a, side_b = [], []
    for i in range(samples + 1):
        t = i / samples
        x, y = bezier(p0, p1, p2, p3, t)
        tx, ty = bezier_tangent(p0, p1, p2, p3, t)
        nx, ny = -ty, tx
        # width profile: plump entry easing to a fine tail, slight belly at 1/3
        base = w_exit + (w_entry - w_exit) * (1 - t) ** 1.35
        belly = 1 + 0.18 * math.sin(math.pi * min(t / 0.66, 1.0))
        w = base * belly / 2
        side_a.append((x + nx*w, y + ny*w))
        side_b.append((x - nx*w, y - ny*w))
    # rounded entry cap: sweep from side_b[0] behind the entry point to side_a[0],
    # radius matching the outline offset at t=0 so it joins seamlessly
    x0, y0 = bezier(p0, p1, p2, p3, 0)
    tx, ty = bezier_tangent(p0, p1, p2, p3, 0)
    nx, ny = -ty, tx
    r = w_entry / 2
    cap = []
    for i in range(1, 10):
        ang = math.pi * i / 10
        cx = x0 - tx*math.sin(ang)*r - nx*math.cos(ang)*r
        cy = y0 - ty*math.sin(ang)*r - ny*math.cos(ang)*r
        cap.append((cx, cy))
    pts = side_a + side_b[::-1] + cap
    d = 'M' + ' L'.join(f'{x:.2f} {y:.2f}' for x, y in pts) + ' Z'
    return d

ROTATE_DEG = -10  # whole-mark tilt: centre stroke leans in from top-left
CENTER = (22.0, 22.0)

def rot(p):
    a = math.radians(ROTATE_DEG)
    x, y = p[0] - CENTER[0], p[1] - CENTER[1]
    return (CENTER[0] + x*math.cos(a) - y*math.sin(a),
            CENTER[1] + x*math.sin(a) + y*math.cos(a))

# all three centerlines pass within ~1 unit of (22, 22.5) so the mark
# radiates from a single heart, with a slight hand-drawn miss.
# stroke spans deliberately vary: the rising flick is the longest gesture,
# the counter-diagonal the shortest.
strokes = [
    # vertical: lands at top, gentle S-sway, tail lifts at bottom
    dict(p0=(23.0, 5.6), p1=(22.0, 14.5), p2=(23.2, 27.0), p3=(20.9, 38.6), w_entry=5.2, w_exit=1.4),
    # rising flick: lands lower-left, one graceful arc to a fine tip upper-right
    dict(p0=(4.6, 35.4), p1=(15.5, 30.0), p2=(27.5, 18.0), p3=(41.0, 6.2), w_entry=5.0, w_exit=1.2),
    # counter-diagonal drawn from lower-right, releasing to a fine tip upper-left,
    # so the heavy entries sit balanced: top, lower-left, lower-right
    dict(p0=(36.8, 32.2), p1=(27.8, 25.8), p2=(16.0, 16.8), p3=(7.2, 11.2), w_entry=4.9, w_exit=1.3),
]
strokes = [
    {**s, 'p0': rot(s['p0']), 'p1': rot(s['p1']), 'p2': rot(s['p2']), 'p3': rot(s['p3'])}
    for s in strokes
]

paths = '\n'.join(
    f'  <path d="{stroke_outline(**s)}" fill="#eb5e28"/>' for s in strokes
)
svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="44" height="44" viewBox="0 0 44 44" fill="none">
  <!-- calligraphic brush asterisk; fill colour matches the accent variable in main.css -->
{paths}
</svg>
'''
import pathlib, sys
out = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else 'marker.svg')
out.write_text(svg)
print(f'wrote {out} ({len(svg)} bytes)')
