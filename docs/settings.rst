Settings
========

sublime-jekyll ships with a number of configurable settings. These can be overridden globally in your User Settings file, or on a per-Project basis using the recommended Project Settings syntax.


Settings lookup
---------------

Settings are read when a command runs. Values in ``settings > Jekyll`` in the current ``.sublime-project`` file take priority over ``Jekyll.sublime-settings`` (User settings and package defaults). A project value of ``false`` or an empty string still overrides the user value. Edit User settings through *Preferences > Package Settings > Jekyll > Settings* or the *Preferences: Jekyll Settings* command in the Command Palette. Package defaults open on the left and editable User settings on the right.

Path resolution
---------------

Paths may be absolute, contain Sublime variables such as ``${project_path}`` (the directory of the saved project file) or ``${folder}`` (the first open folder), or start with ``~`` for the home directory. Variables expand first, then ``~``. Relative paths resolve against the first open folder, or the saved project directory if no folders are open. Without either, use an absolute path. Variables need the matching project or folder context to be available.

For posts, drafts, and uploads, paths are resolved in this order:

1. Use the explicit ``jekyll_posts_path``, ``jekyll_drafts_path``, or ``jekyll_uploads_path`` setting. The directory must exist; an invalid explicit path reports an error instead of falling back.
2. Check each open folder and its immediate children for ``_config.yml`` or ``_config.yaml``. Use existing ``_posts``, ``_drafts``, or ``uploads`` directories directly under those site roots. This works even when ``jekyll_auto_find_paths`` is ``false``. The config file identifies the site; its contents are not parsed for custom directory names.
3. If there are no matching site directories and ``jekyll_auto_find_paths`` is ``true``, search open folders recursively to depth four. Skip hidden directories, ``node_modules``, ``_site``, ``vendor``, ``.jekyll-cache``, ``.sass-cache``, and ``bower_components``. Search does not follow directory symlinks. Large trees can still take time; use explicit paths to avoid a search.
4. If no path is found, show an error with setup guidance. Multiple matches open a directory chooser; cancelling stops the command.

Templates use an explicit ``jekyll_templates_path`` or ``Packages/User/Jekyll Templates``, which is created when a template command runs. Templates do not use site detection or recursive auto-find.

Path strings must follow your system's path conventions. In JSON, escape Windows backslashes, for example ``C:\\Users\\username\\site\\_posts``. Paths such as ``${project_path}/_posts`` and ``_drafts`` are also accepted.

User Settings
-------------

``jekyll_posts_path``
^^^^^^^^^^^^^^^^^^^^^

    :Default: ``""`` (uses path resolution above)
    :Description: This should point to your ``_posts`` directory.


``jekyll_drafts_path``
^^^^^^^^^^^^^^^^^^^^^^

    :Default: ``""`` (uses path resolution above)
    :Description: This should point to your ``_drafts`` directory.


``jekyll_templates_path``
^^^^^^^^^^^^^^^^^^^^^^^^^

    :Default: ``""`` (uses ``Packages/User/Jekyll Templates`` when a template command runs)
    :Description: This should point to your ``_templates`` directory.


``jekyll_auto_find_paths``
^^^^^^^^^^^^^^^^^^^^^^^^^^

    :Default: ``false``
    :Description: Enable the depth-four fallback search for ``_posts``, ``_drafts``, and ``uploads`` described above. It runs only when a command needs a path and site detection finds no matching directory. It does not search for templates.


``jekyll_uploads_path``
^^^^^^^^^^^^^^^^^^^^^^^

    :Default: ``""`` (uses path resolution above)
    :Description: This should point to your ``uploads`` directory.


``jekyll_uploads_baseurl``
^^^^^^^^^^^^^^^^^^^^^^^^^^

    :Default: ``{{site.baseurl}}``
    :Description: This string value should represent the **baseurl** for the uploads directory of your site. For example, if your uploads directory is ``/uploads`` and you have an image called ``image.png``, the output of inserting the image in your post with the ``Insert upload tag`` command would be ``{{ uploads_baseurl }}/uploads/image.png``, with ``{{ uploads_baseurl }}`` replaced by its value.


.. note::

    If you wish to have an absolute link and you have ``url`` defined in your Jekyll ``config.yml`` file, then you can set the value to ``{{site.url}}/{{site.baseurl}}``.


``jekyll_default_markup``
^^^^^^^^^^^^^^^^^^^^^^^^^

    :Default: ``Markdown``
    :Description: This string value determines the file type for new drafts and posts. It can be set to one of four accepted values: ``Markdown``, ``Textile``, ``HTML``, or ``Plain text``.


``jekyll_markdown_extension``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    :Default: ``markdown``
    :Description: Optionally override the file extension format for Markdown files. Valid options include: ``markdown``, ``mdown``, ``mkdn``, ``mkd``, ``md``. Do not include the dot in your string value.

.. note::

    We use ``.markdown`` as the standard file extension for Markdown files as suggested by John Gruber, developer of Markdown, in his blog post here: http://daringfireball.net/linked/2014/01/08/markdown-extension.


``jekyll_send_to_trash``
^^^^^^^^^^^^^^^^^^^^^^^^

    :Default: ``false``
    :Description: Determines if sublime-jekyll should send deleted drafts, posts and templates to the system trash/recycling bin, or immediately purge them from disk.


``jekyll_date_format``
^^^^^^^^^^^^^^^^^^^^^^

    :Default: ``%Y-%m-%d``
    :Description: A valid Python strftime string for a date.


``jekyll_datetime_format``
^^^^^^^^^^^^^^^^^^^^^^^^^^

    :Default: ``%Y-%m-%d %H:%M:%S``
    :Description: A valid Python strftime string for a datetime.


.. note::

    If for some reason you want to change the way either the date or the datetime string is formatted, you can override those formats using valid Python ``datetime.strftime()`` format codes.

    If you need a refresher on these codes, have a look at the Python documentation found here: https://docs.python.org/3/library/datetime.html#strftime-and-strptime-behavior.


``jekyll_debug``
^^^^^^^^^^^^^^^^

    :Default: ``false``
    :Description: If set to ``true``, the application will print Jekyll debug information to the Sublime Text console and can be retrieved by using ``Ctrl + ```.


Project Settings
----------------

For per-project settings, make sure you add your Jekyll settings correctly to your Project settings file. You can typically edit your Project file under *Project > Edit Project*.

.. code-block:: json

    {
        "folders":
        [
            {
                "follow_symlinks": true,
                "path": "/Users/username/site/"
            }
        ],

        "settings":
        {
            "Jekyll":
            {
                "jekyll_posts_path": "${folder}/_posts",
                "jekyll_drafts_path": "_drafts",
                "jekyll_uploads_path": "uploads",
                "jekyll_templates_path": "${project_path}/_templates",
                "jekyll_auto_find_paths": false
            }
        }
    }


.. seealso::
    Read the conversation on `issue #16`_ if you have questions on formatting your Project settings file correctly.


.. _issue #16: https://github.com/23maverick23/sublime-jekyll/issues/16
