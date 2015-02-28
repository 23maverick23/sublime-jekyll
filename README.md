sublime-jekyll
==============

A Sublime Text package for [Jekyll](http://jekyllrb.com/) static sites. This package should help maintaining Jekyll sites and posts easier by providing access to new post/draft shortcuts, key template tags and filters, as well as common completions and a current date/datetime command (for dating posts).

### New in this Release

The 2.2 release introduces a new feature for faster post and draft creation. If you don't want to specify your folder paths, or you don't create a Sublime project for each blog you manage, you can enable a new setting `automatically_find_paths`. Setting this key to `true` will tell sublime-jekyll to search all folders in the active view for any `_posts` or `_drafts` directories. If none are found, it falls back to the normal project or user settings.

For a history of changes or previous releases, have a look at the more detailed [CHANGELOG ➭](CHANGELOG)


Installation
------------

### Package Control

You can install this package using [Package Control](https://sublime.wbond.net/packages/Jekyll) from wbond.net.

* Press `ctrl+shift+p` (Windows/Linux) or `command+shift+p` (OS X) to bring up the Command Palette (or use _Tools > Command Palette_ menu)
* Type to search for the `Package Control: Install Package` command
* Search packages for **Jekyll** and hit `enter` to install
* **NOTE:** You may need to restart in order to use this package

### Manual

[Clone ↻](https://github.com/23maverick23/sublime-jekyll.git) or [download ⬇](https://github.com/23maverick23/sublime-jekyll/archive/master.zip) the contents of this repo into your Sublime Text `Packages` folder.

* OS X: `~/Library/Application\ Support/Sublime\ Text\ 3/Packages`
* Windows: `%APPDATA%\Sublime Text 3\Packages`
* Linux: `~/.config/sublime-text-3/Packages`

### After Installing...

After installing this package, make sure you configure your User settings file. The most important piece of this is to set your `posts_path` location. This can also be set on a per-project basis later if you have multiple Jekyll sites you wish to manage.

```python
{

    // This should point to your "_posts" directory.
    // NOTE: This should be an absolute path. Also, the path should
    // match your system convention. For example, Windows machines should
    // have a path similar to "C:\\Users\\username\\site\\_posts".
    // *nix systems should have a path similar to "/Users/username/site/_posts".
    "posts_path": "",

    // This should point to your "_drafts" directory.
    // NOTE: This should be an absolute path. Also, the path should
    // match your system convention. For example, Windows machines should
    // have a path similar to "C:\\Users\\username\\site\\_drafts".
    // *nix systems should have a path similar to "/Users/username/site/_drafts".
    "drafts_path": "",

    // If you have multiple Jekyll blogs, but don't use Sumblime Projects,
    // you can optionally have sublime-jekyll look for the `_posts` or `_drafts`
    // folders open in your sidebar. This should have a value of true or false.
    "automatically_find_paths": false,

    // This string value should represent the default syntax for a new post.
    // Valid options are: "Markdown", "Textile"
    "default_post_syntax": "Markdown",

    /** *****************************************************************************
     * Post Front-matter Defaults
     *
     * Set these values to make your life easier when composing new posts. This is
     * similar to setting your defaults as part of the `_config.yml` file:
     *
     * http://jekyllrb.com/docs/configuration/#front-matter-defaults
     * ******************************************************************************
     */

    // This string value should represent the default layout for new posts.
    "default_post_layout": "",

    // This value should represent the default categories for new posts.
    // Each category should be entered as a list item in string format
    // with commas separating values ["cat1", "cat2"]. To remove this key
    // from your front-matter completely, pass a value of `null`.
    "default_post_categories": [],

    // This value should represent the default tags for new posts.
    // Each tag should be entered as a list item in string format
    // with commas separating values ["tag1", "tag2"]. To remove this key
    // from your front-matter completely, pass a value of `null`.
    "default_post_tags": [],

    // A boolean specifying if you want new posts to be marked as published.
    // To remove this key from your front-matter completely, pass a value of `null`.
    "default_post_published": true,

    // If you need to add additional front-matter `key: value` information to
    // your posts, you can store them in a dictionary object using a format
    // like {"foo": "bar", "baz": "qux"}. This dictionary will be appended to
    // any of the enabled default keys above (Reminder: the `title` and `layout`
    // keys will always be included, so **DO NOT** include them in the extras dictionary).
    "default_post_extras": {},

    /** ***********************************************************************************
     * If for some reason you want to change the way either the date
     * or the datetime string is formatted, you can override those formats
     * here using valid Python datetime.strftime() format codes.
     *
     * If you need a refresher on these codes, have a look at the Python
     * documentation found here:
     *
     * http://docs.python.org/2/library/datetime.html#strftime-and-strptime-behavior
     * ******************************************************************************
     */

    // A valid Python strftime string
    "insert_date_format": "%Y-%m-%d",

    // A valid Python strftime string
    "insert_datetime_format": "%Y-%m-%d %H:%M:%S"

}

```

For per-project settings, make sure you add your Jekyll settings correctly (read [Issue #16](https://github.com/23maverick23/sublime-jekyll/issues/16) if you have questions on formatting).

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

What's Included
---------------

### Screenshots

![nsoa_console.png](https://github.com/23maverick23/sublime-jekyll/raw/master/Screenshots/sublime_jekyll_screenshot.png "sublime-jekyll")

> Theme: [Centurion](https://sublime.wbond.net/packages/Theme%20-%20Centurion)

> Color Scheme: [Tomorrow Night](https://sublime.wbond.net/packages/Tomorrow%20Color%20Schemes)

> Font: [Source Code Pro](https://github.com/adobe/source-code-pro)

### Syntaxes

* HTML (Jekyll)
* JSON (Jekyll)
* Markdown (Jekyll)
* Textile (Jekyll)

### Commands & Key Bindings

* Jekyll: New post => `CMD+K, CMD+P`
* Jekyll: New draft => `CMD+K, CMD+F`
* Jekyll: Insert current date
* Jekyll: Insert current datetime
* Jekyll: Open post...
* Jekyll: Open draft...
* Jekyll: Promote draft to post...

There are default key bindings for some commands above, however you can re-assign them in your user key bindings file (_Preferences > Package Settings > Jekyll > Key Bindings – User_).

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
    published: true
    categories: []
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

Feel free to open the files in [Tests ➭](https://github.com/23maverick23/sublime-jekyll/tree/master/Tests) to view the syntax highlighting, snippets, and completions, and to test adding the date commands.

Thanks
------

Much of this package would not have been possible without the help (mostly unsolicited) of many community members and open source packages. A big part of my learning experience has been reviewing source code from some really great packages to get ideas for my own uses. I've listed some of those packages below - please visit them and use them as you see fit!

* [liquid-syntax-mode](https://github.com/siteleaf/liquid-syntax-mode) from siteleaf (the original fork for this project)
* [sublime-insertdate](https://github.com/FichteFoll/sublimetext-insertdate) from FichteFoll (basis of insert date commands)
* [Sublime-AdvancedNewFile](https://github.com/skuroda/Sublime-AdvancedNewFile) from skuroda (new post creation tips)
* [Gist](https://github.com/condemil/Gist) from condemil (new post creation tips)

License
-------

[LICENSE ➭](LICENSE)

Changelog
---------

[CHANGELOG ➭](CHANGELOG)

Issues
------

[![Issue Stats](http://issuestats.com/github/23maverick23/sublime-jekyll/badge/issue?style=flat)](http://issuestats.com/github/23maverick23/sublime-jekyll)

You can log issues from the menu at right, or by [clicking here](https://github.com/23maverick23/sublime-jekyll/issues). Curious about responsiveness? Check out our [Issue Stats](http://issuestats.com/github/23maverick23/sublime-jekyll)!

Contribute
----------

[![Issue Stats](http://issuestats.com/github/23maverick23/sublime-jekyll/badge/pr?style=flat)](http://issuestats.com/github/23maverick23/sublime-jekyll)

Read my [contributing guide ➭](CONTRIBUTING.md)

**Thanks to the current contributors!**

* fk128
* Kimi
* Marcos Ojeda
* Robert Holak
* svensvenson

> [View the contributor graph ➭](https://github.com/23maverick23/sublime-jekyll/graphs/contributors)
