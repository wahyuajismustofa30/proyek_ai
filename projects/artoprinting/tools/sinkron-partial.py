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
    "blog/index.html",
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
MARKER = re.compile(r"<!--\s*(?P<tutup>/)?partial:(?P<nama>[a-z0-9-]+)\s*-->")
WAJIB = {"header", "footer"}


def baca_partial(nama):
    f = PARTIALS / f"{nama}.html"
    if not f.exists():
        raise SystemExit(f"Partial tidak ditemukan: {f.relative_to(ROOT)}")
    isi = f.read_text(encoding="utf-8")
    return isi if isi.endswith("\n") else isi + "\n"


def validasi_marker(teks, rel):
    """Pastikan marker header/footer lengkap, unik, dan tersusun berpasangan."""
    kesalahan = []
    stack = []
    jumlah_buka = {}
    jumlah_tutup = {}

    for m in MARKER.finditer(teks):
        nama = m.group("nama")
        if m.group("tutup"):
            jumlah_tutup[nama] = jumlah_tutup.get(nama, 0) + 1
            if not stack or stack[-1] != nama:
                kesalahan.append(f"{rel}: marker penutup partial:{nama} tidak berpasangan")
            else:
                stack.pop()
        else:
            jumlah_buka[nama] = jumlah_buka.get(nama, 0) + 1
            if nama in stack:
                kesalahan.append(f"{rel}: marker pembuka partial:{nama} bersarang/duplikat")
            stack.append(nama)

    for nama in stack:
        kesalahan.append(f"{rel}: marker pembuka partial:{nama} tidak memiliki penutup")
    for nama in sorted(WAJIB):
        buka = jumlah_buka.get(nama, 0)
        tutup = jumlah_tutup.get(nama, 0)
        if buka == 0:
            kesalahan.append(f"{rel}: marker pembuka partial:{nama} hilang")
        elif buka > 1:
            kesalahan.append(f"{rel}: marker pembuka partial:{nama} ditemukan {buka} kali")
        if tutup == 0:
            kesalahan.append(f"{rel}: marker penutup partial:{nama} hilang")
        elif tutup > 1:
            kesalahan.append(f"{rel}: marker penutup partial:{nama} ditemukan {tutup} kali")
    return kesalahan


def main():
    cek_saja = "--cek" in sys.argv
    halaman = []
    kesalahan = []

    # Preflight semua halaman sebelum menulis agar sinkronisasi tidak parsial.
    for rel in HALAMAN:
        path = ROOT / rel
        teks = path.read_text(encoding="utf-8")
        kesalahan.extend(validasi_marker(teks, rel))
        halaman.append((rel, path, teks))

    if kesalahan:
        print("MARKER BERMASALAH:")
        for pesan in kesalahan:
            print("  -", pesan)
        sys.exit(1)

    berubah = []
    for rel, path, teks in halaman:
        baru = POLA.sub(
            lambda m: m.group("buka") + baca_partial(m.group("nama")) + m.group("tutup"),
            teks,
        )
        if baru != teks:
            berubah.append((rel, path, baru))

    if cek_saja:
        if berubah:
            print("Belum sinkron:", ", ".join(rel for rel, _, _ in berubah))
            sys.exit(1)
        print("Semua halaman sudah sinkron dengan partials/.")
        return

    for _, path, baru in berubah:
        path.write_text(baru, encoding="utf-8")
    print("Diperbarui:", ", ".join(rel for rel, _, _ in berubah) if berubah else "(tidak ada perubahan)")

if __name__ == "__main__":
    main()
