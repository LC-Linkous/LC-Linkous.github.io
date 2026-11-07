# LC-Linkous.github.io

## Description
This repo is a semi-migration from a previous project blog, but not intended to be a full blog. Instead, it is being used to host several tutorials for projects shared on GitHub that have additional hardware or physical components. Academic research and project highlights are also included. 


View the main page here: https://lc-linkous.github.io/

## Layout notes
* `_layouts/default.html` – site chrome (header, nav, sidebar). Pages set `title:` and `nav:` (home, projects, tools, posts, publications, bookshelf, about) in front matter; `nav` controls the highlighted menu item.
* `_layouts/page.html` – wraps markdown pages (`tools.md`, `projects.md`, `about.md`) in the same article structure as the HTML pages. Set `title:`, `nav:` and `permalink:` in front matter; no H1 in the body.
* `_layouts/post.html` – wraps posts in `_posts/`. Posts are highlighted under Posts automatically.
* `_layouts/tags.html` – renders `_tags/<tag>.md` as an archive of posts whose `tags:` list contains `tag-name`. Add a new tag by adding a `_tags/<tag>.md` stub with `tag-name: <tag>`.
* `templates/` and `README.md` are excluded from the build (see `exclude:` in `_config.yml`).


## References


General examples for using Jekyll on Github:
* https://github.com/javasteve99/jekyll-content-modeling-example
* https://github.com/pages-themes/minimal 


Tagging examples:
* https://www.untangled.dev/2020/06/02/tag-management-jekyll/
* https://www.smashingmagazine.com/2016/02/content-modeling-with-jekyll/
