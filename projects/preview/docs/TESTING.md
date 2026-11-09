# Testing — Preview

## Pemeriksaan otomatis
Workflow monorepo mendeteksi proyek sebagai static site melalui `index.html` di root proyek dan menjalankan validasi HTML/CSS/aset lokal serta HTTP smoke test. Pada commit main yang diaudit, check `projects/preview / static` berstatus sukses.

## Cara uji lokal
Dari root repository:
```bash
python scripts/check_static_site.py projects/preview
python scripts/validate_web_projects.py
```
Catatan: gunakan opsi/parameter sesuai `--help` pada script bila berbeda; periksa `docs/MONOREPO_CI.md` untuk cara CI resmi.

Untuk preview browser, jalankan server static dari root proyek (contoh):
```bash
python -m http.server 8000 --directory projects/preview
```
Lalu buka `http://127.0.0.1:8000`.

## Checklist manual
- [ ] Desktop dan viewport mobile: layout, nav, spacing, typography.
- [ ] Hamburger: buka/tutup dan navigasi section.
- [ ] Panel visi: expand/collapse dan state aksesibilitas.
- [ ] Kartu misi: detail benar dan fokus/scroll wajar.
- [ ] Program mengarah ke misi yang tepat.
- [ ] Galeri: buka/tutup, prev/next, keyboard, backdrop.
- [ ] Scroll progress dan back-to-top.
- [ ] `prefers-reduced-motion` mengurangi animasi.
- [ ] Console browser bebas error.
- [ ] Semua gambar dan ikon tampil; alt text tersedia.
- [ ] Link internal dan canonical/domain diverifikasi bila deployment berubah.

## Batas bukti
CI green bukan bukti penuh UX, aksesibilitas, konten faktual, atau kesesuaian lintas-browser. Browser E2E belum disiapkan/dijalankan pada audit awal.
