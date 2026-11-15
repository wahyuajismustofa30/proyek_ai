# WhatsApp Business Label Router

## Status implementasi

Fondasi routing label telah ditambahkan. Integrasi API GoWA untuk membaca dan menambahkan label **belum diaktifkan** karena endpoint, autentikasi, dan payload versi GoWA yang sedang berjalan harus diverifikasi terlebih dahulu. Adapter bersifat fail-closed dan tidak mengarang endpoint.

## Label

Nama label dapat diatur melalui environment:

- `WA_LABEL_OWNER` (default `Owner`)
- `WA_LABEL_PERSONAL` (default `Pribadi`)
- `WA_LABEL_ARTOPRINTING` (default `Customer ArtoPrinting`)
- `WA_LABEL_DEKEKU` (default `Customer Dekeku`)

`OWNER_JID` tetap menjadi sumber verifikasi identitas OWNER. Label Owner pada kontak lain akan ditahan dan tidak memberikan akses OWNER.

## Mode Pribadi

`PERSONAL_MODE=true` mengizinkan route PERSONAL untuk kontak berlabel Pribadi. Nilai selain `true` menonaktifkan route tersebut.

## Multi-label

Label ArtoPrinting dan DEKEKU dapat dirutekan bersamaan. Adapter penulisan hanya menyediakan operasi aditif; tidak ada operasi penggantian seluruh label.

## Klasifikasi kontak baru

Kontak tanpa label dikembalikan sebagai tindakan `classify` beserta pertanyaan identifikasi. Label tidak ditambahkan sebelum tujuan dikonfirmasi. Hasil konfirmasi diteruskan melalui `confirmedPurposes`.

## Batasan tahap ini

- Modul router dan adapter belum dipasang ke alur HTTP webhook.
- Penyimpanan status klasifikasi lintas restart belum tersedia.
- Pengiriman balasan dan mutasi label WhatsApp aktual tidak dilakukan.
- Knowledge base ArtoPrinting dan DEKEKU belum terhubung ke Gemini.
- DRY-RUN tetap wajib; integrasi produksi memerlukan adapter GoWA yang diverifikasi dan pengujian berikutnya.

## Pengujian

Jalankan:

```sh
npm test
```
