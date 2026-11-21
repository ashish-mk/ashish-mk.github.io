(function () {
  const STORAGE_KEY = "theme-preference";
  const toggleBtn = document.getElementById("theme-toggle");

  function getPreferredTheme() {
    const saved = localStorage.getItem(STORAGE_KEY);
    if (saved) return saved;
    return window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
  }

  function setTheme(theme) {
    document.documentElement.setAttribute("data-theme", theme);
    localStorage.setItem(STORAGE_KEY, theme);
    if (toggleBtn) {
      toggleBtn.innerHTML = theme === "dark" ? "☀️ Light" : "🌙 Dark";
      toggleBtn.setAttribute("aria-label", `Switch to ${theme === "dark" ? "light" : "dark"} mode`);
    }
  }

  // Set initial theme
  const initialTheme = getPreferredTheme();
  setTheme(initialTheme);

  if (toggleBtn) {
    toggleBtn.addEventListener("click", function () {
      const current = document.documentElement.getAttribute("data-theme") || "light";
      const next = current === "dark" ? "light" : "dark";
      setTheme(next);
    });
  }
})();
