/**
 * Interaksi reusable Master Theme.
 * Komponen diinisialisasi secara idempoten dan hanya aktif pada data-attribute terkait.
 */

const dropdownSelector = "details[data-ui-dropdown]";
const paginationCallbacks = new WeakMap();
const dialogOpeners = new WeakMap();
const toastTimers = new WeakMap();
let initialized = false;

function getDropdownItems(dropdown) {
  return [...dropdown.querySelectorAll(
    ".ui-dropdown-menu a[href], .ui-dropdown-menu button:not(:disabled)"
  )];
}

function closeDropdowns(except = null) {
  document.querySelectorAll(dropdownSelector).forEach((dropdown) => {
    if (dropdown !== except && dropdown.open) dropdown.open = false;
  });
}

function initDropdowns() {
  document.addEventListener("toggle", (event) => {
    const dropdown = event.target;
    if (!(dropdown instanceof HTMLDetailsElement) || !dropdown.matches(dropdownSelector)) return;

    if (!dropdown.open) {
      dropdown.classList.remove("is-align-end");
      return;
    }

    closeDropdowns(dropdown);
    requestAnimationFrame(() => {
      const menu = dropdown.querySelector(".ui-dropdown-menu");
      if (!menu || !dropdown.open) return;
      const bounds = menu.getBoundingClientRect();
      dropdown.classList.toggle("is-align-end", bounds.right > window.innerWidth - 12);
    });
  }, true);

  document.addEventListener("click", (event) => {
    const target = event.target instanceof Element ? event.target : null;
    if (!target) return;

    const current = target.closest(dropdownSelector);
    closeDropdowns(current);

    const item = target.closest(".ui-dropdown-menu a[href], .ui-dropdown-menu button:not(:disabled)");
    if (!current || !item) return;

    current.open = false;
    if (item.matches("button")) current.querySelector("summary")?.focus();
  });
}

function initDropdownKeyboard() {
  document.addEventListener("keydown", (event) => {
    const target = event.target instanceof Element ? event.target : null;
    if (!target) return;

    const dropdown = target.closest(dropdownSelector);
    if (!dropdown) return;

    if (event.key === "Escape" && dropdown.open) {
      dropdown.open = false;
      dropdown.querySelector("summary")?.focus();
      event.preventDefault();
      return;
    }

    if (target.matches("summary") && ["ArrowDown", "ArrowUp"].includes(event.key)) {
      const items = getDropdownItems(dropdown);
      if (!items.length) return;
      event.preventDefault();
      dropdown.open = true;
      items[event.key === "ArrowDown" ? 0 : items.length - 1].focus();
      return;
    }

    if (!target.closest(".ui-dropdown-menu")) return;
    const items = getDropdownItems(dropdown);
    const index = items.indexOf(target);
    if (index < 0) return;

    if (["ArrowDown", "ArrowUp", "Home", "End"].includes(event.key)) {
      event.preventDefault();
      const next = event.key === "Home" ? 0
        : event.key === "End" ? items.length - 1
        : (index + (event.key === "ArrowDown" ? 1 : -1) + items.length) % items.length;
      items[next].focus();
    }
  });
}

function initDialogs() {
  document.addEventListener("click", (event) => {
    const target = event.target instanceof Element ? event.target : null;
    if (!target) return;

    const opener = target.closest("[data-dialog-open]");
    if (opener) {
      const dialog = document.getElementById(opener.dataset.dialogOpen);
      if (dialog instanceof HTMLDialogElement && !dialog.open) {
        dialogOpeners.set(dialog, opener);
        dialog.showModal();
      }
      return;
    }

    const closer = target.closest("[data-dialog-close]");
    if (closer) {
      const dialog = closer.closest("dialog");
      if (dialog instanceof HTMLDialogElement && dialog.open) dialog.close();
    }
  });

  document.addEventListener("click", (event) => {
    const dialog = event.target;
    if (!(dialog instanceof HTMLDialogElement) || !dialog.matches(".ui-dialog") || !dialog.open) return;

    const bounds = dialog.getBoundingClientRect();
    const outside = event.clientX < bounds.left || event.clientX > bounds.right
      || event.clientY < bounds.top || event.clientY > bounds.bottom;
    if (outside) dialog.close();
  });

  document.addEventListener("close", (event) => {
    const dialog = event.target;
    if (!(dialog instanceof HTMLDialogElement)) return;
    const opener = dialogOpeners.get(dialog);
    dialogOpeners.delete(dialog);
    if (opener?.isConnected) requestAnimationFrame(() => opener.focus({ preventScroll: true }));
  }, true);
}

function getPaginationPages(nav) {
  return [...nav.querySelectorAll("[data-page]")];
}

function updatePagination(nav, index, { notify = true } = {}) {
  const pages = getPaginationPages(nav);
  if (!pages.length || index < 0 || index >= pages.length) return false;

  const previousIndex = Math.max(0, pages.findIndex((page) => page.getAttribute("aria-current") === "page"));
  const previousPage = pages[previousIndex]?.dataset.page ?? null;
  const active = pages[index];
  const page = active.dataset.page;

  pages.forEach((button, pageIndex) => {
    if (pageIndex === index) button.setAttribute("aria-current", "page");
    else button.removeAttribute("aria-current");
  });

  const previous = nav.querySelector("[data-page-prev]");
  const following = nav.querySelector("[data-page-next]");
  if (previous) previous.disabled = index === 0;
  if (following) following.disabled = index === pages.length - 1;

  const status = nav.querySelector("[data-page-status]");
  if (status) status.textContent = "Menampilkan halaman " + page + " dari " + pages.length + ".";

  if (notify && previousPage !== page) {
    const detail = { page, previousPage, totalPages: pages.length, element: nav };
    nav.dispatchEvent(new CustomEvent("ui:pagechange", { bubbles: true, detail }));
    (paginationCallbacks.get(nav) || []).forEach((callback) => callback(detail));
  }
  return true;
}

/**
 * Mengubah halaman aktif berdasarkan nilai atribut data-page.
 * @param {HTMLElement|string} target Elemen nav atau selector CSS.
 * @param {string|number} page Nilai data-page yang dituju.
 * @returns {boolean} true jika halaman ditemukan dan diperbarui.
 */
export function setPaginationPage(target, page) {
  const nav = typeof target === "string" ? document.querySelector(target) : target;
  if (!(nav instanceof HTMLElement) || !nav.matches("[data-ui-pagination]")) return false;
  const pages = getPaginationPages(nav);
  const index = pages.findIndex((button) => button.dataset.page === String(page));
  return updatePagination(nav, index);
}

/**
 * Mendaftarkan callback perubahan halaman.
 * Mengembalikan fungsi untuk melepas callback.
 */
export function onPaginationChange(target, callback) {
  const nav = typeof target === "string" ? document.querySelector(target) : target;
  if (!(nav instanceof HTMLElement) || !nav.matches("[data-ui-pagination]") || typeof callback !== "function") {
    return () => {};
  }

  const callbacks = paginationCallbacks.get(nav) || [];
  callbacks.push(callback);
  paginationCallbacks.set(nav, callbacks);
  return () => {
    const current = paginationCallbacks.get(nav) || [];
    paginationCallbacks.set(nav, current.filter((item) => item !== callback));
  };
}

function initPagination() {
  document.addEventListener("click", (event) => {
    const target = event.target instanceof Element ? event.target : null;
    const control = target?.closest("[data-page], [data-page-prev], [data-page-next]");
    const nav = control?.closest("[data-ui-pagination]");
    if (!control || !nav || control.disabled) return;

    const pages = getPaginationPages(nav);
    if (!pages.length) return;
    const current = Math.max(0, pages.findIndex((page) => page.getAttribute("aria-current") === "page"));
    const requested = control.hasAttribute("data-page-prev") ? current - 1
      : control.hasAttribute("data-page-next") ? current + 1
      : pages.indexOf(control);
    updatePagination(nav, requested);
  });

  document.querySelectorAll("[data-ui-pagination]").forEach((nav) => {
    const pages = getPaginationPages(nav);
    if (!pages.length) return;
    const current = pages.findIndex((page) => page.getAttribute("aria-current") === "page");
    updatePagination(nav, current < 0 ? 0 : current, { notify: false });
  });
}

const toastMessages = {
  success: ["Berhasil", "Contoh tindakan berhasil diselesaikan."],
  info: ["Informasi", "Ini adalah informasi tambahan untuk pengguna."],
  warning: ["Perhatian", "Periksa kembali informasi sebelum melanjutkan."],
  danger: ["Terjadi kendala", "Permintaan belum berhasil. Silakan coba kembali."]
};

function getToastRegion() {
  let region = document.querySelector("[data-ui-toast-region]");
  if (region) return region;

  region = document.createElement("div");
  region.className = "ui-toast-region";
  region.dataset.uiToastRegion = "";
  region.setAttribute("role", "region");
  region.setAttribute("aria-label", "Notifikasi");
  document.body.append(region);
  return region;
}

function clearToastTimer(toast) {
  const state = toastTimers.get(toast);
  if (!state?.timer) return;
  clearTimeout(state.timer);
  state.remaining = Math.max(0, state.deadline - Date.now());
  state.timer = null;
}

function startToastTimer(toast) {
  const state = toastTimers.get(toast);
  if (!state || state.duration <= 0 || state.timer || toast.hidden) return;
  if (state.remaining <= 0) {
    toast.remove();
    toastTimers.delete(toast);
    return;
  }

  state.deadline = Date.now() + state.remaining;
  state.timer = setTimeout(() => {
    toast.remove();
    toastTimers.delete(toast);
  }, state.remaining);
}

function dismissToast(toast) {
  clearToastTimer(toast);
  toast.remove();
  toastTimers.delete(toast);
}

/**
 * Menampilkan notifikasi baru.
 * @param {{type?: string, title?: string, message?: string, duration?: number}} options
 * @returns {{dismiss: () => void}} Kontrol untuk menutup notifikasi.
 */
export function showToast({ type = "info", title, message, duration = 6000 } = {}) {
  const normalizedType = type === "error" ? "danger" : type;
  const [defaultTitle, defaultMessage] = toastMessages[normalizedType] || toastMessages.info;
  const toast = document.createElement("div");
  toast.className = "ui-toast";
  toast.dataset.uiToast = "";
  toast.dataset.type = toastMessages[normalizedType] ? normalizedType : "info";
  toast.setAttribute("role", normalizedType === "danger" ? "alert" : "status");
  toast.setAttribute("aria-atomic", "true");

  const content = document.createElement("div");
  const heading = document.createElement("strong");
  heading.textContent = title || defaultTitle;
  const body = document.createElement("p");
  body.textContent = message || defaultMessage;
  content.append(heading, body);

  const close = document.createElement("button");
  close.className = "ui-toast-close";
  close.type = "button";
  close.setAttribute("aria-label", "Tutup notifikasi");
  close.textContent = "×";
  close.addEventListener("click", () => dismissToast(toast));

  toast.append(content, close);
  const safeDuration = Number.isFinite(Number(duration)) ? Math.max(0, Number(duration)) : 6000;
  toastTimers.set(toast, {
    duration: safeDuration,
    remaining: safeDuration,
    deadline: 0,
    timer: null
  });

  toast.addEventListener("pointerenter", () => clearToastTimer(toast));
  toast.addEventListener("pointerleave", () => startToastTimer(toast));
  toast.addEventListener("focusin", () => clearToastTimer(toast));
  toast.addEventListener("focusout", (event) => {
    if (!toast.contains(event.relatedTarget)) startToastTimer(toast);
  });

  getToastRegion().append(toast);
  startToastTimer(toast);
  return { dismiss: () => dismissToast(toast) };
}

function initToastTriggers() {
  document.addEventListener("click", (event) => {
    const target = event.target instanceof Element ? event.target : null;
    const trigger = target?.closest("[data-toast-trigger]");
    if (!trigger) return;

    const type = trigger.dataset.toastTrigger;
    const [defaultTitle, defaultMessage] = toastMessages[type] || toastMessages.info;
    showToast({
      type,
      title: trigger.dataset.toastTitle || defaultTitle,
      message: trigger.dataset.toastMessage || defaultMessage,
      duration: trigger.dataset.toastDuration || 6000
    });
  });
}

export function initInteractionPrimitives() {
  if (initialized) return;
  initialized = true;
  initDropdowns();
  initDropdownKeyboard();
  initDialogs();
  initPagination();
  initToastTriggers();
}

if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", initInteractionPrimitives, { once: true });
} else {
  initInteractionPrimitives();
}
