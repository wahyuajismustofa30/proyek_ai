const EMAIL_LOCAL_PART = /^[a-z0-9.!#$%&'*+/=?^`_{|}~-]+$/i;
const EMAIL_DOMAIN_LABEL = /^[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?$/i;

export function isValidEmail(value) {
  const email = String(value).trim();
  if (!email || email.length > 254 || /\s/.test(email)) return false;

  const separator = email.lastIndexOf("@");
  if (separator <= 0 || separator !== email.indexOf("@")) return false;

  const local = email.slice(0, separator);
  const domain = email.slice(separator + 1);
  if (local.length > 64 || local.startsWith(".") || local.endsWith(".") || local.includes("..")) return false;
  if (!EMAIL_LOCAL_PART.test(local) || domain.length > 253) return false;

  const labels = domain.split(".");
  return labels.length >= 2 && labels.every((label) => label.length <= 63 && EMAIL_DOMAIN_LABEL.test(label));
}

export function initializePage(documentRef) {
  const menuButton = documentRef.querySelector(".menu-toggle");
  const navigation = documentRef.querySelector("#primary-nav");
  const form = documentRef.querySelector("#demo-form");
  const emailInput = documentRef.querySelector("#email");
  const message = documentRef.querySelector("#form-message");

  documentRef.documentElement.classList.add("js");

  menuButton?.addEventListener("click", () => {
    const isExpanded = menuButton.getAttribute("aria-expanded") === "true";
    menuButton.setAttribute("aria-expanded", String(!isExpanded));
    navigation?.classList.toggle("is-open", !isExpanded);
  });

  navigation?.querySelectorAll("a").forEach((link) => {
    link.addEventListener("click", () => {
      navigation.classList.remove("is-open");
      menuButton?.setAttribute("aria-expanded", "false");
    });
  });

  form?.addEventListener("submit", (event) => {
    event.preventDefault();
    const email = emailInput?.value ?? "";

    if (!isValidEmail(email)) {
      if (message) {
        message.dataset.state = "error";
        message.textContent = "Format email belum tepat. Coba nama@contoh.com.";
      }
      emailInput?.focus();
      return;
    }

    if (message) {
      message.dataset.state = "success";
      message.textContent = "Format email valid. Ini hanya simulasi lokal—tidak ada data yang dikirim.";
    }
    form.reset();
  });
}

if (typeof document !== "undefined") initializePage(document);
