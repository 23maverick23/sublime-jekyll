"""Sublime-independent helpers for Jekyll 4."""

import json
import os
import re
from urllib.parse import quote
from datetime import datetime


SKIP_DIRS = {'node_modules', '_site', 'vendor', '.jekyll-cache', '.sass-cache', 'bower_components'}
MARKDOWN_EXTENSIONS = ('markdown', 'mdown', 'mkdn', 'mkd', 'md')


def clean_title_input(title, draft=False):
    slug = re.sub(r'[^\w -]', '', title.lower())
    slug = re.sub(r'[ _-]+', '-', slug).strip('-')
    if not slug or draft:
        return slug
    return datetime.today().strftime('%Y-%m-%d-') + slug


def is_image(path):
    return os.path.splitext(path)[1].lower() in {
        '.png', '.jpg', '.jpeg', '.gif', '.webp', '.svg', '.avif', '.bmp', '.ico',
        '.tif', '.tiff', '.pbm', '.pgm', '.ppm', '.xbm', '.ras', '.rgb', '.exr',
    }


def escape_snippet(text):
    return text.replace('\\', '\\\\').replace('$', '\\$').replace('}', '\\}')


def yaml_quote(text):
    # JSON strings are valid YAML double-quoted scalars, including control escapes.
    return json.dumps(text, ensure_ascii=False)


def file_extension(markup, md_ext):
    if markup in ('Textile', 'HTML', 'Plain text'):
        return {'Textile': '.textile', 'HTML': '.html', 'Plain text': '.txt'}[markup]
    extension = md_ext if isinstance(md_ext, str) else ''
    if extension.startswith('.'):
        extension = extension[1:]
    return '.' + (extension if extension in MARKDOWN_EXTENSIONS else 'markdown')


def _searchable(name):
    return not name.startswith('.') and name not in SKIP_DIRS


def find_site_roots(folders):
    """Check each folder and its immediate children for a Jekyll config."""
    roots = []
    for folder in folders:
        if not os.path.isdir(folder):
            continue
        candidates = [os.path.abspath(folder)]
        with os.scandir(folder) as entries:
            candidates.extend(sorted(entry.path for entry in entries
                                     if _searchable(entry.name) and entry.is_dir(follow_symlinks=False)))
        for candidate in candidates:
            if any(os.path.isfile(os.path.join(candidate, name)) for name in ('_config.yml', '_config.yaml')):
                candidate = os.path.abspath(candidate)
                if candidate not in roots:
                    roots.append(candidate)
    return roots


def bounded_find_dirs(folders, dir_name, max_depth=4):
    """Find matching directories at depths 0 through max_depth, without following links."""
    found = []

    def walk_error(error):
        raise error

    for folder in folders:
        folder = os.path.abspath(folder)
        for root, dirs, _files in os.walk(folder, onerror=walk_error):
            relative = os.path.relpath(root, folder)
            depth = 0 if relative == '.' else len(relative.split(os.sep))
            dirs[:] = sorted(name for name in dirs if _searchable(name)) if depth < max_depth else []
            if os.path.basename(root) == dir_name and root not in found:
                found.append(root)
    return found


def extract_frontmatter_date(text):
    """Return a valid leading ISO date from front matter, or None."""
    lines = text.lstrip('\ufeff').splitlines()
    if not lines or lines[0].strip() != '---':
        return None
    end = next((i for i in range(1, len(lines)) if lines[i].strip() == '---'), None)
    if end is None:
        return None
    for line in lines[1:end]:
        match = re.match(r'''^date:\s*["']?(\d{4}-\d{2}-\d{2})(?=$|[\sT"'])''', line)
        if match:
            value = match.group(1)
            try:
                datetime.strptime(value, '%Y-%m-%d')
            except ValueError:
                return None
            return value
    return None


def promote_destination(draft_path, drafts_dir, posts_dir, date):
    relative = os.path.relpath(draft_path, drafts_dir)
    directory, name = os.path.split(relative)
    name = re.sub(r'^\d{4}-\d{2}-\d{2}-', '', name)
    return os.path.join(posts_dir, directory, date + '-' + name)


def resolve_relative(path, base):
    path = os.path.expanduser(path)
    if not os.path.isabs(path):
        if not base:
            raise ValueError('A relative path needs an open folder or a saved project.')
        path = os.path.join(base, path)
    return os.path.abspath(path)



def markdown_label(text):
    """Escape characters that would end or break a Markdown link label."""
    return re.sub(r'([\\\[\]])', r'\\\1', text)


def url_path(path):
    """Percent-encode a relative URL path, keeping '/' separators."""
    return quote(path, safe='/-._~')
