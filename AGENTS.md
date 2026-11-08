# AGENTS.md

Guidance for AI coding agents (Codex, Claude Code, etc.) working in this repository.

## Project status

`sublime-jekyll` is a Sublime Text package for Jekyll sites. It is in **maintenance mode**: bug fixes and compatibility
updates only, no new features. Keep changes small and scoped to the reported problem.

## Layout

- `jekyll.py` — all Sublime commands. Imports `sublime` / `sublime_plugin`, so it only runs inside Sublime Text.
- `jekyll_utils.py` — pure helpers (paths, titles, escaping, dates). Must **not** import `sublime`; this is what the tests cover.
- `tests/` — pytest suite for `jekyll_utils.py` plus a check that every menu/palette entry maps to a real command.
- `*.sublime-commands`, `*.sublime-menu`, `*.sublime-keymap`, `Jekyll.sublime-settings` — command wiring and default settings.
- `messages/`, `messages.json`, `CHANGELOG` — release notes shown by Package Control.
- `docs/` — Sphinx documentation.

## Requirements and compatibility

- Sublime Text 4 build 4083+ only. `.python-version` (`3.8`) opts into the modern plugin host, which runs Python 3.8 on
  older ST4 builds and 3.14 on build 4215+.
- Code must run on **Python 3.8 through 3.14**: no `match`, no `X | Y` types, no `list[str]`-style generics at runtime,
  no `str.removeprefix`.
- Command names (`jekyll_*`) and setting keys (`jekyll_*`) are public API. Do not rename them.

## Checks

Use a local venv (`.venv` is gitignored):

```bash
uv venv .venv --python 3.13 && uv pip install --python .venv "pytest>=7" "ruff>=0.17,<0.18" "black>=26,<27"
.venv/bin/pytest -q
.venv/bin/ruff check .
.venv/bin/black --check .
.venv/bin/python -W error -m py_compile jekyll.py jekyll_utils.py
ty check            # optional, configured in pyproject.toml (not run in CI)
```

If `docs/` changed, build the docs strictly (CI does this too):

```bash
uv venv .venv-docs --python 3.12 && uv pip install --python .venv-docs -r docs/requirements.txt
.venv-docs/bin/sphinx-build -W --keep-going -b html docs /tmp/sublime-jekyll-docs
```

CI (`.github/workflows/ci.yml`) runs the tests, ruff and the compile check on Python 3.8, 3.13 and 3.14, black on 3.14,
and the strict docs build. Contributor-facing instructions live in `.github/CONTRIBUTING.md`; keep the two in sync.

ty and Pyright resolve `sublime` from the Sublime Text app bundle (`Lib/python314` on macOS, build 4215). If Sublime
updates and that folder changes, update `pyproject.toml` and `pyrightconfig.json`.

## Testing in Sublime Text

Automated tests cannot exercise `jekyll.py`. To test for real, symlink the repo into Sublime's packages folder as
`Jekyll` (the folder name matters):

```bash
ln -s "$PWD" ~/Library/Application\ Support/Sublime\ Text/Packages/Jekyll
```

Use disposable copies of a Jekyll site for delete/promote tests. Say clearly which results came from real Sublime and
which came from mocks or unit tests. The reusable release checklist is `tests/manual-release-checklist.md`; keep it
blank and record results elsewhere.

## Sublime Text gotchas learned the hard way

- In an empty window, `window.active_view()` still returns a hidden placeholder view. Writing to it creates a new
  document. Only treat a view as usable if it is in `window.views()`.
- `${project_path}` is the folder containing the `.sublime-project` file, not the sidebar folder. `${folder}` is the
  first sidebar folder.
- Read settings through `get_setting(window, ...)`, which checks `window.project_data()` first and never needs a view.
- `is_enabled` / `is_visible` run every time a menu or the palette opens: keep them cheap, with no disk walks,
  directory creation or dialogs.
- Text inserted with `insert_snippet` must go through `escape_snippet` (`$`, `}`, `\`). Titles in front matter go through
  `yaml_quote`.
- `send2trash` comes from Sublime's own Default package (`from Default.send2trash import send2trash`); there is no
  bundled copy.
- New development-only files must be added to `.gitattributes` with `export-ignore` so they don't ship in the package.

## Git

- Don't push, tag, publish, or post to GitHub issues without the maintainer's explicit go-ahead.
- Don't add AI attribution lines (`Co-Authored-By`, "Generated with …") to commits or PRs.
- Record user-facing fixes in `CHANGELOG` under the current version.
