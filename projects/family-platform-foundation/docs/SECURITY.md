# Security & Privacy Baseline

## 1. Prinsip

-   Deny by default.
-   Least privilege.
-   Workspace isolation.
-   Auditability.
-   Secrets management.
-   Backup and recovery.

## 2. Authentication

-   Password hash Argon2id.
-   Cookie session `HttpOnly`, `Secure`, `SameSite`.
-   Session rotation setelah login dan perubahan kredensial.
-   Rate limit login.
-   Proses reset password harus memiliki token acak, sekali pakai, dan
    kedaluwarsa.
-   MFA menjadi prioritas sebelum data sensitif dan integrasi eksternal
    diperluas.

## 3. Authorization

-   Validasi membership pada setiap request.
-   Validasi permission untuk setiap aksi.
-   Jangan mempercayai `workspace_id` dari browser.
-   Uji IDOR dengan mengganti UUID resource.
-   File download juga wajib melalui authorization.
-   Owner tidak otomatis boleh membaca private personal data anggota
    lain.

## 4. Data protection

-   HTTPS.
-   Database tidak diekspos ke internet.
-   Enkripsi backup.
-   Jangan log credential, session cookie, API key, atau isi dokumen.
-   Batasi ukuran dan jenis file.
-   Simpan file di luar public web root.
-   Retensi dan penghapusan data harus terdokumentasi.

## 5. Audit

-   Catat login penting, perubahan permission, perubahan konfigurasi,
    posting/reversal jurnal, dan perubahan data penting.
-   Audit log append-only dari aplikasi.
-   Snapshot sebelum/sesudah harus disaring dari data rahasia.
-   Catat actor, waktu UTC, action, resource, workspace, request ID.

## 6. Server Armbian

-   Jangan mengubah service produksi yang ada sebagai bagian dari
    eksperimen.
-   Jangan membuka PostgreSQL ke internet.
-   Gunakan port khusus yang telah diperiksa.
-   Pisahkan direktori, environment, volume, dan log aplikasi.
-   Backup konfigurasi sebelum mengubah reverse proxy.
-   Uji deployment di staging atau port lokal terlebih dahulu.
-   Batasi resource proses/container dan pantau RAM, CPU, disk, suhu.
-   Siapkan rollback ke versi aplikasi sebelumnya.

## 7. Backup & recovery

-   Backup database harian.
-   Backup file terpisah.
-   Salinan backup di media/lokasi lain.
-   Enkripsi backup.
-   Uji restore berkala.
-   Target awal: RPO 24 jam, RTO 4 jam; revisi setelah pengujian.

## 8. Security release checklist

-   [ ] Tidak ada secret di Git.
-   [ ] Authorization diuji pada semua endpoint.
-   [ ] CSRF/XSS/SQL injection ditinjau.
-   [ ] Rate limit aktif.
-   [ ] File upload divalidasi.
-   [ ] Database privat.
-   [ ] Backup dan restore teruji.
-   [ ] Audit log berfungsi.
-   [ ] Dependency vulnerability diperiksa.
