// tamu-undangan/script.js — membuat link undangan per tamu + pesan WhatsApp.
//
// Dipakai oleh dua halaman dengan "mode" berbeda (ditulis di atribut data-mode pada tombol):
//   index.html     -> mode "link"  : spasi di nama jadi "_" ; tombol Salin menyalin LINK undangan
//   generator.html -> mode "pesan" : spasi di nama jadi "+" ; tombol Salin menyalin seluruh PESAN
//
// Bergantung pada showAlert() dari berbagi-koding/js/utils@v1.js (dimuat lebih dulu di <head>).
// Bila skrip itu gagal dimuat, pesan tampil lewat alert() biasa.
//
// Fungsi lama buatLink() dan buatLink2() tetap tersedia agar kompatibel.

(function () {
  'use strict';

  var MODE = {
    link: { pemisahNama: '_', salin: 'link' },
    pesan: { pemisahNama: '+', salin: 'pesan' },
  };

  var TEMPLATE_PESAN = {
    pernikahan: function (d) {
      return 'Assalamu’alaikum Warahmatullahi Wabarakatuh.\n\n' +
        'Dengan memohon rahmat dan ridho Allah SWT, kami mengundang ' + d.nama + ' untuk menghadiri acara pernikahan kami.\n\n' +
        'Link Undangan:\n' + d.link + '\n\n' +
        'Merupakan kehormatan dan kebahagiaan bagi kami apabila berkenan hadir dan memberikan doa restu.\n\n' +
        'Wassalamu’alaikum Warahmatullahi Wabarakatuh.\n\n' +
        'Hormat kami,\n' + d.pengundang;
    },
    khitan: function (d) {
      return 'Assalamu’alaikum Warahmatullahi Wabarakatuh.\n\n' +
        'Dengan memohon rahmat dan ridho Allah SWT, kami mengundang ' + d.nama + ' untuk hadir dalam acara tasyakuran khitan anak kami.\n\n' +
        'Link Undangan:\n' + d.link + '\n\n' +
        'Kehadiran dan doa restu akan menjadi kebahagiaan tersendiri bagi kami.\n\n' +
        'Wassalamu’alaikum Warahmatullahi Wabarakatuh.\n\n' +
        'Hormat kami,\n' + d.pengundang;
    },
  };

  /**
   * Nama tamu untuk parameter ?to=
   *  - mode link : "Bapak Rudi" -> "Bapak_Rudi"
   *  - mode pesan: "Bapak Rudi" -> "Bapak+Rudi"  (tanda + = spasi pada URL)
   * Karakter khusus (&, ?, #, dll.) tetap di-encode supaya link tidak terpotong.
   */
  function kodeNama(nama, mode) {
    if (mode.pemisahNama === '+') {
      return encodeURIComponent(nama.replace(/\s+/g, ' ')).replace(/%20/g, '+');
    }
    return encodeURIComponent(nama.replace(/\s+/g, mode.pemisahNama));
  }

  function tampilkanPesan(pesan, jenis, durasi) {
    if (typeof window.showAlert === 'function') window.showAlert(pesan, jenis, durasi);
    else window.alert(pesan);
  }

  function nilai(id) {
    return document.getElementById(id).value.trim();
  }

  function el(tag, kelas, teks) {
    var e = document.createElement(tag);
    if (kelas) e.className = kelas;
    if (teks != null) e.textContent = teks;
    return e;
  }

  function buatTabel(modeNama) {
    var mode = MODE[modeNama] || MODE.link;
    var jenis = document.getElementById('jenis').value;
    var namaInput = nilai('nama');
    var pengundang = nilai('pengundang');
    var link = nilai('link');

    if (!namaInput) return tampilkanPesan('Nama tamu tidak boleh kosong', 'error');

    var namaArray = namaInput.split(',').map(function (n) { return n.trim(); }).filter(Boolean);
    if (namaArray.length === 0) return window.alert('Silakan isi minimal satu nama.');

    var table = el('table', 'w-full text-sm text-left border border-sky-300 bg-white rounded-lg overflow-hidden');
    var thead = el('thead', 'bg-sky-100 text-sky-700');
    var trHead = el('tr');
    ['Nama Tamu', 'Salin', 'WhatsApp'].forEach(function (h) { trHead.appendChild(el('th', 'px-4 py-2', h)); });
    thead.appendChild(trHead);
    var tbody = el('tbody');

    namaArray.forEach(function (nama) {
      var linkUndangan = link + '?to=' + kodeNama(nama, mode);
      var template = TEMPLATE_PESAN[jenis] || TEMPLATE_PESAN.khitan;
      var pesan = template({ nama: nama, link: linkUndangan, pengundang: pengundang });

      var tr = el('tr', 'border-t');
      tr.appendChild(el('td', 'px-4 py-2', nama));

      var tdSalin = el('td', 'px-4 py-2');
      var btnSalin = el('button', 'bg-sky-500 hover:bg-sky-600 text-white px-3 py-1 rounded', 'Salin');
      btnSalin.type = 'button';
      btnSalin.addEventListener('click', function () {
        var teks = mode.salin === 'pesan' ? pesan : linkUndangan;
        var gagal = function () { window.prompt('Salin secara manual:', teks); };
        if (!navigator.clipboard || !window.isSecureContext) return gagal();
        // pesan sukses hanya tampil bila penyalinan benar-benar berhasil
        navigator.clipboard.writeText(teks).then(function () {
          tampilkanPesan('Link untuk ' + nama + ' berhasil disalin', 'success', '3000');
        }, gagal);
      });
      tdSalin.appendChild(btnSalin);
      tr.appendChild(tdSalin);

      var tdWa = el('td', 'px-4 py-2');
      var a = el('a');
      a.href = 'https://wa.me/?text=' + encodeURIComponent(pesan);
      a.target = '_blank';
      a.rel = 'noopener';
      // struktur <a><button> dipertahankan agar tampilan tombol sama seperti sebelumnya
      var btnWa = el('button', 'bg-green-500 hover:bg-green-600 text-white px-3 py-1 rounded focus:outline-none focus:ring-2 focus:ring-green-400', 'Kirim');
      btnWa.type = 'button';
      a.appendChild(btnWa);
      tdWa.appendChild(a);
      tr.appendChild(tdWa);

      tbody.appendChild(tr);
    });

    table.appendChild(thead);
    table.appendChild(tbody);
    var hasil = document.getElementById('hasil');
    hasil.innerHTML = '';
    hasil.appendChild(table);

    // simpan isian di URL supaya bisa dibagikan / dibuka ulang
    var params = new URLSearchParams({ jenis: jenis, nama: namaArray.join(', '), link: link, pengundang: pengundang });
    window.history.replaceState({}, '', location.pathname + '?' + params);
  }

  function modeHalaman() {
    var tombol = document.getElementById('buat-link');
    return (tombol && tombol.dataset.mode) || 'link';
  }

  function muatDariURL() {
    var params = new URLSearchParams(window.location.search);
    ['jenis', 'nama', 'link', 'pengundang'].forEach(function (k) {
      if (params.has(k)) document.getElementById(k).value = params.get(k);
    });
    if (params.get('jenis') && params.get('nama') && params.get('link') && params.get('pengundang')) {
      buatTabel(modeHalaman());
    }
  }

  // kompatibilitas dengan versi lama (onclick="buatLink()" / "buatLink2()")
  window.buatLink = function () { buatTabel('link'); };
  window.buatLink2 = function () { buatTabel('pesan'); };

  document.addEventListener('DOMContentLoaded', function () {
    var tombol = document.getElementById('buat-link');
    if (tombol) tombol.addEventListener('click', function () { buatTabel(modeHalaman()); });
    muatDariURL();
  });
})();
