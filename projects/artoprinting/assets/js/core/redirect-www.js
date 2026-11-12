// redirect-www.js — khusus hosting GitHub Pages dengan domain sendiri.
// 1) Mengalihkan artoprintingpbg.com -> www.artoprintingpbg.com
// 2) Mengalihkan http -> https
// Tidak berjalan di localhost / jaringan lokal (192.168.x.x) agar mudah dites.
// (dulu: assets/js/github.js — logika tidak berubah)
(function () {
  var host = location.hostname;
  var isLocal = host === 'localhost' || host === '127.0.0.1' || host.indexOf('192.168.') === 0;
  if (isLocal) {
    console.log('Sedang di localhost, fungsi redirect khusus github page tidak dijalankan');
    return;
  }

  if (host.indexOf('www.') !== 0 && !/^localhost$|^\d+\.\d+\.\d+\.\d+$/.test(host)) {
    location.replace(location.protocol + '//www.' + host + location.pathname + location.search + location.hash);
    return;
  }
  if (location.protocol === 'http:') {
    location.href = 'https://' + host + location.pathname + location.search + location.hash;
  }
})();
