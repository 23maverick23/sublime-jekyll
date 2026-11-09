# Manual release checklist (native Sublime Text)

CI runs unit tests, linting, formatting, compilation and the docs build. It **does not** load the plugin in Sublime
Text, so it cannot catch problems with commands, menus, panels, views or settings. Run this checklist in a real
Sublime Text 4 before tagging a release, and for any change to `jekyll.py`.

Copy this file (or the relevant sections) into the release PR or a scratch note and fill it in there. Keep this
template blank. Only mark an item as passed if you ran it for the commit under test; don't copy results from earlier
runs.

## Test environment

| Field | Value |
| --- | --- |
| Commit under test (`git rev-parse --short HEAD`) | |
| OS and version | |
| Sublime Text build (Help → About, or `sublime.version()` in the console) | |
| Plugin host runtime (`import sys; sys.version` in the console) | |
| How the package was loaded (symlink into `Packages/Jekyll`, or a `git archive` `.sublime-package`) | |
| Tester | |

## Setup

- Load the package from the commit under test. Symlink the repo into Sublime's `Packages` folder as `Jekyll`
  (the folder name matters), or build a package with
  `git archive --format=zip -o "<Installed Packages>/Jekyll.sublime-package" HEAD`. Remove any other copy first.
- **Use disposable fixtures.** Delete and promote tests change files on disk. Work on a throwaway copy of a Jekyll
  site, throwaway upload files and throwaway templates, never on a real site.
- Keep the Sublime console open (``Ctrl+` ``) and watch for `Jekyll` tracebacks throughout.

## Loading

- [ ] The package loads with no tracebacks or `SyntaxWarning` lines mentioning `Jekyll` in the console.
- [ ] The runtime recorded above is the modern plugin host (3.8 or later), not 3.3.

## Command matrix

Run each command in three window states:

- **Site:** a window with a disposable Jekyll site folder (containing `_config.yml`) open and no path settings.
- **Non-site:** a window with an unrelated folder open and no path settings.
- **Empty:** a new window with no folders and no files open.

In non-site and empty windows, expect a clear error or status message, or a disabled command. There should be no
traceback and no new untitled document. The template commands (New/Edit/Remove/Browse template) work in every window
because templates live in `Packages/User/Jekyll Templates` unless `jekyll_templates_path` is set.

| Palette command | Site | Non-site | Empty |
| --- | --- | --- | --- |
| New post | [ ] | [ ] | [ ] |
| New post from template | [ ] | [ ] | [ ] |
| Open post | [ ] | [ ] | [ ] |
| Remove post | [ ] | [ ] | [ ] |
| New draft | [ ] | [ ] | [ ] |
| New draft from template | [ ] | [ ] | [ ] |
| Open draft | [ ] | [ ] | [ ] |
| Promote draft to post | [ ] | [ ] | [ ] |
| Remove draft | [ ] | [ ] | [ ] |
| New template | [ ] | [ ] | [ ] |
| Edit template | [ ] | [ ] | [ ] |
| Remove template | [ ] | [ ] | [ ] |
| Browse templates... | [ ] | [ ] | [ ] |
| Edit _config.yml | [ ] | [ ] | [ ] |
| Insert current date | [ ] | [ ] | [ ] |
| Insert current datetime | [ ] | [ ] | [ ] |
| Insert upload | [ ] | [ ] | [ ] |

## Menus and empty windows

- [ ] Opening the Command Palette, the right-click menu and Preferences → Package Settings → Jekyll causes no error
      popups, noticeable delay or new untitled tabs, in all three window states.
- [ ] In an empty window, Insert current date, Insert current datetime and Insert upload are unavailable, and running
      them (for example with `subl --command 'jekyll_insert_date {"format": "date"}'`) creates no document.
- [ ] In an empty window **with an explicit `jekyll_uploads_path` configured** (project settings), Insert upload is
      still unavailable and creates no document.

## Inserting into documents

- [ ] Date and datetime insert into a **saved file** and into an **existing untitled document**.
- [ ] With several cursors and one non-empty selection, the date goes in at every cursor and replaces the selection.
- [ ] A single Undo removes the whole insertion.
- [ ] A non-string `jekyll_date_format` / `jekyll_datetime_format` (for example `123`) falls back to the default format
      without a traceback.
- [ ] Insert upload with a configured uploads path and with auto-detected paths: images (PNG, JPEG, SVG, WebP, AVIF,
      TIFF) produce `![...](...)`; other files produce `[...](...)`. Nested paths and the base URL are correct and use
      forward slashes.
- [ ] Awkward upload names: `photo 1.png` → `photo%201.png` in the URL; `a]b.png` → label `a\]b`.

## Paths and settings

- [ ] Both Preferences → Package Settings → Jekyll → Settings and the palette command Preferences: Jekyll Settings
      open package defaults on the left and User settings on the right, including when no User settings file exists.
- [ ] With no path settings, `_config.yml` / `_config.yaml` in an open folder or its immediate child is detected and
      the standard `_posts`, `_drafts` and `uploads` folders are used.
- [ ] Explicit paths take priority. An invalid explicit path shows an error that includes the configured value and
      what it resolved to.
- [ ] Relative paths, `~/...`, `${folder}/...` and `${project_path}/...` resolve as documented. (`${project_path}` is
      the folder containing the `.sublime-project` file.)
- [ ] Multiple `_posts` folders show a chooser; each choice continues in the chosen folder; cancelling changes nothing.
- [ ] Auto-find on a large disposable tree keeps menus responsive and skips hidden, build and dependency folders.
- [ ] A project setting of `false` overrides a user setting of `true` (for example `jekyll_auto_find_paths`).
- [ ] `jekyll_markdown_extension` set to `md`, then `markdown`, changes the extension of new posts and drafts.

## Delete and promote (disposable fixtures only)

- [ ] Delete a post, draft and template with `jekyll_send_to_trash` `false`: the confirmation says the delete is
      permanent, Cancel leaves the file, and OK removes it.
- [ ] Delete with `jekyll_send_to_trash` `true`: the file appears in the system Trash / Recycle Bin.
- [ ] Deleting closes only the deleted file's tab, even when a different tab is active.
- [ ] **Unsaved edits:** deleting or promoting a file that is open with unsaved changes shows a "Save or revert" error
      and changes nothing on disk.
- [ ] Promote uses a valid front-matter `date:` (also quoted, and with a time), falls back to today when it's missing or
      invalid, and keeps the front matter unchanged.
- [ ] Promote works with a custom drafts folder name and from a nested subfolder.
- [ ] Promote with an existing destination file shows an error, keeps both files and opens nothing.

## Templates and titles

- [ ] New post/draft from template with a title containing `$`, `}`, `:`, single and double quotes (for example
      `Cost $5 }: "quoted" and 'single'`): the title text is exact, the front matter is valid YAML, and the template's
      snippet fields still work.
- [ ] Templates whose `title` is a **multiline** value (`title: >` or `title: |` followed by indented lines): the
      whole value is replaced and the front matter stays valid YAML.
- [ ] A template with no `title` key gets one added.
- [ ] A title with no letters or digits (for example `!!!`) is rejected without creating a file.

## Notes and gaps

Record anything not tested (other operating systems, older ST4 builds, packaged vs. symlinked installs) and any
failures with reproduction steps.
