# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import re

from pypiwrap.consts import __version__

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "pypiwrap"
copyright = "2023, Angel Carias"
author = "Angel Carias"
release = __version__

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.autosectionlabel",
    "sphinx_design",
    "sphinx_copybutton",
]

templates_path = ["_templates"]
exclude_patterns = []

copybutton_prompt_text = r">>> |\.\.\. "
copybutton_prompt_is_regexp = True

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "furo"
html_static_path = ["_static"]

# courtesy of https://stephencharlesweiss.com/regex-markdown-link
MARKDOWN_LINK_PATTERN = (
    r"!?\[([^\]]*)?\]\(((https?:\/\/)?[A-Za-z0-9\:\/\. ]+)(\"(.+)\")?\)"
)


def docstring(app, what, name, obj, options, lines):
    # Some docstrings include Markdown links. This converts them to RST.
    for idx, line in enumerate(lines):
        lines[idx] = re.sub(
            MARKDOWN_LINK_PATTERN,
            lambda mat: f"`{mat.group(1)} <{mat.group(2)}>`_",
            line,
        )


def setup(app):
    app.connect("autodoc-process-docstring", docstring)
