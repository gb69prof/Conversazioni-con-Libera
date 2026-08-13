(() => {
  const root = document.documentElement;
  const savedTheme = localStorage.getItem('libera-theme');
  if (savedTheme) root.dataset.theme = savedTheme;

  document.querySelectorAll('[data-theme-toggle]').forEach((button) => {
    button.addEventListener('click', () => {
      const next = root.dataset.theme === 'dark' ? 'light' : 'dark';
      root.dataset.theme = next;
      localStorage.setItem('libera-theme', next);
    });
  });

  const grid = document.querySelector('[data-archive-grid]');
  if (grid) {
    const search = document.querySelector('[data-search-input]');
    const year = document.querySelector('[data-year-filter]');
    const topic = document.querySelector('[data-topic-filter]');
    const sort = document.querySelector('[data-sort]');
    const count = document.querySelector('[data-result-count]');
    const empty = document.querySelector('[data-empty]');
    const cards = Array.from(grid.querySelectorAll('[data-card]'));

    const update = () => {
      const query = search.value.trim().toLocaleLowerCase('it');
      let visible = 0;
      cards.forEach((card) => {
        const matches = (!query || card.dataset.search.includes(query)) &&
          (!year.value || card.dataset.year === year.value) &&
          (!topic.value || card.dataset.topic.split(' ').includes(topic.value));
        card.hidden = !matches;
        if (matches) visible += 1;
      });
      const ordered = [...cards].sort((a, b) => {
        if (sort.value === 'az') return a.dataset.title.localeCompare(b.dataset.title, 'it');
        return sort.value === 'oldest'
          ? a.dataset.date.localeCompare(b.dataset.date)
          : b.dataset.date.localeCompare(a.dataset.date);
      });
      ordered.forEach((card) => grid.appendChild(card));
      count.textContent = String(visible);
      empty.hidden = visible !== 0;
    };

    [search, year, topic, sort].forEach((control) => control.addEventListener('input', update));
    document.querySelector('[data-reset]')?.addEventListener('click', () => {
      search.value = ''; year.value = ''; topic.value = ''; sort.value = 'newest'; update(); search.focus();
    });
  }

  const progress = document.querySelector('[data-reading-progress]');
  if (progress) {
    const updateProgress = () => {
      const max = document.documentElement.scrollHeight - innerHeight;
      progress.style.width = `${max > 0 ? (scrollY / max) * 100 : 0}%`;
    };
    addEventListener('scroll', updateProgress, { passive: true });
    updateProgress();
  }

  const readingText = document.querySelector('[data-reading-text]');
  if (readingText) {
    let size = Number(localStorage.getItem('libera-reading-size') || 1.08);
    const setSize = () => root.style.setProperty('--reading-size', `${size}rem`);
    setSize();
    document.querySelectorAll('[data-font]').forEach((button) => button.addEventListener('click', () => {
      size = Math.max(.92, Math.min(1.38, size + (button.dataset.font === 'up' ? .08 : -.08)));
      localStorage.setItem('libera-reading-size', size.toFixed(2)); setSize();
    }));
    document.querySelector('[data-print]')?.addEventListener('click', () => print());
    document.querySelector('[data-copy-link]')?.addEventListener('click', async () => {
      await navigator.clipboard.writeText(location.href);
      const toast = document.createElement('div'); toast.className = 'toast'; toast.textContent = 'Link copiato'; document.body.appendChild(toast);
      setTimeout(() => toast.remove(), 1800);
    });
  }
})();
