# Stat Mania — Courses

Course material for [www.statmania.info/courses/](https://www.statmania.info/courses/).

| Folder | What it is |
| :--- | :--- |
| `index.html` | The course hub page (hand-maintained; see below) |
| `rprogramming/` | Interactive R course: a Quarto website with live WebR code blocks and quizzes. Reference implementation for new courses |
| `clang/` | C code samples |
| `structured-programming-language/` | Syllabus notes |
| `css/` | Shared dark-theme CSS |
| `firebase-progress-plan.md` | Notes on adding login and progress tracking (not implemented) |
| `CLAUDE.md` | Conventions for adding or editing a course |

## This repo depends on the main site repo

This repo is **not standalone**. It is served by GitHub Pages under the same user and custom domain as the main site repo, [statmania/statmania.github.io](https://github.com/statmania/statmania.github.io) (checked out locally as `smroot`), so `/courses/` resolves to this repo. Do not add a `CNAME` here.

The pages reach into the main site with relative paths:

- `../styles.css`, `../site_libs/`, `../starfield.js`, `../assets/`, `../img/` and the site navbar links from `index.html`
- `../../starfield-include.html`, `../../img/` and `../../index.html` from each course project, such as `rprogramming/`

Opened from this repo alone, the pages look unstyled. To work on them locally, clone this repo next to `smroot` and symlink it into the main site:

```
cd smroot
ln -s ../courses courses      # gitignored in smroot
python3 -m http.server        # then open http://localhost:8000/courses/
```

**Quizzes.** Each course may include `<slug>/<slug>_question_bank.tex`. The main site's `question/build_quiz.py` (using `question/discover_quiz_banks.py`) reads these files through the symlink and builds `question/stat-prob.html` in the main site repo. After changing a bank, re-run it there:

```
cd smroot/question && python3 build_quiz.py
```

**Hub page.** `index.html` was originally rendered from the main site's `raw/` project and is now edited by hand. When the main navbar or footer changes, update the copies in `index.html` to match.

**Sitemaps.** `sitemap.xml` (hub) and `rprogramming/sitemap.xml` are listed in the main site's `robots.txt`.
