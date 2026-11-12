#!/usr/bin/env python3
"""
cek-proyek.py — pemeriksaan statis sebelum upload/deploy.

    python tools/cek-proyek.py
    python tools/cek-proyek.py --tulis-daftar-gambar   # juga menulis docs/daftar-gambar-produk.txt

Yang diperiksa:
  1. Semua file JSON di assets/data valid.
  2. Semua referensi lokal di HTML (src, href), CSS (url(...), @import) dan
     JavaScript (import ... from) mengarah ke file yang ada.
  3. Semua gambar lokal yang dirujuk produk.json (field img) dan artikel ada di folder.
  4. Link internal produk.json (link_produk /produk.html?p=..&id=..) menunjuk data yang ada.
  5. Header/footer di setiap halaman sama dengan partials/ (lewat sinkron-partial.py --cek).

Keluar dengan kode 1 bila ada masalah selain gambar produk yang belum disalin
(gambar produk dilaporkan terpisah karena memang tidak ikut ZIP).
Hanya memakai pustaka standar Python 3.
"""
import json
import pathlib
import re
import subprocess
import sys
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote, parse_qs

ROOT = pathlib.Path(__file__).resolve().parent.parent
ABAIKAN_DIR = {"docs", "tools", "partials", ".git", "node_modules"}

masalah = []
gambar_hilang = []


def rel(p):
    return str(p.relative_to(ROOT)).replace("\\", "/")


def resolve(ref, dari):
    """Ubah referensi lokal jadi path file. None bila eksternal / bukan file."""
    if not ref or ref.startswith(("http://", "https://", "//", "data:", "mailto:", "tel:", "#", "javascript:")):
        return None
    path = unquote(urlsplit(ref).path)
    if not path:
        return None
    target = (ROOT / path.lstrip("/")) if path.startswith("/") else (dari.parent / path)
    target = target.resolve()
    if target.is_dir() or path.endswith("/"):
        target = target / "index.html"
    return target


class Kumpul(HTMLParser):
    def __init__(self):
        super().__init__()
        self.refs = []
        self.ids = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if "id" in a:
            self.ids.append(a["id"])
        for k in ("src", "href"):
            if a.get(k):
                if tag == "link" and a.get("rel") in ("preconnect", "canonical"):
                    continue
                if tag == "a" and k == "href" and not a[k].startswith("/") and not a[k].endswith(".html"):
                    continue
                self.refs.append((tag, k, a[k]))


def cek_json():
    data = {}
    for f in sorted((ROOT / "assets/data").glob("*.json")):
        try:
            data[f.name] = json.loads(f.read_text(encoding="utf-8"))
        except Exception as e:  # noqa: BLE001
            masalah.append(f"JSON tidak valid: {rel(f)} ({e})")
    return data


def cek_html():
    for f in sorted(ROOT.rglob("*.html")):
        if set(f.relative_to(ROOT).parts) & ABAIKAN_DIR:
            continue
        p = Kumpul()
        p.feed(f.read_text(encoding="utf-8"))
        dup = {i for i in p.ids if p.ids.count(i) > 1}
        if dup:
            masalah.append(f"{rel(f)}: id ganda {sorted(dup)}")
        for tag, attr, ref in p.refs:
            t = resolve(ref, f)
            if t is None:
                continue
            if not t.exists():
                pesan = f"{rel(f)}: <{tag} {attr}=\"{ref}\"> tidak ditemukan"
                if "https://drive.dekeku.my.id/storage/old/artoprinting/" in ref and "/brand/" not in ref:
                    gambar_hilang.append(ref)
                else:
                    masalah.append(pesan)


def cek_css_js():
    for f in sorted((ROOT / "assets").rglob("*.css")) + sorted(ROOT.glob("tamu-undangan/*.css")):
        for ref in re.findall(r"url\(\s*['\"]?([^'\")]+)['\"]?\s*\)", f.read_text(encoding="utf-8")):
            t = resolve(ref, f)
            if t is not None and not t.exists():
                masalah.append(f"{rel(f)}: url({ref}) tidak ditemukan")
        for ref in re.findall(r"@import\s+(?:url\()?['\"]([^'\"]+)", f.read_text(encoding="utf-8")):
            t = resolve(ref, f)
            if t is not None and not t.exists():
                masalah.append(f"{rel(f)}: @import {ref} tidak ditemukan")
    for f in sorted((ROOT / "assets/js").rglob("*.js")):
        teks = f.read_text(encoding="utf-8")
        for ref in re.findall(r"^\s*import\s+(?:[^'\"]+from\s+)?['\"]([^'\"]+)['\"]", teks, re.M):
            t = resolve(ref, f)
            if t is not None and not t.exists():
                masalah.append(f"{rel(f)}: import '{ref}' tidak ditemukan")
        for ref in re.findall(r"['\"](/assets/[^'\"]+\.(?:json|webp|png|jpe?g|svg))['\"]", teks):
            t = resolve(ref, f)
            if not t.exists():
                masalah.append(f"{rel(f)}: '{ref}' tidak ditemukan")


def cek_produk(data):
    produk = data.get("produk.json", {})
    for kunci, daftar in produk.items():
        if not isinstance(daftar, list):
            continue
        ids = {str(x.get("id")) for x in daftar}
        for x in daftar:
            img = x.get("img") or ""
            t = resolve(img, ROOT / "index.html")
            if t is not None and not t.exists():
                gambar_hilang.append(img)
            link = x.get("link_produk") or ""
            if link.startswith("/produk.html"):
                q = parse_qs(urlsplit(link).query)
                p, i = q.get("p", [""])[0], q.get("id", [""])[0]
                if p not in produk or i not in {str(y.get("id")) for y in produk[p]}:
                    masalah.append(f"produk.json {kunci} id={x.get('id')}: link_produk {link} tidak menunjuk data yang ada")
        if len(ids) != len(daftar):
            masalah.append(f"produk.json {kunci}: ada id ganda")


def cek_partial():
    r = subprocess.run([sys.executable, str(ROOT / "tools/sinkron-partial.py"), "--cek"], capture_output=True, text=True)
    if r.returncode != 0:
        masalah.append("Header/footer belum sinkron dengan partials/: " + r.stdout.strip())


def main():
    data = cek_json()
    cek_html()
    cek_css_js()
    cek_produk(data)
    cek_partial()

    unik = sorted(set(gambar_hilang))
    if "--tulis-daftar-gambar" in sys.argv:
        semua = set()
        for daftar in data.get("produk.json", {}).values():
            if isinstance(daftar, list):
                semua.update(x["img"] for x in daftar if str(x.get("img", "")).startswith("https://drive.dekeku.my.id/storage/old/artoprinting/"))
        for f in ROOT.glob("post/*.html"):
            semua.update(re.findall(r'src="(https://drive.dekeku.my.id/storage/old/artoprinting/(?!brand/)[^"]+)"', f.read_text(encoding="utf-8")))
        out = ROOT / "docs/daftar-gambar-produk.txt"
        out.parent.mkdir(exist_ok=True)
        out.write_text(
            "# Gambar lokal yang dirujuk produk.json dan artikel.\n"
            "# Semuanya harus ada di folder https://drive.dekeku.my.id/storage/old/artoprinting/ sebelum deploy.\n"
            f"# Jumlah: {len(semua)}\n" + "\n".join(sorted(semua)) + "\n", encoding="utf-8")
        print(f"Daftar gambar ditulis ke {rel(out)} ({len(semua)} file)")

    if masalah:
        print(f"MASALAH ({len(masalah)}):")
        for m in masalah:
            print("  -", m)
    else:
        print("OK: semua referensi file lokal, data JSON, link internal produk, dan partial valid.")
    if unik:
        print(f"PERHATIAN: {len(unik)} gambar di https://drive.dekeku.my.id/storage/old/artoprinting/ belum ada di folder ini "
              "(salin dari backup gambar sebelum deploy). Contoh:")
        for g in unik[:5]:
            print("  -", g)
    else:
        print("OK: semua gambar produk tersedia.")
    sys.exit(1 if masalah else 0)


if __name__ == "__main__":
    main()
