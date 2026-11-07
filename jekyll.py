"""Jekyll 4.0.0 commands for Sublime Text 4 (build 4083+)."""

import os
import re
import shutil
import traceback
from datetime import datetime, timezone
from functools import wraps

import sublime
import sublime_plugin

from .jekyll_utils import (
    MARKDOWN_EXTENSIONS,
    bounded_find_dirs,
    clean_title_input,
    escape_snippet,
    extract_frontmatter_date,
    file_extension,
    find_site_roots,
    is_image,
    markdown_label,
    promote_destination,
    resolve_relative,
    url_path,
    yaml_quote,
)


class MissingPathException(Exception):
    pass


def get_setting(window, key, default=None):
    if window is not None:
        settings = (window.project_data() or {}).get("settings", {}).get("Jekyll", {})
        if key in settings:
            return settings[key]
    return sublime.load_settings("Jekyll.sublime-settings").get(key, default)


def get_str_setting(window, key, default=""):
    """Like get_setting, but falls back to default when the value isn't a string."""
    value = get_setting(window, key, default)
    return value if isinstance(value, str) else default


def is_debug():
    return get_setting(sublime.active_window(), "jekyll_debug", False)


def plugin_loaded():
    if is_debug():
        print(f"Jekyll 4.0.0 loaded at {datetime.now(timezone.utc)} (Sublime {sublime.version()})")


def catch_errors(fn):
    @wraps(fn)
    def wrapped(*args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except MissingPathException as error:
            sublime.error_message(
                f"Jekyll: {error}\n\nSet an absolute or ${{project_path}}-relative path in Jekyll settings, "
                "or open the site folder containing _config.yml (or _config.yaml)."
            )
        except Exception as error:
            traceback.print_exc()
            sublime.error_message(f"Jekyll: {error}. See the console for details.")

    return wrapped


def insert_when_loaded(view, contents, retries=100):
    @catch_errors
    def update(remaining):
        if not view.is_valid():
            raise RuntimeError("The new file was closed before its contents could be inserted")
        if view.is_loading():
            if remaining <= 0:
                raise RuntimeError("Timed out waiting for the file to load")
            sublime.set_timeout(lambda: update(remaining - 1), 50)
            return
        view.run_command("insert_snippet", {"contents": contents})
        view.run_command("save")

    update(retries)


class JekyllWindowBase(sublime_plugin.WindowCommand):
    kind = "posts"

    def is_enabled(self):
        return True

    def is_visible(self):
        return True

    def expanded_path(self, value):
        folders = self.window.folders()
        project = self.window.project_file_name()
        base = folders[0] if folders else (os.path.dirname(project) if project else None)
        value = sublime.expand_variables(value, self.window.extract_variables())
        try:
            return resolve_relative(value, base)
        except ValueError as error:
            raise MissingPathException(str(error)) from error

    def path_candidates(self, kind):
        key = f"jekyll_{kind}_path"
        configured = get_setting(self.window, key)
        if configured not in (None, ""):
            path = self.expanded_path(configured)
            if not os.path.isdir(path):
                raise MissingPathException(f'{key} is not a directory: "{path}".')
            return [path]
        if kind == "templates":
            path = os.path.join(sublime.packages_path(), "User", "Jekyll Templates")
            os.makedirs(path, exist_ok=True)
            return [path]
        dir_name = {"posts": "_posts", "drafts": "_drafts", "uploads": "uploads"}[kind]
        folders = self.window.folders()
        candidates = [
            os.path.join(root, dir_name)
            for root in find_site_roots(folders)
            if os.path.isdir(os.path.join(root, dir_name))
        ]
        if not candidates and get_setting(self.window, "jekyll_auto_find_paths", False):
            candidates = bounded_find_dirs(folders, dir_name, 4)
        if not candidates:
            raise MissingPathException(f'Unable to find the "{dir_name}" directory ({key}).')
        return candidates

    def choose_path(self, paths, on_resolved):
        callback = catch_errors(on_resolved)
        if len(paths) == 1:
            callback(paths[0])
            return

        @catch_errors
        def selected(index):
            if 0 <= index < len(paths):
                callback(paths[index])

        items = [sublime.QuickPanelItem(os.path.basename(path), details=path) for path in paths]
        self.window.show_quick_panel(items, selected, placeholder="Choose a Jekyll directory")

    @catch_errors
    def resolve_path(self, kind, on_resolved):
        self.choose_path(self.path_candidates(kind), on_resolved)

    def show_file_panel(self, path, on_select, filter_ext=True, preview=True):
        files = []
        extensions = MARKDOWN_EXTENSIONS + ("html", "htm", "textile", "txt", "yaml", "yml")
        if os.path.isdir(path):

            def walk_error(error):
                raise error

            for root, _dirs, names in os.walk(path, onerror=walk_error):
                for name in names:
                    extension = os.path.splitext(name)[1].lower().lstrip(".")
                    if filter_ext and extension not in extensions:
                        continue
                    files.append(os.path.join(root, name))
            files.sort(key=os.path.getmtime, reverse=True)
            empty_message = "No items found!"
        else:
            empty_message = "Directory does not exist!"
        items = [
            sublime.QuickPanelItem(os.path.basename(file), annotation=os.path.relpath(file, path)) for file in files
        ] or [sublime.QuickPanelItem(empty_message)]

        @catch_errors
        def selected(index):
            if 0 <= index < len(files):
                on_select(files[index])

        @catch_errors
        def highlighted(index):
            if 0 <= index < len(files):
                self.window.open_file(files[index], sublime.TRANSIENT)

        self.window.show_quick_panel(items, selected, on_highlight=highlighted if preview else None)

    def prompt_title(self, path, content=None):
        @catch_errors
        def entered(title):
            self.create_post(path, title, content)

        label = "draft" if self.kind == "drafts" else "post"
        self.window.show_input_panel(f"Jekyll {label} title:", "", entered, None, None)

    def create_post_frontmatter(self, title, comment=None):
        description = "".join(f"# {line}\n" for line in comment.splitlines()) if comment else ""
        return (
            escape_snippet(description)
            + "---\ntitle: "
            + escape_snippet(yaml_quote(title))
            + "\nlayout: ${1:post}\n---\n$0"
        )

    def create_post(self, path, title, content=None):
        slug = clean_title_input(title, self.kind == "drafts")
        if not slug:
            sublime.error_message("Jekyll: Enter a title with at least one letter or number.")
            return
        extension = file_extension(
            get_setting(self.window, "jekyll_default_markup", "Markdown"),
            get_setting(self.window, "jekyll_markdown_extension", "markdown"),
        )
        if content is None:
            contents = self.create_post_frontmatter(title)
        else:
            # Templates may contain snippet fields; only escape the supplied title.
            title_line = "title: " + escape_snippet(yaml_quote(title)) + "\n"
            lines = content.splitlines(keepends=True)
            end = next((i for i in range(1, len(lines)) if lines[i].strip() == "---"), None)
            if lines and lines[0].strip() == "---" and end is not None:
                frontmatter = "".join(lines[1:end])
                if re.search(r"^title\s*:", frontmatter, flags=re.MULTILINE):
                    frontmatter = re.sub(
                        r"^title\s*:.*(?:\n|$)", lambda _match: title_line, frontmatter, flags=re.MULTILINE
                    )
                else:
                    frontmatter = title_line + frontmatter
                contents = "---\n" + frontmatter + "".join(lines[end:])
            else:
                contents = "---\n" + title_line + "---\n" + content
        self.create_and_open_file(os.path.join(path, slug + extension), contents)

    def create_and_open_file(self, path, frontmatter):
        if os.path.lexists(path):
            sublime.error_message(f'Jekyll: File already exists at "{path}"')
            return
        view = self.window.open_file(path)
        insert_when_loaded(view, frontmatter)

    def close_file_view(self, path):
        view = self.window.find_open_file(path)
        if view is not None:
            view.close()

    def remove_file(self, path):
        open_view = self.window.find_open_file(path)
        if open_view is not None and open_view.is_dirty():
            sublime.error_message(f'Jekyll: Save or revert "{os.path.basename(path)}" before deleting it.')
            return
        to_trash = get_setting(self.window, "jekyll_send_to_trash", False)
        send2trash = None
        if to_trash:
            # Sublime Text 4 bundles send2trash in its Default package.
            try:
                from Default.send2trash import send2trash  # pyright: ignore[reportMissingImports]
            except ImportError:
                sublime.error_message(
                    "Jekyll: Sublime's bundled send2trash module is unavailable, so the file was not deleted. "
                    "Set jekyll_send_to_trash to false to delete permanently."
                )
                return
        message = f"Delete this Jekyll file?\n\n{path}"
        message += "\n\nYou can recover it from the system Trash." if to_trash else "\n\nThis is permanent."
        if not sublime.ok_cancel_dialog(message, "Confirm Delete"):
            return
        if send2trash is not None:
            send2trash(path)
        else:
            os.remove(path)
        self.close_file_view(path)
        self.window.run_command("refresh_folder_list")


class JekyllNewPostCommand(JekyllWindowBase):
    @catch_errors
    def run(self):
        self.resolve_path(self.kind, self.prompt_title)


class JekyllNewDraftCommand(JekyllNewPostCommand):
    kind = "drafts"


class JekyllFromTemplateBase(JekyllWindowBase):
    @catch_errors
    def run(self):
        self.resolve_path("templates", lambda path: self.show_file_panel(path, self.template_selected))

    def template_selected(self, template):
        with open(template, encoding="utf-8") as source:
            lines = source.readlines()
        while lines and lines[0].startswith("#"):
            lines.pop(0)
        content = "".join(lines)
        self.resolve_path(self.kind, lambda path: self.prompt_title(path, content))


class JekyllNewPostFromTemplateCommand(JekyllFromTemplateBase):
    pass


class JekyllNewDraftFromTemplateCommand(JekyllFromTemplateBase):
    kind = "drafts"


class JekyllOpenPostCommand(JekyllWindowBase):
    @catch_errors
    def run(self):
        self.resolve_path(self.kind, lambda path: self.show_file_panel(path, self.window.open_file))


class JekyllOpenDraftCommand(JekyllOpenPostCommand):
    kind = "drafts"


class JekyllEditTemplateCommand(JekyllOpenPostCommand):
    kind = "templates"


class JekyllRemovePostCommand(JekyllWindowBase):
    @catch_errors
    def run(self):
        self.resolve_path(self.kind, lambda path: self.show_file_panel(path, self.remove_file))


class JekyllRemoveDraftCommand(JekyllRemovePostCommand):
    kind = "drafts"


class JekyllRemoveTemplateCommand(JekyllRemovePostCommand):
    kind = "templates"


class JekyllPromoteDraftCommand(JekyllWindowBase):
    @catch_errors
    def run(self):
        self.resolve_path("drafts", self.list_drafts)

    def list_drafts(self, drafts_dir):
        def selected(draft):
            self.resolve_path("posts", lambda posts_dir: self.promote(draft, drafts_dir, posts_dir))

        self.show_file_panel(drafts_dir, selected)

    def promote(self, draft, drafts_dir, posts_dir):
        open_view = self.window.find_open_file(draft)
        if open_view is not None and open_view.is_dirty():
            sublime.error_message(f'Jekyll: Save or revert "{os.path.basename(draft)}" before promoting it.')
            return
        with open(draft, encoding="utf-8") as source:
            date = extract_frontmatter_date(source.read()) or datetime.today().strftime("%Y-%m-%d")
        destination = promote_destination(draft, drafts_dir, posts_dir, date)
        if os.path.lexists(destination):
            sublime.error_message(f'Jekyll: File already exists at "{destination}"')
            return
        os.makedirs(os.path.dirname(destination), exist_ok=True)
        shutil.move(draft, destination)
        self.close_file_view(draft)
        self.window.run_command("refresh_folder_list")
        self.window.open_file(destination)


class JekyllNewTemplateCommand(JekyllWindowBase):
    @catch_errors
    def run(self):
        self.resolve_path("templates", self.prompt_template)

    def prompt_template(self, path):
        @catch_errors
        def named(title):
            slug = clean_title_input(title, True)
            if not slug:
                sublime.error_message("Jekyll: Enter a template name with at least one letter or number.")
                return

            @catch_errors
            def described(description):
                self.create_and_open_file(
                    os.path.join(path, slug + ".yaml"), self.create_post_frontmatter(title, description)
                )

            self.window.show_input_panel("Jekyll template description (optional):", "", described, None, None)

        self.window.show_input_panel("Jekyll template name:", "", named, None, None)


class JekyllBrowseTemplatesCommand(JekyllWindowBase):
    @catch_errors
    def run(self):
        self.resolve_path("templates", lambda path: self.window.run_command("open_dir", {"dir": path}))


class JekyllListUploadsCommand(JekyllWindowBase):
    @catch_errors
    def run(self):
        view = self.window.active_view()
        if view is None:
            sublime.status_message("Jekyll: Open a document before inserting an upload.")
            return

        def resolved(uploads_dir):
            def selected(path):
                view.run_command(
                    "jekyll_insert_upload",
                    {
                        "name": os.path.splitext(os.path.basename(path))[0],
                        "path": path,
                        "uploads_dir": uploads_dir,
                    },
                )

            self.show_file_panel(uploads_dir, selected, filter_ext=False, preview=False)

        self.resolve_path("uploads", resolved)


class JekyllEditConfigCommand(JekyllWindowBase):
    @catch_errors
    def run(self):
        roots = []
        try:
            roots = [os.path.dirname(path) for path in self.path_candidates("posts")]
        except MissingPathException:
            pass
        roots.extend(find_site_roots(self.window.folders()))
        configs = []
        for root in roots:
            for name in ("_config.yml", "_config.yaml"):
                path = os.path.join(root, name)
                if os.path.isfile(path) and path not in configs:
                    configs.append(path)
        if configs:
            self.choose_path(configs, lambda path: self.window.open_file(path, sublime.TRANSIENT))
        else:
            sublime.status_message("Jekyll: Unable to find _config.yml or _config.yaml. Open the site folder.")


class JekyllPostFrontmatterCommand(sublime_plugin.TextCommand):
    @catch_errors
    def run(self, edit, path=None, frontmatter=""):
        window = self.view.window() or sublime.active_window()
        view = window.open_file(path) if path else self.view
        insert_when_loaded(view, frontmatter)


class JekyllInsertDateCommand(sublime_plugin.TextCommand):
    @catch_errors
    def run(self, edit, format="date"):
        window = self.view.window() or sublime.active_window()
        key = "jekyll_datetime_format" if format == "datetime" else "jekyll_date_format"
        default = "%Y-%m-%d %H:%M:%S" if format == "datetime" else "%Y-%m-%d"
        text = datetime.today().strftime(get_str_setting(window, key, default) or default)
        if not text.strip():
            return
        for region in reversed(list(self.view.sel())):
            if region.empty():
                self.view.insert(edit, region.a, text)
            else:
                self.view.replace(edit, region, text)


class JekyllInsertUpload(sublime_plugin.TextCommand):
    @catch_errors
    def run(self, edit, name="", path="", uploads_dir=None):
        if not path:
            raise ValueError('jekyll_insert_upload requires a "path" argument')
        name = name or os.path.splitext(os.path.basename(path))[0]
        window = self.view.window() or sublime.active_window()
        if uploads_dir is None:
            resolver = JekyllWindowBase(window)
            resolver.resolve_path(
                "uploads",
                lambda directory: self.view.run_command(
                    "jekyll_insert_upload", {"name": name, "path": path, "uploads_dir": directory}
                ),
            )
            return
        baseurl = get_str_setting(window, "jekyll_uploads_baseurl", "")
        relative = os.path.relpath(path, os.path.dirname(uploads_dir)).replace(os.sep, "/")
        link = "{}[${{1:{}}}]({}/{})".format(
            "!" if is_image(path) else "",
            escape_snippet(markdown_label(name)),
            escape_snippet(baseurl.rstrip("/")),
            escape_snippet(url_path(relative)),
        )
        self.view.run_command("insert_snippet", {"contents": link})
