// analytics.js — memasang Google Analytics (gtag.js).
// Dimuat sebagai script biasa di <head> pada setiap halaman utama.
// (dulu: assets/js/gtag.js — logika tidak berubah)
//
// Catatan: setting.json menyimpan google_tag "G-7D0RLQEEQD", berbeda dari ID
// yang dimuat di bawah ini. Repository belum membuktikan properti yang benar;
// jangan mengubah ID sampai pemilik mengonfirmasi Measurement ID aktif.
(function () {
  var GA_MEASUREMENT_ID = 'G-RTHYD0QDMC';

  // Cegah tag terpasang dua kali
  if (document.querySelector('script[src*="googletagmanager.com/gtag/js"]')) return;

  var gtagScript = document.createElement('script');
  gtagScript.async = true;
  gtagScript.src = 'https://www.googletagmanager.com/gtag/js?id=' + GA_MEASUREMENT_ID;

  var inlineScript = document.createElement('script');
  inlineScript.text =
    'window.dataLayer = window.dataLayer || [];' +
    'function gtag(){dataLayer.push(arguments);}' +
    "gtag('js', new Date());" +
    "gtag('config', '" + GA_MEASUREMENT_ID + "');";

  var head = document.head || document.getElementsByTagName('head')[0];
  head.appendChild(gtagScript);
  head.appendChild(inlineScript);
})();
