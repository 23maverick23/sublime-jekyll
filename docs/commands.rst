Commands
========

sublime-jekyll ships with a number of commands for helping you get things done more efficiently.


Paths are resolved when a command runs. See :doc:`settings` for explicit paths, site auto-detection, and the optional fallback search. Opening a menu or the Command Palette does not search folders or create an untitled document.


Jekyll
------


New post
^^^^^^^^

    :Command: ``jekyll_new_post``
    :Description: Brings up an input panel for naming and creating a new post in your ``_posts`` directory. The filename uses a slug of the title prefixed with the current date. The title is escaped for YAML and Sublime snippet syntax.


New post from template
^^^^^^^^^^^^^^^^^^^^^^

    :Command: ``jekyll_new_post_from_template``
    :Description: Brings up a quick panel for selecting a post template. Once selected, brings up an input panel for naming and creating a new post in your ``_posts`` directory. The filename uses a slug of the title prefixed with the current date. The title is escaped for YAML and Sublime snippet syntax.

Remove post
^^^^^^^^^^^

    :Command: ``jekyll_remove_post``
    :Description: Brings up a quick panel for choosing a post in your ``_posts`` directory to delete. A confirmation dialog is shown. With ``jekyll_send_to_trash: true``, the file goes to system Trash; otherwise deletion is permanent. Only the selected file's tab is closed.


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
    :Description: Brings up a quick panel for choosing an existing draft in your ``_drafts`` directory to move to the ``_posts`` directory. The filename uses a valid leading ``YYYY-MM-DD`` date from the saved draft's top-level ``date:`` front-matter field, including quoted dates or dates with a time. Missing, invalid, or unsupported dates fall back to today's local date. The front matter itself is unchanged. Subdirectories are kept, and custom draft directory names are supported. Save or revert an unsaved draft before promoting it. An existing target reports an error and leaves the draft in place.


Remove draft
^^^^^^^^^^^^

    :Command: ``jekyll_remove_draft``
    :Description: Brings up a quick panel for choosing a post in your ``_drafts`` directory to delete. A confirmation dialog is shown. With ``jekyll_send_to_trash: true``, the file goes to system Trash; otherwise deletion is permanent. Only the selected file's tab is closed.


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
    :Description: Brings up a quick panel for choosing an existing template in your ``Jekyll Templates`` directory to delete. A confirmation dialog is shown. With ``jekyll_send_to_trash: true``, the file goes to system Trash; otherwise deletion is permanent. Only the selected file's tab is closed.


Browse templates...
^^^^^^^^^^^^^^^^^^^

    :Command: ``jekyll_browse_templates``
    :Description: Opens your ``Jekyll Templates`` directory in your system-specific default file browser (helpful for managing templates directly).


Edit _config.yml
^^^^^^^^^^^^^^^^

    :Command: ``jekyll_edit_config``
    :Description: Looks for ``_config.yml`` or ``_config.yaml`` in the parent of resolved post directories and in detected site roots. Multiple matches open a chooser. If none is found, a status message asks you to open the site folder.


Insert current date
^^^^^^^^^^^^^^^^^^^

    :Command: ``jekyll_insert_date``
    :Args: ``{"format": "date"}``
    :Description: Inserts the current date at the cursor using the format specified by the ``jekyll_date_format`` setting.


Insert current datetime
^^^^^^^^^^^^^^^^^^^^^^^

    :Command: ``jekyll_insert_date``
    :Args: ``{"format": "datetime"}``
    :Description: Inserts the current datetime at the cursor using the format specified by the ``jekyll_datetime_format`` setting.


Insert upload tag
^^^^^^^^^^^^^^^^^

    :Command: ``jekyll_list_uploads``
    :Description: Brings up a quick panel allowing you to choose an existing file from your ``jekyll_uploads_path`` directory, and creates a pre-formatted link at the cursor. Images are identified by file extension and receive Markdown image syntax; other files receive a Markdown link. Open a document before running this command. This will not move the selected file, nor will it check if the relative URL it creates points to an actual file.
