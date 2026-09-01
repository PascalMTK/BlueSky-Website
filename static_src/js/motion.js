(function () {
  "use strict";

  var reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var finePointer = window.matchMedia("(pointer: fine)").matches;

  function initHeader() {
    var header = document.querySelector("header");
    if (!header) return;
    var scrollQueued = false;
    function updateHeader() {
      header.classList.toggle("is-scrolled", window.scrollY > 12);
      scrollQueued = false;
    }
    window.addEventListener("scroll", function () {
      if (!scrollQueued) { scrollQueued = true; requestAnimationFrame(updateHeader); }
    }, { passive: true });
    updateHeader();

    var toggle = header.querySelector("[data-mobile-nav-toggle]");
    var menu = header.querySelector("[data-mobile-nav]");
    if (!toggle || !menu) return;
    menu.classList.remove("hidden");
    menu.classList.add("mobile-nav-enhanced");

    function setMenu(open) {
      menu.classList.toggle("is-open", open);
      toggle.setAttribute("aria-expanded", String(open));
      document.body.style.overflow = open ? "hidden" : "";
    }
    toggle.addEventListener("click", function () {
      setMenu(toggle.getAttribute("aria-expanded") !== "true");
    });
    menu.addEventListener("click", function (event) {
      if (event.target.closest("a")) setMenu(false);
    });
    document.addEventListener("keydown", function (event) {
      if (event.key === "Escape" && toggle.getAttribute("aria-expanded") === "true") {
        setMenu(false);
        toggle.focus();
      }
    });
    window.addEventListener("resize", function () {
      if (window.innerWidth >= 1280) setMenu(false);
    });
  }

  // Fixed hairline at the top of the viewport tracking scroll progress.
  function initScrollProgress() {
    var bar = document.createElement("div");
    bar.className = "scroll-progress";
    bar.setAttribute("aria-hidden", "true");
    document.body.appendChild(bar);
    var root = document.documentElement;
    var ticking = false;
    function update() {
      var max = root.scrollHeight - window.innerHeight;
      root.style.setProperty("--scroll-progress", max > 0 ? Math.min(window.scrollY / max, 1).toFixed(4) : "0");
      ticking = false;
    }
    function request() {
      if (!ticking) { ticking = true; requestAnimationFrame(update); }
    }
    window.addEventListener("scroll", request, { passive: true });
    window.addEventListener("resize", request, { passive: true });
    update();
  }

  // A soft glow that trails the pointer, smoothed with simple lerp easing
  // so it drifts rather than snaps.
  function initCursorAura() {
    var aura = document.createElement("div");
    aura.className = "cursor-aura";
    aura.setAttribute("aria-hidden", "true");
    document.body.appendChild(aura);
    var root = document.documentElement;
    var targetX = 0, targetY = 0, curX = 0, curY = 0;
    var first = true;
    var running = false;

    function tick() {
      curX += (targetX - curX) * 0.14;
      curY += (targetY - curY) * 0.14;
      root.style.setProperty("--aura-x", curX.toFixed(1) + "px");
      root.style.setProperty("--aura-y", curY.toFixed(1) + "px");
      if (Math.abs(targetX - curX) > 0.4 || Math.abs(targetY - curY) > 0.4) {
        requestAnimationFrame(tick);
      } else {
        running = false;
      }
    }

    window.addEventListener("pointermove", function (event) {
      targetX = event.clientX;
      targetY = event.clientY;
      if (first) { curX = targetX; curY = targetY; first = false; }
      aura.style.opacity = "1";
      if (!running) { running = true; requestAnimationFrame(tick); }
    }, { passive: true });

    window.addEventListener("pointerleave", function () { aura.style.opacity = "0"; });
    document.addEventListener("pointerdown", function () { aura.style.opacity = ".55"; });
    document.addEventListener("pointerup", function () { aura.style.opacity = "1"; });
  }

  // 3D tilt for framed / premium / full-bleed photo cards, following the
  // pointer within the card; CSS handles the release transition.
  function initTilt(root) {
    var cards = root.querySelectorAll(".framed-card, .premium-card, .service-image-card");
    cards.forEach(function (card) {
      var raf = null;
      card.addEventListener("pointermove", function (event) {
        if (raf) return;
        raf = requestAnimationFrame(function () {
          var rect = card.getBoundingClientRect();
          var px = (event.clientX - rect.left) / rect.width;
          var py = (event.clientY - rect.top) / rect.height;
          card.style.setProperty("--tilt-rx", ((0.5 - py) * 7).toFixed(2) + "deg");
          card.style.setProperty("--tilt-ry", ((px - 0.5) * 7).toFixed(2) + "deg");
          raf = null;
        });
      });
      card.addEventListener("pointerleave", function () {
        card.style.setProperty("--tilt-rx", "0deg");
        card.style.setProperty("--tilt-ry", "0deg");
      });
    });
  }

  // A composed hero scene: the whole visual follows the pointer with a
  // restrained camera move, while individual overlays travel at different
  // depths. This creates real parallax instead of a flat rotate effect.
  function initHeroScene(main) {
    var scene = main.querySelector("[data-hero-scene]");
    if (!scene) return;
    var layers = scene.querySelectorAll("[data-depth]");
    var targetX = 0, targetY = 0, currentX = 0, currentY = 0, running = false;

    function render() {
      currentX += (targetX - currentX) * .09;
      currentY += (targetY - currentY) * .09;
      scene.style.setProperty("--scene-rx", (-currentY * 4.5).toFixed(2) + "deg");
      scene.style.setProperty("--scene-ry", (currentX * 5.5).toFixed(2) + "deg");
      layers.forEach(function (layer) {
        var depth = Number(layer.getAttribute("data-depth")) || 1;
        layer.style.setProperty("--depth-x", (currentX * depth * 7).toFixed(1) + "px");
        layer.style.setProperty("--depth-y", (currentY * depth * 7).toFixed(1) + "px");
      });
      if (Math.abs(targetX - currentX) > .003 || Math.abs(targetY - currentY) > .003) requestAnimationFrame(render);
      else running = false;
    }
    function move(event) {
      var rect = scene.getBoundingClientRect();
      targetX = Math.max(-1, Math.min(1, (event.clientX - rect.left) / rect.width * 2 - 1));
      targetY = Math.max(-1, Math.min(1, (event.clientY - rect.top) / rect.height * 2 - 1));
      scene.style.setProperty("--shine-x", (((targetX + 1) / 2) * 100).toFixed(1) + "%");
      scene.style.setProperty("--shine-y", (((targetY + 1) / 2) * 100).toFixed(1) + "%");
      if (!running) { running = true; requestAnimationFrame(render); }
    }
    scene.addEventListener("pointermove", move, { passive: true });
    scene.addEventListener("pointerleave", function () {
      targetX = 0; targetY = 0;
      if (!running) { running = true; requestAnimationFrame(render); }
    });
  }

  // Cursor-following radial highlight for content cards / summary panel —
  // lighter than tilt, so it reads well on dense dashboard screens too.
  function initSpotlight() {
    var cards = document.querySelectorAll(".content-card, .summary-card");
    cards.forEach(function (card) {
      card.addEventListener("pointermove", function (event) {
        var rect = card.getBoundingClientRect();
        card.style.setProperty("--mx", (((event.clientX - rect.left) / rect.width) * 100).toFixed(1) + "%");
        card.style.setProperty("--my", (((event.clientY - rect.top) / rect.height) * 100).toFixed(1) + "%");
      });
    });
  }

  // Primary buttons and the WhatsApp pill pull gently toward the cursor
  // while hovered.
  function initMagnetic() {
    // .whatsapp-fab is deliberately excluded: it already carries a
    // forwards-filled entrance animation on `transform`, which would keep
    // outranking this hover transform in the cascade.
    var els = document.querySelectorAll(".btn-primary, .contact-pill");
    var max = 10, strength = 0.35;
    els.forEach(function (el) {
      el.classList.add("magnetic");
      el.addEventListener("pointermove", function (event) {
        var rect = el.getBoundingClientRect();
        var mx = event.clientX - (rect.left + rect.width / 2);
        var my = event.clientY - (rect.top + rect.height / 2);
        el.style.setProperty("--mag-x", Math.max(-max, Math.min(max, mx * strength)).toFixed(1) + "px");
        el.style.setProperty("--mag-y", Math.max(-max, Math.min(max, my * strength)).toFixed(1) + "px");
      });
      el.addEventListener("pointerleave", function () {
        el.style.setProperty("--mag-x", "0px");
        el.style.setProperty("--mag-y", "0px");
      });
    });
  }

  // Section background photos drift slower than the page as it scrolls.
  function initParallax(main) {
    var targets = Array.prototype.slice.call(main.querySelectorAll(".section-photo-bg img"));
    if (!targets.length) return;
    var ticking = false;
    function update() {
      var vh = window.innerHeight;
      targets.forEach(function (img) {
        var rect = img.parentElement.getBoundingClientRect();
        var progress = (rect.top + rect.height / 2 - vh / 2) / vh;
        var shift = Math.max(-40, Math.min(40, progress * 26));
        img.style.transform = "translate3d(0," + shift.toFixed(1) + "px,0) scale(1.12)";
      });
      ticking = false;
    }
    function request() {
      if (!ticking) { ticking = true; requestAnimationFrame(update); }
    }
    window.addEventListener("scroll", request, { passive: true });
    window.addEventListener("resize", request, { passive: true });
    update();
  }

  function initHero(main) {
    var hero = main.querySelector("section:first-child");
    if (!hero || !hero.querySelector("h1")) return;
    var heading = hero.querySelector("h1");
    var label = hero.querySelector(".editorial-label");
    var paragraph = heading.nextElementSibling;
    var actions = paragraph && paragraph.nextElementSibling;
    var image = hero.querySelector("img");
    var heroVisual = hero.querySelector("[data-hero-scene]");
    var sequence = [label, heading, paragraph, actions, heroVisual || (image && image.parentElement)].filter(Boolean);
    sequence.forEach(function (element, index) {
      element.setAttribute("data-hero-motion", "");
      element.style.setProperty("--motion-delay", (index * 70) + "ms");
    });
  }

  function initHeroVideos(main) {
    var slider = main.querySelector("[data-hero-video-slider]");
    if (!slider || reducedMotion) return;
    var videos = Array.prototype.slice.call(slider.querySelectorAll("video"));
    if (!videos.length) return;
    var activeIndex = 0;

    function play(index, previousIndex) {
      var current = videos[index];
      current.currentTime = 0;
      var promise = current.play();
      if (promise && promise.catch) promise.catch(function () {});
      requestAnimationFrame(function () {
        current.classList.add("is-active");
        if (typeof previousIndex !== "number") return;
        var previous = videos[previousIndex];
        previous.classList.remove("is-active");
        window.setTimeout(function () {
          previous.pause();
          previous.currentTime = 0;
        }, 1150);
      });
    }

    videos.forEach(function (video, index) {
      video.addEventListener("ended", function () {
        var previousIndex = index;
        activeIndex = (index + 1) % videos.length;
        play(activeIndex, previousIndex);
      });
      video.addEventListener("error", function () {
        if (index !== activeIndex) return;
        video.classList.remove("is-active");
        activeIndex = (index + 1) % videos.length;
        play(activeIndex);
      });
    });
    var initialPlay = videos[activeIndex].play();
    if (initialPlay && initialPlay.catch) initialPlay.catch(function () {});
  }

  function initCountryCards(main) {
    var cards = main.querySelectorAll("[data-country-card]");
    var activeDialog = null;

    function closeDialog(dialog, restoreFocus) {
      if (!dialog || !dialog.hasAttribute("open") || dialog.classList.contains("is-closing")) return;
      dialog.classList.add("is-closing");
      window.setTimeout(function () {
        dialog.classList.remove("is-closing");
        if (typeof dialog.close === "function") dialog.close();
        else dialog.removeAttribute("open");
        if (activeDialog === dialog) activeDialog = null;
        if (restoreFocus) restoreFocus.focus();
      }, reducedMotion ? 0 : 180);
    }

    cards.forEach(function (card) {
      var dialog = document.getElementById(card.getAttribute("data-country-dialog"));
      if (!dialog) return;
      function openDialog() {
        if (activeDialog === dialog && dialog.hasAttribute("open")) return;
        if (activeDialog && activeDialog.hasAttribute("open")) {
          activeDialog.classList.remove("is-closing");
          if (typeof activeDialog.close === "function") activeDialog.close();
          else activeDialog.removeAttribute("open");
        }
        activeDialog = dialog;
        dialog.classList.remove("is-closing");
        if (typeof dialog.showModal === "function") dialog.showModal();
        else dialog.setAttribute("open", "");
      }
      card.addEventListener("click", openDialog);
      card.addEventListener("keydown", function (event) {
        if (event.key === "Enter" || event.key === " ") {
          event.preventDefault();
          openDialog();
        }
      });
      var close = dialog.querySelector("[data-country-dialog-close]");
      if (close) close.addEventListener("click", function () { closeDialog(dialog, card); });
      dialog.addEventListener("click", function (event) {
        if (event.target === dialog) closeDialog(dialog, card);
      });
      dialog.addEventListener("cancel", function (event) {
        event.preventDefault();
        closeDialog(dialog, card);
      });
    });
  }

  // Selects an element's most "card-like" direct (or one-level-nested)
  // children so a grid of cards can cascade in one after another instead
  // of the whole block fading in at once.
  function findCardGroup(content) {
    var selector = ":scope > article, :scope > .content-card, :scope > .framed-card, :scope > .premium-card, :scope > .service-image-card";
    try {
      var direct = Array.prototype.slice.call(content.querySelectorAll(selector));
      if (direct.length >= 3) return direct;
      var wrappers = Array.prototype.slice.call(content.querySelectorAll(":scope > div, :scope > .grid"));
      for (var i = 0; i < wrappers.length; i++) {
        var nested = Array.prototype.slice.call(wrappers[i].querySelectorAll(selector));
        if (nested.length >= 3) return nested;
      }
    } catch (e) { /* :scope unsupported — fall back to whole-block reveal */ }
    return null;
  }

  function registerRevealTarget(content, targets) {
    if (!content) return;
    var cardGroup = findCardGroup(content);
    if (cardGroup) {
      cardGroup.forEach(function (child, index) {
        child.setAttribute("data-motion", "card");
        child.style.setProperty("--motion-delay", Math.min(index * 70, 420) + "ms");
        targets.push(child);
      });
    } else {
      content.setAttribute("data-motion", "section");
      targets.push(content);
    }
  }

  function initSectionReveal(main) {
    if (!("IntersectionObserver" in window)) return;
    var sections = Array.prototype.slice.call(main.querySelectorAll("section"));
    var targets = [];

    if (sections.length > 1) {
      // Marketing-style pages: skip the hero (handled by initHero), reveal
      // every section after it.
      sections.slice(1).forEach(function (section) {
        var content = Array.prototype.find.call(section.children, function (child) {
          return !child.classList.contains("section-photo-bg");
        });
        registerRevealTarget(content, targets);
      });
    } else if (sections.length === 0) {
      // Dashboard/staff-style pages: no <section> wrapper — reveal main's
      // own top-level content blocks.
      Array.prototype.forEach.call(main.children, function (child) {
        registerRevealTarget(child, targets);
      });
    }

    document.documentElement.classList.add("motion-ready");
    var observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        entry.target.classList.add("is-visible");
        observer.unobserve(entry.target);
      });
    }, { rootMargin: "0px 0px -10% 0px", threshold: .08 });
    targets.forEach(function (target) { observer.observe(target); });
  }

  function initCounters(main) {
    if (!("IntersectionObserver" in window)) return;
    var numbers = main.querySelectorAll(".text-3xl.font-extrabold, .text-2xl.font-extrabold, .text-4xl.font-extrabold");
    var observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        var node = entry.target;
        var original = node.textContent.trim();
        var match = original.match(/^(\d+)(.*)$/);
        if (!match) return;
        var target = Number(match[1]);
        var suffix = match[2];
        var start;
        function tick(time) {
          if (!start) start = time;
          var progress = Math.min((time - start) / 700, 1);
          node.textContent = Math.round(target * (1 - Math.pow(1 - progress, 3))) + suffix;
          if (progress < 1) {
            requestAnimationFrame(tick);
          } else {
            node.textContent = original;
            node.classList.add("motion-count-in");
          }
        }
        requestAnimationFrame(tick);
        observer.unobserve(node);
      });
    }, { threshold: .7 });
    numbers.forEach(function (number) {
      if (/^\d/.test(number.textContent.trim())) observer.observe(number);
    });
  }

  function init() {
    var main = document.querySelector("main");
    initHeader();
    initScrollProgress();
    if (!main) return;
    initCountryCards(main);
    initHeroVideos(main);
    if (reducedMotion) return;
    initHero(main);
    initSectionReveal(main);
    initCounters(main);
    initParallax(main);
    if (finePointer) {
      initCursorAura();
      initHeroScene(main);
      initTilt(main);
      initSpotlight();
      initMagnetic();
    }
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init);
  else init();
})();
