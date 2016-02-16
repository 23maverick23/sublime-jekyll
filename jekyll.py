# -*- coding: utf-8 -*-

import imghdr
import os
import re
import sublime
import sublime_plugin
import sys
import traceback
import uuid

from datetime import datetime
from functools import wraps

try:
    import simple_json as json
except ImportError:
    import json


## ********************************************************************************************** ##
#  BEGIN STATIC VARIABLES
## ********************************************************************************************** ##


ST3 = sublime.version() >= '3000'
DEBUG = False
ALLOWED_MARKUPS = ('Markdown', 'Textile', 'HTML', )
POST_DATE_FORMAT = '%Y-%m-%d'

settings = sublime.load_settings('Jekyll.sublime-settings')

if settings.has('jekyll_debug') and settings.get('jekyll_debug') is True:
    DEBUG = True


if ST3:
    from .send2trash import send2trash
else:
    from send2trash import send2trash


## ********************************************************************************************** ##
#  BEGIN GLOBAL METHODS
## ********************************************************************************************** ##


def plugin_loaded():
    """

    """
    if DEBUG:
        UTC_TIME = datetime.utcnow()
        PYTHON = sys.version_info[:3]
        VERSION = sublime.version()
        PLATFORM = sublime.platform()
        ARCH = sublime.arch()
        PACKAGE = sublime.packages_path()
        INSTALL = sublime.installed_packages_path()

        message = (
            'Jekyll debugging mode enabled...\n\n'
            '\tUTC Time: {time}\n'
            '\tSystem Python: {python}\n'
            '\tSystem Platform: {plat}\n'
            '\tSystem Architecture: {arch}\n'
            '\tSublime Version: {ver}\n'
            '\tSublime Packages Path: {package}\n'
            '\tSublime Installed Packages Path: {install}\n'
        ).format(time=UTC_TIME, python=PYTHON, plat=PLATFORM, arch=ARCH,
                 ver=VERSION, package=PACKAGE, install=INSTALL)

        sublime.status_message('Jekyll: Debugging enabled...')
        debug('Plugin successfully loaded.', prefix='\n\nJekyll', level='info')
        debug(message, prefix='Jekyll', level='info')


def plugin_unloaded():
    if DEBUG:
        debug('Plugin successfully unloaded.\n\n', prefix='Jekyll', level='info')


def debug(message, prefix='Jekyll', level='debug'):
    """Console print utility method.

    Prints a formatted console entry to the Sublime Text console
    if debugging is enabled in the User settings file.

    Args:
        message (string): A message to print to the console
        prefix (string): An optional prefix
        level (string): One of debug, info, warning, error [Default: debug]

    Return:
        string: Issue a standard console print command.

    """
    if DEBUG:
        print('{prefix}: [{level}] {message}'.format(
            message=message,
            prefix=prefix,
            level=level
        ))


def catch_errors(fn):
    """Generic function decorator for catching exceptions.

    Use this to primarily catch and alert the user to path issues
    which are needed for nearly every command.

    Args:
        fn (func): A function

    Returns:
        bool: Description of return value

    """
    @wraps(fn)
    def _fn(*args, **kwargs):
        try:
            return fn(*args, **kwargs)

        except MissingPathException:
            debug('Unable to resolve path information!', prefix='Jekyll', level='error')
            message = (
                'Jekyll: Unable to resolve path information!\n\n'
                'Please double-check that you have defined absolute '
                'paths to your Jekyll directories, or that you have '
                'enabled the `jekyll_auto_find_paths` setting.\n\n'
                'If you have set your path settings correctly, please '
                'copy the console output and create a new issue.\n'
            )
            sublime.error_message(message)

        except:
            debug('Unexpected error. Stack trace:\n\t{stack}'.format(stack=traceback.print_exc()),
                prefix='Jekyll', level='error')
            message = (
                'Jekyll: Oops! - this is a bit embarassing\n\t\t¯\_(ツ)_/¯ \n\n'
                'You\'ve encountered an unexpected error, which likely '
                'means you\'ve found a bug in our code. It would be great '
                'if you could copy any related console output into a new '
                'issue and send it over to us. We\'ll take a look and get '
                'back to you as soon as we can. Thanks!\n'
            )
            sublime.error_message(message)

    return _fn


def get_setting(view, key, default=None):
    """Returns a specific setting key value or default.

    Get a Sublime Text setting value, starting in the project-specific
    settings file, then the user-specific settings file, and finally
    the package-specific settings file. Also accepts an optional default.

    Args:
        view (obj): A Sublime view object
        key (string): A settings dictionary key

    Returns:
        bool: Description of return value

    """
    try:
        debug('Getting key "{key}" from settings.'.format(key=key))

        settings = view.settings()
        if settings.has('Jekyll'):
            s = settings.get('Jekyll').get(key)

            if s and s is not None:
                return s

            else:
                pass

        else:
            pass

    except:
        pass

    global_settings = sublime.load_settings('Jekyll.sublime-settings')
    return global_settings.get(key, default)


def find_dir_path(window, dir_name):
    """Find a named directory in a given Sublime window.

    Searches the folder tree of the current window for
    a named path and returns any potential matches.

    Args:
        window (obj): A Sublime window object
        dir_name (string): A directory name

    Returns:
        array: An array of potential path string matches

    """
    all_dirs = []
    debug('Searching for directory "{name}" in folder tree.'.format(name=dir_name))

    for folder in window.folders():

        for root, dirs, files in os.walk(folder):
            dirs[:] = [d for d in dirs if not d[0] == '.']

            if all(x in dirs for x in [dir_name]):
                all_dirs.append(os.path.abspath(os.path.join(root, dir_name)))

    debug('Found these sub-folder(s) in the sidebar: {0}'.format(all_dirs))
    return all_dirs


def clean_title_input(title, draft=False):
    """Convert a string into a valide Jekyll filename.

    Remove non-word characters, replace spaces and underscores with dashes,
    and add a date stamp if the file is marked as a Post, not a Draft.

    Args:
        title (string): A string based title
        draft (bool): A boolean indicating that the file is a draft

    Returns:
        string: a cleaned title for saving a new Jekyll post file

    """
    title_clean = title.lower()
    title_clean = re.sub(r'[^\w -]', '', title_clean)
    title_clean = re.sub(r' |_', '-', title_clean)

    today = datetime.today()
    title_date = today.strftime('%Y-%m-%d')

    return title_date + '-' + title_clean if not draft else title_clean


def create_file(path):
    """Create a new file using the directory path of the filename.

    Args:
        path (string): A full path string for the new file

    Returns:
        none

    """
    filename = os.path.split(path)[1]

    if filename and filename != '':
        open(path, 'a').close()


## ********************************************************************************************** ##
#  BEGIN BASE CLASSES
## ********************************************************************************************** ##

class MissingPathException(Exception):
    pass


class JekyllWindowBase(sublime_plugin.WindowCommand):
    """Abstract base class for Jekyll window commands.

    """
    markup = None


    def posts_path_string(self):
        p = get_setting(self.window.active_view(), 'jekyll_posts_path')
        return self.determine_path(p, '_posts')


    def drafts_path_string(self):
        p = get_setting(self.window.active_view(), 'jekyll_drafts_path')
        return self.determine_path(p, '_drafts')


    def uploads_path_string(self):
        p = get_setting(self.window.active_view(), 'jekyll_uploads_path')
        return self.determine_path(p, 'uploads')


    def templates_path_string(self):
        # TODO: allow for user-specific or project-specific template directories?
        # TODO: specify where every template is saved, which slows down workflow?
        return os.path.join(sublime.packages_path(), 'User', 'Jekyll Templates')


    @catch_errors
    def determine_path(self, path, dir_name):
        """Determine a directory path.

        Args:
            path (string): A string directory path
            dir_name (string): A string directory name

        Returns:
            string: a cleaned title for saving a new Jekyll post file

        """
        if not self.window.views():
            view = self.window.new_file()

        else:
            view = self.window.active_view()

        auto = get_setting(view, 'jekyll_auto_find_paths', False)

        if auto:
            self.dirs = find_dir_path(self.window, dir_name)

            if not self.dirs:

                if not path or path == '' or not os.path.exists(path):
                    debug('Unable to resolve path information! ({path})'.format(
                        path=path), prefix='Jekyll', level='error')
                    raise MissingPathException

                return path

            elif self.dirs and len(self.dirs) > 1:
                # more than one directory was found
                # so choose which one to use

                def callback(self, index):
                    if index > -1 and type(self.dirs[index]) is list:
                        return self.dirs[index]

                    else:
                        self.dirs = []
                        return None

                self.window.show_quick_panel(self.dirs, callback)

            elif self.dirs and len(self.dirs) == 1:
                # only one directory was found, so use it
                return self.dirs[0]

        else:
            if not path or path == '' or not os.path.exists(path):
                debug('Invalid path! - ({path})'.format(
                        path=path), prefix='Jekyll', level='error')
                raise MissingPathException

            return path


    def create_post_frontmatter(self, title, comment=None):
        """Create post frontmatter content.

        Args:
            title (str): A post title
            comment (str): An optional comment block

        Returns:
            string: A Sublime snippet string

        """
        if not comment or comment == '':
            comment = ''

        else:
            comment = '# {0}\n'.format(comment)

        frontmatter = (
            '{comment}---\n'
            'title: {title}\n'
        ).format(comment=str(comment), title=str(title))
        frontmatter += (
            'layout: ${1:post}\n'
            '---\n$0'
        )
        return frontmatter


    @catch_errors
    def title_input(self, title, path=None):
        """Sanitize a file title, save and open

        Args:
            title (string): A post title
            path (string): A path string

        Returns:
            None

        """
        post_dir = self.path_string() if path is None else path

        self.markup = get_setting(self.window.active_view(), 'jekyll_default_markup', 'Markdown')

        if self.markup == 'Textile':
            file_ext = '.textile'

        elif self.markup == 'HTML':
            file_ext = '.html'

        else:
            file_ext = '.markdown'

        clean_title = clean_title_input(title, self.IS_DRAFT) + file_ext
        full_path = os.path.join(post_dir, clean_title)

        if os.path.lexists(full_path):
            sublime.error_message('Jekyll: File already exists at "{0}"'.format(full_path))
            return

        else:
            frontmatter = self.create_post_frontmatter(title)
            self.create_and_open_file(full_path, frontmatter)


    def list_files(self, path, filter_ext=True):
        """Create an array of string arrays for files

        Args:
            path (string): A directory path of files
            filter_ext (bool): Filters files by type

        Returns:
            None

        """
        self.item_list = []

        if os.path.exists(path) and os.path.isdir(path):

            for root, dirs, files in os.walk(path):

                for f in files:

                    if filter_ext and not self.get_markup(f):
                        continue

                    fname = os.path.splitext(f)[0]
                    fpath = os.path.join(root, f)
                    self.item_list.append([fname, fpath])

            self.item_list.sort(key=lambda x: os.path.getmtime(x[1]), reverse=True)

        else:
            self.item_list.append(['Directory does not exist!'])

        if not len(self.item_list) > 0:
            self.item_list.append(['No items found!'])


    def on_highlight(self, index):
        self.window.open_file(self.item_list[index][1], sublime.TRANSIENT)


    def get_markup(self, file):
        if (
            file.endswith('.markdown') or
            file.endswith('.mdown') or
            file.endswith('.mkdn') or
            file.endswith('.mkd') or
            file.endswith('.md')
        ):
            self.markup = 'Markdown'

        elif (
            file.endswith('.html') or
            file.endswith('.htm')
        ):
            self.markup = 'HTML'

        elif (
            file.endswith('.textile')
        ):
            self.markup = 'Textile'

        elif (
            file.endswith('.yaml') or
            file.endswith('.yml')
        ):
            self.markup = 'YAML'

        else:
            self.markup = None

        return self.markup


    def create_and_open_file(self, path, frontmatter):
        create_file(path)

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


    def remove_file(self, file, message):
        to_trash = get_setting(self.window.active_view(), 'jekyll_send_to_trash', False)

        if to_trash:
            message = message + (
                '\n\nYou seem to be using the `jekyll_send_to_trash` setting, so you '
                'can retrieve this file later in your system Trash or Recylcing Bin.'
            )
        else:
            message = message + (
                '\n\nThis action is permanent and irreversible since you are not using '
                'the `jekyll_send_to_trash` setting. Are you sure you want to continue?'
            )

        delete = sublime.ok_cancel_dialog(message, 'Confirm Delete')

        if delete is True:
            self.window.run_command('close_file')
            self.window.run_command('refresh_folder_list')

            if to_trash:
                send2trash(file)

            else:
                os.remove(file)

        else:
            return


class JekyllPostBase(JekyllWindowBase):
    IS_DRAFT = False

    def path_string(self):
        return self.posts_path_string()


class JekyllDraftBase(JekyllWindowBase):
    IS_DRAFT = True

    def path_string(self):
        return self.drafts_path_string()


class JekyllUploadBase(JekyllWindowBase):
    def path_string(self):
        return self.uploads_path_string()


class JekyllTemplateBase(JekyllWindowBase):
    def path_string(self):
        return self.templates_path_string()


    def title_input(self, title, description=None):
        template_dir = self.path_string()

        if not os.path.exists(template_dir):
                os.makedirs(template_dir)

        clean_title = clean_title_input(title, True)
        full_path = os.path.join(template_dir, title + '.yaml')

        if os.path.lexists(full_path):
            sublime.error_message('Jekyll: File already exists at "{0}"'.format(full_path))
            return

        else:
            frontmatter = self.create_post_frontmatter(clean_title, description)
            self.create_and_open_file(
                full_path,
                frontmatter
            )


class JekyllFromTemplateBase(JekyllTemplateBase):
    def title_input(self, title, content):

        if not self.window.views():
            view = self.window.new_file()

        else:
            view = self.window.active_view()

        post_dir = self.drafts_path_string() if self.IS_DRAFT is True else self.posts_path_string()

        if not post_dir:
            raise MissingPathException

        self.markup = get_setting(view, 'jekyll_default_markup', 'Markdown')

        if self.markup == 'Textile':
            file_ext = '.textile'

        elif self.markup == 'HTML':
            file_ext = '.html'

        else:
            file_ext = '.markdown'

        clean_title = clean_title_input(title, self.IS_DRAFT) + file_ext
        full_path = os.path.join(post_dir, clean_title)

        if os.path.lexists(full_path):
            sublime.error_message('Jekyll: File already exists at "{0}"'.format(full_path))
            return

        else:
            yaml_title = 'title: {0}\n'.format(title)

            # Check for existence of `title` key in YAML frontmatter
            re_search_title = '(?<=\\n)(title.*?)(?:\\n)'
            re_add_title = '(^---\\n)'
            has_title_key = re.search(re_search_title, content)

            if has_title_key:
                yaml_content = re.sub(re_search_title, yaml_title, content)

            else:
                yaml_content = re.sub(re_add_title, '---\n' + yaml_title, content)

            frontmatter = self.create_post_frontmatter(yaml_content)
            self.create_and_open_file(
                full_path,
                frontmatter
            )


    def create_post_frontmatter(self, frontmatter):
        return frontmatter


## ********************************************************************************************** ##
#  BEGIN WINDOW COMMAND CLASSES
## ********************************************************************************************** ##


class JekyllNewPostCommand(JekyllPostBase):
    def on_done(self, title):
        self.title_input(title)


    def run(self):
        self.window.show_input_panel(
            'Jekyll post title:',
            '',
            self.on_done,
            None,
            None
        )


class JekyllNewPostFromTemplateCommand(JekyllFromTemplateBase):
    IS_DRAFT = False


    def on_done(self, index):
        if index > -1 and type(self.item_list[index]) is list:
            template = self.item_list[index][1]

            # Remove any leading comment from YAML frontmatter
            with open(template, 'rU') as f:
                first_line = f.readline().strip()

                if first_line[:1] != '#':
                    f.seek(0)

                file_contents = f.read()


            def on_done_inner(title):
                self.title_input(title, file_contents)


            self.window.show_input_panel(
                'Jekyll post title:',
                '',
                on_done_inner,
                None,
                None
            )

        else:
            self.item_list = []


    def run(self):
        template_dir = self.templates_path_string()
        self.list_files(template_dir)

        if ST3:
            self.window.show_quick_panel(
                self.item_list,
                self.on_done,
                on_highlight=self.on_highlight
            )

        else:
            self.window.show_quick_panel(
                self.item_list,
                self.on_done
            )


    def is_enabled(self):
        return True if os.path.exists(self.templates_path_string()) else False


class JekyllOpenPostCommand(JekyllPostBase):
    def on_done(self, index):
        if index > -1 and type(self.item_list[index]) is list:
            f = self.item_list[index][1]
            output_view = self.window.open_file(f)

        else:
            self.item_list = []


    def run(self):
        path = self.path_string()
        self.list_files(path)

        if ST3:
            self.window.show_quick_panel(
                self.item_list,
                self.on_done,
                on_highlight=self.on_highlight
            )

        else:
            self.window.show_quick_panel(
            self.item_list,
            self.on_done
        )


class JekyllRemovePostCommand(JekyllPostBase):
    def on_done(self, index):

        if index > -1 and type(self.item_list[index]) is list:
            f = self.item_list[index][1]

            confirm = 'You are about to delete the selected Jekyll post.'

            self.remove_file(f, confirm)


        else:
            self.item_list = []


    def run(self):
        path = self.path_string()
        self.list_files(path)

        if ST3:
            self.window.show_quick_panel(
                self.item_list,
                self.on_done,
                on_highlight=self.on_highlight
            )

        else:
            self.window.show_quick_panel(
                self.item_list,
                self.on_done
            )


class JekyllNewDraftCommand(JekyllDraftBase):
    def on_done(self, title):
        self.title_input(title)


    def run(self):
        self.window.show_input_panel(
            'Jekyll draft title:',
            '',
            self.on_done,
            None,
            None
        )


class JekyllNewDraftFromTemplateCommand(JekyllFromTemplateBase):
    IS_DRAFT = True


    def on_done(self, index):
        if index > -1 and type(self.item_list[index]) is list:
            template = self.item_list[index][1]

            # Remove any leading comment from YAML frontmatter
            with open(template, 'rU') as f:
                first_line = f.readline().strip()

                if first_line[:1] != '#':
                    f.seek(0)

                file_contents = f.read()


            def on_done_inner(title):
                self.title_input(title, file_contents)


            self.window.show_input_panel(
                'Jekyll draft title:',
                '',
                on_done_inner,
                None,
                None
            )

        else:
            self.item_list = []


    def run(self):
        template_dir = self.templates_path_string()
        self.list_files(template_dir)

        if ST3:
            self.window.show_quick_panel(
                self.item_list,
                self.on_done,
                on_highlight=self.on_highlight
            )

        else:
            self.window.show_quick_panel(
                self.item_list,
                self.on_done
            )


    def is_enabled(self):
        return True if os.path.exists(self.templates_path_string()) else False


class JekyllPromoteDraftCommand(JekyllDraftBase):
    def on_done(self, index):
        p_path = self.posts_path_string()

        if index != -1 and type(self.item_list[index]) is list:
            f = self.item_list[index][1]
            # return a list of directory names using platform specific separator
            dirlist = f.rsplit(os.sep)

            # check the draft name for a date
            # if you find one, replace it
            # if you don't find one, add it
            dirlist[-1] = re.sub(r'(^\d{4}-\d{2}-\d{2}-)', '', dirlist[-1])
            d = datetime.today()
            d_str = "{0}-".format(d.strftime(POST_DATE_FORMAT))
            dirlist[-1] = d_str + dirlist[-1]

            spath = dirlist[dirlist.index('_drafts')+1:]
            fpath = os.path.join(p_path, *spath)
            bpath = os.path.split(fpath)[0]

            # if the folder path doesn't yet exist, create it recursively
            if not os.path.exists(bpath):
                os.makedirs(bpath)

            if not os.path.exists(fpath):
                shutil.move(f, fpath)

            self.window.run_command('close_file')
            self.window.run_command('refresh_folder_list')
            output_view = self.window.open_file(fpath)

        else:
            self.item_list = []


    def run(self):
        d_path = self.drafts_path_string()
        self.list_files(d_path)

        if ST3:
            self.window.show_quick_panel(
                self.item_list,
                self.on_done,
                on_highlight=self.on_highlight
            )

        else:
            self.window.show_quick_panel(
                self.item_list,
                self.on_done
            )


class JekyllRemoveDraftCommand(JekyllDraftBase):
    def on_done(self, index):

        if index > -1 and type(self.item_list[index]) is list:
            f = self.item_list[index][1]

            confirm = 'You are about to delete the selected Jekyll draft.'

            self.remove_file(f, confirm)


        else:
            self.item_list = []


    def run(self):
        path = self.path_string()
        self.list_files(path)

        if ST3:
            self.window.show_quick_panel(
                self.item_list,
                self.on_done,
                on_highlight=self.on_highlight
            )

        else:
            self.window.show_quick_panel(
                self.item_list,
                self.on_done
            )


class JekyllOpenDraftCommand(JekyllDraftBase):
    def on_done(self, index):
        if index > -1 and type(self.item_list[index]) is list:
            f = self.item_list[index][1]
            output_view = self.window.open_file(f)

        else:
            self.item_list = []

    def run(self):
        path = self.path_string()
        self.list_files(path)

        if ST3:
            self.window.show_quick_panel(
                self.item_list,
                self.on_done,
                on_highlight=self.on_highlight
            )

        else:
            self.window.show_quick_panel(
                self.item_list,
                self.on_done
            )


class JekyllNewTemplateCommand(JekyllTemplateBase):
    def on_done(self, title):
        self.title = title

        def on_done_inner(description):
            self.title_input(self.title, description)


        self.window.show_input_panel(
            'Jekyll template description (optional):',
            '',
            on_done_inner,
            None,
            None
        )


    def run(self):
        self.window.show_input_panel(
            'Jekyll template name:',
            '',
            self.on_done,
            None,
            None
        )


class JekyllEditTemplateCommand(JekyllTemplateBase):
    def on_done(self, index):
        if index > -1 and type(self.item_list[index]) is list:
            f = self.item_list[index][1]
            output_view = self.window.open_file(f)

        else:
            self.item_list = []


    def run(self):
        template_dir = self.path_string()
        self.list_files(template_dir)

        if ST3:
            self.window.show_quick_panel(
                self.item_list,
                self.on_done,
                on_highlight=self.on_highlight
            )

        else:
            self.window.show_quick_panel(
                self.item_list,
                self.on_done
            )


    def is_enabled(self):
        return True if os.path.exists(self.templates_path_string()) else False


class JekyllRemoveTemplateCommand(JekyllTemplateBase):
    def on_done(self, index):
        if index > -1 and type(self.item_list[index]) is list:
            f = self.item_list[index][1]

            confirm = 'You are about to delete the selected Jekyll template.'

            self.remove_file(f, confirm)


        else:
            self.item_list = []


    def run(self):
        template_dir = self.path_string()
        self.list_files(template_dir)

        if ST3:
            self.window.show_quick_panel(
                self.item_list,
                self.on_done,
                on_highlight=self.on_highlight
            )

        else:
            self.window.show_quick_panel(
                self.item_list,
                self.on_done
            )


    def is_enabled(self):
        return True if os.path.exists(self.templates_path_string()) else False


class JekyllBrowseTemplatesCommand(JekyllTemplateBase):
    def run(self):
        sublime.active_window().run_command(
            'open_dir',
            {
                'dir': self.templates_path_string()
            }
        )


    def is_enabled(self):
        return True if os.path.exists(self.templates_path_string()) else False


class JekyllListUploadsCommand(JekyllUploadBase):
    """
    A subclass for displaying uploads in the upload directory.

    """
    def on_done(self, index):
        if index > -1 and type(self.item_list[index]) is list:
            path = self.item_list[index][1]
            fname = self.item_list[index][0]
            view = self.window.active_view()
            view.run_command(
                'jekyll_insert_upload',
                {
                    'name': fname,
                    'path': path
                }
            )


    def run(self):
        path = self.uploads_path_string()
        self.list_files(path, False)
        self.window.show_quick_panel(self.item_list, self.on_done)


class JekyllEditConfigCommand(JekyllWindowBase):
    def run(self):
        site_dir = os.path.join(self.posts_path_string(), os.pardir)

        if os.path.exists(site_dir):
            config_file = os.path.join(site_dir, '_config.yml')

            if os.path.exists(config_file):
                self.window.open_file(config_file, sublime.TRANSIENT)


## ********************************************************************************************** ##
#  BEGIN TEXT COMMAND CLASSES
## ********************************************************************************************** ##

class JekyllPostFrontmatterCommand(sublime_plugin.TextCommand):
    """
    Creates a new post using post defaults.

    """
    def run(self, edit, **args):
        path = args.get('path')
        frontmatter = args.get('frontmatter', '')
        output_view = self.view.window().open_file(path)

        def update():
            if output_view.is_loading():

                if ST3:
                    sublime.set_timeout_async(update, 1)

                else:
                    sublime.set_timeout(update, 1)

            else:
                output_view.run_command(
                    'insert_snippet',
                    {
                        'contents': frontmatter
                    }
                )

                output_view.run_command('save')

        update()


class JekyllInsertDateCommand(sublime_plugin.TextCommand):
    """
    Prints todays date according to format in settings file.

    """
    def run(self, edit, **args):
        DEFAULT_FORMAT = '%Y-%m-%d'
        view = self.view
        date_format = get_setting(view, 'jekyll_date_format', '%Y-%m-%d')
        datetime_format = get_setting(view, 'jekyll_datetime_format', '%Y-%m-%d %H:%M:%S')

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


class JekyllInsertUpload(sublime_plugin.TextCommand):
    """
    Insert the upload link at the current position

    """
    def run(self, edit, **args):
        uploads_path = get_setting(self.view, 'jekyll_uploads_path')
        uploads_baseurl = get_setting(self.view, 'jekyll_uploads_baseurl')
        relative_path = os.path.relpath(args["path"], os.path.dirname(uploads_path))

        # check if image
        link_str = "{0}[{1}]({2}/{3})".format(
            '!' if imghdr.what(args["path"]) is not None else '',
            '${1:' + args["name"] + '}', uploads_baseurl, relative_path
        )

        self.view.run_command(
            'insert_snippet',
            {
                'contents': link_str
            }
        )


## ********************************************************************************************** ##
#  BEGIN MIGRATION CLASSES
## ********************************************************************************************** ##

class JekyllMigrateSettingsBase(sublime_plugin.WindowCommand):
    """Base class to help migrate settings from pre-Jekyll 3.0 versions.

    Converts pre-Jekyll 3.0 settings keys to their new values.
    New values have been namespaced for easier management and
    debugging.

    """
    settings_to_swap = {
        "posts_path": "jekyll_posts_path",
        "drafts_path": "jekyll_drafts_path",
        "uploads_path": "jekyll_uploads_path",
        "uploads_baseurl": "jekyll_uploads_baseurl",
        "automatically_find_paths": "jekyll_auto_find_paths",

        "default_post_syntax": "jekyll_default_markup",

        "insert_date_format": "jekyll_date_format",
        "insert_datetime_format": "jekyll_datetime_format"
    }

    def on_done(self):
        self.window.show_input_panel(
            'Type MIGRATE to continue with migration: ',
            '',
            self.validate_secret,
            None,
            None
        )


    def settings_path(self):
        return os.path.join(sublime.packages_path(), 'User', 'Jekyll.sublime-settings')


    def backups_path(self):
        return os.path.join(sublime.packages_path(), 'User', 'Jekyll Backups')


    def create_backup(self, type):
        hex_string = uuid.uuid4().hex

        if type and type == 'user':
            src = self.settings_path()
            dir = self.backups_path()

            # Create a new backups directory if it doesn't exist yet
            if not os.path.exists(dir):
                os.makedirs(dir)

            dst = os.path.join(dir, 'Jekyll.sublime-settings-backup-{hex}'.format(hex=hex_string))
            shutil.copy(src, dst)
            debug('User settings backed up to "{path}".'.format(path=dst), prefix='Jekyll Utility', level='info')

        elif type and type == 'project':
            src = self.window.project_file_name()
            dir = self.backups_path()

            if not os.path.exists(dir):
                os.makedirs(dir)

            dst = os.path.join(dir, '{filename}-{hex}'.format(filename=os.path.basename(src), hex=hex_string))
            shutil.copy(src, dst)
            debug('Project settings backed up to "{path}".'.format(path=dst), prefix='Jekyll Utility', level='info')

        else:
            debug('Unable to perform settings backup!', prefix='Jekyll Utility', level='warning')
            pass

    def validate_secret(self, secret):
        """Validate a string against a known simple secret key.

        Validates user input against a simple
        text-based "secret" token. This is used
        to help prevent accidental migrations.

        Args:
            self (class): A Jekyll Migrate base class
            secret (string): A secret string

        Returns:
            none

        """
        if secret and secret == 'MIGRATE':
            confirm = ("You are about to migrate your Jekyll settings to v3.0! "
                       "\n\nThere is no automated undo command. "
                       "Backup settings files are stored in a 'Jekyll Backups' "
                       "directory inside your User and/or Project directory. "
                       "\n\nClick the migrate button below to continue.\n\n")

            migrate = sublime.ok_cancel_dialog(confirm, 'Migrate')

            if migrate:
                debug('Migration started...', prefix='Jekyll Utility', level='info')
                sublime.set_timeout(lambda: self.begin_migration(), 100)

            else:
                sublime.message_dialog('Jekyll settings migration canceled!')
                debug('Migration canceled by user.', prefix='Jekyll Utility', level='warning')

        else:
            sublime.message_dialog('You entered an incorrect secret. Try again')
            debug('Migration canceled by user.', prefix='Jekyll Utility', level='warning')
            sublime.set_timeout(lambda: self.on_done(), 100)


class JekyllMigrateUserSettingsCommand(JekyllMigrateSettingsBase):
    def run(self):
        sublime.set_timeout(lambda: self.on_done(), 100)


    def is_visible(self):
        settings = sublime.load_settings('Jekyll.sublime-settings')

        if settings.has('jekyll_utility_disable') and settings.get('jekyll_utility_disable') is True:
            return False

        else:
            return True


    def begin_migration(self):
        sublime.set_timeout(lambda: self.create_backup('user'), 100)
        settings = sublime.load_settings('Jekyll.sublime-settings')

        for key in self.settings_to_swap:

            if settings.has(key):
                settings.set(self.settings_to_swap[key], settings.get(key))

                debug('Migrated old settings key "{key}" to new settings key "{swap}"'.format(
                    key=key, swap=self.settings_to_swap[key]
                ), prefix='Jekyll Utility', level='info')

                settings.erase(key)
                debug('Deleted old settings key "{key}"'.format(key=key), prefix='Jekyll Utility', level='info')

        sublime.save_settings('Jekyll.sublime-settings')


class JekyllMigrateProjectSettingsCommand(JekyllMigrateSettingsBase):
    def run(self):
        sublime.set_timeout(lambda: self.on_done(), 100)


    def is_enabled(self):
        # NOTE: the Sublime API only exposes projects in v3+
        return True if ST3 and self.window.project_file_name() else False


    def is_visible(self):
        settings = sublime.load_settings('Jekyll.sublime-settings')

        if settings.has('jekyll_utility_disable') and settings.get('jekyll_utility_disable') is True:
            return False

        else:
            return True


    def begin_migration_old(self):
        project_file_path = self.window.project_file_name()
        debug('Project file path = {path}'.format(path=project_file_path), prefix='Jekyll Utility')

        if os.path.exists(project_file_path):

            with open(project_file_path, 'r+') as project_file:
                project_data = json.load(project_file)

                if not 'settings' in project_data:
                    # No project settings found
                    sublime.message_dialog('Unable to find project settings!')
                    debug('Unable to find project settings.', prefix='Jekyll Utility', level='error')
                    return

                settings = project_data['settings']

                if 'Jekyll' in settings:
                    # Create backup of current project settings file
                    sublime.set_timeout(lambda: self.create_backup('project'), 100)
                    jekyll_settings = settings['Jekyll']

                    for key in self.settings_to_swap:

                        if key in jekyll_settings:
                            jekyll_settings[self.settings_to_swap[key]] = jekyll_settings[key]
                            debug('Migrated old settings key "{key}" to new settings key "{swap}"'.format(
                                key=key, swap=self.settings_to_swap[key]
                            ), prefix='Jekyll Utility', level='info')

                            jekyll_settings.pop(key, None)
                            debug('Deleted old settings key "{key}"'.format(key=key),
                                prefix='Jekyll Utility', level='info')

                    settings['Jekyll'] = jekyll_settings
                    project_data['settings'] = settings
                    project_file.seek(0)
                    project_file.truncate()
                    json.dump(project_data, project_file, indent=4, sort_keys=True)

                else:
                    # No Jekyll project settings found
                    sublime.message_dialog('Unable to find Jekyll in project settings!')
                    debug('Unable to find Jekyll in project settings.',
                        prefix='Jekyll Utility', level='error')


class JekyllBrowseBackupsCommand(JekyllMigrateSettingsBase):
    def run(self):
        sublime.active_window().run_command(
            'open_dir',
            {
                'dir': self.backups_path()
            }
        )


    def is_enabled(self):
        return True if os.path.exists(self.backups_path()) else False

    def is_visible(self):
        settings = sublime.load_settings('Jekyll.sublime-settings')

        if settings.has('jekyll_utility_disable') and settings.get('jekyll_utility_disable') is True:
            return False

        else:
            return True
