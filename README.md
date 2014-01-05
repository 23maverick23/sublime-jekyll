# sublime-jekyll

A Sublime Text package for [Jekyll](http://jekyllrb.com/) static sites. This is a fork of the [liquid-syntax-mode](https://github.com/siteleaf/liquid-syntax-mode) repo from [siteleaf](https://github.com/siteleaf).

## What's Included
### Syntaxes
* HTML (Jekyll)
* JSON (Jekyll)
* Markdown (Jekyll)

### Snippets
* assign: `{% assign a = b %}`
* capture: `{% capture %}{% endcapture %}`
* case: `{% case %}{% endcase %}`
* comment: `{% comment %}{% endcomment %}`
* va: `{{ variable }}`
* cycle: `{% cycle %}`
* elsif: `{% elsif %}`
* for: `{% for item in list %}{% endfor %}`
* front-matter:

    ```yaml
    ---
    layout: post
    title:
    date: YYYY-MM-DD
    category:
    tags: []
    ---
    ```
* gist: `{% gist url %}`
* highlight: `{% highlight syntax|linenos %}{% endhighlight %}`
* if: `{% if this %}{% endif %}`
* ifelse: `{% if this %}{% else %}{% endif %}`
* include: `{% include this.html %}`
* post_url: `{% post_url url %}`
* raw: `{% raw %}{% endraw %}`
* unless: `{% unless this %}{% endunless %}`
* when: `{% when this %}`

### Completions
#### Tags
* page
    * page.categories
    * page.content
    * page.date
    * page.excerpt
    * page.id
    * page.path
    * page.tags
    * page.title
    * page.url
* paginator
    * paginator.next_page
    * paginator.next_page_path
    * paginator.page
    * paginator.per_page
    * paginator.posts
    * paginator.previous_page
    * paginator.previous_page_path
    * paginator.total_pages
    * paginator.total_posts
* site
    * site.date
    * site.domain
    * site.feed_url
    * site.pages
    * site.permalink
    * site.posts
    * site.sitemap_url
    * site.time
    * site.related_posts
    * site.categories
    * site.tags

#### Filters
* append
* array_to_sentence_string
* camelize
* capitalize
* cgi_escape
* date
* date_to_long_string
* date_to_rfc822
* date_to_string
* date_to_xmlschema
* divided_by
* downcase
* escape
* first
* handleize
* highlight_active_tag
* img_tag
* join
* json
* jsonify
* last
* link_to
* markdownify
* minus
* money
* money_with_currency
* money_without_currency
* newline_to_br
* number_of_words
* pluralize
* plus
* prepend
* remove
* remove_first
* replace
* replace_first
* script_tag
* size
* split
* strip_html
* strip_newlines
* stylesheet_tag
* textilize
* times
* trim
* truncate
* truncatewords
* upcase
* uri_escape
* weight_with_unit
* xml_escape

## Installation
### Manual
[Clone](https://github.com/23maverick23/sublime-jekyll.git) or [download](https://github.com/23maverick23/sublime-jekyll/archive/master.zip) the contents of this repo into your Sublime Text `Packages` folder.

* OS X: `~/Library/Application\ Support/Sublime\ Text\ 3/Packages`
* Windows: `%APPDATA%\Sublime Text 3\Packages`
* Linux: `~/.config/sublime-text-3/Packages`

### Package Control
coming soon...

## Tests
Feel free to open the files in [Tests](https://github.com/23maverick23/sublime-jekyll/tree/master/Tests) to view the syntax highlighting, snippets, and completions.

## License
[LICENSE](LICENSE)

## Changelog
[CHANGELOG](CHANGELOG.md)

## Contribute
1. [Fork](https://github.com/23maverick23/sublime-jekyll/fork) this repo.
2. Create a branch `git checkout -b my_feature`
3. Commit your changes `git commit -am "Added Feature"`
4. Push to the branch `git push origin my_feature`
5. Open a [Pull Request](https://github.com/23maverick23/sublime-jekyll/pulls)
