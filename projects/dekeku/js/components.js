/* Loads shared DEKEKU layout components with accessible failure fallbacks. */
(function () {
  "use strict";

  var mounts = document.querySelectorAll("[data-component]");

  function element(tag, className, text) {
    var node = document.createElement(tag);
    if (className) node.className = className;
    if (text !== undefined) node.textContent = text;
    return node;
  }

  function link(parent, href, text, className) {
    var node = element("a", className, text);
    node.href = href;
    parent.appendChild(node);
    return node;
  }

  function renderFallback(mount, name, root) {
    if (name === "header") {
      var header = element("header", "site-header component-fallback");
      var wrap = element("div", "container nav-wrap");
      var brand = link(wrap, root + "index.html", "DEKEKU", "brand");
      brand.setAttribute("aria-label", "DEKEKU, beranda");

      var menu = element("button", "icon-button menu-toggle");
      menu.type = "button";
      menu.id = "menu-toggle";
      menu.setAttribute("aria-expanded", "false");
      menu.setAttribute("aria-controls", "primary-nav");
      menu.setAttribute("aria-label", "Buka navigasi");
      menu.append(element("span"), element("span"));

      var nav = element("nav", "primary-nav");
      nav.id = "primary-nav";
      nav.setAttribute("aria-label", "Navigasi utama");
      [
        ["index.html", "Beranda"],
        ["pages/produk.html", "Produk"],
        ["pages/paket.html", "Paket"],
        ["pages/tentang.html", "Tentang"],
        ["pages/kontak.html", "Kontak"]
      ].forEach(function (item) {
        link(nav, root + item[0], item[1]).setAttribute("data-page", item[0]);
      });
      link(nav, "https://wa.me/6285161517176", "WhatsApp Admin", "button button-small button-dark nav-cta")
        .setAttribute("rel", "noopener noreferrer");

      var tools = element("div", "nav-tools");
      var theme = element("button", "icon-button theme-toggle", "Tema");
      theme.type = "button";
      theme.id = "theme-toggle";
      theme.setAttribute("aria-label", "Aktifkan tema gelap");
      theme.setAttribute("aria-pressed", "false");
      tools.appendChild(theme);

      wrap.append(brand, menu, nav, tools);
      header.appendChild(wrap);
      mount.replaceWith(header);
      return;
    }

    if (name === "footer") {
      var footer = element("footer", "site-footer component-fallback");
      var wrap = element("div", "container footer-top");
      var brand = element("div", "footer-brand");
      link(brand, root + "index.html", "DEKEKU");
      brand.appendChild(element("p", "", "Your Digital Space."));
      var links = element("nav", "footer-links");
      links.setAttribute("aria-label", "Tautan footer");
      [
        ["index.html#layanan", "Layanan"],
        ["pages/produk.html", "Produk"],
        ["pages/paket.html", "Paket"],
        ["pages/tentang.html", "Tentang Kami"],
        ["pages/kontak.html", "Kontak"]
      ].forEach(function (item) {
        link(links, root + item[0], item[1]);
      });
      wrap.append(brand, links);
      var bottom = element("div", "container footer-bottom");
      bottom.appendChild(element("span", "", "© " + new Date().getFullYear() + " DEKEKU."));
      footer.append(wrap, bottom);
      mount.replaceWith(footer);
    }
  }

  var tasks = Array.prototype.map.call(mounts, function (mount) {
    var name = mount.getAttribute("data-component");
    var root = mount.getAttribute("data-root") || "";
    if (name !== "header" && name !== "footer") return Promise.resolve();

    return fetch(root + "components/" + name + ".html")
      .then(function (response) {
        if (!response.ok) throw new Error("Komponen " + name + " gagal dimuat.");
        return response.text();
      })
      .then(function (html) {
        mount.outerHTML = html.replace(/\{\{root\}\}/g, root);
      })
      .catch(function (error) {
        console.error(error);
        renderFallback(mount, name, root);
      });
  });

  Promise.all(tasks).then(function () {
    var currentPath = window.location.pathname.replace(/\/$/, "").split("/").pop() || "index.html";
    var currentPage = window.location.pathname.indexOf("/pages/") !== -1
      ? "pages/" + currentPath
      : currentPath;

    document.querySelectorAll(".primary-nav [data-page]").forEach(function (link) {
      if (link.getAttribute("data-page") === currentPage) {
        link.setAttribute("aria-current", "page");
      }
    });

    document.dispatchEvent(new CustomEvent("dekeku:components-loaded"));
  });
}());
