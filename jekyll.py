from datetime import datetime
import functools
import os
import re
import shutil
import sys
import traceback

import sublime
import sublime_plugin

PY3 = sys.version > '3'
ST3 = sublime.version() >= '3000'


## Exception Decorator                                                       ##
## ------------------------------------------------------------------------- ##
# This function allows for custom exceptions while preserving the stacktrace. #
# See discussion on Stack Overflow here: http://stackoverflow.com/a/9006442   #
## ------------------------------------------------------------------------- ##

class MissingPathException(Exception):
    pass


def catch_errors(fn):
    @functools.wraps(fn)
    def _fn(*args, **kwargs):
        try:
            return fn(*args, **kwargs)

        except MissingPathException:
            sublime.error_message('Jekyll: Unable to find path information for Jekyll!')
            user_settings_path = os.path.join(sublime.packages_path(), 'User', 'Jekyll.sublime-settings')
            if not os.path.exists(user_settings_path):
                default_settings_path = os.path.join(sublime.packages_path(), 'Jekyll', 'Jekyll.sublime-settings')
                shutil.copy(default_settings_path, user_settings_path)
            sublime.active_window().open_file(user_settings_path)

        except:
            traceback.print_exc()
            sublime.error_message('Jekyll: unknown error (please, report a bug!)')

    return _fn


def get_setting(view, key, default=None):
    """
    Get a Sublime Text setting value, starting in the project-specific
    settings file, then the user-specific settings file, and finally
    the package-specific settings file. Also accepts an optional default.

    """
    try:
        settings = view.settings()
        if settings.has('Jekyll'):
            s = settings.get('Jekyll').get(key)
            if s:
                return s
            else:
                pass
        else:
            pass
    except:
        pass
    global_settings = sublime.load_settings('Jekyll.sublime-settings')
    return global_settings.get(key, default)


def get_syntax_path(view, syntax='Markdown'):
    """
    Sets the view syntax.

    """
    full_syntax = os.path.join('Jekyll', 'Syntaxes', '{0} (Jekyll).tmLanguage'.format(syntax))

    if PY3:
        syntax_path = os.path.join('Packages', full_syntax)

        if sublime.platform() == 'windows':
            syntax_path = full_syntax.replace('\\', '/')
        try:
            sublime.load_resource(syntax_path)
            view.set_syntax_file(syntax_path)
        except:
            pass
    else:
        syntax_path = os.path.join(sublime.packages_path(), full_syntax)
        if os.path.exists(syntax_path):
            view.set_syntax_file(syntax_path)


def find_dir_path(window, dir_name):
    """
    Attempts to find a named directory in a given sublime window.

    Params:
        window: a Sublime window object
        dir_name: a string directory name
    Returns:
        {Array} array of path strings

    """
    all_dirs = []

    for folder in window.folders():
        for root, dirs, files in os.walk(folder):
            dirs[:] = [d for d in dirs if not d[0] == '.']

            if all(x in dirs for x in [dir_name]):
                all_dirs.append(os.path.abspath(os.path.join(root, dir_name)))

    return all_dirs


class JekyllNewPostBase(sublime_plugin.WindowCommand):
    """
    A Sublime window command base class for creating Jekyll posts.

    """
    def doCommand(self):
        post_type = 'draft' if self.IS_DRAFT else 'post'
        self.window.show_input_panel(
            'Jekyll {0} title:'.format(post_type),
            '',
            self.title_input,
            None,
            None
        )

    @catch_errors
    def determine_path(self, p, d):
        a = get_setting(self.window.active_view(), 'automatically_find_paths', False)

        if not a:
            if not p or p == '':
                raise MissingPathException
            return p

        elif a:
            self.dirs = find_dir_path(self.window, d)

            if not self.dirs:
                # there were no directories found, fallback to settings
                if not p or p == '':
                    raise MissingPathException
                return p

            elif self.dirs and len(self.dirs) > 1:
                # more than one directory was found, but we only support one currently
                # TODO: figure out how to support many with a quick_panel?
                msg = (
                    'More than one folder was found in the active view:\n{0}'
                    '\nClick confirm to use the first folder in the list, '
                    'otherwise cancel and use Project settings instead'.format('\n'.join(self.dirs))
                )

                if sublime.ok_cancel_dialog(msg, 'Confirm'):
                    return self.dirs[0]
                else:
                    return None

            elif self.dirs and len(self.dirs) == 1:
                # only one directory was found, so use it
                return self.dirs[0]

    @catch_errors
    def posts_path_string(self):
        p = get_setting(self.window.active_view(), 'posts_path')
        return self.determine_path(p, '_posts')

    @catch_errors
    def drafts_path_string(self):
        p = get_setting(self.window.active_view(), 'drafts_path')
        return self.determine_path(p, '_drafts')

    def create_file(self, filename):
        base, filename = os.path.split(filename)
        if filename != '':
            creation_path = os.path.join(base, filename)
            open(creation_path, 'a').close()

    def clean_title_input(self, title, draft=False):
        t = title.lower()
        t_str = re.sub(r'[^\w -]', '', t)
        t_str = re.sub(r' |_', '-', t_str)
        d = datetime.today()
        POST_DATE_FORMAT = '%Y-%m-%d'
        d_str = d.strftime(POST_DATE_FORMAT)
        return d_str + '-' + t_str if not draft else t_str

    def create_post_frontmatter(self, title):
        view = self.window.active_view()
        POST_CATEGORIES = get_setting(view, 'default_post_categories')
        POST_TAGS = get_setting(view, 'default_post_tags')
        POST_PUBLISHED = get_setting(view, 'default_post_published', True)
        POST_EXTRAS = get_setting(view, 'default_post_extras', {})

        POST_TITLE_STR = str(title)
        POST_LAYOUT_STR = str(get_setting(view, 'default_post_layout'))

        POST_CATEGORIES_STR = str(
            'categories: {0}\n'.format(POST_CATEGORIES) if POST_CATEGORIES is not None else ''
        )
        POST_TAGS_STR = str(
            'tags: {0}\n'.format(POST_TAGS) if POST_TAGS is not None else ''
        )
        POST_PUBLISHED_STR = str(
            'published: {0}\n'.format(POST_PUBLISHED) if POST_PUBLISHED is not None else ''
        )

        def pretty_walk(settings_dict):
            """
            Walks through a multi-level dictionary and returns
            a YAML-like string.

            :param settings_dict: a dictionary object
            :returns: formatted string
            """
            s = []

            def walk(d, indent=-1):
                """
                Walk through a dictionary of key/values
                and append the results in a placeholder list.

                :param d: dictionary object
                :param indent: the starting indent value; default -1
                """
                try:
                    for key, value in d.items():
                        if isinstance(value, dict):
                            s.append('{0}{1}:\n'.format('\t' * (indent + 1), key))
                            walk(value, indent + 1)
                        else:
                            s.append('{0}{1}: {2}\n'.format('\t' * (indent + 1), key, value))
                except Exception as e:
                    print('Jekyll: Settings parsing error - {0}'.format(e))
                    return

            walk(settings_dict)
            return ''.join(s)

        POST_EXTRAS_STR = pretty_walk(POST_EXTRAS)

        frontmatter = (
            '---\n'
            'layout: {0}\n'
            'title: {1}\n'
            '{2}'
            '{3}'
            '{4}'
            '{5}'
            '\n---\n\n'
        ).format(
            POST_LAYOUT_STR,
            POST_TITLE_STR,
            POST_CATEGORIES_STR,
            POST_TAGS_STR,
            POST_PUBLISHED_STR,
            POST_EXTRAS_STR
        )
        return frontmatter

    @catch_errors
    def title_input(self, title):
        if self.IS_DRAFT:
            post_dir = self.drafts_path_string()
        else:
            post_dir = self.posts_path_string()

        if not post_dir:
            raise MissingPathException

        syntax = get_setting(self.window.active_view(), 'default_post_syntax', 'Markdown')
        if syntax == 'Textile':
            file_ext = '.textile'
        elif syntax == 'Markdown':
            file_ext = '.md'
        else:
            file_ext = '.txt'

        clean_title = self.clean_title_input(title, self.IS_DRAFT) + file_ext
        full_path = os.path.join(post_dir, clean_title)

        if os.path.lexists(full_path):
            sublime.error_message('Jekyll: File already exists at "{0}"'.format(full_path))
            return
        else:
            frontmatter = self.create_post_frontmatter(title)
            self.create_and_open_file(full_path, frontmatter)


class JekyllListPostsBase(JekyllNewPostBase):
    """
    A subclass for displaying Jekyll posts.

    """
    def callback(self, index):
        if index > -1 and type(self.posts[index]) is list:
            f = self.posts[index][1]
            syntax = self.get_syntax(self.posts[index][0])
            output_view = self.window.open_file(f)
            if syntax and syntax == 'Markdown' or syntax == 'Textile':
                get_syntax_path(output_view, syntax)
        else:
            self.posts = []

    def get_syntax(self, file):
        # Uses Github preferred file extensions as referenced here: http://superuser.com/a/285878
        f = file
        if (
            f.endswith('.markdown') or
            f.endswith('.mdown') or
            f.endswith('.mkdn') or
            f.endswith('.mkd') or
            f.endswith('.md')
        ):
            self.syntax = 'Markdown'
        elif f.endswith('.textile'):
            self.syntax = 'Textile'
        else:
            self.syntax = None

        return self.syntax


class JekyllOpenPostCommand(JekyllListPostsBase):
    """
    A subclass for displaying posts in the _posts directory.

    """

    syntax = None

    def run(self):
        self.posts = []
        path = self.posts_path_string()
        if os.path.isdir(path):
            for root, dirs, files in os.walk(path):
                for f in files:
                    if self.get_syntax(f):
                        fname = os.path.splitext(f)[0]
                        fpath = os.path.join(root, f)
                        self.posts.append([fname, fpath])
        else:
            self.posts.append(['Posts directory does not exist!'])

        if not len(self.posts) > 0:
            self.posts.append(['No posts found!'])

        self.posts.sort(key=lambda x: os.path.getmtime(x[1]), reverse=True)
        self.window.show_quick_panel(self.posts, self.callback)


class JekyllOpenDraftCommand(JekyllListPostsBase):
    """
    A subclass for displaying posts in the _drafts directory.

    """

    syntax = None

    def run(self):
        self.posts = []
        path = self.drafts_path_string()
        if os.path.isdir(path):
            for root, dirs, files in os.walk(path):
                for f in files:
                    if self.get_syntax(f):
                        fname = os.path.splitext(f)[0]
                        fpath = os.path.join(root, f)
                        self.posts.append([fname, fpath])
        else:
            self.posts.append(['Drafts directory does not exist!'])

        if not len(self.posts) > 0:
            self.posts.append(['No drafts found!'])

        self.posts.sort(key=lambda x: os.path.getmtime(x[1]), reverse=True)
        self.window.show_quick_panel(self.posts, self.callback)


class JekyllPromoteDraftCommand(JekyllListPostsBase):
    """
    A subclass for displaying posts in the _drafts directory.

    """

    syntax = None

    def move_post(self, index):
        p_path = self.posts_path_string()
        if index != -1 and type(self.posts[index]) is list:
            f = self.posts[index][1]
            syntax = self.get_syntax(self.posts[index][0])
            # return a list of directory names using platform specific separator
            dirlist = f.rsplit(os.sep)

            # check the draft name for a date
            # if you find one, replace it
            # if you don't find one, add it
            dirlist[-1] = re.sub(r'(^\d{4}-\d{2}-\d{2}-)', '', dirlist[-1])
            d = datetime.today()
            POST_DATE_FORMAT = '%Y-%m-%d'
            d_str = "{0}-".format(d.strftime(POST_DATE_FORMAT))
            dirlist[-1] = d_str + dirlist[-1]

            # return the full dirpath after the drafts folder
            spath = dirlist[dirlist.index('_drafts')+1:]
            # join the dirpath with the posts path
            fpath = os.path.join(p_path, *spath)
            # get the new, full folder path for the file
            bpath = os.path.split(fpath)[0]

            # if the folder path doesn't yet exist, create it recursively
            if not os.path.exists(bpath):
                os.makedirs(bpath)

            if not os.path.exists(fpath):
                shutil.move(f, fpath)

            output_view = self.window.open_file(fpath)
            if syntax:
                get_syntax_path(output_view, syntax)

        else:
            self.posts = []

    def run(self):
        self.posts = []
        d_path = self.drafts_path_string()
        if os.path.isdir(d_path):
            for root, dirs, files in os.walk(d_path):
                for f in files:
                    if self.get_syntax(f):
                        fname = os.path.splitext(f)[0]
                        fpath = os.path.join(root, f)
                        self.posts.append([fname, fpath])
        else:
            self.posts.append(['Drafts directory does not exist!'])

        if not len(self.posts) > 0:
            self.posts.append(['No drafts found!'])

        self.posts.sort(key=lambda x: os.path.getmtime(x[1]), reverse=True)
        self.window.show_quick_panel(self.posts, self.move_post)


class JekyllNewPostCommand(JekyllNewPostBase):
    """
    A subclass for creating new posts

    """
    IS_DRAFT = False

    def run(self):
        self.doCommand()

    def create_and_open_file(self, path, frontmatter):
        self.create_file(path)
        if not self.window.views():
            view = self.window.new_file()
        else:
            view = self.window.active_view()
        view.run_command(
            'jekyll_post_frontmatter',
            {
                'path': path,
                'frontmatter': frontmatter
            }
        )


class JekyllNewDraftCommand(JekyllNewPostBase):
    """
    A subclass for creating new draft posts.

    """
    IS_DRAFT = True

    def run(self):
        self.doCommand()

    def create_and_open_file(self, path, frontmatter):
        self.create_file(path)
        if not self.window.views():
            view = self.window.new_file()
        else:
            view = self.window.active_view()
        view.run_command(
            'jekyll_post_frontmatter',
            {
                'path': path,
                'frontmatter': frontmatter
            }
        )


class JekyllPostFrontmatterCommand(sublime_plugin.TextCommand):
    """
    Creates a new post using post defaults.

    """
    def run(self, edit, **args):
        view = self.view
        path = args.get('path')
        frontmatter = args.get('frontmatter', '-there was an error-')
        syntax = get_setting(view, 'default_post_syntax', 'Markdown')

        output_view = self.view.window().open_file(path)

        def update():
            if output_view.is_loading():
                if ST3:
                    sublime.set_timeout_async(update, 1)
                else:
                    sublime.set_timeout(update, 1)
            else:
                if PY3:
                    output_view.run_command(
                        'insert_snippet',
                        {
                            'contents': frontmatter
                        }
                    )
                else:
                    edit = output_view.begin_edit()
                    output_view.insert(edit, 0, frontmatter)
                    output_view.end_edit(edit)

                get_syntax_path(output_view, syntax)
                output_view.run_command('save')
        update()


class JekyllInsertDateCommand(sublime_plugin.TextCommand):
    """
    Prints todays date according to format in settings file.

    """
    def run(self, edit, **args):
        DEFAULT_FORMAT = '%Y-%m-%d'
        view = self.view
        date_format = get_setting(view, 'insert_date_format', '%Y-%m-%d')
        datetime_format = get_setting(view, 'insert_datetime_format', '%Y-%m-%d %H:%M:%S')

        try:
            d = datetime.today()
            if args['format'] and args['format'] == 'date':
                text = d.strftime(date_format)
            elif args['format'] and args['format'] == 'datetime':
                text = d.strftime(datetime_format)
            else:
                text = d.strftime(DEFAULT_FORMAT)

        except Exception as e:
            sublime.error_message('Jekyll: {0}: {1}'.format(type(e).__name__, e))
            return

        # Don't bother replacing selections if no text exists
        if text == '' or text.isspace():
            return

        # Do replacements
        for r in self.view.sel():
            # Insert when sel is empty to not select the contents
            if r.empty():
                self.view.insert(edit, r.a, text)
            else:
                self.view.replace(edit, r, text)
