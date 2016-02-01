Templates
=========

sublime-jekyll allows new drafts and posts to be created from user-defined YAML front-matter templates. This allows for a truly customized approach to writing posts.


The basic format of a post template should just include the front-matter.

.. code-block:: yaml

    ---
    layout: post
    category: blog
    ---

Post templates support Sublime Text snippet formatting for more complex layouts and increased automation in your writing. For more documentation on using snippet variables, have a look at the official Sublime Text `snippet documentation`_.

.. _snippet documentation: http://sublimetext.info/docs/en/extensibility/snippets.html

.. code-block:: yaml

    ---
    layout: ${1:post}
    tags: [$2]
    image:
        url:
        alt:
    ---

Although the post ``title`` key will be added automatically as the first key in the template, you can optionally pass a blank ``title:`` key anywhere in the front-matter and it will be replaced with the title of your post.

.. code-block:: yaml

    ---
    layout: post
    title:
    category: blog
    ---

When creating a new template, you will be able to optionally pass in a description of what that template is used for. This is helpful if you have multiple templates and you want to remember what each is used for. The description will show in the quick panel under the name of the template. The description is stored as a YAML comment on the first line of the file, and will be stripped out when a new draft or post is created.

.. code-block:: yaml

    # Used this for image posts
    ---
    layout: ${1:image}
    tags: ['$2']
    image:
        url: $3
        alt: $4
    ---

.. note::

    sublime-jekyll does not provide YAML front-matter validation or. If you need help with YAML formatting, please refer to the official `Jekyll documentation`_.

.. _Jekyll documentation: http://jekyllrb.com/docs/frontmatter/
