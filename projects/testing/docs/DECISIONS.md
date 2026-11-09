# Architecture & Product Decisions

## DEC-001 — Static-first demo
- Tanggal: 2026-11-09
- Status: Accepted
- Konteks: Proyek dibuat untuk menguji pembuatan halaman web dan validasi CI monorepo.
- Pilihan: framework frontend, generator statis, atau HTML/CSS/JavaScript vanilla.
- Keputusan: gunakan HTML/CSS/JavaScript vanilla dengan Node built-in test runner.
- Konsekuensi: tidak ada dependency runtime; browser automation belum tersedia dan harus ditambahkan hanya jika dibutuhkan.
