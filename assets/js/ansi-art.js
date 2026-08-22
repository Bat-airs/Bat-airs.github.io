/* ANSI → HTML 彩色渲染器（自包含，零依赖，无 CDN）
 *
 * 用途：渲染 chafa 输出的 ANSI 彩色字符画（支持 24bit / 256 / 16 色 SGR 码）。
 * 背景：此前依赖 jsdelivr CDN 的 ansi_up，国内常被墙导致渲染脚本整体失效，
 *       字符画显示为原始转义码乱码（看起来"被压扁"）。现改为本地内置。
 * 契约：ART-RENDERING.md（行高 = 2 × 字形宽比，保持 chafa 1:2 字符格假设）
 */
(function () {
  "use strict";

  var BASIC = ["#000", "#a00", "#0a0", "#a50", "#00a", "#a0a", "#0aa", "#aaa",
               "#555", "#f55", "#5f5", "#ff5", "#55f", "#f5f", "#5ff", "#fff"];

  function xterm256(n) {
    if (n < 16) return BASIC[n];
    if (n < 232) {
      n -= 16;
      function v(c) { return c === 0 ? "00" : (55 + c * 40).toString(16); }
      return "#" + v(Math.floor(n / 36)) + v(Math.floor((n % 36) / 6)) + v(n % 6);
    }
    var g = (8 + (n - 232) * 10).toString(16);
    return "#" + g + g + g;
  }

  /* 把含 ANSI 转义序列的文本转成带 <span> 的彩色 HTML */
  window.ansiToHtml = function (text) {
    var esc = text.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
    var html = "", fg = null, bg = null, open = false;
    var re = /\x1b\[([0-9;]*)m/g;
    var last = 0, m;
    function close() { if (open) { html += "</span>"; open = false; } }
    function apply() {
      close();
      var parts = [];
      if (fg) parts.push("color:" + fg);
      if (bg) parts.push("background-color:" + bg);
      if (parts.length) { html += '<span style="' + parts.join(";") + '">'; open = true; }
    }
    while ((m = re.exec(esc)) !== null) {
      html += esc.slice(last, m.index);
      last = m.index + m[0].length;
      var codes = m[1] ? m[1].split(";").map(Number) : [0];
      var i = 0;
      while (i < codes.length) {
        var c = codes[i];
        if (c === 0) { fg = null; bg = null; i++; }
        else if (c >= 30 && c <= 37) { fg = BASIC[c - 30]; i++; }
        else if (c >= 90 && c <= 97) { fg = BASIC[c - 90 + 8]; i++; }
        else if (c >= 40 && c <= 47) { bg = BASIC[c - 40]; i++; }
        else if (c >= 100 && c <= 107) { bg = BASIC[c - 100 + 8]; i++; }
        else if ((c === 38 || c === 48) && codes[i + 1] === 5) {
          var col5 = xterm256(codes[i + 2]);
          if (c === 38) fg = col5; else bg = col5;
          i += 3;
        } else if ((c === 38 || c === 48) && codes[i + 1] === 2) {
          var col2 = "rgb(" + codes[i + 2] + "," + codes[i + 3] + "," + codes[i + 4] + ")";
          if (c === 38) fg = col2; else bg = col2;
          i += 5;
        } else i++;
      }
      apply();
    }
    html += esc.slice(last);
    close();
    return html;
  };

  /* 去掉 ANSI 码，只留纯字符（兜底显示） */
  window.stripAnsi = function (text) {
    return text.replace(/\x1b\[[0-9;?]*[A-Za-z]/g, "");
  };

  /* 清理 chafa 原始输出：字面 \x1b → 真实 ESC；去掉光标控制等非 SGR 序列 */
  window.cleanAnsi = function (text) {
    return text
      .replace(/\\x1b/g, "\x1b")
      .replace(/\x1b\[\?25[lh]/g, "")
      .replace(/\x1b\[[0-9;?]*[A-LN-Za-ln-z]/g, "");
  };
})();
