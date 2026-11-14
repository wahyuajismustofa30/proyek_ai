// config.js — semua pengaturan situs di satu tempat.
// Ubah nilai di sini, bukan di dalam modul fitur.

export const CONFIG = {
  // Nomor WhatsApp admin utama (format internasional tanpa "+")
  waAdmin: '6285712110870',

  // Lokasi file data. Path ini juga dipakai alur sinkronisasi spreadsheet,
  // jadi jangan dipindahkan tanpa menyesuaikan alur tersebut.
  dataUrl: {
    produk: '/assets/data/produk.json',
    setting: '/assets/data/setting.json',
    ulasan: '/assets/data/ulasan.json',
  },

  // Alamat halaman. Semua huruf kecil; halaman selain beranda ada di folder /laman/.
  halaman: {
    beranda: '/',
    katalog: '/laman/katalog/',
    layanan: '/laman/layanan/',
    caraPesan: '/laman/cara-pesan/',
    testimoni: '/laman/testimoni/',
    kontak: '/laman/kontak/',
    produk: '/laman/produk/',
  },

  // Aset merek
  img: {
    maskot: 'https://drive.dekeku.my.id/storage/old/artoprinting/brand/maskot.webp',
    fallbackProduk: 'https://drive.dekeku.my.id/storage/old/artoprinting/brand/logo-arto-printing.webp',
  },

  // Katalog di beranda
  katalog: {
    perHalaman: 20,
    produkAwal: 'Undangan_Cetak',
    jedaCariMs: 150,
  },

  // Testimoni: jumlah ulasan yang tampil sebelum tombol "Baca ... ulasan lainnya"
  testimoniAwal: 9,
  // Jumlah ulasan yang dicuplik di Beranda
  testimoniBeranda: 3,

  // Urutan tab produk (kunci yang tidak ada di sini tetap tampil di belakang)
  urutanProduk: [
    'Undangan_Cetak', 'Undangan_Web', 'Undangan_Custom', 'Aqiqah', 'Mug',
    'Kartu_Nama', 'Kartu_Ucapan', 'Pigura', 'Cover', 'Stiker', 'Banner', 'Layanan',
  ],

  // Deskripsi pengganti untuk kategori yang teksnya di setting.json belum sesuai
  // (kunci = slug produk, mis. "undangan-cetak")
  deskripsiKhusus: {
    'undangan-cetak': 'Ratusan model undangan cetak untuk pernikahan, khitan, dan pengajian.',
    'undangan-web': 'Undangan digital yang tinggal dibagikan lewat link. Buka demonya untuk melihat tampilan lengkapnya.',
    'undangan-custom': 'Contoh undangan yang dirancang khusus sesuai permintaan pelanggan.',
    'stiker': 'Stiker label produk, kemasan, dan acara dengan berbagai bahan dan ukuran.',
    'banner': 'Banner dan backdrop untuk promosi toko, acara, maupun kegiatan instansi.',
  },
};
