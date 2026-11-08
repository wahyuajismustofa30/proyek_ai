#!/usr/bin/env python3
"""Bangun tokens.css dan sprite logo/icon, lalu suntikkan ke halaman referensi.

Pemakaian: python3 scripts/build_tokens.py [tokens.json] [halaman.html]
Tanpa argumen: tokens/tokens.json dan referensi/DEKEKU_ Halaman Referensi Tema v<versi>.html

Yang dilakukan:
1. tokens/tokens.json -> tokens/tokens.css, lalu disalin ke <style> halaman di antara
   penanda BEGIN/END (halaman publik tidak bisa memuat CSS lokal).
2. assets/logo/dekeku-logo-compact.svg dan assets/maskot/svg/maskot-*.svg -> <symbol>
   inline di halaman (badan maskot ditulis sekali, ekspresi lewat <use>) (warna mengikuti currentColor, jadi ikut tema terang/gelap).
3. Pemeriksaan: var() belum terdefinisi (gagal), warna tertanam di luar token
   (peringatan), tautan berkas lokal yang tidak ada (gagal).
Jalankan ulang setiap tokens.json atau berkas di assets/ berubah.
"""
import json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
src = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "tokens" / "tokens.json"
t = json.load(open(src, encoding="utf-8"))
page = Path(sys.argv[2]) if len(sys.argv) > 2 else ROOT / "referensi" / f"DEKEKU_ Halaman Referensi Tema v{t['meta']['version']}.html"
assert set(t["light"]) == set(t["dark"]), "Kunci light dan dark harus sama"


def block(d, ind="  "):
    return "\n".join(f"{ind}--{k}: {v};" for k, v in d.items())


# --- 1. Token ---
inv = {(k if k.startswith("inv-") else "inv-" + k): v for k, v in t["invitation"].items()}
css = f"""/* DEKEKU Master Theme v{t['meta']['version']}: DIHASILKAN dari tokens.json. Jangan diedit manual. */
:root {{
{block(t['static'])}
{block(t['light'])}
{block(inv)}
}}

@media (prefers-color-scheme: dark) {{
  :root:not([data-theme='light']) {{
{block(t['dark'], '    ')}
    color-scheme: dark;
  }}
}}

:root[data-theme='dark'] {{
{block(t['dark'])}
  color-scheme: dark;
}}
"""
(src.parent / "tokens.css").write_text(css, encoding="utf-8")

BEGIN, END = "/* BEGIN tokens (dihasilkan, jangan diedit) */", "/* END tokens */"
extra = (
    ":root{box-sizing:border-box;padding-top:env(safe-area-inset-top,0px);"
    "padding-bottom:env(safe-area-inset-bottom,0px)}"
)
inject = f"{BEGIN}\n{css}{END}\n{extra}\n"

html = page.read_text(encoding="utf-8")
if BEGIN in html:
    html = re.sub(re.escape(BEGIN) + r".*?" + re.escape(END) + r"\n.*?\n", lambda m: inject, html, count=1, flags=re.S)
else:
    html, n = re.subn(r"(<style>\n).*?(\*\{box-sizing:border-box\})", lambda m: m.group(1) + inject + m.group(2), html, count=1, flags=re.S)
    assert n == 1, "Blok token lama tidak ditemukan"

# --- 2. Sprite logo dan maskot ---
LOGO = [("dk-logo-compact", "assets/logo/dekeku-logo-compact.svg")]
# id symbol -> berkas assets/maskot/svg/maskot-<nama>.svg (dk-icon = ekspresi senang)
MASKOT = [("dk-icon", "senang"), ("dk-maskot-oops", "oops"), ("dk-maskot-mikir", "mikir"), ("dk-maskot-sukses", "sukses")]
MDIR = ROOT / "assets" / "maskot" / "svg"


def to_current(x):
    x = re.sub(r'(fill|stroke)="#[0-9A-Fa-f]{6}"', r'\1="currentColor"', x)
    assert not re.search(r"#[0-9A-Fa-f]{6}", x), "masih ada warna tetap"
    return x


def symbol(sid, rel):
    s = (ROOT / rel).read_text(encoding="utf-8")
    vb = re.search(r'viewBox="([^"]+)"', s).group(1)
    inner = re.search(r"<svg[^>]*>(.*)</svg>", s, re.S).group(1)
    inner = re.sub(r"<title>.*?</title>", "", inner, flags=re.S)
    return f'<symbol id="{sid}" viewBox="{vb}">{to_current(inner)}</symbol>'


def maskot(name):
    return (MDIR / f"maskot-{name}.svg").read_text(encoding="utf-8")


def d_of(x):
    return re.search(r' d="([^"]+)"', x).group(1)


# Badan maskot ditulis sekali (polos = tanpa mata asli, penuh = dengan mata senang), lalu dipakai ulang lewat <use>.
D_POLOS, D_PENUH = d_of(maskot("polos")), d_of(maskot("senang"))


def maskot_symbol(sid, name):
    x = maskot(name)
    vb = re.search(r'viewBox="([^"]+)"', x).group(1)
    ref = "dk-path-polos" if d_of(x) == D_POLOS else "dk-path-penuh"
    extra = re.search(r'<path fill-rule="evenodd"[^>]*/>(.*)</svg>', x, re.S).group(1)
    return f'<symbol id="{sid}" viewBox="{vb}"><use href="#{ref}" fill="currentColor"/>{to_current(extra)}</symbol>'


SB, SE = "<!-- BEGIN sprite (dihasilkan dari assets/, jangan diedit) -->", "<!-- END sprite -->"
defs = f'<defs><path id="dk-path-polos" fill-rule="evenodd" d="{D_POLOS}"/><path id="dk-path-penuh" fill-rule="evenodd" d="{D_PENUH}"/></defs>'
sprite = (SB + '\n<svg width="0" height="0" style="position:absolute" aria-hidden="true" focusable="false">\n' + defs + "\n"
          + "\n".join(symbol(*x) for x in LOGO) + "\n" + "\n".join(maskot_symbol(*x) for x in MASKOT) + "\n</svg>\n" + SE)
assert SB in html and SE in html, "Penanda sprite tidak ada di halaman"
html = re.sub(re.escape(SB) + r".*?" + re.escape(SE), lambda m: sprite, html, count=1, flags=re.S)
page.write_text(html, encoding="utf-8")
print("OK:", len(css), "byte token,", len(sprite), "byte sprite ->", page.name)

# --- 3. Pemeriksaan ---
defined = set(re.findall(r"--([\w-]+)\s*:", html))
used = set(re.findall(r"var\(--([\w-]+)", html))
missing = sorted(used - defined)
bad = False
if missing:
    print("GAGAL: var() belum didefinisikan:", ", ".join(missing)); bad = True
ids = set(re.findall(r'<(?:symbol|path) id="([^"]+)"', html))
for u in set(re.findall(r'<use href="#([^"]+)"', html)):
    if u not in ids:
        print("GAGAL: <use> menunjuk symbol yang tidak ada:", u); bad = True
for ref in sorted(set(re.findall(r'(?:href|src)="([^"#:][^"]*)"', html))):
    if ref.startswith(("http", "mailto", "tel", "//")):
        continue
    if not (page.parent / ref).resolve().exists():
        print("GAGAL: berkas tidak ada:", ref); bad = True
outside = html.replace(css, "")
outside = re.sub(r'<meta name="theme-color"[^>]*>', "", outside)
hard = sorted(set(re.findall(r"#[0-9A-Fa-f]{3,8}\b(?![\w-])|rgba?\([^)]*\)", outside)))
if hard:
    print("PERINGATAN: warna tertanam di luar token:", ", ".join(hard))
if bad:
    sys.exit(1)
if not hard:
    print("Pemeriksaan: var(), symbol, tautan berkas, dan warna semuanya bersih.")
