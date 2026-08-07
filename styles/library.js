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

  function bookRow(book, { compact = false } = {}) {
    const { page, pages, pct, done } = progress(book);
    const author = book.author
      ? `<span class="lib-author">${escapeHtml(book.author)}</span>`
      : "";
    const meta = done
      ? `<span class="lib-meta">Finished</span>`
      : `<span class="lib-meta">p.&nbsp;${page}&nbsp;/&nbsp;${pages}</span>`;

    return `
      <article class="lib-book${compact ? " is-compact" : ""}${done ? " is-done" : ""}">
        <div class="lib-book-top">
          <div class="lib-book-text">
            <strong class="lib-title">${escapeHtml(book.title)}</strong>
            ${author}
          </div>
          <span class="lib-cat">${escapeHtml(labelCategory(book.category))}</span>
        </div>
        <div class="lib-bar" role="progressbar" aria-valuemin="0" aria-valuemax="100" aria-valuenow="${pct}" aria-label="${escapeHtml(book.title)} progress">
          <span class="lib-bar-fill" style="width:${pct}%"></span>
        </div>
        <div class="lib-book-foot">
          ${meta}
          <span class="lib-pct">${pct}%</span>
        </div>
      </article>
    `;
  }

  function escapeHtml(s) {
    return String(s)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  function renderHome(el) {
    const reading = data.books.filter((b) => !progress(b).done);
    if (!reading.length) {
      el.hidden = true;
      return;
    }
    el.hidden = false;
    el.innerHTML = `
      <p class="lib-eyebrow">Currently reading</p>
      <div class="lib-stack">
        ${reading.map((b) => bookRow(b, { compact: true })).join("")}
      </div>
      <p class="lib-more"><a href="library.html">Library</a></p>
    `;
  }

  function renderLibrary(el) {
    const reading = [];
    const doneByCat = new Map();

    for (const book of data.books) {
      if (progress(book).done) {
        const key = book.category || "other";
        if (!doneByCat.has(key)) doneByCat.set(key, []);
        doneByCat.get(key).push(book);
      } else {
        reading.push(book);
      }
    }

    const readingHtml = reading.length
      ? `<div class="lib-stack">${reading.map((b) => bookRow(b)).join("")}</div>`
      : `<p class="lib-empty">Nothing in progress.</p>`;

    const cats = [...doneByCat.keys()].sort((a, b) => a.localeCompare(b));
    let readHtml;
    if (!cats.length) {
      readHtml = `<p class="lib-empty">Finished books will land here by category.</p>`;
    } else {
      readHtml = cats
        .map((cat) => {
          const items = doneByCat.get(cat);
          return `
            <section class="lib-cat-group">
              <h3>${escapeHtml(labelCategory(cat))}</h3>
              <div class="lib-stack">
                ${items.map((b) => bookRow(b)).join("")}
              </div>
            </section>
          `;
        })
        .join("");
    }

    el.innerHTML = `
      <section class="lib-section">
        <h2>Currently reading</h2>
        ${readingHtml}
      </section>
      <section class="lib-section">
        <h2>Read</h2>
        ${readHtml}
      </section>
      <p class="lib-hint">Update <code>data/library.yml</code> — set <code>page</code> and <code>pages</code>; at 100% a book moves into Read.</p>
    `;
  }

  const home = document.getElementById("library-home");
  if (home) renderHome(home);

  const page = document.getElementById("library-page");
  if (page) renderLibrary(page);
})();
