const STORAGE_KEY = 'context-store-entries';

const $ = (id) => document.getElementById(id);

const els = {
  search: $('search'),
  exportBtn: $('export-btn'),
  importFile: $('import-file'),
  entryInput: $('entry-input'),
  addBtn: $('add-btn'),
  entryList: $('entry-list'),
  emptyState: $('empty-state'),
};

let entries = loadEntries();
let query = '';

function loadEntries() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    return raw ? JSON.parse(raw) : [];
  } catch {
    return [];
  }
}

function saveEntries() {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(entries));
}

function nowStamp() {
  const d = new Date();
  const pad = (n) => String(n).padStart(2, '0');
  return `${d.getFullYear()}-${pad(d.getMonth()+1)}-${pad(d.getDate())} ${pad(d.getHours())}:${pad(d.getMinutes())}`;
}

function escapeHtml(str) {
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');
}

function highlight(text, q) {
  if (!q) return escapeHtml(text);
  const escaped = escapeHtml(text);
  const re = new RegExp(`(${q.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')})`, 'gi');
  return escaped.replace(re, '<mark>$1</mark>');
}

function render() {
  const q = els.search.value.trim();
  query = q;
  const list = q
    ? entries.filter((e) => e.text.toLowerCase().includes(q.toLowerCase()))
    : entries;

  if (list.length === 0) {
    els.emptyState.classList.remove('hidden');
    els.entryList.innerHTML = '';
    return;
  }
  els.emptyState.classList.add('hidden');

  els.entryList.innerHTML = list.map((e, i) => {
    const realIndex = entries.indexOf(e);
    return `
      <div class="entry" data-index="${realIndex}">
        <div class="entry-header">
          <span class="entry-date">${escapeHtml(e.date)}</span>
          <div>
            <button class="edit-btn" data-act="edit">Edit</button>
            <button class="delete-btn" data-act="delete">Hapus</button>
          </div>
        </div>
        <div class="entry-text">${highlight(e.text, q)}</div>
      </div>
    `;
  }).join('');
}

function addEntry() {
  const text = els.entryInput.value.trim();
  if (!text) return;
  entries.unshift({ text, date: nowStamp() });
  saveEntries();
  els.entryInput.value = '';
  render();
}

function deleteEntry(index) {
  entries.splice(index, 1);
  saveEntries();
  render();
}

function editEntry(index) {
  const text = entries[index].text;
  const newText = prompt('Edit konteks:', text);
  if (newText === null) return;
  entries[index].text = newText.trim();
  saveEntries();
  render();
}

function exportJson() {
  const blob = new Blob([JSON.stringify(entries, null, 2)], { type: 'application/json' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = `context-store-${nowStamp().replace(/[ :]/g, '-')}.json`;
  document.body.appendChild(a);
  a.click();
  a.remove();
  URL.revokeObjectURL(url);
}

function importJson(file) {
  const reader = new FileReader();
  reader.onload = () => {
    try {
      const data = JSON.parse(reader.result);
      if (!Array.isArray(data)) throw new Error('Bukan array');
      entries = data.map((item) => ({
        text: String(item.text ?? ''),
        date: String(item.date ?? nowStamp()),
      }));
      saveEntries();
      render();
    } catch (err) {
      alert('Gagal mengimpor: ' + err.message);
    }
  };
  reader.readAsText(file);
}

els.addBtn.addEventListener('click', addEntry);
els.entryInput.addEventListener('keydown', (e) => {
  if (e.key === 'Enter' && (e.ctrlKey || e.metaKey)) {
    e.preventDefault();
    addEntry();
  }
});
els.search.addEventListener('input', render);
els.exportBtn.addEventListener('click', exportJson);
els.importFile.addEventListener('change', (e) => {
  const file = e.target.files[0];
  if (file) importJson(file);
  e.target.value = '';
});
els.entryList.addEventListener('click', (e) => {
  const btn = e.target.closest('[data-act]');
  if (!btn) return;
  const entry = e.target.closest('.entry');
  const index = parseInt(entry.dataset.index, 10);
  if (btn.dataset.act === 'delete') deleteEntry(index);
  if (btn.dataset.act === 'edit') editEntry(index);
});

render();
