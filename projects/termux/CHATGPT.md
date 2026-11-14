# chatGPT — Termux CLI

Program Bash interaktif untuk OpenAI Responses API di Android/Termux.

## Persyaratan

- Bash
- `curl`
- `jq`
- `id`, `stat`, `date`
- `mktemp` untuk penyimpanan riwayat

Program memeriksa dependensi utama saat dijalankan. Tidak diperlukan root.

## API key dan model

API key dibaca dari environment variable `OPENAI_API_KEY` (prioritas) atau file `~/.config/openai.env` dengan satu deklarasi `OPENAI_API_KEY=nilai` atau `export OPENAI_API_KEY=nilai`. File konfigurasi harus berupa file biasa, dimiliki pengguna saat ini, dan tidak dapat dibaca group/others. Program tidak mengubah permission secara otomatis.

Model default tetap `gpt-6-luna`. Gunakan `OPENAI_MODEL` untuk menentukan model awal, atau `/model NAMA` untuk mengganti model hanya pada sesi aktif.

## Perintah

| Perintah | Fungsi |
|---|---|
| `/help` | Bantuan perintah |
| `/keluar` | Keluar |
| `/reset` | Memulai konteks percakapan baru tanpa menghapus riwayat |
| `/model` | Menampilkan model aktif |
| `/model NAMA` | Mengganti model untuk sesi aktif |
| `/info` | Menampilkan ID, model, jumlah pesan, dan status riwayat |
| `/clear` | Membersihkan tampilan terminal tanpa menghapus riwayat |
| `/history` | Menampilkan daftar percakapan tersimpan |
| `/history on` | Mengaktifkan penyimpanan untuk sesi ini |
| `/history off` | Menonaktifkan penyimpanan untuk sesi ini; riwayat lama dipertahankan |
| `/resume ID` | Melanjutkan percakapan tersimpan |
| `/delete ID` | Menghapus satu percakapan setelah konfirmasi |
| `/history-clear` | Menghapus seluruh riwayat setelah konfirmasi |

Penyimpanan riwayat secara default nonaktif. Aktifkan dengan `/history on`. Riwayat menyimpan pesan pengguna, jawaban, model, waktu, dan ID respons API; jangan aktifkan pada perangkat bersama jika isi percakapan bersifat sensitif.

## Lokasi dan keamanan riwayat

Riwayat disimpan di:

`~/.local/share/chatGPT/conversations.json`

Direktori dan file dibuat privat menggunakan umask `077`. Program menolak symlink, pemilik yang berbeda, permission group/others, serta format data yang tidak valid. Permission yang sudah ada tidak diubah otomatis; perbaiki secara manual jika ditolak. File riwayat tidak disimpan di direktori proyek.

## Konteks percakapan

Program menyimpan `previous_response_id` per percakapan. `/reset` membuat konteks baru. `/resume ID` memulihkan ID respons terakhir; konteks API dapat kedaluwarsa atau tidak tersedia. Jika API menolak konteks sebelumnya, gunakan `/reset` untuk melanjutkan dengan percakapan baru. Kegagalan API tidak mengganti ID respons terakhir yang valid.

Program memerlukan terminal interaktif. Pengujian otomatis sebaiknya menggunakan mock `curl`; jangan mengirim API request sungguhan untuk pengujian.
