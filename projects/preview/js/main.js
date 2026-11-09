/* global campaignData */
(() => {
  const $ = (selector, scope = document) => scope.querySelector(selector);
  const $$ = (selector, scope = document) => [...scope.querySelectorAll(selector)];
  const navigationIcons = new Set(['circle-check', 'chevron-down', 'arrow-right', 'arrow-up-right', 'arrow-up', 'chevron-left', 'chevron-right', 'x']);
  const icon = (name, extraClass = '') => navigationIcons.has(name)
    ? `<span class="icon icon-mask icon-${name} ${extraClass}" style="--icon:url('assets/icons/monochrome/${name}.svg')" aria-hidden="true"></span>`
    : `<img class="icon icon-image icon-${name} ${extraClass}" src="assets/icons/color/${name}.svg" alt="" aria-hidden="true">`;
  const refreshIcons = () => $$('[data-icon]').forEach(element => { element.outerHTML = icon(element.dataset.icon, element.className || ''); });

  const missionGrid = $('#mission-grid');
  const missionDetail = $('#mission-detail');
  const programGrid = $('#program-grid');
  let activeMissionId = null;

  function renderProfile() {
    const profile = campaignData.profile;
    $('#profile-label').textContent = profile.label;
    $('#profile-name-photo').textContent = profile.name;
    $('#profile-heading').innerHTML = `${profile.headingPrefix} <span>${profile.name}</span>`;
    $('#profile-role').textContent = profile.role;
    $('#profile-summary').textContent = profile.summary;
    $('#profile-image').src = profile.image;
    $('#profile-image').alt = profile.imageAlt;
    $('#profile-meta').innerHTML = profile.meta.map(item => `<span>${icon(item.icon)}<b>${item.label}</b>${item.value}</span>`).join('');
    const educationItems = profile.education.map(school => `<li>${school}</li>`).join('');
    const workItems = profile.workExperience.map(job => `
      <li class="work-entry${job.current ? ' current' : ''}">
        <span class="work-period">${job.period}</span>
        <div><strong>${job.organization}</strong>
          ${job.role ? `<span class="work-role">${job.role}</span>` : ''}
          ${job.description ? `<p>${job.description}</p>` : ''}
        </div>
      </li>`).join('');
    $('#profile-facts').innerHTML = `
      <section class="profile-history-card" aria-labelledby="education-heading">
        <div class="profile-history-title"><span class="profile-fact-icon">${icon('graduation-cap')}</span><h3 id="education-heading">Riwayat Pendidikan</h3></div>
        <ol class="education-list">${educationItems}</ol>
      </section>
      <section class="profile-history-card" aria-labelledby="work-heading">
        <div class="profile-history-title"><span class="profile-fact-icon">${icon('briefcase-business')}</span><h3 id="work-heading">Riwayat Pekerjaan</h3></div>
        <ol class="work-list">${workItems}</ol>
      </section>`;
  }

  function renderMissions() {
    missionGrid.innerHTML = campaignData.missions.map(mission => `
      <article class="mission-card" data-mission-id="${mission.id}">
        <span class="mission-num">MISI ${String(mission.id).padStart(2, '0')}</span>
        <span class="mission-icon">${icon(mission.icon)}</span>
        <h3>${mission.title}</h3><p>${mission.description}</p>
        <button class="card-more" type="button" aria-expanded="false" aria-controls="mission-detail">Lihat Selengkapnya ${icon('chevron-down')}</button>
      </article>`).join('');
    refreshIcons();
  }

  function openMission(id, shouldScroll = true) {
    const mission = campaignData.missions.find(item => item.id === id);
    if (!mission) return;
    if (activeMissionId === id) { closeMission(); return; }
    activeMissionId = id;
    $$('.mission-card').forEach(card => {
      const active = Number(card.dataset.missionId) === id;
      card.classList.toggle('active', active);
      $('button', card).setAttribute('aria-expanded', String(active));
    });
    const items = mission.details.map((detail, index) => `<li>${icon(mission.detailIcons?.[index] || 'circle-check')}<span>${detail}</span></li>`).join('');
    missionDetail.innerHTML = `<div class="detail-head"><div><p class="eyebrow"><span></span> MISI ${String(mission.id).padStart(2, '0')}</p><h3>${mission.detailTitle || mission.title}</h3></div><button class="detail-close" type="button">Tutup ${icon('x')}</button></div><ul class="detail-list">${items}</ul>`;
    missionDetail.hidden = false;
    missionDetail.focus({ preventScroll: true });
    refreshIcons();
    if (shouldScroll) setTimeout(() => missionDetail.scrollIntoView({ behavior: 'smooth', block: 'center' }), 90);
  }
  function closeMission() {
    activeMissionId = null;
    missionDetail.hidden = true;
    missionDetail.innerHTML = '';
    $$('.mission-card').forEach(card => { card.classList.remove('active'); $('button', card).setAttribute('aria-expanded', 'false'); });
  }
  missionGrid.addEventListener('click', event => {
    const card = event.target.closest('.mission-card');
    if (card) openMission(Number(card.dataset.missionId));
  });
  missionGrid.addEventListener('keydown', event => {
    if ((event.key === 'Enter' || event.key === ' ') && event.target.closest('.mission-card')) { event.preventDefault(); openMission(Number(event.target.closest('.mission-card').dataset.missionId)); }
  });
  missionDetail.addEventListener('click', event => { if (event.target.closest('.detail-close')) closeMission(); });

  function renderPrograms() {
    programGrid.innerHTML = campaignData.missions.map(mission => `<article class="program-card reveal"><span class="mission-num">${String(mission.id).padStart(2, '0')}</span><span class="program-icon">${icon(mission.icon)}</span><h3>${mission.title}</h3><p>${mission.description}</p><button class="button program-link" data-program-id="${mission.id}" type="button">Pelajari Program ${icon('arrow-up-right')}</button></article>`).join('');
    $$('.program-link', programGrid).forEach(button => button.addEventListener('click', () => openProgram(Number(button.dataset.programId))));
    refreshIcons();
  }
  function openProgram(id) {
    document.querySelector('#visi-misi').scrollIntoView({ behavior: 'smooth', block: 'start' });
    setTimeout(() => openMission(id, true), 450);
  }

  function renderPotentials() {
    $('#potential-grid').innerHTML = campaignData.potentials.map(([name, symbol]) => `<article class="potential-card reveal">${icon(symbol)}<h3>${name}</h3></article>`).join('');
    refreshIcons();
  }
  const galleryItems = campaignData.gallery.map((title, index) => ({
    title,
    src: `assets/images/gallery/gallery-${String(index + 1).padStart(2, '0')}.jpg`
  }));
  function renderGallery() {
    $('#gallery-grid').innerHTML = galleryItems.map((item, index) => `<button class="gallery-item reveal" data-gallery-index="${index}" aria-label="Buka gambar ${item.title}"><img src="${item.src}" alt="Placeholder galeri: ${item.title}" loading="lazy"><span>${item.title}</span></button>`).join('');
  }
  const lightbox = $('#lightbox'); let galleryIndex = 0;
  function displayGallery(index) {
    galleryIndex = (index + galleryItems.length) % galleryItems.length;
    const item = galleryItems[galleryIndex];
    $('img', lightbox).src = item.src; $('img', lightbox).alt = `Placeholder galeri: ${item.title}`; $('figcaption', lightbox).textContent = item.title;
  }
  $('#gallery-grid').addEventListener('click', event => { const item = event.target.closest('.gallery-item'); if (item) { displayGallery(Number(item.dataset.galleryIndex)); lightbox.showModal(); } });
  $('.lightbox-close').addEventListener('click', () => lightbox.close());
  $('.lightbox-nav.prev').addEventListener('click', () => displayGallery(galleryIndex - 1));
  $('.lightbox-nav.next').addEventListener('click', () => displayGallery(galleryIndex + 1));
  lightbox.addEventListener('click', event => { if (event.target === lightbox) lightbox.close(); });
  document.addEventListener('keydown', event => { if (!lightbox.open) return; if (event.key === 'ArrowLeft') displayGallery(galleryIndex - 1); if (event.key === 'ArrowRight') displayGallery(galleryIndex + 1); });


  // Satu tombol mengelola mulai putar dan mute/unmute musik latar.
  const BACKGROUND_AUDIO_SOURCE = 'assets/mp3/music.mp3';
  const backgroundAudio = $('#background-audio');
  const audioToggle = $('#audio-toggle');
  const audioStatus = $('#audio-status');
  backgroundAudio.volume = 0.18;

  const audioIcons = {
    play: '<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="m8 5 12 7-12 7z" fill="currentColor"></path></svg>',
    playing: '<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M3 10v4h4l5 4V6l-5 4H3Z" fill="currentColor"></path><path d="M16 9a5 5 0 0 1 0 6M18.5 6.5a9 9 0 0 1 0 11" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"></path></svg>',
    muted: '<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M3 10v4h4l5 4V6l-5 4H3Z" fill="currentColor"></path><path d="m16 9 5 6m0-6-5 6" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"></path></svg>'
  };

  function updateAudioState(message) {
    const playing = !backgroundAudio.paused && !backgroundAudio.ended;
    const muted = backgroundAudio.muted;
    const label = playing
      ? (muted ? 'Aktifkan suara musik latar' : 'Bisukan musik latar')
      : 'Putar musik latar';

    audioToggle.innerHTML = playing ? (muted ? audioIcons.muted : audioIcons.playing) : audioIcons.play;
    audioToggle.setAttribute('aria-label', label);
    audioToggle.setAttribute('title', label);
    audioToggle.setAttribute('aria-pressed', String(playing && muted));
    audioStatus.textContent = message || (playing
      ? (muted ? 'Musik sedang dibisukan' : 'Musik sedang diputar')
      : 'Musik siap diputar');
  }

  backgroundAudio.src = BACKGROUND_AUDIO_SOURCE;
  updateAudioState('Musik siap diputar');

  audioToggle.addEventListener('click', async () => {
    if (!backgroundAudio.paused && !backgroundAudio.ended) {
      backgroundAudio.muted = !backgroundAudio.muted;
      updateAudioState();
      return;
    }

    try {
      await backgroundAudio.play();
      updateAudioState();
    } catch {
      updateAudioState('Musik gagal diputar. Periksa ketersediaan file audio.');
    }
  });

  backgroundAudio.addEventListener('play', () => updateAudioState());
  backgroundAudio.addEventListener('pause', () => updateAudioState('Musik dijeda'));
  backgroundAudio.addEventListener('ended', () => updateAudioState('Pemutaran selesai'));
  backgroundAudio.addEventListener('error', () => updateAudioState('Musik gagal dimuat. File audio tidak tersedia.'));

  document.addEventListener('visibilitychange', () => {
    if (document.hidden && !backgroundAudio.paused) {
      backgroundAudio.pause();
      updateAudioState('Musik dihentikan saat tab tidak aktif');
    }
  });
  window.addEventListener('pagehide', () => backgroundAudio.pause());

  const visionTrigger = $('.vision-trigger');
  visionTrigger.addEventListener('click', () => { const expanded = visionTrigger.getAttribute('aria-expanded') === 'true'; visionTrigger.setAttribute('aria-expanded', String(!expanded)); $('#vision-detail').hidden = expanded; });

  const navToggle = $('.nav-toggle'), navLinks = $('.nav-links');
  navToggle.addEventListener('click', () => { const open = navLinks.classList.toggle('open'); navToggle.setAttribute('aria-expanded', String(open)); });
  $$('.nav-links a').forEach(link => link.addEventListener('click', () => { navLinks.classList.remove('open'); navToggle.setAttribute('aria-expanded', 'false'); }));
  const header = $('.site-header'), progress = $('.scroll-progress span');
  function onScroll() { const y = window.scrollY; header.classList.toggle('sticky', y > 25); progress.style.width = `${(y / (document.documentElement.scrollHeight - innerHeight)) * 100}%`; }
  addEventListener('scroll', onScroll, { passive: true }); onScroll();
  const observer = new IntersectionObserver(entries => entries.forEach(entry => { if (entry.isIntersecting) { entry.target.classList.add('visible'); observer.unobserve(entry.target); } }), { threshold: .12 });
  const observeReveals = () => $$('.reveal:not(.visible)').forEach(item => observer.observe(item));
  renderProfile(); renderMissions(); renderPrograms(); renderPotentials(); renderGallery(); observeReveals();
  $('#copyright-year').textContent = new Date().getFullYear();
  refreshIcons();
})();
