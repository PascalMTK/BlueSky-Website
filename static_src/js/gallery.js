(() => {
  const root = document.querySelector('[data-gallery]');
  if (!root) return;
  const links = [...root.querySelectorAll('[data-gallery-image]')];
  if (!links.length) return;
  const dialog = root.querySelector('dialog');
  const play = root.querySelector('[data-gallery-play]');
  const motion = matchMedia('(prefers-reduced-motion: reduce)');
  const feature = root.querySelector('[data-feature-image]');
  const featureLink = root.querySelector('[data-feature-link]');
  const timeline = root.querySelector('.gallery-timeline span');
  let paused = motion.matches, active = 0, elapsed = 0, last = performance.now(), returnFocus;
  function playState() {
    play.textContent = paused ? play.dataset.playLabel : play.dataset.pauseLabel;
    play.setAttribute('aria-pressed', String(paused));
  }
  function modalContent() {
    dialog.querySelector('img').src = links[active].href;
    dialog.querySelector('img').alt = links[active].dataset.title;
    root.querySelector('[data-gallery-caption]').textContent = links[active].dataset.title;
    root.querySelector('[data-gallery-count]').textContent = `${active + 1} / ${links.length}`;
  }
  function select(index, reveal = false) {
    active = (index + links.length) % links.length;
    const selected = links[active];
    feature.src = selected.href;
    feature.alt = selected.dataset.title;
    featureLink.href = selected.href;
    root.querySelector('[data-feature-title]').textContent = selected.dataset.title;
    root.querySelector('[data-feature-description]').textContent = selected.dataset.description;
    root.querySelector('[data-feature-number]').textContent = String(active + 1).padStart(2, '0');
    links.forEach((link, i) => {
      link.classList.toggle('is-selected', i === active);
      link.setAttribute('aria-current', String(i === active));
    });
    if (!motion.matches && feature.animate) feature.animate([{opacity:.3, transform:'translateY(8px)'},{opacity:1, transform:'translateY(0)'}], {duration:450, easing:'ease-out'});
    if (reveal) {
      const strip = selected.parentElement;
      strip.scrollTo({left:selected.offsetLeft - strip.offsetLeft - strip.clientWidth / 2 + selected.clientWidth / 2, behavior:motion.matches ? 'instant' : 'smooth'});
    }
    elapsed = 0;
    timeline.style.width = '0%';
    if (dialog.open) modalContent();
  }
  playState();
  play.onclick = () => { paused = !paused; playState(); };
  motion.addEventListener('change', () => { paused = motion.matches; playState(); });
  root.querySelector('[data-gallery-prev]').onclick = () => select(active - 1, true);
  root.querySelector('[data-gallery-next]').onclick = () => select(active + 1, true);
  links.forEach((link, i) => link.addEventListener('click', event => {
    if (event.ctrlKey || event.metaKey || event.shiftKey) return;
    event.preventDefault(); select(i);
  }));
  root.addEventListener('keydown', event => {
    if (event.key === 'ArrowRight' || event.key === 'ArrowLeft') {
      event.preventDefault(); select(active + (event.key === 'ArrowRight' ? 1 : -1), true);
    }
  });
  setInterval(() => {
    const now = performance.now(), delta = Math.min(now - last, 250); last = now;
    const bounds = root.getBoundingClientRect();
    if (paused || document.hidden || dialog.open || root.matches(':hover') || root.contains(document.activeElement) || bounds.top >= innerHeight || bounds.bottom <= 0) return;
    elapsed += delta;
    timeline.style.width = `${Math.min(100, elapsed / 6500 * 100)}%`;
    if (elapsed >= 6500) select(active + 1, true);
  }, 100);
  featureLink.addEventListener('click', event => {
    if (event.ctrlKey || event.metaKey || event.shiftKey || !dialog.showModal) return;
    event.preventDefault(); returnFocus = document.activeElement; modalContent(); dialog.showModal(); document.body.style.overflow = 'hidden';
  });
  root.querySelector('[data-gallery-close]').onclick = () => dialog.close();
  root.querySelector('[data-modal-prev]').onclick = () => select(active - 1, true);
  root.querySelector('[data-modal-next]').onclick = () => select(active + 1, true);
  dialog.addEventListener('click', event => { if (event.target === dialog) dialog.close(); });
  dialog.addEventListener('close', () => { document.body.style.overflow = ''; if (returnFocus) returnFocus.focus({preventScroll:true}); });
  let touchStart;
  featureLink.addEventListener('touchstart', event => { touchStart = event.changedTouches[0].clientX; }, {passive:true});
  featureLink.addEventListener('touchend', event => {
    const distance = event.changedTouches[0].clientX - touchStart;
    if (Math.abs(distance) > 50) { select(active + (distance < 0 ? 1 : -1), true); }
  }, {passive:true});
})();
