# Laporan Audit GoWA ↔ Gemini Bridge

- **Tanggal audit:** 15 November 2026
- **Waktu snapshot:** 2026-11-15 17:16:20 UTC
- **Metode:** snapshot bukti berbasis pencarian pola pada source GoWA dan Bridge
- **Status:** audit statis awal; kompatibilitas runtime belum dinyatakan terverifikasi

> Laporan ini merupakan rangkuman aman dari snapshot lokal. Path absolut, nilai konfigurasi, identitas akun, dan data sensitif tidak disertakan. Snapshot sumber lengkap tetap berada di lingkungan lokal.

## 1. Cakupan dan kelengkapan

| Item | Hasil |
|---|---:|
| Source GoWA tersedia | Ya |
| File GoWA yang dipindai | 383 |
| File Bridge yang dipindai | 5 |
| Pemindaian GoWA terpotong | **Ya** |
| File .env tersedia | Ya |
| Permission .env | 0600 |
| Nilai environment/secret dikumpulkan | Tidak |

**Catatan:** karena pemindaian GoWA terpotong, hasil ini bukan inventaris menyeluruh. Pencarian pola hanya menunjukkan lokasi kandidat bukti, bukan membuktikan semantik atau kompatibilitas.

## 2. Temuan utama

### 2.1 Potensi ketidaksesuaian identitas perangkat — prioritas tinggi

Pada Bridge, konfigurasi memuat dua nilai terpisah:
- `OWNER_JID` sebagai identitas akun WhatsApp pemilik.
- `GOWA_DEVICE_ID` sebagai identitas device GoWA.

Namun, handler webhook pada `index.js:144` membandingkan `data.device_id` dengan `ownerJid`, bukan dengan `deviceId`.

Bukti Bridge:
- `index.js:40-41`: konfigurasi `ownerJid` dan `deviceId` dimuat terpisah.
- `index.js:144`: pemeriksaan `data.device_id !== ownerJid`.
- `index.js:154`: `OWNER_JID` juga dipakai untuk pemeriksaan self-chat.

Bukti GoWA:
- `docs/openapi.yaml:310-316`: dokumentasi memisahkan field `device_id` dan `jid`; `jid` dideskripsikan sebagai WhatsApp JID akun yang login.
- Dokumentasi GoWA juga menyediakan konfigurasi webhook khusus per-device dan endpoint yang menggunakan `device_id`.

**Analisis:** ada indikasi kuat bahwa pemeriksaan identitas device pada Bridge menggunakan variabel yang salah. Tetapi perubahan belum dilakukan. Sebelum memperbaiki, cocokkan implementasi payload webhook GoWA aktual (bukan hanya OpenAPI) untuk memastikan bentuk dan makna `data.device_id`.

### 2.2 Kontrak event dan payload

Bridge saat ini mengharapkan:
- `event === "message"`
- `payload` berupa object
- field pesan `chat_id`, `from`, `is_from_me`, `body`, dan `id`

Bukti utama Bridge berada di `index.js:145-162`. Snapshot GoWA menemukan dokumentasi event/message, field `is_from_me`, dan beberapa referensi message ID pada `docs/openapi.yaml`.

**Status:** belum cukup untuk menyatakan seluruh payload cocok. Perlu menelusuri fungsi dispatch webhook GoWA dan contoh payload message yang benar-benar dikirim.

### 2.3 Verifikasi signature webhook

Bridge:
- Membuat HMAC-SHA256 dari raw request body.
- Membandingkan signature dengan `crypto.timingSafeEqual` setelah memeriksa panjang buffer.
- Membaca header `x-hub-signature-256`.

Bukti: `index.js:100-109` dan `index.js:193`.

GoWA:
- OpenAPI memuat konfigurasi webhook global dan per-device, termasuk secret untuk menandatangani payload.
- Dokumentasi juga menyebut header `X-Hub-Signature-256` untuk HMAC-SHA256 raw body pada salah satu jalur webhook Chatwoot.

**Status:** mekanisme Bridge tampak menerapkan pemeriksaan HMAC dengan perbandingan constant-time. Namun, kecocokan antara jalur webhook GoWA yang digunakan, raw body, format prefix/encoding signature, dan secret aktual belum dibuktikan. Dokumentasi jalur Chatwoot tidak otomatis membuktikan kontrak webhook message biasa.

### 2.4 Retry dan timeout

Pola yang ditemukan pada GoWA mencakup request timeout middleware, timeout berbasis context, serta worker retry untuk beberapa alur. Hasil pencarian juga menemukan beberapa mekanisme retry terjadwal dan retry media.

**Status:** bukti ini bersifat umum pada source GoWA. Belum membuktikan retry delivery webhook menuju Bridge atau perilaku retry pada kegagalan HTTP Bridge.

## 3. Konfigurasi yang terdeteksi

Hanya nama variabel yang dicatat; nilai tidak dikumpulkan.

- `BRIDGE_HOST`
- `BRIDGE_PORT`
- `GEMINI_API_KEY`
- `GEMINI_MODEL`
- `GOWA_DEVICE_ID`
- `GOWA_PASSWORD`
- `GOWA_URL`
- `GOWA_USERNAME`
- `OWNER_JID`
- `WEBHOOK_SECRET`

Permission file `.env` terdeteksi `0600`, yang membatasi akses file kepada pemiliknya.

## 4. Bukti integritas source

SHA-256 file yang menjadi bukti utama snapshot:

| File | SHA-256 |
|---|---|
| GoWA `docs/openapi.yaml` | `8910c54538089eaca1e3982407bab2887b6c6f7a0882d612a7998bb560023436` |
| GoWA `src/cmd/root.go` | `bf1f37c3fde454a07d9298e5b281e9f3bf871129745293a45bac8fb73299bbac` |
| Bridge `index.js` | `32560d3069508f1b36f06fd384dcb90380548df0278bcd4e0c228ae43fd2a0ce` |
| Bridge `test/helpers.js` | `b03c9ff446b22a410f343a22c00709c7341595d26d3dc1ede5d5eb5d24c618cb` |
| Bridge `test/bridge.test.js` | `4bca7b8c14fdb34d273884e6cfb6d24fbfb2afe05d65b31c539806965d37f0b5` |

Hash mengidentifikasi isi file saat snapshot dibuat; hash bukan bukti bahwa file tersebut masih sama pada commit repository saat ini.

## 5. Rekomendasi tindak lanjut

1. Periksa implementasi GoWA yang benar-benar membentuk dan mengirim webhook message, termasuk nilai dan sumber `device_id`.
2. Verifikasi apakah `device_id` harus dibandingkan dengan `GOWA_DEVICE_ID`; jangan menyamakan device ID dengan `OWNER_JID` tanpa bukti.
3. Cocokkan event name dan struktur payload aktual dengan parser Bridge.
4. Verifikasi signature end-to-end: raw body, secret yang digunakan, header, prefix, dan encoding.
5. Audit apakah GoWA melakukan retry delivery webhook ketika Bridge merespons error atau timeout.
6. Jalankan regression test untuk device mismatch, event tidak dikenal, payload invalid, signature invalid, dan pemrosesan duplikat setelah kontrak payload dipastikan.

## 6. Batasan dan keselamatan audit

- Snapshot menggunakan pencarian pola teks dan pemindaian GoWA terpotong.
- Nilai secret dan environment tidak dikumpulkan.
- Tidak ada service yang dihentikan atau diubah.
- Tidak ada endpoint/API eksternal yang dipanggil oleh proses snapshot.
- Tidak ada pesan WhatsApp yang dikirim.
- Laporan ini tidak menyatakan integrasi siap production.

## 7. Kesimpulan

Temuan paling penting adalah potensi bug pemeriksaan identitas: Bridge memuat `GOWA_DEVICE_ID`, tetapi pemeriksaan `data.device_id` pada handler menggunakan `OWNER_JID`. Ini harus diverifikasi terhadap implementasi webhook GoWA aktual sebelum perubahan kode dilakukan.

**Keputusan audit:** lanjutkan ke pemeriksaan source dispatch webhook GoWA; jangan menaikkan integrasi ke staging/production berdasarkan snapshot ini saja.
