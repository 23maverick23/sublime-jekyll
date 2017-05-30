Build System
============

If desired, you can add a custom Jekyll build system to your Sublime projects. This allows you to create a specific build system for each Jekyll project you're working on.

From what I can tell, a project-specific build system needs to be used, as opposed to a standard build system. This is because the ``jekyll`` CLT command must be run from the main Jekyll folder that contains the *_config.yml* file (which cannot be guaranteed to be the current project folder).

.. code-block:: python

    {
        "folders":
        [
            {
                "follow_symlinks": true,
                "path": "/Users/username/site/"
            }
        ],

        "build_systems":
        [
            // This will build your Jekyll site, and print a trace to the console
            {
                "name": "Jekyll",
                // Change this directory to match your top-level Jekyll project folder
                "working_dir": "$project_path",
                "cmd": "jekyll build -t",
                "shell": true,
                "encoding": "UTF-8"
            }
        ]
    }


.. note::

    You can read up further on Build systems in general from the documentation found here:

    http://sublimetext.info/docs/en/reference/build_systems.html
    http://docs.sublimetext.info/en/latest/reference/build_systems.html
