sublime-jekyll
==============

A Sublime Text package for [Jekyll](http://jekyllrb.com/) static sites. This package should help maintaining Jekyll sites and posts easier by providing access to new post/draft shortcuts, key template tags and filters, as well as common completions and a current date/datetime command (for dating posts).

### New in this Release

The 2.0.0 release brings some brand new commands for creating posts and drafts, as well as the ability to set per-project settings for paths and defaults. Also added is the ability to access existing posts from the Command Palette for making quick edits.

For per-project settings, make sure you add your Jekyll settings correctly:

```python
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
        }
    }
}
```

Installation
------------

### Package Control

You can install this package using [Package Control](https://sublime.wbond.net/packages/Jekyll) from wbond.net.

* Press `ctrl+shift+p` (Windows/Linux) or `command+shift+p` (OS X) to bring up the Command Palette (or use _Tools > Command Palette_ menu)
* Type to search for the `Package Control: Install Package` command
* Search packages for **Jekyll** and hit `enter` to install
* You may need to restart in order to use this package

### Manual

[Clone](https://github.com/23maverick23/sublime-jekyll.git) or [download](https://github.com/23maverick23/sublime-jekyll/archive/master.zip) the contents of this repo into your Sublime Text `Packages` folder.

* OS X: `~/Library/Application\ Support/Sublime\ Text\ 3/Packages`
* Windows: `%APPDATA%\Sublime Text 3\Packages`
* Linux: `~/.config/sublime-text-3/Packages`

What's Included
---------------

### Syntaxes

* HTML (Jekyll)
* JSON (Jekyll)
* Markdown (Jekyll)
* Textile (Jekyll)

### Commands

* Jekyll: New post
* Jekyll: New draft
* Jekyll: Insert current date
* Jekyll: Insert current datetime

You can change the default format of both the date and datetime commands in your user settings file (_Preferences > Package Settings > Jekyll > Settings – User_).

```python
{
    "jekyll_insert_date_format": "%Y-%m-%d",
    "jekyll_insert_datetime_format": "%Y-%m-%d %H:%M:%S"
}
```

### Key Bindings

There no default key bindings for any commands, however you set them in your user key bindings file (_Preferences > Package Settings > Jekyll > Key Bindings – User_).

### Snippets

- assign: `{% assign a = b %}`
- capture: `{% capture %}{% endcapture %}`
- case: `{% case %}{% endcase %}`
- comment: `{% comment %}{% endcomment %}`
- va: `{{ variable }}`
- cycle: `{% cycle %}`
- elsif: `{% elsif %}`
- for: `{% for item in list %}{% endfor %}`
- front-matter:

    ```yaml
    ---
    layout: post
    title:
    date:
    category:
    tags: []
    ---
    ```

- gist: `{% gist url %}`
- highlight: `{% highlight syntax|linenos %}{% endhighlight %}`
- if: `{% if this %}{% endif %}`
- ifelse: `{% if this %}{% else %}{% endif %}`
- include: `{% include this.html %}`
- post_url: `{% post_url url %}`
- raw: `{% raw %}{% endraw %}`
- unless: `{% unless this %}{% endunless %}`
- when: `{% when this %}`

### Completions

#### Tags

* page
    - page.categories
    - page.content
    - page.date
    - page.excerpt
    - page.id
    - page.path
    - page.tags
    - page.title
    - page.url
* paginator
    - paginator.next_page
    - paginator.next_page_path
    - paginator.page
    - paginator.per_page
    - paginator.posts
    - paginator.previous_page
    - paginator.previous_page_path
    - paginator.total_pages
    - paginator.total_posts
* site
    - site.date
    - site.domain
    - site.feed_url
    - site.pages
    - site.permalink
    - site.posts
    - site.sitemap_url
    - site.time
    - site.related_posts
    - site.categories
    - site.tags

#### Filters

- append
- array_to_sentence_string
- camelize
- capitalize
- cgi_escape
- date
- date_to_long_string
- date_to_rfc822
- date_to_string
- date_to_xmlschema
- divided_by
- downcase
- escape
- first
- group_by
- handleize
- highlight_active_tag
- img_tag
- join
- json
- jsonify
- last
- link_to
- markdownify
- minus
- money
- money_with_currency
- money_without_currency
- newline_to_br
- number_of_words
- pluralize
- plus
- prepend
- remove
- remove_first
- replace
- replace_first
- script_tag
- size
- sort
- split
- strip_html
- strip_newlines
- stylesheet_tag
- textilize
- times
- trim
- truncate
- truncatewords
- upcase
- uri_escape
- weight_with_unit
- where
- xml_escape

### Build Systems

If desired, you can add a custom Jekyll build system to your Sublime projects. This allows you to create a specific build system for each Jekyll project you're working on. From what I can tell, a project-specific build system needs to be used, as opposed to a standard build system. This is because the `jekyll` CLT command must be run from the main Jekyll folder that contains the _config.yml file (which cannot be guaranteed to be the current project folder).

```python
{
    "build_systems":
    [
        // This will build your Jekyll site, and print a trace to the console
        {
            "name": "Jekyll",
            // Change this directory to match your top-level Jekyll project folder
            "working_dir": "/path/to/jekyll/project/root",
            "cmd": "jekyll build -t",
            "shell": true,
            "encoding": "UTF-8"
        }
    ]
}
```

Tests
-----

Feel free to open the files in [Tests](https://github.com/23maverick23/sublime-jekyll/tree/master/Tests) to view the syntax highlighting, snippets, and completions, and to test adding the date commands.

Thanks
------

Much of this package would not have been possible without the help (mostly unsolicited) of many community members and open source packages. A big part of my learning experience has been reviewing source code from some really great packages to get ideas for my own uses. I've listed some of those packages below - please visit them and use them as you see fit!

* [liquid-syntax-mode](https://github.com/siteleaf/liquid-syntax-mode) from siteleaf (the original fork for this project)
* [sublime-insertdate](https://github.com/FichteFoll/sublimetext-insertdate) from FichteFoll (basis of insert date commands)
* [Sublime-AdvancedNewFile](https://github.com/skuroda/Sublime-AdvancedNewFile) from skuroda (new post creation tips)
* [Gist](https://github.com/condemil/Gist) from condemil (new post creation tips)

License
-------

[LICENSE](LICENSE)

Changelog
---------

[CHANGELOG](CHANGELOG)

Contribute
----------

1. [Fork](https://github.com/23maverick23/sublime-jekyll/fork) this repo.
2. Create a branch `git checkout -b my_feature`
3. Commit your changes `git commit -am "Added Feature"`
4. Push to the branch `git push origin my_feature`
5. Open a [Pull Request](https://github.com/23maverick23/sublime-jekyll/pulls)
