import json
import os
from datetime import datetime

import pytest

from jekyll_utils import (
    bounded_find_dirs,
    clean_title_input,
    escape_snippet,
    extract_frontmatter_date,
    file_extension,
    find_site_roots,
    is_image,
    promote_destination,
    resolve_relative,
    yaml_quote,
)


@pytest.mark.parametrize(('title', 'slug'), [
    ('Hello, World!', 'hello-world'),
    ('Café 日本語', 'café-日本語'),
    ('  many__ spaces---here  ', 'many-spaces-here'),
    ('$}{!\\', ''),
    ('___ ---', ''),
    ('', ''),
])
def test_clean_title_input(title, slug):
    assert clean_title_input(title, draft=True) == slug
    before = datetime.today().strftime('%Y-%m-%d-')
    result = clean_title_input(title)
    after = datetime.today().strftime('%Y-%m-%d-')
    assert result in (before + slug, after + slug) if slug else result == ''


@pytest.mark.parametrize('extension', ['png', 'jpg', 'jpeg', 'gif', 'webp', 'svg', 'avif', 'bmp', 'ico', 'tif', 'tiff'])
def test_image_extensions(extension):
    assert is_image('missing/file.' + extension)
    assert is_image('file.' + extension.upper())


@pytest.mark.parametrize('path', ['image.png.txt', 'png', '/png/file', 'file.pdf', 'file'])
def test_not_image(path):
    assert not is_image(path)


def test_escape_snippet():
    assert escape_snippet('a\\b $1 ${title} }') == 'a\\\\b \\$1 \\${title\\} \\}'
    assert escape_snippet('Café: "title"') == 'Café: "title"'
    assert escape_snippet('') == ''


@pytest.mark.parametrize('title', ['A "quote": C:\\posts', 'Café 日本語', 'a\nb\tc', '', '${1:Hello}'])
def test_yaml_quote(title):
    quoted = yaml_quote(title)
    assert quoted.startswith('"') and quoted.endswith('"')
    assert json.loads(quoted) == title
    assert '\n' not in quoted


def test_yaml_quotes_and_backslashes():
    assert yaml_quote('"a": \\b') == '"\\"a\\": \\\\b"'


@pytest.mark.parametrize(('markup', 'extension', 'expected'), [
    ('Markdown', 'markdown', '.markdown'),
    ('Markdown', 'mdown', '.mdown'),
    ('Markdown', 'mkdn', '.mkdn'),
    ('Markdown', 'mkd', '.mkd'),
    ('Markdown', 'md', '.md'),
    ('Markdown', '.md', '.md'),
    ('Markdown', '..md', '.markdown'),
    ('Markdown', 'exe', '.markdown'),
    ('Markdown', '', '.markdown'),
    ('Markdown', None, '.markdown'),
    ('Unknown', 'md', '.md'),
    ('Textile', 'md', '.textile'),
    ('HTML', 'md', '.html'),
    ('Plain text', 'md', '.txt'),
])
def test_file_extension(markup, extension, expected):
    assert file_extension(markup, extension) == expected


def make_dir(root, relative):
    path = root / relative
    path.mkdir(parents=True, exist_ok=True)
    return path


def test_site_roots_at_folder_and_child_level(tmp_path):
    (tmp_path / '_config.yml').write_text('')
    child = make_dir(tmp_path, 'blog')
    (child / '_config.yaml').write_text('')
    grandchild = make_dir(child, 'nested')
    (grandchild / '_config.yml').write_text('')
    make_dir(tmp_path, 'not-a-site')
    assert find_site_roots([str(tmp_path)]) == [str(tmp_path), str(child)]
    assert find_site_roots([str(tmp_path), str(child)]) == [str(tmp_path), str(child), str(grandchild)]


def test_site_roots_missing_and_config_directory(tmp_path):
    make_dir(tmp_path, '_config.yml')
    assert find_site_roots([str(tmp_path / 'missing'), str(tmp_path)]) == []


@pytest.mark.parametrize('excluded', [
    'node_modules', '_site', 'vendor', '.jekyll-cache', '.sass-cache', 'bower_components', '.hidden'
])
def test_bounded_walk_skips_dirs(tmp_path, excluded):
    make_dir(tmp_path, excluded + '/_posts')
    wanted = make_dir(tmp_path, 'blog/_posts')
    assert bounded_find_dirs([str(tmp_path)], '_posts', 4) == [str(wanted)]


def test_bounded_walk_depth_and_deduplication(tmp_path):
    at_four = make_dir(tmp_path, 'a/b/c/_posts')
    make_dir(tmp_path, 'a/b/c/d/_posts')
    assert bounded_find_dirs([str(tmp_path)], '_posts', 3) == []
    assert bounded_find_dirs([str(tmp_path), str(tmp_path)], '_posts', 4) == [str(at_four)]
    assert bounded_find_dirs([str(at_four)], '_posts', 0) == [str(at_four)]


def test_walk_does_not_follow_symlinks(tmp_path):
    target = make_dir(tmp_path, 'vendor/blog/_posts')
    (tmp_path / 'linked').symlink_to(target.parent, target_is_directory=True)
    assert bounded_find_dirs([str(tmp_path)], '_posts', 4) == []
    (target.parent / '_config.yml').write_text('')
    assert find_site_roots([str(tmp_path)]) == []


@pytest.mark.parametrize(('text', 'expected'), [
    ('---\ndate: 2024-02-29\n---\nbody', '2024-02-29'),
    ('---\ndate: 2026-11-07 12:00:00 -0700\n---', '2026-11-07'),
    ('---\ndate: "2026-11-07T12:00:00Z"\n---', '2026-11-07'),
    ("---\ndate: '2026-11-07'\n---", '2026-11-07'),
    ('\ufeff---\r\ndate: 2026-11-07\r\n---', '2026-11-07'),
    ('---\ntitle: Example\n---\ndate: 2020-01-01', None),
    ('---\ndate: 2026-02-30\n---', None),
    ('---\ndate: tomorrow\n---', None),
    ('---\ndate: 2026-11-077\n---', None),
    ('---\ndate: 2026-11-07', None),
    ('date: 2026-11-07', None),
    ('---\nmetadata:\n  date: 2026-11-07\n---', None),
    ('', None),
])
def test_extract_frontmatter_date(text, expected):
    assert extract_frontmatter_date(text) == expected


@pytest.mark.parametrize(('relative', 'expected'), [
    ('title.md', '2026-11-07-title.md'),
    ('nested/title.txt', 'nested/2026-11-07-title.txt'),
    ('nested/deeper/2020-01-02-title.md', 'nested/deeper/2026-11-07-title.md'),
    ('title-2020-01-02.md', '2026-11-07-title-2020-01-02.md'),
])
def test_promote_destination(tmp_path, relative, expected):
    drafts = tmp_path / 'custom-drafts'
    posts = tmp_path / 'custom-posts'
    assert promote_destination(str(drafts / relative), str(drafts), str(posts), '2026-11-07') == str(posts / expected)


def test_resolve_relative(tmp_path):
    assert resolve_relative('posts/../_posts', str(tmp_path)) == str(tmp_path / '_posts')
    assert resolve_relative(str(tmp_path / '_posts'), None) == str(tmp_path / '_posts')
    assert resolve_relative('~/blog', None) == os.path.join(os.path.expanduser('~'), 'blog')
    with pytest.raises(ValueError, match='relative path'):
        resolve_relative('_posts', None)


def test_markdown_label_escapes_brackets_and_backslash():
    from jekyll_utils import markdown_label
    assert markdown_label('a]b[c\\d') == 'a\\]b\\[c\\\\d'
    assert markdown_label('plain name') == 'plain name'


def test_url_path_percent_encodes_but_keeps_slashes():
    from jekyll_utils import url_path
    assert url_path('uploads/photo 1#2.png') == 'uploads/photo%201%232.png'
    assert url_path('uploads/2026/ok-file_v1.png') == 'uploads/2026/ok-file_v1.png'
    assert url_path('uploads/caf\u00e9.png') == 'uploads/caf%C3%A9.png'
