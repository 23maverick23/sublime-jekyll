Contributing
============

Thanks for helping keep sublime-jekyll working.

## Maintenance mode

This package is in **maintenance mode**. Pull requests are welcome for:

- bug fixes, and
- compatibility work for current Sublime Text 4 builds and plugin-host Python versions.

New features are not planned, and feature PRs will usually be closed. Bug-fix PRs are reviewed as time allows, with no
guaranteed response time. For anything non-trivial, please open an issue first so we can agree on the problem.

## Supported versions

- **Sublime Text 4, build 4083 or later.** Sublime Text 3 and earlier are not supported; ST3 users should stay on 3.1.7.
- **Python 3.8 through 3.14.** ST4 runs the plugin on Python 3.8 (older builds) or 3.14 (build 4215 and later), so code
  must work on both. Avoid `match`, `X | Y` type unions, `list[str]`-style generics at runtime and `str.removeprefix`.
- Command names (`jekyll_*`) and setting keys (`jekyll_*`) are public API. Don't rename them.

## Setting up and running checks

These are the same checks CI runs. The tools need Python 3.10 or later; with [uv](https://docs.astral.sh/uv/):

```bash
uv venv .venv --python 3.13
uv pip install --python .venv "pytest>=7" "ruff>=0.17,<0.18" "black>=26,<27"
```

Or with only the standard library:

```bash
python3 -m venv .venv
.venv/bin/pip install "pytest>=7" "ruff>=0.17,<0.18" "black>=26,<27"
```

Then run:

```bash
.venv/bin/pytest -q                                          # unit tests
.venv/bin/ruff check .                                       # lint
.venv/bin/black --check .                                    # formatting (run `.venv/bin/black .` to fix)
.venv/bin/python -W error -m py_compile jekyll.py jekyll_lib/jekyll_utils.py   # compile, warnings as errors
```

If you change anything under `docs/`, also build the docs strictly:

```bash
uv venv .venv-docs --python 3.12
uv pip install --python .venv-docs -r docs/requirements.txt
.venv-docs/bin/sphinx-build -W --keep-going -b html docs /tmp/sublime-jekyll-docs
```

CI runs the tests on Python 3.8, 3.13 and 3.14. If you can, also run `pytest` under Python 3.8
(`uv venv .venv38 --python 3.8`) to catch syntax that newer Pythons accept.

## Testing in Sublime Text

The automated tests only cover `jekyll_lib/jekyll_utils.py` (pure helpers) and the menu/command wiring. **They don't load the
plugin in Sublime Text**, so they can't catch problems with commands, menus, panels or views. Mocked or simulated
Sublime checks have the same limit.

For any change to `jekyll.py`, test it in a real Sublime Text 4. Symlink your clone into Sublime's `Packages` folder as
`Jekyll` (the folder name matters), for example on macOS:

```bash
ln -s "$PWD" ~/Library/Application\ Support/Sublime\ Text/Packages/Jekyll
```

Use the relevant parts of the [manual release checklist](../tests/manual-release-checklist.md). Always use disposable
copies of a site for delete and promote tests.

## Pull requests

Please include, in the PR description (the template prompts for these):

- **The problem:** what was wrong, how to reproduce it, and the linked issue if there is one. Use one closing keyword
  per issue, e.g. `Closes #123`.
- **The change:** what you changed and why.
- **Testing:** which checks you ran and their results. Keep automated/unit/mocked checks separate from testing in a real
  Sublime Text, and list the Sublime build, OS and plugin host Python you used.
- **Gaps:** anything you couldn't test (other operating systems, older ST4 builds, and so on).
- A `CHANGELOG` entry under the upcoming version for user-facing fixes.

Keep commits focused, with a short subject using a conventional prefix (`fix:`, `docs:`, `ci:`, `build:`, `style:`,
`chore:`) and a body explaining why when it isn't obvious.

## AI-assisted contributions

AI coding tools are allowed, but you don't need to use any particular tool, paid or otherwise.

- **Disclose substantial AI assistance** in the PR description: which tools you used and for what (for example,
  "drafted the fix with an AI assistant, then reviewed and tested it"). Routine autocomplete doesn't need a mention.
- **You are responsible for everything you submit.** Read, understand and review all of the code, and be ready to
  explain it. Don't submit code you haven't run.
- **AI review is optional.** If you use an AI reviewer, it doesn't replace running the checks above, testing in Sublime
  Text, or maintainer review.

## Code of conduct

This project follows the [Contributor Covenant code of conduct](../CODE_OF_CONDUCT.md).
