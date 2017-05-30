Completions
===========

sublime-jekyll ships with a large number of auto-completions for helping you get things done more efficiently. Included are a number of standard Liquid template filters, as well as Jekyll specific filters and template variables.

.. note::

    If wanted, you can update your ``Markdown.sublime-settings`` file to include some overrides to trigger completions in Markdown files. Add ``"auto_complete_selector": "text.html.markdown"`` and ``"auto_complete_triggers": [ {"selector": "text.html.markdown"} ]`` as new key:value pairs.


Global Variables
----------------

========= =============
Trigger   Contents
========= =============
site      ``site``
page      ``page``
layout    ``layout``
content   ``content``
paginator ``paginator``
========= =============


Site Variables
--------------

================== ======================
Trigger            Contents
================== ======================
site.time          ``site.time``
site.pages         ``site.pages``
site.posts         ``site.posts``
site.related_posts ``site.related_posts``
site.static_files  ``site.static_files``
site.html_pages    ``site.html_pages``
site.html_files    ``site.html_files``
site.collections   ``site.collections``
site.data          ``site.data.$1``
site.documents     ``site.documents.$1``
site.categories    ``site.categories.$1``
site.tags          ``site.tags.$1``
================== ======================


Page Variables
--------------

=============== ===================
Trigger         Contents
=============== ===================
page.content    ``page.content``
page.title      ``page.content``
page.excerpt    ``page.excerpt``
page.url        ``page.url``
page.date       ``page.date``
page.id         ``page.id``
page.categories ``page.categories``
page.tags       ``page.tags``
page.path       ``page.path``
page.next       ``page.next``
page.previous   ``page.previous``
=============== ===================


Paginator Variables
-------------------

============================ ================================
Trigger                      Contents
============================ ================================
paginator.per_page           ``paginator.per_page``
paginator.posts              ``paginator.posts``
paginator.total_posts        ``paginator.total_posts``
paginator.total_pages        ``paginator.total_pages``
paginator.page               ``paginator.page``
paginator.previous_page      ``paginator.previous_page``
paginator.previous_page_path ``paginator.previous_page_path``
paginator.next_page          ``paginator.next_page``
paginator.next_page_path     ``paginator.next_page_path``
============================ ================================


Forloop Variables
-----------------

=============== ===================
Trigger         Contents
=============== ===================
forloop.first   ``forloop.first``
forloop.index   ``forloop.index``
forloop.index0  ``forloop.index0``
forloop.last    ``forloop.last``
forloop.length  ``forloop.length``
forloop.rindex  ``forloop.rindex``
forloop.rindex0 ``forloop.rindex0``
=============== ===================


Array Filters
-------------

============== ======================
Trigger        Contents
============== ======================
join           ``join``
first          ``first``
last           ``last``
concat         ``concat``
index          ``index``
map            ``map``
reverse        ``reverse``
size           ``size``
sort           ``sort``
uniq           ``uniq``
============== ======================


String Filters
---------------

============== ======================
Trigger        Contents
============== ======================
append         ``append:'$1'``
capitalize     ``capitalize``
downcase       ``downcase``
escape         ``escape``
newline_to_br  ``newline_to_br``
pluralize      ``pluralize``
prepend        ``prepend:'$1'``
remove         ``remove:'$1'``
remove_first   ``remove_first:'$1'``
replace        ``replace:'$1'``
replace_first  ``replace_first:'$1'``
slice          ``slice:$2, $1``
split          ``split:'$1'``
strip          ``strip``
lstrip         ``lstrip``
rstrip         ``rstrip``
strip_html     ``strip_html``
strip_newlines ``strip_newlines``
truncate       ``truncate:$2, '$1'``
truncatewords  ``truncatewords``
upcase         ``upcase``
============== ======================


Math Filters
------------

============== ======================
Trigger        Contents
============== ======================
abs            ``abs:$1``
ceil           ``ceil:$1``
divided_by     ``divided_by:$1``
floor          ``floor``
minus          ``minus:$1``
plus           ``plus:$1``
round          ``round``
times          ``times:$1``
modulo         ``modulo:$1``
============== ======================


Handy Filters
-------------

======================== ============================
Trigger                  Contents
======================== ============================
relative_url             ``relative_url``
absolute_url             ``absolute_url``
date_to_xmlschema        ``date_to_xmlschema``
date_to_rfc822           ``date_to_rfc822``
date_to_string           ``date_to_string``
date_to_long_string      ``date_to_long_string``
where                    ``where:'$2','$1'``
where_exp                ``where_exp:'$2','$1'``
group_by                 ``group_by:'$1'``
group_by_exp             ``group_by_exp:'$1'``
xml_escape               ``xml_escape``
cgi_escape               ``cgi_escape``
uri_escape               ``uri_escape``
number_of_words          ``number_of_words``
array_to_sentence_string ``array_to_sentence_string``
markdownify              ``markdownify``
smartify                 ``smartify``
scssify                  ``scssify``
sassisfy                 ``sassisfy``
slugify                  ``slugify``
jsonify                  ``jsonify``
normalize_whitespace     ``normalize_whitespace``
sample                   ``sample``
to_integer               ``to_integer``
push                     ``push``
pop                      ``pop``
shift                    ``shift``
unshift                  ``unshift``
inspect                  ``inspect``
date                     ``date``
======================== ============================
