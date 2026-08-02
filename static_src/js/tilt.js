(function () {
  function attach(el) {
    var intensity = parseFloat(el.dataset.tiltIntensity || "10");

    function handleMove(e) {
      var rect = el.getBoundingClientRect();
      var px = (e.clientX - rect.left) / rect.width;
      var py = (e.clientY - rect.top) / rect.height;
      el.style.setProperty("--rx", (0.5 - py) * intensity + "deg");
      el.style.setProperty("--ry", (px - 0.5) * intensity + "deg");
      el.style.setProperty("--mx", px * 100 + "%");
      el.style.setProperty("--my", py * 100 + "%");
    }

    function handleLeave() {
      el.style.setProperty("--rx", "0deg");
      el.style.setProperty("--ry", "0deg");
    }

    el.addEventListener("mousemove", handleMove);
    el.addEventListener("mouseleave", handleLeave);
  }

  document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll("[data-tilt]").forEach(attach);
  });
})();
