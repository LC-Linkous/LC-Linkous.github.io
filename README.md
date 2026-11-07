# LC-Linkous.github.io

## Description
This repo is a semi-migration from a previous project blog, but not intended to be a full blog. Instead, it is being used to host several tutorials for projects shared on GitHub that have additional hardware or physical components. Academic research and project highlights are also included. 


View the main page here: https://lc-linkous.github.io/

## Layout notes
* `_layouts/default.html` – site chrome (header, nav, sidebar). Pages set `title:` and `nav:` (home, projects, tools, posts, publications, bookshelf, about) in front matter; `nav` controls the highlighted menu item.
* `_layouts/page.html` – wraps markdown pages (`tools.md`, `projects.md`, `about.md`) in the same article structure as the HTML pages. Set `title:`, `nav:` and `permalink:` in front matter; no H1 in the body.
* `_layouts/post.html` – wraps posts in `_posts/`. Posts are highlighted under Posts automatically.
* `_layouts/tags.html` – renders `_tags/<tag>.md` as an archive of posts whose `tags:` list contains `tag-name`. Add a new tag by adding a `_tags/<tag>.md` stub with `tag-name: <tag>`.
* `README.md` is excluded from the build (see `exclude:` in `_config.yml`).

## Data files
* `_data/publications.yml`, `_data/news.yml` – source for the Publications page and the home page's "Latest paper" / "Latest news" cards. Newest first within each type; `date` (YYYY-MM-01 for month precision) decides what is "latest".
* `_data/featured.yml` – the hand-picked "Featured project" and "Featured tool" cards on the home page.
* `_data/stats.yml` – GitHub and PyPI numbers for the home page, written nightly by the stats workflow; do not edit by hand.

## Adding things
* **Page:** add `name.md` at the root with front matter `layout: page`, `title:`, `nav:` and `permalink: /name/`; add a nav entry in `_layouts/default.html` if it should appear in the menu.
* **Post:** add `_posts/<group>/YYYY-MM-DD-slug.md` with `layout: post`, `title:`, `summary:` and `tags: [a, b]`. Posts sort by the date in the filename.
* **Tag:** add `_tags/<tag>.md` containing `layout: tags` and `tag-name: <tag>`. A tag used on a post without a stub is shown as plain text, not a link, until the stub exists.


## References


General examples for using Jekyll on Github:
* https://github.com/javasteve99/jekyll-content-modeling-example
* https://github.com/pages-themes/minimal 


Tagging examples:
* https://www.untangled.dev/2020/06/02/tag-management-jekyll/
* https://www.smashingmagazine.com/2016/02/content-modeling-with-jekyll/
