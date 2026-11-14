// share-links.js — tombol bagikan (WhatsApp, Facebook, X) dan "Salin link".
// Link dibentuk saat diklik supaya parameter URL terbaru (?produk=...) ikut terbawa.

/** Cadangan untuk browser lama / koneksi non-HTTPS: salin lewat textarea sementara. */
function salinCadangan(teks, selesai) {
  const ta = document.createElement('textarea');
  ta.value = teks;
  ta.setAttribute('readonly', '');
  ta.style.position = 'fixed';
  ta.style.opacity = '0';
  document.body.appendChild(ta);
  ta.select();
  let ok = false;
  try { ok = document.execCommand('copy'); } catch (e) { ok = false; }
  ta.remove();
  if (ok) selesai();
  else window.prompt('Salin link ini:', teks);
}

const PEMBENTUK = {
  'facebook-share': (u) => `https://www.facebook.com/sharer/sharer.php?u=${u}`,
  'twitter-share': (u) => `https://twitter.com/intent/tweet?url=${u}`,
  'whatsapp-share': (u) => `https://wa.me/?text=${u}`,
};

export function initShareLinks() {
  Object.keys(PEMBENTUK).forEach((id) => {
    const a = document.getElementById(id);
    if (!a) return;
    a.addEventListener('click', function () {
      this.href = PEMBENTUK[id](encodeURIComponent(window.location.href));
    });
  });

  const salin = document.getElementById('copy-link');
  if (salin) {
    const labelAwal = salin.getAttribute('aria-label');
    const titleAwal = salin.getAttribute('title');
    const teksAwal = salin.textContent;
    const tombolIkon = Boolean(salin.querySelector('svg'));
    const status = document.createElement('span');
    status.className = 'sr-only';
    status.setAttribute('role', 'status');
    (salin.closest('.share') || salin.parentElement).append(status);

    let timerStatus;
    salin.addEventListener('click', () => {
      const selesai = () => {
        status.textContent = 'Link berhasil disalin.';
        salin.classList.add('is-copied');
        if (tombolIkon) {
          salin.setAttribute('aria-label', 'Link berhasil disalin');
          salin.setAttribute('title', 'Link berhasil disalin');
        } else {
          salin.textContent = 'Link disalin';
        }

        window.clearTimeout(timerStatus);
        timerStatus = window.setTimeout(() => {
          status.textContent = '';
          salin.classList.remove('is-copied');
          if (tombolIkon) {
            if (labelAwal === null) salin.removeAttribute('aria-label');
            else salin.setAttribute('aria-label', labelAwal);
            if (titleAwal === null) salin.removeAttribute('title');
            else salin.setAttribute('title', titleAwal);
          } else {
            salin.textContent = teksAwal;
          }
        }, 2000);
      };
      const url = window.location.href;
      if (navigator.clipboard && window.isSecureContext) {
        navigator.clipboard.writeText(url).then(selesai, () => salinCadangan(url, selesai));
      } else {
        salinCadangan(url, selesai);
      }
    });
  }
}
