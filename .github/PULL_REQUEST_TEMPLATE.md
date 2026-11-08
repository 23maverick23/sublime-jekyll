<!--
This package is in maintenance mode: bug fixes and Sublime Text 4 / Python compatibility only.
See .github/CONTRIBUTING.md for setup and checks.
-->

## Problem

<!-- What is wrong, and how to reproduce it. -->

Closes #

## Change

<!-- What you changed and why. -->

## Testing

**Automated checks** (same as CI), with results:

- [ ] `pytest -q`
- [ ] `ruff check .`
- [ ] `black --check .`
- [ ] `python -W error -m py_compile jekyll.py jekyll_utils.py`
- [ ] Strict docs build (only if `docs/` changed)

**Testing in Sublime Text** (required for changes to `jekyll.py`). Unit tests and mocks don't count here.

- Sublime Text build:
- OS:
- Plugin host Python (`import sys; sys.version` in the console):
- What you tested and the result:

**Not tested / known gaps:**

## AI assistance

<!-- If AI tools substantially helped write or review this change, name them and say what they did. Otherwise write "None". -->

## Checklist

- [ ] This is a bug fix or compatibility change, not a new feature.
- [ ] I have read, understood and reviewed all of the code in this PR.
- [ ] User-facing fixes have a `CHANGELOG` entry.
