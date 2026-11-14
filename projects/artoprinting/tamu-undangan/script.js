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
    link: { pemisahNama: '+', salin: 'link' },
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
  function kodeNama(nama) {
    // Dalam query string, tanda "+" dibaca sebagai spasi oleh URLSearchParams.
    return encodeURIComponent(nama.replace(/\s+/g, ' ')).replace(/%20/g, '+');
  }

  function templateAwal(jenis) {
    var pembuka = 'Assalamu’alaikum Warahmatullahi Wabarakatuh.\\n\\n';
    var isi = jenis === 'pernikahan'
      ? 'Dengan memohon rahmat dan ridho Allah SWT, kami mengundang {{nama}} untuk menghadiri acara pernikahan kami.\\n\\n'
      : 'Dengan memohon rahmat dan ridho Allah SWT, kami mengundang {{nama}} untuk hadir dalam acara tasyakuran khitan anak kami.\\n\\n';
    var penutup = jenis === 'pernikahan'
      ? 'Merupakan kehormatan dan kebahagiaan bagi kami apabila berkenan hadir dan memberikan doa restu.\\n\\n'
      : 'Kehadiran dan doa restu akan menjadi kebahagiaan tersendiri bagi kami.\\n\\n';
    return pembuka + isi + 'Link Undangan:\\n{{link}}\\n\\n' + penutup +
      'Wassalamu’alaikum Warahmatullahi Wabarakatuh.\\n\\nHormat kami,\\n{{pengundang}}';
  }

  function buatPesan(data) {
    var editor = document.getElementById('template-pesan');
    var template = editor && editor.value.trim() ? editor.value : templateAwal(document.getElementById('jenis').value);
    return template
      .split('{{nama}}').join(data.nama)
      .split('{{link}}').join(data.link)
      .split('{{pengundang}}').join(data.pengundang);
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
    ['Nama Tamu', 'Salin', 'WhatsApp'].forEach(function (h) {
      var th = el('th', 'px-4 py-2', h);
      th.scope = 'col';
      trHead.appendChild(th);
    });
    thead.appendChild(trHead);
    var tbody = el('tbody');

    namaArray.forEach(function (nama) {
      var linkUndangan = link + '?to=' + kodeNama(nama);
      var pesan = buatPesan({ nama: nama, link: linkUndangan, pengundang: pengundang });

      var tr = el('tr', 'border-t');
      tr.appendChild(el('td', 'px-4 py-2', nama));

      var tdSalin = el('td', 'px-4 py-2');
      var btnSalin = el('button', 'bg-sky-500 hover:bg-sky-600 text-white px-3 py-3 rounded', 'Salin');
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
      var a = el('a', 'bg-green-500 hover:bg-green-600 text-white px-3 py-3 rounded focus:outline-none focus:ring-2 focus:ring-green-400', 'Kirim');
      a.href = 'https://wa.me/?text=' + encodeURIComponent(pesan);
      a.target = '_blank';
      a.rel = 'noopener';
      // Tautan langsung menjadi kontrol aksi agar tidak ada elemen interaktif bersarang.
      tdWa.appendChild(a);
      tr.appendChild(tdWa);

      tbody.appendChild(tr);
    });

    var caption = el('caption', 'sr-only', 'Daftar tautan undangan untuk setiap tamu');
    table.appendChild(caption);
    table.appendChild(thead);
    table.appendChild(tbody);
    var hasil = document.getElementById('hasil');
    hasil.innerHTML = '';
    hasil.appendChild(table);

    // simpan isian di URL supaya bisa dibagikan / dibuka ulang
    var params = new URLSearchParams({ jenis: jenis, nama: namaArray.join(', '), link: link, pengundang: pengundang });
    window.history.replaceState({}, '', location.pathname + '#' + params.toString());
  }

  function modeHalaman() {
    var tombol = document.getElementById('buat-link');
    return (tombol && tombol.dataset.mode) || 'link';
  }

  function muatDariURL() {
    var kunci = ['jenis', 'nama', 'link', 'pengundang'];
    var query = new URLSearchParams(window.location.search);
    var params = query;
    var dataLama = kunci.some(function (k) { return query.has(k); });

    // Link lama berbentuk query tetap dibaca, lalu dipindahkan ke fragment.
    // Fragment tidak dikirim ke server sebagai bagian HTTP request atau Referer.
    if (!dataLama && window.location.hash.length > 1) {
      params = new URLSearchParams(window.location.hash.slice(1));
    }

    kunci.forEach(function (k) {
      if (params.has(k)) document.getElementById(k).value = params.get(k);
    });

    if (dataLama) {
      window.history.replaceState({}, '', location.pathname + '#' + params.toString());
    }

    if (params.get('jenis') && params.get('nama') && params.get('link') && params.get('pengundang')) {
      buatTabel(modeHalaman());
    }
  }

  // kompatibilitas dengan versi lama (onclick="buatLink()" / "buatLink2()")
  window.buatLink = function () { buatTabel('link'); };
  window.buatLink2 = function () { buatTabel('pesan'); };

  document.addEventListener('DOMContentLoaded', function () {
    var tombol = document.getElementById('buat-link');
    var editor = document.getElementById('template-pesan');
    var resetTemplate = document.getElementById('reset-template');
    var jenis = document.getElementById('jenis');
    var templateDiubah = false;

    if (editor) {
      editor.value = templateAwal(jenis ? jenis.value : 'khitan');
      editor.addEventListener('input', function () { templateDiubah = true; });
    }
    if (jenis) {
      jenis.addEventListener('change', function () {
        if (editor && !templateDiubah) editor.value = templateAwal(jenis.value);
      });
    }
    if (resetTemplate && editor) {
      resetTemplate.addEventListener('click', function () {
        editor.value = templateAwal(jenis ? jenis.value : 'khitan');
        templateDiubah = false;
        editor.focus();
      });
    }
    if (tombol) tombol.addEventListener('click', function () { buatTabel(modeHalaman()); });
    muatDariURL();
  });
})();
