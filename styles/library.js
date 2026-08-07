(() => {
  const data = window.LIBRARY;
  if (!data || !Array.isArray(data.books)) return;

  const clamp = (n, lo, hi) => Math.max(lo, Math.min(hi, n));

  function progress(book) {
    const pages = Math.max(1, Number(book.pages) || 1);
    const page = clamp(Number(book.page) || 0, 0, pages);
    const pct = Math.round((page / pages) * 100);
    const done = page >= pages;
    return { page, pages, pct, done };
  }

  function labelCategory(cat) {
    if (!cat) return "Other";
    return cat.charAt(0).toUpperCase() + cat.slice(1);
  }

  function escapeHtml(s) {
    return String(s)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  /** Home: currently reading only, with progress bars. */
  function readingCard(book) {
    const { page, pages, pct } = progress(book);
    return `
      <article class="lib-book is-compact">
        <div class="lib-book-top">
          <div class="lib-book-text">
            <strong class="lib-title">${escapeHtml(book.title)}</strong>
          </div>
          <span class="lib-cat">${escapeHtml(labelCategory(book.category))}</span>
        </div>
        <div class="lib-bar" role="progressbar" aria-valuemin="0" aria-valuemax="100" aria-valuenow="${pct}" aria-label="${escapeHtml(book.title)} progress">
          <span class="lib-bar-fill" style="width:${pct}%"></span>
        </div>
        <div class="lib-book-foot">
          <span class="lib-meta">p.&nbsp;${page}&nbsp;/&nbsp;${pages}</span>
          <span class="lib-pct">${pct}%</span>
        </div>
      </article>
    `;
  }

  /** Library: finished books only — no bars. */
  function finishedCard(book) {
    const author = book.author
      ? `<span class="lib-author">${escapeHtml(book.author)}</span>`
      : "";
    return `
      <article class="lib-book is-finished">
        <div class="lib-book-top">
          <div class="lib-book-text">
            <strong class="lib-title">${escapeHtml(book.title)}</strong>
            ${author}
          </div>
        </div>
      </article>
    `;
  }

  function renderHome(el) {
    const reading = data.books.filter((b) => !progress(b).done);
    if (!reading.length) {
      el.hidden = true;
      el.innerHTML = "";
      return;
    }
    el.hidden = false;
    el.innerHTML = `
      <p class="lib-eyebrow">Currently reading</p>
      <div class="lib-stack">
        ${reading.map(readingCard).join("")}
      </div>
    `;
  }

  function renderLibrary(el) {
    const doneByCat = new Map();

    for (const book of data.books) {
      if (!progress(book).done) continue;
      const key = book.category || "other";
      if (!doneByCat.has(key)) doneByCat.set(key, []);
      doneByCat.get(key).push(book);
    }

    const cats = [...doneByCat.keys()].sort((a, b) => a.localeCompare(b));
    if (!cats.length) {
      el.innerHTML = "";
      return;
    }

    el.innerHTML = cats
      .map((cat) => {
        const items = doneByCat.get(cat);
        return `
          <section class="lib-cat-group">
            <h3>${escapeHtml(labelCategory(cat))}</h3>
            <div class="lib-stack">
              ${items.map(finishedCard).join("")}
            </div>
          </section>
        `;
      })
      .join("");
  }

  const home = document.getElementById("library-home");
  if (home) renderHome(home);

  const page = document.getElementById("library-page");
  if (page) renderLibrary(page);
})();
