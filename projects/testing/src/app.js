export function isValidEmail(value) {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(String(value).trim());
}

if (typeof document !== "undefined") {
  const menuButton = document.querySelector(".menu-toggle");
  const navigation = document.querySelector("#primary-nav");
  const form = document.querySelector("#demo-form");
  const emailInput = document.querySelector("#email");
  const message = document.querySelector("#form-message");

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
