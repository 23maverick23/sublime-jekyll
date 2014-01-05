from datetime import datetime

import sublime
import sublime_plugin


# Get a value from a key in the sublime-settings file
def get_setting(key, default_value='%Y-%m-%d'):
    try:
        settings = sublime.active_window().active_view().settings()
        if settings.has(key):
            return settings.get(key)
    except:
        pass
    s = sublime.load_settings('Jekyll.sublime-settings')
    return s.get(key, default_value)


class JekyllInsertDateCommand(sublime_plugin.TextCommand):
    """
    Prints Date according to format in settings file

    """
    def run(self, edit, **args):
        DEFAULT_FORMAT = '%Y-%m-%d'
        date_format = get_setting('jekyll_insert_date_format', '%Y-%m-%d')
        datetime_format = get_setting('jekyll_insert_datetime_format', '%Y-%m-%d %H:%M:%S')

        try:
            d = datetime.today()
            if args['format'] and args['format'] == 'date':
                text = d.strftime(date_format)
            elif args['format'] and args['format'] == 'datetime':
                text = d.strftime(datetime_format)
            else:
                text = d.strftime(DEFAULT_FORMAT)

        except Exception as e:
            sublime.error_message("[JekyllInsertDate]\n%s: %s" % (type(e).__name__, e))
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
