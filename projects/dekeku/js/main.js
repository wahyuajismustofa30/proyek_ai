/* DEKEKU shared layout interactions. */
(function () {
  "use strict";

  var root = document.documentElement;
  var themeStorageKey = "dekeku-theme";

  function getSystemTheme() {
    return window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches
      ? "dark"
      : "light";
  }

  function getCurrentTheme() {
    return root.getAttribute("data-theme") || getSystemTheme();
  }

  function syncThemeControl() {
    var themeButton = document.getElementById("theme-toggle");
    if (!themeButton) return;

    var isDark = getCurrentTheme() === "dark";
    themeButton.setAttribute("aria-pressed", String(isDark));
    themeButton.setAttribute("aria-label", isDark ? "Aktifkan tema terang" : "Aktifkan tema gelap");
  }

  function initializeLayout() {
    var year = document.getElementById("year");
    if (year) year.textContent = String(new Date().getFullYear());
    syncThemeControl();
  }

  /* Restore an explicit user choice when available; otherwise follow the OS. */
  try {
    var savedTheme = window.localStorage.getItem(themeStorageKey);
    if (savedTheme === "light" || savedTheme === "dark") {
      root.setAttribute("data-theme", savedTheme);
    }
  } catch (error) {
    /* Theme switching remains available when storage is restricted. */
  }

  /*
   * Delegate interactions from document so controls work even when the shared
   * header is injected asynchronously after this script has executed.
   */
  document.addEventListener("click", function (event) {
    var target = event.target;
    if (!target || typeof target.closest !== "function") return;

    var menuButton = target.closest("#menu-toggle");
    if (menuButton) {
      var navigation = document.getElementById("primary-nav");
      if (!navigation) return;

      var isOpen = menuButton.getAttribute("aria-expanded") !== "true";
      menuButton.setAttribute("aria-expanded", String(isOpen));
      menuButton.setAttribute("aria-label", isOpen ? "Tutup navigasi" : "Buka navigasi");
      navigation.classList.toggle("is-open", isOpen);
      return;
    }

    if (target.closest("#primary-nav a")) {
      var activeMenuButton = document.getElementById("menu-toggle");
      var activeNavigation = document.getElementById("primary-nav");
      if (activeMenuButton && activeNavigation) {
        activeMenuButton.setAttribute("aria-expanded", "false");
        activeMenuButton.setAttribute("aria-label", "Buka navigasi");
        activeNavigation.classList.remove("is-open");
      }
    }

    var themeButton = target.closest("#theme-toggle");
    if (themeButton) {
      var nextTheme = getCurrentTheme() === "dark" ? "light" : "dark";
      root.setAttribute("data-theme", nextTheme);
      try {
        window.localStorage.setItem(themeStorageKey, nextTheme);
      } catch (error) {
        /* The selected theme still applies for the current page session. */
      }
      syncThemeControl();
    }
  });

  document.addEventListener("keydown", function (event) {
    if (event.key !== "Escape") return;

    var navigation = document.getElementById("primary-nav");
    var menuButton = document.getElementById("menu-toggle");
    if (!navigation || !menuButton || !navigation.classList.contains("is-open")) return;

    navigation.classList.remove("is-open");
    menuButton.setAttribute("aria-expanded", "false");
    menuButton.setAttribute("aria-label", "Buka navigasi");
    menuButton.focus();
  });

  if (window.matchMedia) {
    window.matchMedia("(prefers-color-scheme: dark)").addEventListener?.("change", function () {
      if (!root.hasAttribute("data-theme")) syncThemeControl();
    });
  }

  /* Handle both fast and delayed asynchronous component injection. */
  document.addEventListener("DOMContentLoaded", initializeLayout);
  document.addEventListener("dekeku:components-loaded", initializeLayout);
}());
