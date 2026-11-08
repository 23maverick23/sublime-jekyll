sublime-jekyll
==============

[![GitHub license](https://img.shields.io/github/license/23maverick23/sublime-jekyll.svg)](https://github.com/23maverick23/sublime-jekyll/blob/main/LICENSE) [![GitHub tag](https://img.shields.io/github/tag/23maverick23/sublime-jekyll.svg)](https://github.com/23maverick23/sublime-jekyll/tags) [![Package Control](https://img.shields.io/packagecontrol/dt/Jekyll.svg)](https://packagecontrol.io/packages/Jekyll)

> **Maintenance mode:** This package is no longer in active development. Version 4.0.0 restores compatibility with current Sublime Text 4 and fixes outstanding bugs. No new features are planned. Bug-fix PRs may be reviewed as time allows.
>
> Version 4.0.0 was prepared with help from AI coding tools (Claude Code and Codex) and reviewed and tested by the maintainer.

[sublime-jekyll](http://23maverick23.github.io/sublime-jekyll/) is a [Sublime Text](http://www.sublimetext.com/) package for [Jekyll](http://jekyllrb.com/) static sites.

This package is aimed at streamlining the process of managing and creating new Jekyll posts. It does this by providing quick and easy access to new post and draft commands, snippets and completions for [Liquid](https://github.com/Shopify/liquid/wiki/Liquid-for-Designers) template tags and filters, as well as some handy commands for adding dates and upload links to your posts.

If you use Jekyll as your static site generator, and Sublime Text as your text editor, you should absolutely install and use this package!

Installation
------------

Version 4.0.0 requires Sublime Text 4, build 4083 or later, and uses the modern Python plugin host. **Sublime Text 3 users should stay on 3.1.7.**

The recommended way to install and update this package is using [Package Control](https://packagecontrol.io/). Search for `Jekyll` and install the latest version. If you prefer to install this package manually, you can `git clone` this repo or extract the ZIP archive into your Sublime Text `Packages` folder.

Settings and paths
------------------

Paths can be absolute, use Sublime variables such as `${project_path}` (the saved project directory) and `${folder}` (the first open folder), or start with `~` for your home directory. Relative paths use the first open folder, or the saved project directory if no folders are open.

Explicit paths take priority. Otherwise, the package checks open folders and their immediate children for `_config.yml` or `_config.yaml`, then uses existing `_posts`, `_drafts`, or `uploads` folders in those sites. Optional `jekyll_auto_find_paths` searches to depth four if no site match is found. Templates use `jekyll_templates_path` or `Packages/User/Jekyll Templates`.

The old settings migration and backup browsing commands, and `jekyll_utility_disable`, have been removed. Update old settings by hand using the [settings guide](docs/settings.rst), which also covers lookup order and project overrides.

Documentation
-------------

Installation instructions, available commands and features, detailed documentation, and FAQs can be found at [sublime-jekyll.rtfd.org](http://sublime-jekyll.rtfd.org/).

License
-------

sublime-jekyll is licensed under the MIT license. [LICENSE](https://raw.githubusercontent.com/23maverick23/sublime-jekyll/main/LICENSE)

[![](https://sourcerer.io/fame/23maverick23/23maverick23/sublime-jekyll/images/0)](https://sourcerer.io/fame/23maverick23/23maverick23/sublime-jekyll/links/0)[![](https://sourcerer.io/fame/23maverick23/23maverick23/sublime-jekyll/images/1)](https://sourcerer.io/fame/23maverick23/23maverick23/sublime-jekyll/links/1)[![](https://sourcerer.io/fame/23maverick23/23maverick23/sublime-jekyll/images/2)](https://sourcerer.io/fame/23maverick23/23maverick23/sublime-jekyll/links/2)[![](https://sourcerer.io/fame/23maverick23/23maverick23/sublime-jekyll/images/3)](https://sourcerer.io/fame/23maverick23/23maverick23/sublime-jekyll/links/3)[![](https://sourcerer.io/fame/23maverick23/23maverick23/sublime-jekyll/images/4)](https://sourcerer.io/fame/23maverick23/23maverick23/sublime-jekyll/links/4)[![](https://sourcerer.io/fame/23maverick23/23maverick23/sublime-jekyll/images/5)](https://sourcerer.io/fame/23maverick23/23maverick23/sublime-jekyll/links/5)[![](https://sourcerer.io/fame/23maverick23/23maverick23/sublime-jekyll/images/6)](https://sourcerer.io/fame/23maverick23/23maverick23/sublime-jekyll/links/6)[![](https://sourcerer.io/fame/23maverick23/23maverick23/sublime-jekyll/images/7)](https://sourcerer.io/fame/23maverick23/23maverick23/sublime-jekyll/links/7)

This project adheres to the [Contributor Covenant code of conduct](https://raw.githubusercontent.com/23maverick23/sublime-jekyll/main/CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code. Please report unacceptable behavior to github@rymo.io.
