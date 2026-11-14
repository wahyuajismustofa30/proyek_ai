// redirect-lama.js — menjaga link lama tetap jalan setelah beranda dipecah per halaman.
// Dimuat sebagai script biasa di <head> index.html (berjalan sebelum halaman dirender).
//
//   /?produk=mug&kategori=...   -> /laman/katalog/?produk=mug&kategori=...
//   /#katalog-section           -> /laman/katalog/
//   /#layanan-section           -> /laman/layanan/
//   /#cara-pesan                -> /laman/cara-pesan/
//   /#testimoni-section         -> /laman/testimoni/
//   /#tentang-section           -> /laman/kontak/
(function () {
  var q = new URLSearchParams(location.search);
  if (q.has('produk') || q.has('kategori')) {
    location.replace('/laman/katalog/' + location.search);
    return;
  }
  var peta = {
    '#katalog-section': '/laman/katalog/',
    '#layanan-section': '/laman/layanan/',
    '#cara-pesan': '/laman/cara-pesan/',
    '#testimoni-section': '/laman/testimoni/',
    '#tentang-section': '/laman/kontak/'
  };
  if (peta[location.hash]) location.replace(peta[location.hash]);
})();
