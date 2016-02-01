Completions
===========

sublime-jekyll ships with a large number of auto-completions for helping you get things done more efficiently. Included are a number of standard Liquid template filters, as well as Jekyll specific filters and template variables.


Global Variables
----------------

========= =============
Trigger   Contents
========= =============
site      ``site``
page      ``page``
content   ``content``
paginator ``paginator``
========= =============


Site Variables
--------------

================== ======================
Trigger            Contents
================== ======================
site.categories    ``site.categories.$1``
site.collections   ``site.collections``
site.data          ``site.data.$1``
site.date          ``site.date``
site.domain        ``site.domain``
site.html_files    ``site.html_files``
site.members       ``site.members``
site.pages         ``site.pages``
site.posts         ``site.posts``
site.related_posts ``site.related_posts``
site.sitemap_url   ``site.sitemap_url``
site.source        ``site.source``
site.static_files  ``site.static_files``
site.tags          ``site.tags.$1``
site.time          ``site.time``
site.url           ``site.url``
================== ======================


Page Variables
--------------

=============== ===================
Trigger         Contents
=============== ===================
page.categories ``page.categories``
page.content    ``page.content``
page.date       ``page.date``
page.excerpt    ``page.excerpt``
page.id         ``page.id``
page.next       ``page.next``
page.path       ``page.path``
page.previous   ``page.previous``
page.tags       ``page.tags``
page.title      ``page.content``
page.url        ``page.url``
=============== ===================


Paginator Variables
-------------------

============================ ================================
Trigger                      Contents
============================ ================================
paginator.next_page          ``paginator.next_page``
paginator.next_page_path     ``paginator.next_page_path``
paginator.page               ``paginator.page``
paginator.per_page           ``paginator.per_page``
paginator.posts              ``paginator.posts``
paginator.previous_page      ``paginator.previous_page``
paginator.previous_page_path ``paginator.previous_page_path``
paginator.total_pages        ``paginator.total_pages``
paginator.total_posts        ``paginator.total_posts``
============================ ================================


Forloop Variables
-----------------

=============== ===================
Trigger         Contents
=============== ===================
forloop.first   ``forloop.first``
forloop.index0  ``forloop.index0``
forloop.index   ``forloop.index``
forloop.last    ``forloop.last``
forloop.length  ``forloop.length``
forloop.rindex0 ``forloop.rindex0``
forloop.rindex  ``forloop.rindex``
=============== ===================


Standard Filters
----------------

============== ======================
Trigger        Contents
============== ======================
append         ``append:'$1'``
capitalize     ``capitalize``
date           ``date:'$1'``
divided_by     ``divided_by:$1``
downcase       ``downcase``
escape         ``escape``
escape_once    ``escape_once``
first          ``first``
join           ``join``
last           ``last``
map            ``map``
minus          ``minus:$1``
modulo         ``modulo:$1``
newline_to_br  ``newline_to_br``
plus           ``plus:$1``
prepend        ``prepend:'$1'``
remove         ``remove:'$1'``
remove_first   ``remove_first:'$1'``
replace        ``replace:'$1'``
replace_first  ``replace_first:'$1'``
round          ``round``
size           ``size``
slice          ``slice:$2, $1``
sort           ``sort``
split          ``split:'$1'``
strip_html     ``strip_html``
strip_newlines ``strip_newlines``
times          ``times:$1``
truncate       ``truncate:$2, '$1'``
truncatewords  ``truncatewords``
upcase         ``upcase``
============== ======================


Handy Filters
-------------

======================== ============================
Trigger                  Contents
======================== ============================
array_to_sentence_string ``array_to_sentence_string``
cgi_escape               ``cgi_escape``
date_to_long_string      ``date_to_long_string``
date_to_rfc822           ``date_to_rfc822``
date_to_string           ``date_to_string``
date_to_xmlschema        ``date_to_xmlschema``
group_by                 ``group_by:'$1'``
jsonify                  ``jsonify``
markdownify              ``markdownify``
number_of_words          ``number_of_words``
scssify                  ``scssify``
sassisfy                 ``sassisfy``
slugify                  ``slugify``
sort                     ``sort``
textilize                ``textilize``
uri_escape               ``uri_escape``
where                    ``where:'$2','$1'``
xml_escape               ``xml_escape``
======================== ============================
