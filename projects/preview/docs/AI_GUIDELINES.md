# Panduan AI — Preview

Instruksi umum repository tetap berlaku dari `/AGENTS.md`; dokumen ini hanya menambahkan konteks khusus proyek.

## Tujuan kerja

- Proyek: landing page statis kampanye SLAMET — calon Kepala Desa Tlagayasa, periode 2027–2035.
- Fokus: menjaga konsistensi konten, aksesibilitas, responsivitas, dan integritas aset.
- Target deploy yang dinyatakan proyek: GitHub Pages. Domain/canonical perlu diverifikasi sebelum perubahan deployment.

## Peta konteks sebelum mengedit

1. `README.md` proyek untuk cara menjalankan dan konvensi konten.
2. `docs/PROJECT_CONTEXT.md` untuk tujuan, ruang lingkup, dan batas data.
3. `docs/ARCHITECTURE.md` untuk struktur HTML/CSS/JS dan alur render.
4. `docs/ASSETS.md` untuk aset, nama file, serta aturan penggantian.
5. `docs/TESTING.md` untuk pemeriksaan yang tersedia dan keterbatasannya.
6. `docs/DECISIONS.md` untuk keputusan teknis.

## Batasan khusus

- Jangan mengarang biografi, pendidikan, organisasi, pekerjaan, kontak, statistik, dukungan, atau klaim kampanye.
- Placeholder yang belum memiliki sumber harus tetap ditandai; jangan tampilkan sebagai fakta.
- Pertahankan nama dan path aset yang dirujuk kode, kecuali perubahan referensi dilakukan konsisten.
- Jangan mengekstrak, menimpa, atau menganggap ZIP sebagai source kanonis tanpa membandingkan isinya.
- Hindari dependency/framework baru; proyek saat ini menggunakan HTML, CSS, dan JavaScript vanilla.
- Perubahan website harus tetap berada dalam `projects/preview/`; jangan menyentuh proyek lain.
- Jangan gunakan skrip sinkronisasi yang melakukan push langsung ke `main`; ikuti branch + PR repository.

## Selesai bila

- Perubahan sesuai scope dan tidak mengandung data rekaan.
- Link/aset lokal yang terdampak valid.
- Pemeriksaan CI relevan lolos; interaksi browser yang tidak dapat diuji otomatis dicatat sebagai belum diverifikasi.
- PR menjelaskan file, perilaku, verifikasi, dan risiko.
