/**
 * Interaksi reusable Master Theme.
 * Modul ini hanya menginisialisasi elemen yang memiliki data-attribute terkait.
 */
const dropdownSelector = "details[data-ui-dropdown]";

function closeDropdowns(except = null) {
  document.querySelectorAll(dropdownSelector).forEach((dropdown) => {
    if (dropdown !== except && dropdown.open) dropdown.open = false;
  });
}

function initDropdowns() {
  document.querySelectorAll(dropdownSelector).forEach((dropdown) => {
    dropdown.addEventListener("toggle", () => {
      if (!dropdown.open) {
        dropdown.classList.remove("is-align-end");
        return;
      }
      requestAnimationFrame(() => {
        const menu = dropdown.querySelector(".ui-dropdown-menu");
        if (!menu) return;
        const bounds = menu.getBoundingClientRect();
        dropdown.classList.toggle("is-align-end", bounds.right > window.innerWidth - 12);
      });
    });
  });

  document.addEventListener("click", (event) => {
    const current = event.target.closest(dropdownSelector);
    closeDropdowns(current);
    if (current && event.target.closest(".ui-dropdown-menu a, .ui-dropdown-menu button")) {
      current.open = false;
    }
  });

  document.addEventListener("keydown", (event) => {
    const dropdown = event.target.closest(dropdownSelector);
    if (!dropdown) return;

    if (event.key === "Escape" && dropdown.open) {
      dropdown.open = false;
      dropdown.querySelector("summary")?.focus();
      event.preventDefault();
      return;
    }

    if (event.target.matches("summary") && ["ArrowDown", "ArrowUp"].includes(event.key)) {
      event.preventDefault();
      dropdown.open = true;
      const items = [...dropdown.querySelectorAll(".ui-dropdown-menu a[href], .ui-dropdown-menu button:not(:disabled)")];
      (event.key === "ArrowDown" ? items[0] : items[items.length - 1])?.focus();
      return;
    }

    if (["ArrowDown", "ArrowUp", "Home", "End"].includes(event.key) && event.target.closest(".ui-dropdown-menu")) {
      const items = [...dropdown.querySelectorAll(".ui-dropdown-menu a[href], .ui-dropdown-menu button:not(:disabled)")];
      const index = items.indexOf(event.target);
      if (index < 0 || !items.length) return;
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
    const opener = event.target.closest("[data-dialog-open]");
    if (opener) {
      const dialog = document.getElementById(opener.dataset.dialogOpen);
      if (dialog instanceof HTMLDialogElement && !dialog.open) dialog.showModal();
      return;
    }

    const closer = event.target.closest("[data-dialog-close]");
    if (closer) {
      const dialog = closer.closest("dialog");
      if (dialog instanceof HTMLDialogElement && dialog.open) dialog.close();
    }
  });
}

function initPagination() {
  document.addEventListener("click", (event) => {
    const control = event.target.closest("[data-page], [data-page-prev], [data-page-next]");
    if (!control) return;
    const nav = control.closest("[data-ui-pagination]");
    if (!nav) return;

    const pages = [...nav.querySelectorAll("[data-page]")];
    if (!pages.length) return;
    const current = Math.max(0, pages.findIndex((page) => page.getAttribute("aria-current") === "page"));
    const requested = control.hasAttribute("data-page-prev") ? current - 1
      : control.hasAttribute("data-page-next") ? current + 1
      : pages.indexOf(control);
    const next = Math.min(pages.length - 1, Math.max(0, requested));
    pages.forEach((page, index) => {
      if (index === next) page.setAttribute("aria-current", "page");
      else page.removeAttribute("aria-current");
    });
    const previous = nav.querySelector("[data-page-prev]");
    const following = nav.querySelector("[data-page-next]");
    if (previous) previous.disabled = next === 0;
    if (following) following.disabled = next === pages.length - 1;
    const status = nav.querySelector("[data-page-status]");
    if (status) status.textContent = "Menampilkan contoh halaman " + (next + 1) + " dari " + pages.length + ".";
  });
}

const toastMessages = {
  success: ["Berhasil", "Contoh tindakan berhasil diselesaikan."],
  info: ["Informasi", "Ini adalah informasi tambahan untuk pengguna."],
  warning: ["Perhatian", "Periksa kembali informasi sebelum melanjutkan."],
  error: ["Terjadi kendala", "Permintaan belum berhasil. Silakan coba kembali."]
};

function initToast() {
  const toastRegion = document.querySelector("[data-ui-toast-region]");
  const toastNode = toastRegion?.querySelector("[data-ui-toast]");
  if (!toastNode) return;

  document.addEventListener("click", (event) => {
    const trigger = event.target.closest("[data-toast-trigger]");
    if (trigger) {
      const type = trigger.dataset.toastTrigger;
      const [defaultTitle, defaultMessage] = toastMessages[type] || toastMessages.info;
      toastNode.dataset.type = type;
      const titleNode = toastNode.querySelector("[data-toast-title]");
      const messageNode = toastNode.querySelector("[data-toast-message]");
      if (!titleNode || !messageNode) return;
      titleNode.textContent = trigger.dataset.toastTitle || defaultTitle;
      messageNode.textContent = trigger.dataset.toastMessage || defaultMessage;
      toastNode.setAttribute("role", type === "error" ? "alert" : "status");
      toastNode.hidden = false;
      return;
    }

    if (event.target.closest("[data-toast-close]")) toastNode.hidden = true;
  });
}

function init() {
  initDropdowns();
  initDialogs();
  initPagination();
  initToast();
}

if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", init, { once: true });
} else {
  init();
}
