// tamu-undangan/script.js — membuat link undangan per tamu + pesan WhatsApp.
//
// Dipakai oleh dua halaman dengan "mode" berbeda (ditulis di atribut data-mode pada tombol):
//   Kedua halaman: tombol Salin menyalin seluruh PESAN undangan personal.
// Nama tamu pada kedua mode memakai tanda "+" sebagai pengganti spasi di URL.
//
// Bergantung pada showAlert() dari berbagi-koding/js/utils@v1.js (dimuat lebih dulu di <head>).
// Bila skrip itu gagal dimuat, pesan tampil lewat alert() biasa.
//
// Fungsi lama buatLink() dan buatLink2() tetap tersedia agar kompatibel.

(function () {
  'use strict';

  /**
   * Nama tamu untuk parameter ?to=
   *  - kedua mode : "Bapak Rudi" -> "Bapak+Rudi" (tanda + = spasi pada URL)
   * Karakter khusus (&, ?, #, dll.) tetap di-encode supaya link tidak terpotong.
   */
  function kodeNama(nama) {
    // Dalam query string, tanda "+" dibaca sebagai spasi oleh URLSearchParams.
    return encodeURIComponent(nama.replace(/\s+/g, ' ')).replace(/%20/g, '+');
  }

  function templateAwal(jenis) {
    var pembuka = 'Assalamu’alaikum Warahmatullahi Wabarakatuh.\n\n';
    var isi = jenis === 'pernikahan'
      ? 'Dengan memohon rahmat dan ridho Allah SWT, kami mengundang {{nama}} untuk menghadiri acara pernikahan kami.\n\n'
      : 'Dengan memohon rahmat dan ridho Allah SWT, kami mengundang {{nama}} untuk hadir dalam acara tasyakuran khitan anak kami.\n\n';
    var penutup = jenis === 'pernikahan'
      ? 'Merupakan kehormatan dan kebahagiaan bagi kami apabila berkenan hadir dan memberikan doa restu.\n\n'
      : 'Kehadiran dan doa restu akan menjadi kebahagiaan tersendiri bagi kami.\n\n';
    return pembuka + isi + 'Link Undangan:\n{{link}}\n\n' + penutup +
      'Wassalamu’alaikum Warahmatullahi Wabarakatuh.\n\nHormat kami,\n{{pengundang}}';
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

  function simpanDaftar(namaArray) {
    var params = new URLSearchParams({
      jenis: nilai('jenis'),
      nama: namaArray.join(', '),
      link: nilai('link'),
      pengundang: nilai('pengundang')
    });
    window.history.replaceState({}, '', location.pathname + '#' + params.toString());
  }

  function buatTabel(modeNama) {
    var jenis = document.getElementById('jenis').value;
    var namaInput = nilai('nama');
    var pengundang = nilai('pengundang');
    var link = nilai('link');

    if (!namaInput) return tampilkanPesan('Nama tamu tidak boleh kosong', 'error');

    var namaArray = namaInput.split(',').map(function (n) { return n.trim(); }).filter(Boolean);
    if (namaArray.length === 0) return tampilkanPesan('Silakan isi minimal satu nama.', 'error');

    var hasil = document.getElementById('hasil');
    hasil.innerHTML = '';

    var toolbar = el('div', 'invite-results-toolbar');
    var ringkasan = el('p', 'invite-results-count', namaArray.length + ' tamu tersimpan');
    var hapusSemua = el('button', 'invite-delete-all', 'Hapus semua');
    hapusSemua.type = 'button';
    hapusSemua.addEventListener('click', function () {
      if (!window.confirm('Hapus seluruh daftar tamu tersimpan?')) return;
      document.getElementById('nama').value = '';
      hasil.innerHTML = '';
      hasil.appendChild(el('p', 'invite-empty-state', 'Daftar tamu sudah dikosongkan.'));
      simpanDaftar([]);
      tampilkanPesan('Semua daftar tamu berhasil dihapus.', 'success', '3000');
    });
    toolbar.appendChild(ringkasan);
    toolbar.appendChild(hapusSemua);
    hasil.appendChild(toolbar);

    var tableWrap = el('div', 'ui-table-wrap');
    tableWrap.tabIndex = 0;
    tableWrap.setAttribute('role', 'region');
    tableWrap.setAttribute('aria-label', 'Daftar tamu dan aksi, geser horizontal jika diperlukan');
    var table = el('table', 'ui-table invite-guest-table');
    var thead = el('thead');
    var trHead = el('tr');
    ['Nama tamu', 'Aksi'].forEach(function (h) {
      var th = el('th', '', h);
      th.scope = 'col';
      trHead.appendChild(th);
    });
    thead.appendChild(trHead);
    var tbody = el('tbody');

    function perbaruiDaftar() {
      var tersisa = Array.prototype.map.call(tbody.querySelectorAll('tr'), function (row) {
        return row.getAttribute('data-guest-name');
      });
      document.getElementById('nama').value = tersisa.join(', ');
      ringkasan.textContent = tersisa.length + ' tamu tersimpan';
      simpanDaftar(tersisa);
      if (!tersisa.length) {
        hasil.innerHTML = '';
        hasil.appendChild(el('p', 'invite-empty-state', 'Semua tamu telah dihapus dari daftar.'));
      }
    }

    namaArray.forEach(function (nama) {
      var linkUndangan = link + '?to=' + kodeNama(nama);
      var pesan = buatPesan({ nama: nama, link: linkUndangan, pengundang: pengundang });
      var tr = el('tr', 'invite-guest-row');
      tr.setAttribute('data-guest-name', nama);

      var tdNama = el('th', 'invite-guest-name', nama);
      tdNama.scope = 'row';
      tr.appendChild(tdNama);

      var tdAksi = el('td', 'invite-guest-actions');
      
      var btnSalin = el('button', 'invite-action invite-copy', 'Salin');
      btnSalin.type = 'button';
      btnSalin.addEventListener('click', function () {
        var teks = pesan;
        var gagal = function () { window.prompt('Salin secara manual:', teks); };
        if (!navigator.clipboard || !window.isSecureContext) return gagal();
        navigator.clipboard.writeText(teks).then(function () {
          tampilkanPesan('Pesan undangan untuk ' + nama + ' berhasil disalin', 'success', '3000');
        }, gagal);
      });

      var a = el('a', 'invite-action invite-whatsapp', 'Kirim via WhatsApp');
      a.href = 'https://wa.me/?text=' + encodeURIComponent(pesan);
      a.target = '_blank';
      a.rel = 'noopener';

      var btnHapus = el('button', 'invite-action invite-delete', 'Hapus');
      btnHapus.type = 'button';
      btnHapus.setAttribute('aria-label', 'Hapus ' + nama + ' dari daftar');
      btnHapus.addEventListener('click', function () {
        tr.remove();
        perbaruiDaftar();
        tampilkanPesan('Tamu ' + nama + ' dihapus dari daftar.', 'success', '2500');
      });

      tdAksi.appendChild(btnSalin);
      tdAksi.appendChild(a);
      tdAksi.appendChild(btnHapus);
      tr.appendChild(tdAksi);
      tbody.appendChild(tr);
    });

    var caption = el('caption', 'sr-only', 'Daftar link undangan personal untuk setiap tamu');
    table.appendChild(caption);
    table.appendChild(thead);
    table.appendChild(tbody);
    tableWrap.appendChild(table);
    hasil.appendChild(tableWrap);
    simpanDaftar(namaArray);
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
