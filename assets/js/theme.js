/* 主题切换：深色模式支持 */
(function () {
  var KEY = "bat-airs-theme";
  var root = document.documentElement;
  var btn = document.getElementById("themeBtn");

  function apply(theme) {
    root.setAttribute("data-theme", theme);
    if (btn) {
      btn.textContent = theme === "dark" ? "☀️" : "🌙";
    }
  }

  // 初始化：优先 localStorage，其次跟随系统
  var saved = null;
  try { saved = localStorage.getItem(KEY); } catch (e) { /* ignore */ }
  var theme = saved ||
    (window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches
      ? "dark" : "light");
  apply(theme);

  if (btn) {
    btn.addEventListener("click", function () {
      var next = root.getAttribute("data-theme") === "dark" ? "light" : "dark";
      apply(next);
      try { localStorage.setItem(KEY, next); } catch (e) { /* ignore */ }
    });
  }
})();
