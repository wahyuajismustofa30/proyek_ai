/* DEKEKU shared layout interactions. */
(function () {
  "use strict";

  function initializeLayout() {
    var root = document.documentElement;
    var menuButton = document.getElementById("menu-toggle");
    var navigation = document.getElementById("primary-nav");
    var themeButton = document.getElementById("theme-toggle");
    var year = document.getElementById("year");

    if (year) year.textContent = String(new Date().getFullYear());

    if (menuButton && navigation && !menuButton.dataset.initialized) {
      menuButton.dataset.initialized = "true";
      menuButton.addEventListener("click", function () {
        var isOpen = menuButton.getAttribute("aria-expanded") !== "true";
        menuButton.setAttribute("aria-expanded", String(isOpen));
        menuButton.setAttribute("aria-label", isOpen ? "Tutup navigasi" : "Buka navigasi");
        navigation.classList.toggle("is-open", isOpen);
      });
      navigation.addEventListener("click", function (event) {
        if (event.target.closest("a")) {
          menuButton.setAttribute("aria-expanded", "false");
          menuButton.setAttribute("aria-label", "Buka navigasi");
          navigation.classList.remove("is-open");
        }
      });
      document.addEventListener("keydown", function (event) {
        if (event.key === "Escape" && navigation.classList.contains("is-open")) {
          menuButton.setAttribute("aria-expanded", "false");
          menuButton.setAttribute("aria-label", "Buka navigasi");
          navigation.classList.remove("is-open");
          menuButton.focus();
        }
      });
    }

    if (themeButton && !themeButton.dataset.initialized) {
      themeButton.dataset.initialized = "true";
      themeButton.addEventListener("click", function () {
        var isDark = root.getAttribute("data-theme") !== "dark";
        root.setAttribute("data-theme", isDark ? "dark" : "light");
        themeButton.setAttribute("aria-pressed", String(isDark));
        themeButton.setAttribute("aria-label", isDark ? "Aktifkan tema terang" : "Aktifkan tema gelap");
      });
    }
  }

  document.addEventListener("dekeku:components-loaded", initializeLayout);
}());
