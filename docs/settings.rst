Settings
========

sublime-jekyll ships with a number of configurable settings. These can be overridden globally in your User Settings file, or on a per-Project basis using the recommended Project Settings syntax.


.. warning::

    **sublime-jekyll settings prior to v3.0 have been deprecated!**

    We know that is a bit of a pain - we get it - but it was for the best moving forward.

    To help with the transition, we have created some **Jekyll Utility** commands that automatically migrate your old, deprecated settings to new, fully supported settings. You can find these in the Command Palatte by searching for *Jekyll Utility*.


User Settings
-------------

``jekyll_posts_path``
^^^^^^^^^^^^^^^^^^^^^

    :Default: None
    :Description: This should point to your ``_posts`` directory.


``jekyll_drafts_path``
^^^^^^^^^^^^^^^^^^^^^^

    :Default: None
    :Description: This should point to your ``_drafts`` directory.


``jekyll_uploads_path``
^^^^^^^^^^^^^^^^^^^^^^^

    :Default: None
    :Description: This should point to your ``_uploads`` directory.


.. warning::

    These should be **absolute paths**, not relative paths!

    Also, the paths should follow your system-specific path convention. For example, Windows machines should have a path similar to ``C:\\Users\\username\\site\\_posts``. Unix/Linux systems should have a path similar to ``/Users/username/site/_posts``.


``jekyll_auto_find_paths``
^^^^^^^^^^^^^^^^^^^^^^^^^^

    :Default: ``false``
    :Description: If you don't want to hard-code your ``_posts``, ``_drafts``, or ``uploads`` paths into your settings file, you can optionally have sublime-jekyll look for ``_posts``, ``_drafts`` or ``_uploads`` folders open in your sidebar. If you don't name the folders appropriately, or you use a non-standard file structure for your Jekyll project, you have a higher chance of returning path exception errors. This should have a value of ``true`` or ``false``.


``jekyll_uploads_baseurl``
^^^^^^^^^^^^^^^^^^^^^^^^^^

    :Default: ``{{ site.baseurl }}``
    :Description: This string value should represent the **baseurl** for the uploads directory. For example, if your uploads directory is ``_uploads/`` and you have an image called ``image.png``, the output of inserting the image in your post would be ``{{ uploads_baseurl }}/uploads/image.png``, with ``{{ uploads_baseurl }}`` replace by its value.


.. note::

    If you wish to have an absolute link and you have ``url`` defined in your Jekyll ``config.yml`` file, then you can set the value to ``{{ site.url }}/{{ site.baseurl }}``.


``jekyll_default_markup``
^^^^^^^^^^^^^^^^^^^^^^^^^

    :Default: ``Markdown``
    :Description: This string value determines the file type for new drafts and posts. It can be set to one of three accepted values: ``Markdown``, ``Textile`` or ``HTML``.


.. note::

    We use ``.markdown`` as the standard file extension for Markdown files as suggested by John Gruber, developer of Markdown, in his blog post here: http://daringfireball.net/linked/2014/01/08/markdown-extension


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

    If you need a refresher on these codes, have a look at the Python documentation found here: http://docs.python.org/2/library/datetime.html#strftime-and-strptime-behavior.


``jekyll_debug``
^^^^^^^^^^^^^^^^

    :Default: ``false``
    :Description: If set to ``true``, the application will print Jekyll debug information to the Sublime Text console and can be retrieved by using ``Ctrl + ```.


``jekyll_utility_disable``
^^^^^^^^^^^^^^^^^^^^^^^^^^

    :Default: ``false``
    :Description: If set to ``true``, the application will hide the **Jekyll Utility** commands from the Command Palatte, and disable the commands from the menu.


Project Settings
----------------

For per-project settings, make sure you add your Jekyll settings correctly to your Project settings file. You can typically edit your Project file under *Project > Edit Project*.

.. warning::
    These should be **absolute paths**, not relative paths!

    Also, the paths should follow your system-specific path convention. For example, Windows machines should have a path similar to ``C:\\Users\\username\\site\\_posts``. Unix/Linux systems should have a path similar to ``/Users/username/site/_posts``.


.. code-block:: python

    # some-file.sublime-settings
    
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
                "posts_path": "/Users/username/site/_posts",
                "drafts_path": "/Users/username/site/_drafts",
                "uploads_path": "/Users/username/site/_uploads",
            }
        }
    }


.. seealso::
    Read the conversation on `issue #16`_ if you have questions on formatting your Project settings file correctly.


.. _issue #16: https://github.com/23maverick23/sublime-jekyll/issues/16