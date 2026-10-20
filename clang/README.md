# C Programming (Stat Mania course)

A Quarto course served at `www.statmania.info/courses/clang/`. Lessons are adapted from the
`c-*` blog posts in `smroot/blograw/posts/`.

## Built from the course kit

This course is a copy of the template in the sibling repo
[`course-kit`](https://github.com/statmania/course-kit) (locally `../../course-kit`).
Files are split by owner so that template updates can be re-imported without clobbering the course:

| Owner | Files | Rule |
| :--- | :--- | :--- |
| **Kit** | `theme/`, `scripts/`, `img/`, `.gitignore`, `.nojekyll` | Never edit here; overwritten on update |
| **Course** | `_quarto.yml`, `index.qmd`, `modules/`, `media/`, `courses.yml`, `extra.scss`, `extra.html`, `tools/`, `code/` | Yours to edit |
| **Generated** | `_generated/`, `*.html`, `site_libs/`, `search.json`, `sitemap.xml`, `robots.txt` | Rewritten by `quarto render` |

`.kit-version` records the kit commit this course was last synced with.

**Feature requests go into the kit first.** Change the kit (`theme/`, `scripts/`), then import it
here with `tools/update-kit.sh`. Editing kit-owned files in this course is lost on the next update.
Course-only tweaks belong in `extra.scss` / `extra.html`.

## Updating when the kit changes

```bash
tools/update-kit.sh --pull   # git pull the kit, then copy its files in
quarto render
```

(Omit `--pull` to sync from whatever is already checked out in `../../course-kit`; set
`KIT=/path/to/course-kit` if it lives elsewhere.)

The script prints the kit commits since the last sync, then diffs the `project:` and `format:`
blocks of the kit's `_quarto.yml` against this course's. Those blocks live in the course-owned
`_quarto.yml`, so **merge any template changes there by hand**. The only expected differences are
`extra.scss` in the theme list and `extra.html` in `include-after-body`. Commit the result.

## Working on the course

```bash
python3 scripts/build.py   # first time only (generates _generated/)
quarto preview
```

- The sidebar in `_quarto.yml` is the table of contents (module → lesson); the home page and
  module pages are generated from it and from each lesson's front matter.
- Run `quarto render` before committing: the built site is committed and served as-is.
- `courses.yml` is a stub only because the kit's `build.py` requires it; "All Courses" links to the hub page.
- `tools/import_posts.py` was the one-off importer from the blog. Re-running it overwrites the lessons.

## Progress tracking

Progress, checkmarks and notes are saved **in the learner's browser only** (localStorage): no
account, no server. They do not follow the learner to another browser or device, and clearing
site data erases them.
