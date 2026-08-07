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
```

Then sync (CI does this on publish too):

```bash
pip install pyyaml   # once
python3 scripts/sync_library.py
```

Progress is `page / pages`. Home shows currently-reading bars. At 100% a book leaves the home strip and appears on **Library** under its category.

## Preview

```bash
export PATH="$HOME/workspace/.tools/quarto/bin:$PATH"
cd ~/workspace/github.com/blog
python3 scripts/sync_library.py
quarto preview
```

Push to `master` to publish.
