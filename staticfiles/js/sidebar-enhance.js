(function () {
  function normalizePath(path) {
    return (path || "").replace(/\/+$/, "") || "/";
  }

  document.addEventListener("DOMContentLoaded", function () {
    const currentPath = normalizePath(window.location.pathname);
    const sidebarLinks = document.querySelectorAll("#sidebar .sidebar-menu a[href]");

    let bestMatch = null;
    let bestLength = -1;

    sidebarLinks.forEach(function (link) {
      const href = link.getAttribute("href");
      if (!href || href.startsWith("#")) return;

      const linkPath = normalizePath(new URL(href, window.location.origin).pathname);
      const isExact = currentPath === linkPath;
      const isPrefix = linkPath !== "/" && currentPath.startsWith(linkPath);

      if (isExact || isPrefix) {
        if (linkPath.length > bestLength) {
          bestMatch = link;
          bestLength = linkPath.length;
        }
      }
    });

    if (bestMatch) {
      bestMatch.classList.add("is-active");
    }
  });
})();
