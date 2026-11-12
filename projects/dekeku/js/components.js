/* Loads shared DEKEKU layout components. */
(function () {
  "use strict";

  var mounts = document.querySelectorAll("[data-component]");
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
        mount.setAttribute("data-component-error", name);
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