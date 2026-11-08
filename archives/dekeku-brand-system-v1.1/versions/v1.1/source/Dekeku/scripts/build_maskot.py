#!/usr/bin/env python3
"""Hasilkan set ekspresi maskot DEKEKU dari assets/icon/dekeku-icon.svg.

Pemakaian: python3 scripts/build_maskot.py [--png]

Badan, lubang wajah, dan dua kotak piksel diambil dari icon asli (satu sumber
kebenaran). Hanya ekspresi (mata dan mulut) yang digambar di sini, dalam kerangka
lokal yang mengikuti kemiringan wajah asli (pusat 891,584; putar -19,6 derajat).
Keluaran: assets/maskot/svg/maskot-<nama>.svg (hitam #0C0C0C) dan -white.svg (putih),
ditambah maskot-polos (tanpa ekspresi). Dengan --png juga membuat PNG transparan 512 px
(butuh playwright).
"""
import re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "assets" / "icon" / "dekeku-icon.svg"
OUT = ROOT / "assets" / "maskot"
VIEWBOX = "19.7 7.7 1296.3 984.7"
BLACK, WHITE = "#0C0C0C", "#FFFFFF"
STROKE = 40  # ketebalan garis mata, mengikuti mata asli

s = SRC.read_text(encoding="utf-8")
d = re.search(r' d="([^"]+)"', s).group(1)
subs = [x for x in re.split(r"(?=M)", d) if x.strip()]
assert len(subs) == 6, "Struktur icon berubah: harus 6 subpath (badan, wajah, 2 mata, 2 kotak)"
BASE = "".join(subs[i] for i in (0, 1, 4, 5))  # tanpa dua mata asli
FULL = d                                         # dengan mata senang asli

LEFT, RIGHT, EY = -145, 129, -11  # pusat mata asli pada kerangka lokal


def dot(cx, cy, r=30):
    return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{{c}}"/>'


SWEAT = '<path d="M214 -134C214 -134 178 -92 178 -64A36 36 0 0 0 250 -64C250 -92 214 -134 214 -134Z" fill="{c}"/>'

# nama: (label, badan, elemen ekspresi)
EXPR = {
    "oops": ("Oops", BASE, [
        dot(LEFT, EY + 4, 38), dot(RIGHT, EY + 4, 38),
        '<ellipse cx="-4" cy="110" rx="30" ry="38" fill="{c}"/>',
        SWEAT,
    ]),
    "mikir": ("Mikir", BASE, [
        dot(LEFT + 22, EY - 24, 34), dot(RIGHT + 22, EY - 24, 34),
        '<path d="M-48 112L30 98" fill="none" stroke="{c}" stroke-width="32" stroke-linecap="round"/>',
    ]),
    "sukses": ("Sukses", FULL, [  # mata senang asli + senyum terbuka
        '<path d="M-50 100H50A50 50 0 0 1-50 100Z" fill="{c}"/>',
    ]),
}


def svg(label, body, color, eyes=None):
    g = ""
    if eyes:
        g = '<g transform="translate(891 584) rotate(-19.6)">' + "".join(e.replace("{c}", color) for e in eyes) + "</g>"
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{VIEWBOX}" role="img" aria-label="{label}">'
            f'<title>{label}</title><path fill-rule="evenodd" fill="{color}" d="{body}"/>{g}</svg>\n')


files = {"polos": ("Maskot DEKEKU, tanpa ekspresi", BASE, None),
         "senang": ("Maskot DEKEKU, ekspresi senang", FULL, None)}
for k, (nm, body, parts) in EXPR.items():
    files[k] = (f"Maskot DEKEKU, ekspresi {nm.lower()}", body, parts)

(OUT / "svg").mkdir(parents=True, exist_ok=True)
for key, (label, body, eyes) in files.items():
    (OUT / "svg" / f"maskot-{key}.svg").write_text(svg(label, body, BLACK, eyes), encoding="utf-8")
    (OUT / "svg" / f"maskot-{key}-white.svg").write_text(svg(label, body, WHITE, eyes), encoding="utf-8")
print("SVG:", len(files) * 2, "berkas ->", OUT / "svg")

if "--png" in sys.argv:
    import asyncio
    from playwright.async_api import async_playwright

    async def run():
        (OUT / "png").mkdir(exist_ok=True)
        async with async_playwright() as p:
            b = await p.chromium.launch()
            pg = await b.new_page(viewport={"width": 512, "height": 389})
            for f in sorted((OUT / "svg").glob("maskot-*.svg")):
                await pg.set_content(f'<body style="margin:0;background:transparent"><img src="file://{f}" style="width:512px;display:block">')
                await pg.wait_for_timeout(100)
                await pg.screenshot(path=str(OUT / "png" / (f.stem + "-512.png")), omit_background=True, clip={"x": 0, "y": 0, "width": 512, "height": 389})
            await b.close()
    asyncio.run(run())
    print("PNG ->", OUT / "png")
