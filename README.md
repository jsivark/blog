# Random Notes

[jsivark.github.io/blog](https://jsivark.github.io/blog/) — Quarto site.

## New post

```bash
cp -R templates/post posts/YYYY-MM-DD-slug
```

Edit `posts/YYYY-MM-DD-slug/index.qmd`: set title / date, set `categories: [technical]`, `[notes]`, or `[personal]`, remove `draft: true`.

Useful bits:

- Math: `$inline$` or `$$display$$`
- Sidenote: `^[margin note]`
- Margin block: `::: {.column-margin} ... :::`
- Image: `![alt](figure.png)`
- Video: drop an `mp4` next to the post and embed (see template)

## Projects page

Copy `templates/project.md` into `projects.qmd` (newest first). Each entry has title,
date/tags, tagline, blurb, and links. The TOC builds from the `###` headings.

## Library (currently reading)

Edit `data/library.yml`:

```yaml
- title: "Book title"
  author: "Author"
  category: systems   # any label you like
  page: 120           # where you are
  pages: 1120         # total in your edition
  added: 2026-07-15   # started / added
  # finished: 2026-08-07   # set when page >= pages
  quote: ""           # optional; shown on Home while reading, on Library when done
```

Then sync (CI does this on publish too):

```bash
pip install pyyaml   # once
python3 scripts/sync_library.py
# optional: python3 scripts/test_library.py
```

Progress is `page / pages`. Home shows currently-reading bars. A non-empty `quote` appears on Home while that book is in progress; at 100% set `finished:` — the book (and its quote) move to **Library**.

`sync_library.py` also writes cache-busted script tags (`?v=…`) so browsers pick up new page numbers after publish without a hard refresh.

## Preview

```bash
export PATH="$HOME/workspace/.tools/quarto/bin:$PATH"
cd ~/workspace/github.com/blog
python3 scripts/sync_library.py
quarto preview
```

Push to `master` to publish.
