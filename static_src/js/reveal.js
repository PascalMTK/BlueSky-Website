(function () {
  var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  function showAll(items) {
    items.forEach(function (el) {
      el.classList.add("is-visible");
    });
  }

  document.addEventListener("DOMContentLoaded", function () {
    var items = Array.prototype.slice.call(document.querySelectorAll(".reveal-on-scroll"));
    if (!items.length) return;

    // Stagger siblings inside a [data-reveal-group] by their DOM order, so
    // grids of cards fan in one after another instead of all at once.
    document.querySelectorAll("[data-reveal-group]").forEach(function (group) {
      var index = 0;
      Array.prototype.forEach.call(group.children, function (child) {
        if (child.classList.contains("reveal-on-scroll")) {
          child.style.setProperty("--reveal-index", index);
          index += 1;
        }
      });
    });

    if (reduceMotion || !("IntersectionObserver" in window)) {
      showAll(items);
      return;
    }

    var observer = new IntersectionObserver(
      function (entries, obs) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add("is-visible");
            obs.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.15, rootMargin: "0px 0px -8% 0px" }
    );

    items.forEach(function (el) {
      observer.observe(el);
    });

    // Safety net: never leave content permanently invisible (e.g. an
    // element whose container is hidden at observe-time and only shown
    // later by unrelated script) — force everything in after a few seconds.
    window.setTimeout(function () {
      showAll(items);
    }, 4000);
  });
})();
