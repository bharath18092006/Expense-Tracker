(function () {
  function applyTheme(theme) {
    const body = document.body;
    body.classList.remove("theme-aurora", "theme-zen", "theme-carbon");
    body.classList.add(theme);
    const icon = document.querySelector("#themeToggleBtn i");
    if (icon) {
      icon.className = theme === "theme-carbon" ? "fa fa-sun-o" : "fa fa-moon-o";
    }
  }

  document.addEventListener("DOMContentLoaded", function () {
    const savedTheme = localStorage.getItem("expensewise_theme") || "theme-aurora";
    applyTheme(savedTheme);
    const toggleBtn = document.getElementById("themeToggleBtn");
    if (!toggleBtn) return;
    toggleBtn.addEventListener("click", function () {
      const nextTheme = document.body.classList.contains("theme-carbon")
        ? "theme-aurora"
        : "theme-carbon";
      localStorage.setItem("expensewise_theme", nextTheme);
      applyTheme(nextTheme);
    });
  });
})();
