Snippets
========

sublime-jekyll ships with a number of handy Liquid template snippets so you don't waste time remembering code or looking up documentation.


Common
------


Assign
^^^^^^

    :Trigger: assign
    :Description: Create a Liquid template variable.
    :Content:

        .. code-block:: liquid

            {% assign $1 = $2 %}


Break
^^^^^

    :Trigger: break
    :Description: Insert a Liquid template break tag.
    :Content:

        .. code-block:: liquid

            {% break %}


Capture
^^^^^^^

    :Trigger: capture
    :Description: Capture a string and assign to a variable.
    :Content:

        .. code-block:: liquid

            {% capture $1 %}
            $0
            {% endcapture %}


Case
^^^^

    :Trigger: case
    :Description: Creates the start of a switch statement (used with ``{% when %}`` tags).
    :Content:

        .. code-block:: liquid

            {% case $1 %}
            $0
            {% endcase %}


Comment
^^^^^^^

    :Trigger: comment
    :Description: Add a comment block.
    :Content:

        .. code-block:: liquid

            {% comment $1 %}
            $0
            {% endcomment %}


Context variable
^^^^^^^^^^^^^^^^

    :Trigger: va
    :Description: Create a variable.
    :Content:

        .. code-block:: liquid

            {{ $1 }}


Continue
^^^^^^^^

    :Trigger: continue
    :Description: Add a continue tag to a loop.
    :Content:

        .. code-block:: liquid

            {% continue %}


Cycle
^^^^^

    :Trigger: cycle
    :Description: Cycle through values in a for block.
    :Content:

        .. code-block:: liquid

            {% cycle $1 %}


Decrement
^^^^^^^^^

    :Trigger: decrement
    :Description: Decrement an amount.
    :Content:

        .. code-block:: liquid

            {% decrement $1 %}


Else/if
^^^^^^^

    :Trigger: elsif
    :Description: Add an else/if clause.
    :Content:

        .. code-block:: liquid

            {% elsif $1 %}


For
^^^

    :Trigger: for
    :Description: Create a for block.
    :Content:

        .. code-block:: liquid

            {% for $1 in $2 %}
            $0
            {% endfor %}


If
^^

    :Trigger: if
    :Description: Create an if statement.
    :Content:

        .. code-block:: liquid

            {% if $1 %}
            $0
            {% endif %}


If/else
^^^^^^^

    :Trigger: ifelse
    :Description: Create an if/else statement.
    :Content:

        .. code-block:: liquid

            {% if $1 %}
            $2
            {% else %}
            $0
            {% endif %}


Increment
^^^^^^^^^

    :Trigger: increment
    :Description: Increment an amount.
    :Content:

        .. code-block:: liquid

            {% increment $1 %}


Raw
^^^

    :Trigger: raw
    :Description: Create a raw/unprocessed block.
    :Content:

        .. code-block:: liquid

            {% raw %}
            $0
            {% endraw %}


Unless
^^^^^^

    :Trigger: unless
    :Description: Opposite of an if clause.
    :Content:

        .. code-block:: liquid

            {% unless $1 %}
            $0
            {% endunless %}


When
^^^^

    :Trigger: when
    :Description: Part of a switch statement.
    :Content:

        .. code-block:: liquid

            {% when $1 %}


Obscure
-------


Gist
^^^^

    :Trigger: gist
    :Description: Quickly include a tag for a Gist code snippet.
    :Content:

        .. code-block:: liquid

            {% gist $1 %}


Highlight
^^^^^^^^^

    :Trigger: highlight
    :Description: Quickly include a code block for use with the Rouge syntax highlighter.
    :Content:

        .. code-block:: liquid

            {% highlight $1 %}
            $0
            {% endhighlight %}


Include
^^^^^^^

    :Trigger: include
    :Description: Include a named template.
    :Content:

        .. code-block:: liquid

            {% include $1 %}


Include relative
^^^^^^^^^^^^^^^^

    :Trigger: include_relative
    :Description: Include a named template relative to the current file.
    :Content:

        .. code-block:: liquid

            {% include_relative $1 %}


Post URL
^^^^^^^^

    :Trigger: post_url
    :Description: Quickly include a tag for the current post's permalink URL.
    :Content:

        .. code-block:: liquid

            {% post_url $1 %}

