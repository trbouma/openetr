"""Publish repository documentation without maintaining a second source copy."""

import posixpath
import re
from pathlib import Path
from urllib.parse import unquote, urlsplit

from mkdocs.structure.files import File, InclusionLevel

ROOT = Path(__file__).resolve().parents[1]
DOCS_URL = "https://github.com/trbouma/openetr/blob/main/"


def on_config(config):
    def localize(items):
        if isinstance(items, list):
            return [localize(item) for item in items]
        if isinstance(items, dict):
            return {key: localize(value) for key, value in items.items()}
        if isinstance(items, str) and items.startswith(DOCS_URL + "docs/"):
            return items[len(DOCS_URL):]
        return items

    config.nav = localize(config.nav)
    return config


def on_files(files, config):
    for path in sorted((ROOT / "docs").rglob("*")):
        if (path.is_file() and path.relative_to(ROOT / "docs").parts[0] in {"specs", "images", "source"}
                and not any(part.startswith(".") for part in path.relative_to(ROOT).parts)):
            files.append(File(
                path.relative_to(ROOT).as_posix(), str(ROOT), config.site_dir,
                config.use_directory_urls, inclusion=InclusionLevel.NOT_IN_NAV,
            ))
    return files


def on_page_markdown(markdown, page, config, files):
    directory = posixpath.dirname(page.file.src_uri)
    if page.file.src_uri.startswith("docs/"):
        # Repository-relative links to the curated site lose its source-directory prefix.
        markdown = re.sub(r"(?<=\]\()\.\./\.\./docs-site/", "../../", markdown)
        page.edit_url = config.repo_url.rstrip("/") + "/edit/main/" + page.file.src_uri
    def replace(match):
        target = match.group(0)[len(DOCS_URL):]
        parsed = urlsplit(target)
        if files.get_file_from_path(unquote(parsed.path)) is None:
            return match.group(0)
        relative = posixpath.relpath(unquote(parsed.path), directory or ".")
        return relative + ("#" + parsed.fragment if parsed.fragment else "")

    return re.sub(re.escape(DOCS_URL) + r"docs/[^\s)\]>\"']+", replace, markdown)


def on_serve(server, config, builder):
    server.watch(str(ROOT / "docs"))
    return server
