// alias-404.js — dipakai 404.html (GitHub Pages menampilkannya untuk alamat yang tidak ada).
// Mengarahkan alamat pendek, alamat lama, dan variasi huruf besar ke alamat resmi:
//   /katalog, /Katalog, /KATALOG, /Laman/Katalog  -> /laman/katalog/
//   /cara-pesan, /Cara Pesan, /carapesan          -> /laman/cara-pesan/
//   /produk                                       -> /laman/produk/
//   /beranda                                      -> /
// Query (?produk=..., ?p=..&id=..) dan hash ikut dibawa.
(function () {
  var resmi = {
    'beranda': '/',
    'katalog': '/laman/katalog/',
    'layanan': '/laman/layanan/',
    'cara-pesan': '/laman/cara-pesan/',
    'carapesan': '/laman/cara-pesan/',
    'cara_pesan': '/laman/cara-pesan/',
    'testimoni': '/laman/testimoni/',
    'kontak': '/laman/kontak/',
    'produk': '/laman/produk/'
  };
  var jalur = decodeURIComponent(location.pathname)
    .replace(/\/index\.html$/i, '')
    .replace(/^\/+|\/+$/g, '')
    .toLowerCase()
    .replace(/\s+/g, '-')
    .replace(/^laman\//, '');
  var tujuan = resmi[jalur];
  if (tujuan && tujuan !== location.pathname) {
    location.replace(tujuan + location.search + location.hash);
  }
})();
