"""Audit package wiring without importing Sublime or jekyll.py."""

import ast
import json
import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
FILES = [*ROOT.glob("*.sublime-menu"), *ROOT.glob("*.sublime-commands"), *ROOT.glob("*.sublime-keymap")]
# The menus and palette also use these commands supplied by Sublime itself.
BUILTIN_COMMANDS = {"open_file", "edit_settings"}


def read_jsonc(path):
    text = path.read_text(encoding="utf-8")
    # Match strings first so // inside quoted paths and URLs survives.
    text = re.sub(
        r'"(?:\\.|[^"\\])*"|//[^\n]*', lambda match: "" if match.group().startswith("//") else match.group(), text
    )
    text = re.sub(
        r'"(?:\\.|[^"\\])*"|,\s*(?=[}\]])', lambda match: match.group() if match.group().startswith('"') else "", text
    )
    return json.loads(text)


def command_names(value):
    if isinstance(value, list):
        for item in value:
            yield from command_names(item)
    elif isinstance(value, dict):
        if "command" in value:
            yield value["command"]
        if "children" in value:
            yield from command_names(value["children"])


def plugin_commands():
    tree = ast.parse((ROOT / "jekyll.py").read_text(encoding="utf-8"))
    classes = {node.name: node for node in tree.body if isinstance(node, ast.ClassDef)}

    def has_run(node):
        return any(isinstance(item, ast.FunctionDef) and item.name == "run" for item in node.body) or any(
            has_run(classes[base.id]) for base in node.bases if isinstance(base, ast.Name) and base.id in classes
        )

    return {
        re.sub(r"(?<!^)(?=[A-Z])", "_", name[:-7] if name.endswith("Command") else name).lower()
        for name, node in classes.items()
        if has_run(node)
    }


@pytest.mark.parametrize("path", FILES, ids=lambda path: path.name)
def test_menu_commands_exist(path):
    names = set(command_names(read_jsonc(path)))
    assert names <= plugin_commands() | BUILTIN_COMMANDS
    assert not any(re.search(r"migrate|backups|utility", name) for name in names)


def test_settings_json_and_host():
    assert "jekyll_utility_disable" not in read_jsonc(ROOT / "Jekyll.sublime-settings")
    assert (ROOT / ".python-version").read_bytes() == b"3.8\n"


@pytest.mark.parametrize("name", ["jekyll.py", "jekyll_lib/__init__.py", "jekyll_lib/jekyll_utils.py"])
def test_python38_syntax(name):
    ast.parse((ROOT / name).read_text(encoding="utf-8"), feature_version=(3, 8))
