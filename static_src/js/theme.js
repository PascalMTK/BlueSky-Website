(function () {
  var STORAGE_KEY = "bluesky-theme";

  function applyIcons() {
    var isDark = document.documentElement.classList.contains("dark");
    document.querySelectorAll(".theme-icon-moon").forEach(function (el) {
      el.classList.toggle("hidden", isDark);
    });
    document.querySelectorAll(".theme-icon-sun").forEach(function (el) {
      el.classList.toggle("hidden", !isDark);
    });
  }

  function toggleTheme() {
    var next = document.documentElement.classList.toggle("dark");
    try {
      localStorage.setItem(STORAGE_KEY, next ? "dark" : "light");
    } catch (e) {}
    applyIcons();
  }

  document.addEventListener("DOMContentLoaded", function () {
    applyIcons();
    document.querySelectorAll("[data-theme-toggle]").forEach(function (btn) {
      btn.addEventListener("click", toggleTheme);
    });
  });
})();
