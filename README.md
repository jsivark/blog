# Random Notes

Personal technical blog — [jsivark.github.io/blog](https://jsivark.github.io/blog/)

Built with **Quarto** (reading-first, Tufte-inspired layout).

## Write a post

```bash
cp -R templates/post posts/YYYY-MM-DD-slug
```

Edit `posts/YYYY-MM-DD-slug/index.qmd`:

- Set title, description, date; remove `draft: true`
- Math: `$inline$` or `$$display$$`
- Sidenote: `^[appears in the margin]`
- Longer margin note: `::: {.column-margin} ... :::`
- Image: `![alt](figure.png)`
- Manim / viz: render offline → drop `png`/`mp4` in the post folder → embed (see template)

Preview, then push — GitHub Actions publishes.

## Local preview

```bash
export PATH="$HOME/workspace/.tools/quarto/bin:$PATH"   # local install path on this machine
cd ~/workspace/github.com/blog
quarto preview
```

Or install Quarto from <https://quarto.org/docs/get-started/>.

## Deploy

Pushes to `master`/`main` run `.github/workflows/publish.yml`.

On GitHub once: **Settings → Pages → Source: GitHub Actions**.
