# Posts Instructions

This file is for authoring guidance and directory conventions for OpenETR posts.

## Purpose

The `docs/posts` directory is for long-form OpenETR articles that live in the repository and can be rendered through GitHub Pages.

## Suggested workflow

- Add one Markdown file per article in `docs/posts/`.
- Give each post a short slug such as `portable-control.md`.
- Add a short front matter block so Jekyll can render it nicely.
- Add the post to the published list in `index.md` when it is ready.

## Suggested post front matter

```yaml
---
title: Your Post Title
eyebrow: Essay
description: One-sentence summary of the article.
---
```

## Files

- `index.md` is the Jekyll-rendered posts landing page.
- `index.html` is the explicit GitHub Pages entry file for the posts directory.
- `REPO_INDEX.md` is the repository-oriented reference page.
- `post-template.md` is a starter file for new posts.

## Notes

- Content in `docs/posts` is part of the repository and can be linked from the landing page.
- It is not part of the Python package install payload because it is outside the `openetr/` package and is not listed in Poetry package includes.
