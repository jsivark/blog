(() => {
  const buttons = Array.from(document.querySelectorAll("[data-filter]"));
  const status = document.querySelector("#filter-status");
  const valid = new Set(["technical", "notes"]);

  const posts = () =>
    Array.from(document.querySelectorAll(".quarto-listing .quarto-post"));

  if (!buttons.length) return;

  const kindOf = (post) => {
    const cats = Array.from(post.querySelectorAll(".listing-category"))
      .map((el) => el.textContent.trim().toLowerCase());
    if (cats.includes("notes")) return "notes";
    if (cats.includes("technical")) return "technical";
    return "technical";
  };

  const filterFromHash = () => {
    const value = window.location.hash.slice(1).toLowerCase();
    return valid.has(value) ? value : "technical";
  };

  const applyFilter = (filter, updateUrl = false) => {
    buttons.forEach((button) => {
      button.setAttribute("aria-pressed", String(button.dataset.filter === filter));
    });

    const items = posts();
    const visible = items.filter((post) => kindOf(post) === filter);

    items.forEach((post) => {
      post.hidden = !visible.includes(post);
    });

    visible.forEach((post, index) => {
      post.dataset.side = index % 2 === 0 ? "left" : "right";
    });

    if (status) {
      status.textContent = `${visible.length} ${filter} ${
        visible.length === 1 ? "post" : "posts"
      }`;
    }

    if (updateUrl) {
      history.replaceState(null, "", `#${filter}`);
    }
  };

  buttons.forEach((button) => {
    button.addEventListener("click", () => applyFilter(button.dataset.filter, true));
  });

  window.addEventListener("hashchange", () => applyFilter(filterFromHash()));

  const start = () => applyFilter(filterFromHash());
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", start);
  } else {
    start();
  }
  window.addEventListener("load", () => applyFilter(filterFromHash()));
})();
