from datetime import datetime

import sublime
import sublime_plugin


# Get a value from a key in the sublime-settings file
def get_setting(key, default_value=True):
    try:
        settings = sublime.active_window().active_view().settings()
        if settings.has(key):
            return settings.get(key)
    except:
        pass
    s = sublime.load_settings('Jekyll.sublime-settings')
    return s.get(key, default_value)


class InsertDateCommand(sublime_plugin.TextCommand):
    """
    Prints Date according to format in settings file

    """
    def run(self, edit):
        DEFAULT_DATE_FORMAT = '%Y-%m-%d'
        try:
            if not get_setting('insert_date_only'):
                date_format = DEFAULT_DATE_FORMAT
            else:
                date_format = '%Y-%m-%d %H:%M:%S'
        except Exception as e:
            sublime.error_message("[InsertDate]\n%s: %s" % (type(e).__name__, e))
            date_format = DEFAULT_DATE_FORMAT

        try:
            d = datetime.today()
            text = d.strftime(date_format)
        except Exception as e:
            sublime.error_message("[InsertDate]\n%s: %s" % (type(e).__name__, e))
            return

        # Don't bother replacing selections with actually nothing
        if text == '' or text.isspace():
            return

        # Do replacements
        for r in self.view.sel():
            # Insert when sel is empty to not select the contents
            if r.empty():
                self.view.insert(edit, r.a, text)
            else:
                self.view.replace(edit, r, text)
