Commands
========

sublime-jekyll ships with a number of commands for helping you get things done more efficiently.


.. warning::

    Users who are upgrading from pre-v3.0 will want to review the **Jekyll Utility** commands. These allow you to easily migrate over your ``sublime-settings`` so that you can continue using sublime-jekyll moving forward.

    If you prefer to hide these commands and remove them from the Command Palatte, you can set the settings key ``jekyll_utility_disable`` to ``true`` and restart Sublime Text.


Jekyll
------


New post
^^^^^^^^

    :Command: ``jekyll_new_post``
    :Description: Brings up an input panel for naming and creating a new post in your ``_posts`` directory. The post title is automatically slugified, and the current date is appended to the title.


New post from template
^^^^^^^^^^^^^^^^^^^^^^

    :Command: ``jekyll_new_post_from_template``
    :Description: Brings up a quick panel for selecting a post template. Once selected, brings up an input panel for naming and creating a new post in your ``_posts`` directory. The post title is automatically slugified, and the current date is appended to the title.

Remove post
^^^^^^^^^^^

    :Command: ``jekyll_remove_post``
    :Description: Brings up a quick panel for choosing a post in your ``_posts`` directory to delete. This action is irreversible.


Open post...
^^^^^^^^^^^^

    :Command: ``jekyll_open_post``
    :Description: Brings up a quick panel for choosing an existing post in your ``_posts`` directory.


New draft
^^^^^^^^^

    :Command: ``jekyll_new_draft``
    :Description: Brings up an input panel for naming and creating a new draft in your ``_drafts`` directory. The post title is automatically slugified, however no date is appended to the title.


New draft from template
^^^^^^^^^^^^^^^^^^^^^^^

    :Command: ``jekyll_new_draft_from_template``
    :Description: Brings up a quick panel for selecting a post template. Once selected, brings up an input panel for naming and creating a new post in your ``_drafts`` directory. The post title is automatically slugified.


Promote draft to post
^^^^^^^^^^^^^^^^^^^^^

    :Command: ``jekyll_promote_draft``
    :Description: Brings up a quick panel for choosing an existing draft in your ``_drafts`` directory to move to the ``_posts`` directory. The post title is automatically updated with the current date.


Remove draft
^^^^^^^^^^^^

    :Command: ``jekyll_remove_draft``
    :Description: Brings up a quick panel for choosing a post in your ``_drafts`` directory to delete. This action is irreversible.


Open draft
^^^^^^^^^^

    :Command: ``jekyll_open_draft``
    :Description: Brings up a quick panel for choosing an existing draft in your ``_drafts`` directory.


New template
^^^^^^^^^^^^

    :Command: ``jekyll_new_template``
    :Description: Brings up an input panel for naming and creating a new post template in your ``Jekyll Templates`` directory.


Edit template
^^^^^^^^^^^^^

    :Command: ``jekyll_edit_template``
    :Description: Brings up a quick panel for choosing an existing template in your ``Jekyll Templates`` directory.


Remove template
^^^^^^^^^^^^^^^

    :Command: ``jekyll_remove_template``
    :Description: Brings up a quick panel for choosing an existing template in your ``Jekyll Templates`` directory to delete. This action is irreversible.


Browse templates...
^^^^^^^^^^^^^^^^^^^

    :Command: ``jekyll_browse_templates``
    :Description: Opens your ``Jekyll Templates`` directory in your system-specific default file browser (helpful for managing templates directly).


Insert current date
^^^^^^^^^^^^^^^^^^^

    :Command: ``jekyll_insert_date``
    :Args: ``{"format": "date"}``
    :Description: Inserts the current date at the cursor using the format specified by the ``jekyll_date_format`` setting.


Insert current datetime
^^^^^^^^^^^^^^^^^^^^^^^

    :Command: ``jekyll_insert_datetime``
    :Args: ``{"format": "datetime"}``
    :Description: Inserts the current datetime at the cursor using the format specified by the ``jekyll_datetime_format`` setting.


Insert upload
^^^^^^^^^^^^^

    :Command: ``jekyll_insert_upload``
    :Description: Brings up a quick panel for choosing an existing file in your ``uploads`` directory, and adds a pre-formatted link at the cursor.


Jekyll Utility
--------------


Migrate user settings
^^^^^^^^^^^^^^^^^^^^^

    :Command: ``jekyll_migrate_user_settings``
    :Description: Attempts to migrate pre-v3.0 User Settings files to the new v3.0 format. This command only needs to be run once per machine/user. Settings backup files can be found in the ``Jekyll Backup`` folder within your ``User`` directory.


Migrate project settings
^^^^^^^^^^^^^^^^^^^^^^^^

    :Command: ``jekyll_migrate_project_settings``
    :Description: Attempts to migrate pre-v3.0 Project Settings files to the new v3.0 format. This command should be run for each Project using sublime-jekyll settings keys. Settings backup files can be found in the ``Jekyll Backup`` folder within your ``User`` directory.


.. note::

    Users of Sublime Text 2 will not see the ``Migrate project settings`` command, as there is no project API. You will need to update your project settings manually.


Browse backups...
^^^^^^^^^^^^^^^^^

    :Command: ``jekyll_browse_backups``
    :Description: Opens your ``Jekyll Backups`` directory in your system-specific default file browser (helpful for managing backups directly).
