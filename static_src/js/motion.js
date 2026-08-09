(function () {
  var reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  document.addEventListener("DOMContentLoaded", function () {
    var root = document.documentElement;
    var progress = document.createElement("div");
    progress.className = "scroll-progress";
    progress.setAttribute("aria-hidden", "true");
    document.body.appendChild(progress);

    var aura;
    if (!reduced && window.matchMedia("(pointer: fine)").matches) {
      aura = document.createElement("div");
      aura.className = "cursor-aura";
      aura.setAttribute("aria-hidden", "true");
      document.body.appendChild(aura);
      window.addEventListener("pointermove", function (event) {
        root.style.setProperty("--aura-x", event.clientX + "px");
        root.style.setProperty("--aura-y", event.clientY + "px");
      }, { passive: true });
    }

    var parallaxItems = Array.prototype.slice.call(document.querySelectorAll("[data-parallax]"));
    var ticking = false;
    function updateMotion() {
      var max = root.scrollHeight - window.innerHeight;
      root.style.setProperty("--scroll-progress", max > 0 ? Math.min(window.scrollY / max, 1) : 0);
      if (!reduced) {
        parallaxItems.forEach(function (item) {
          var rect = item.getBoundingClientRect();
          var speed = parseFloat(item.dataset.parallax || "0.08");
          var offset = (rect.top + rect.height / 2 - window.innerHeight / 2) * speed;
          item.style.setProperty("--parallax-y", offset.toFixed(1) + "px");
        });
      }
      ticking = false;
    }
    function requestUpdate() {
      if (!ticking) {
        window.requestAnimationFrame(updateMotion);
        ticking = true;
      }
    }
    window.addEventListener("scroll", requestUpdate, { passive: true });
    window.addEventListener("resize", requestUpdate, { passive: true });
    updateMotion();

    if (reduced || !("IntersectionObserver" in window)) return;
    var counters = document.querySelectorAll("[data-count]");
    var counterObserver = new IntersectionObserver(function (entries, observer) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        var el = entry.target;
        var match = el.textContent.trim().match(/^(\d+)(.*)$/);
        if (!match) return observer.unobserve(el);
        var target = parseInt(match[1], 10);
        var suffix = match[2];
        var start = performance.now();
        function count(now) {
          var elapsed = Math.min((now - start) / 900, 1);
          var eased = 1 - Math.pow(1 - elapsed, 3);
          el.textContent = Math.round(target * eased) + suffix;
          if (elapsed < 1) window.requestAnimationFrame(count);
        }
        window.requestAnimationFrame(count);
        observer.unobserve(el);
      });
    }, { threshold: 0.6 });
    counters.forEach(function (counter) { counterObserver.observe(counter); });
  });
})();
