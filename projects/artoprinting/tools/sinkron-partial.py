#!/usr/bin/env python3
"""
sinkron-partial.py — menyalin isi partials/*.html ke setiap halaman HTML.

Situs ini HTML statis tanpa build. Header dan footer ditulis langsung di setiap
halaman (supaya tetap terbaca mesin pencari dan jalan tanpa JavaScript), tetapi
sumber tunggalnya ada di folder partials/. Setelah mengubah partial, jalankan:

    python tools/sinkron-partial.py          # tulis perubahan
    python tools/sinkron-partial.py --cek    # hanya periksa, keluar kode 1 bila belum sinkron

Di halaman, blok yang dikelola ditandai seperti ini:

    <!-- partial:header -->
    ... isi otomatis, jangan diedit langsung ...
    <!-- /partial:header -->

Hanya memakai pustaka standar Python 3.
"""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
PARTIALS = ROOT / "partials"
# Halaman yang memakai header/footer bersama. Tambahkan halaman baru di sini.
HALAMAN = [
    "index.html",
    "laman/katalog/index.html",
    "laman/layanan/index.html",
    "laman/cara-pesan/index.html",
    "laman/testimoni/index.html",
    "laman/kontak/index.html",
    "laman/produk/index.html",
    "post/percetakan-murah-purbalingga.html",
    "404.html",
]

POLA = re.compile(r"(?P<buka>[ \t]*<!-- partial:(?P<nama>[a-z0-9-]+) -->\n)(?P<isi>.*?)(?P<tutup>[ \t]*<!-- /partial:(?P=nama) -->)", re.S)


def baca_partial(nama):
    f = PARTIALS / f"{nama}.html"
    if not f.exists():
        raise SystemExit(f"Partial tidak ditemukan: {f.relative_to(ROOT)}")
    isi = f.read_text(encoding="utf-8")
    return isi if isi.endswith("\n") else isi + "\n"


def main():
    cek_saja = "--cek" in sys.argv
    berubah = []
    for rel in HALAMAN:
        path = ROOT / rel
        teks = path.read_text(encoding="utf-8")
        baru = POLA.sub(lambda m: m.group("buka") + baca_partial(m.group("nama")) + m.group("tutup"), teks)
        if not POLA.search(teks):
            print(f"! {rel}: tidak ada penanda partial")
        if baru != teks:
            berubah.append(rel)
            if not cek_saja:
                path.write_text(baru, encoding="utf-8")
    if cek_saja:
        if berubah:
            print("Belum sinkron:", ", ".join(berubah))
            sys.exit(1)
        print("Semua halaman sudah sinkron dengan partials/.")
    else:
        print("Diperbarui:", ", ".join(berubah) if berubah else "(tidak ada perubahan)")


if __name__ == "__main__":
    main()
