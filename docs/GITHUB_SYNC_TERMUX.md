# GitHub Sync untuk Termux

Tool berada di `scripts/github-sync-termux.sh` dan bekerja langsung pada branch
`main` di repository Git yang memakai remote `origin`. Jalankan dari direktori
repository yang ingin disinkronkan.

## Instalasi di Termux

Pastikan Git tersedia:

```sh
pkg install git
mkdir -p "$HOME/bin"
```

Dari root clone repository `proyek_ai`, buat shortcut:

```sh
ln -sfn "$PWD/scripts/github-sync-termux.sh" "$HOME/bin/github-sync"
```

Pastikan `$HOME/bin` sudah ada di `PATH`. Jika belum, tambahkan ke
`~/.bashrc`:

```sh
export PATH="$HOME/bin:$PATH"
```

Muat ulang konfigurasi shell:

```sh
source ~/.bashrc
```

Kemudian dari repository:

```sh
cd ~/git-repos/proyek_ai
github-sync
```

## Alur kerja

1. Memastikan perintah dijalankan di repository Git, remote `origin` tersedia,
   dan branch aktif adalah `main`. Tool tidak berpindah branch atau membuat
   branch baru.
2. Menjalankan `git fetch origin` untuk membaca kondisi remote.
3. Jika `main` lokal tertinggal dan working tree bersih, tool memperbaruinya
   dengan `git merge --ff-only origin/main`. Jika working tree memiliki
   perubahan, tool berhenti tanpa mengubah atau membuang perubahan tersebut.
4. Jika branch lokal dan remote divergen, tool berhenti. Pengguna perlu meninjau
   riwayat dan menyelesaikan perbedaan secara manual; tool tidak melakukan
   merge, rebase, reset, atau force-push otomatis.
5. Jika direktori `projects/` berubah, tool memperbarui
   `docs/PROJECT_INDEX.md` menggunakan generator repository.
6. Tool memeriksa nama file yang umum digunakan untuk secret, menampilkan
   perubahan, lalu meminta konfirmasi sebelum staging dan commit.
7. Setelah konfirmasi, tool menjalankan `git add -A`, memeriksa whitespace,
   menampilkan ringkasan staging, dan meminta pesan commit. Jika konfirmasi
   commit ditolak, staging dan file kerja tetap dipertahankan.
8. Tool memastikan `origin/main` masih merupakan leluhur commit lokal, lalu
   meminta konfirmasi sebelum menjalankan `git push origin main`.
9. Push adalah push biasa ke `main`. Jika remote berubah bersamaan atau push
   ditolak, commit lokal tetap tersimpan dan tool tidak melakukan force-push.

## Pengamanan

- Periksa daftar file sebelum menyetujui staging. Jangan ikutkan token, password,
  file `.env`, private key, atau data pribadi.
- Pemeriksaan nama file rahasia merupakan lapisan pencegahan sederhana, bukan
  pengganti secret scanner CI.
- Perubahan staged milik pengguna tidak dihapus saat proses dibatalkan.
- Tool tidak menjalankan `reset`, `clean`, `stash`, `rebase`,
  `merge --abort`, atau force-push.
- Pull Request tidak diperlukan untuk alur normal. Buat PR hanya jika memang
  diminta secara eksplisit.
- CI tetap dapat berjalan setelah push sebagai pemeriksaan kualitas; CI tidak
  menjadi syarat lokal untuk membuat commit.

## Pengujian

Dari root repository:

```sh
python -m unittest scripts.tests.test_github_sync_termux -v
bash -n scripts/github-sync-termux.sh
```
