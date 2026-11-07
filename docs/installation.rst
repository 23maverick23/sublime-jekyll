Installation
============

Requirements
------------

Version 4.0.0 requires **Sublime Text 4, build 4083 or later**. Sublime Text 3 users should stay on **3.1.7**; do not install 4.0.0 or the current branch on ST3.

Package Control
---------------

The recommended way to install and update this package is using `Package Control`_. Search for **Jekyll** and install the latest version.

.. _Package Control: https://packagecontrol.io/packages/Jekyll

* Press ``Ctrl + Shift + P`` (Windows/Linux) or ``Command + Shift + P`` (OS X) to bring up the Command Palette (or use the *Tools > Command Palette* menu)
* Search for the **Package Control: Install Package** command
* Search packages for **Jekyll** and hit ``Enter`` to install the latest version

Manual
------

If you would prefer to install this package manually, you can do that directly from GitHub.

* `Clone the git repo <https://github.com/23maverick23/sublime-jekyll.git>`_
* `Download the repo ZIP archive <https://github.com/23maverick23/sublime-jekyll/archive/master.zip>`_

Put the contents in a ``Jekyll`` folder under your Sublime Text ``Packages`` directory. Use *Preferences > Browse Packages...* to find the correct directory, including for portable or upgraded installations.

For a manual ST3 installation, use the `v3.1.7 archive <https://github.com/23maverick23/sublime-jekyll/archive/refs/tags/v3.1.7.zip>`_.

Upgrading
---------

The settings migration and backup browsing commands were removed in 4.0.0. Update pre-3.0 settings by hand using :doc:`settings`. Remove the obsolete ``jekyll_utility_disable`` key if present.

The package is now in maintenance mode. No new features are planned; bug-fix PRs may be reviewed as time allows.
