FAQs
====

I'm getting *Unable to find path information* errors.
-----------------------------------------------------

In order for sublime-jekyll to create new posts for your static site, it must know where to put them. There are 2 required settings that must be set **before** you use this package: ``jekyll_posts_path`` and ``jekyll_drafts_path``. If those are not set in either your User settings file, or your Project settings file, sublime-jekyll will fail with a ``MissingPathException``.


What happened to all the syntax files?
----------------------------------------------------

Syntax files in Sublime Text suck - period. They were becoming really difficult to manage and debug, and in my opinion they weren't all that good anyway. I have `moved them to a separate repository`_ where folks can feel free to push pull requests for any bugs or fixes. I don't plan on maintaining this respository with proactive updates (outside of community pull requests).

If you want my recommendation for a syntax package, install `Markdown Extended`_ or `MarkdownEditing`_ - both are very good and well maintained.

.. _moved them to a separate repository: https://github.com/23maverick23/sublime-jekyll-syntaxes
.. _Markdown Extended: https://packagecontrol.io/packages/Markdown%20Extended
.. _MarkdownEditing: https://packagecontrol.io/packages/MarkdownEditing


Where do I put my Project settings?
-----------------------------------

When you create a new project in Sublime Text, you are asked to save a file with a suffix of *.sublime-project*. By default, that file has some minimal settings, and allows you to control things about your specific project (`project documentation`_). To add Project specific settings for sublime-jekyll, you can just add your Jekyll settings under the "settings" key in your *.sublime-project* file.

.. code-block:: python

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
                "jekyll_posts_path": "/Users/username/site/_posts",
                "jekyll_drafts_path": "/Users/username/site/_drafts",
            }
        }
    }

.. _project documentation: https://www.sublimetext.com/docs/3/projects.html


How do I log a bug?
-------------------

Bugs suck - and I'm sorry you had to find one. I'm typically pretty responsive to fixing them if you help me gather as much information as possible.

* First, **enable debug mode** for sublime-jekyll by setting the ``jekyll_debug`` setting to ``true``, and restart Sublime Text.
* Next, try to reproduce the bug again. If it still happens, open up the Sublime console ( ``Ctrl + ``` or *View > Show Console*) and copy the Jekyll-specific debugging output (it should have a ``Jekyll`` or ``Jekyll Utility`` prefix).
* Check the list of open issues on the `GitHub issue tracker`_ for similar problems with other users. If you find one, add your name to it.
* If no issues exist, open a new one being sure to include the following information:

    1. A summary or description of the specific issue
    2. Your version of Sublime Text (2 or 3, as well as build)
    3. Your operating system (Windows, OS X, Linux)
    4. The debug output of the Sublime console

* Lastly, be open to us asking some questions about your bug as we attempt to reproduce and squash it!

.. _Github issue tracker: https://github.com/23maverick23/sublime-jekyll/issues
