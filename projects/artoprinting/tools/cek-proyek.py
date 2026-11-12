#!/usr/bin/env python3
"""
cek-proyek.py — pemeriksaan statis sebelum upload/deploy.

    python tools/cek-proyek.py
    python tools/cek-proyek.py --cek-url-eksternal    # periksa URL gambar eksternal
    python tools/cek-proyek.py --tulis-daftar-gambar   # tulis daftar URL gambar eksternal

Yang diperiksa:
  1. Semua file JSON di assets/data valid.
  2. Semua referensi lokal di HTML (src, href), CSS (url(...), @import) dan
     JavaScript (import ... from) mengarah ke file yang ada.
  3. Gambar lokal yang dirujuk produk.json dan HTML diperiksa keberadaannya.
  4. Gambar eksternal dilaporkan belum diverifikasi; --cek-url-eksternal memeriksa
     status HTTP dan Content-Type dengan timeout, satu per satu.
  5. Link internal produk.json (link_produk /produk.html?p=..&id=..) menunjuk data yang ada.
  6. Header/footer di setiap halaman sama dengan partials/ (lewat sinkron-partial.py --cek).

Keluar dengan kode 1 bila ada masalah lokal atau URL eksternal yang terkonfirmasi
menghasilkan HTTP 404/410. Kegagalan jaringan lain dilaporkan sebagai gagal
diverifikasi, bukan dianggap gambar hilang.
Hanya memakai pustaka standar Python 3.
"""
import json
import pathlib
import re
import subprocess
import sys
import urllib.error
import urllib.request
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote, parse_qs

ROOT = pathlib.Path(__file__).resolve().parent.parent
ABAIKAN_DIR = {"docs", "tools", "partials", ".git", "node_modules"}

masalah = []
gambar_hilang = []
gambar_lokal_valid = set()
gambar_eksternal = set()
gambar_eksternal_valid = set()
gambar_eksternal_hilang = {}
gambar_eksternal_gagal = {}


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
            if tag in ("img", "source") and attr == "src":
                bagian = urlsplit(ref)
                if bagian.scheme in ("http", "https") or ref.startswith("//"):
                    gambar_eksternal.add(ref)
                else:
                    gambar = resolve(ref, f)
                    if gambar is not None:
                        if gambar.exists():
                            gambar_lokal_valid.add(str(gambar))
                        else:
                            gambar_hilang.append(ref)

            t = resolve(ref, f)
            if t is None:
                continue
            if not t.exists():
                masalah.append(f"{rel(f)}: <{tag} {attr}=\"{ref}\"> tidak ditemukan")


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
            bagian = urlsplit(img)
            if bagian.scheme in ("http", "https") or img.startswith("//"):
                gambar_eksternal.add(img)
            else:
                t = resolve(img, ROOT / "index.html")
                if t is not None:
                    if t.exists():
                        gambar_lokal_valid.add(str(t))
                    else:
                        gambar_hilang.append(img)
            link = x.get("link_produk") or ""
            if link.startswith("/produk.html"):
                q = parse_qs(urlsplit(link).query)
                p, i = q.get("p", [""])[0], q.get("id", [""])[0]
                if p not in produk or i not in {str(y.get("id")) for y in produk[p]}:
                    masalah.append(f"produk.json {kunci} id={x.get('id')}: link_produk {link} tidak menunjuk data yang ada")
        if len(ids) != len(daftar):
            masalah.append(f"produk.json {kunci}: ada id ganda")



def cek_url_gambar(url):
    """Periksa URL gambar eksternal dengan GET terbatas dan timeout."""
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "ArtoPrinting-Project-Validator/1.0", "Range": "bytes=0-0"},
    )
    try:
        with urllib.request.urlopen(req, timeout=6) as response:
            status = getattr(response, "status", 200)
            tipe = response.headers.get("Content-Type", "").split(";", 1)[0].strip().lower()
            if status < 200 or status >= 400:
                gambar_eksternal_gagal[url] = f"HTTP {status}"
            elif not tipe.startswith("image/"):
                gambar_eksternal_gagal[url] = f"Content-Type bukan gambar ({tipe or 'tidak diketahui'})"
            else:
                response.read(1)
                gambar_eksternal_valid.add(url)
    except urllib.error.HTTPError as e:
        if e.code in (404, 410):
            gambar_eksternal_hilang[url] = f"HTTP {e.code}"
        else:
            gambar_eksternal_gagal[url] = f"HTTP {e.code}"
    except (urllib.error.URLError, TimeoutError, OSError, ValueError) as e:
        gambar_eksternal_gagal[url] = str(getattr(e, "reason", e))

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

    if "--cek-url-eksternal" in sys.argv:
        for url in sorted(gambar_eksternal):
            cek_url_gambar(url)

    if "--tulis-daftar-gambar" in sys.argv:
        semua = set()
        for daftar in data.get("produk.json", {}).values():
            if isinstance(daftar, list):
                semua.update(
                    x["img"] for x in daftar
                    if str(x.get("img", "")).startswith(
                        "https://drive.dekeku.my.id/storage/old/artoprinting/"
                    )
                )
        for f in ROOT.glob("post/*.html"):
            semua.update(re.findall(
                r'src="(https://drive.dekeku.my.id/storage/old/artoprinting/(?!brand/)[^"]+)"',
                f.read_text(encoding="utf-8"),
            ))
        out = ROOT / "docs/daftar-gambar-produk.txt"
        out.parent.mkdir(exist_ok=True)
        out.write_text(
            "# URL gambar eksternal yang dirujuk produk.json dan artikel.\n"
            "# Pastikan URL dapat diakses sebelum deploy.\n"
            f"# Jumlah: {len(semua)}\n" + "\n".join(sorted(semua)) + "\n",
            encoding="utf-8",
        )
        print(f"Daftar gambar ditulis ke {rel(out)} ({len(semua)} URL)")

    lokal_hilang = sorted(set(gambar_hilang))
    if masalah:
        print(f"MASALAH ({len(masalah)}):")
        for m in masalah:
            print("  -", m)
    else:
        print("OK: referensi lokal, JSON, link internal produk, dan partial valid.")

    print(f"GAMBAR LOKAL: {len(gambar_lokal_valid)} valid, {len(lokal_hilang)} hilang.")
    for gambar in lokal_hilang[:5]:
        print("  -", gambar)

    if "--cek-url-eksternal" in sys.argv:
        print(
            f"GAMBAR EKSTERNAL: {len(gambar_eksternal_valid)} valid, "
            f"{len(gambar_eksternal_hilang)} hilang, "
            f"{len(gambar_eksternal_gagal)} gagal diverifikasi."
        )
        for url, alasan in gambar_eksternal_hilang.items():
            print(f"  - HILANG {url} ({alasan})")
        for url, alasan in gambar_eksternal_gagal.items():
            print(f"  - GAGAL {url} ({alasan})")
    else:
        print(
            f"GAMBAR EKSTERNAL: {len(gambar_eksternal)} belum diverifikasi "
            "(gunakan --cek-url-eksternal untuk pemeriksaan jaringan)."
        )

    sys.exit(1 if masalah or gambar_eksternal_hilang else 0)

if __name__ == "__main__":
    main()
