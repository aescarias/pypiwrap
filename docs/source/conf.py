# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import re

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'pypiwrap'
copyright = '2023, Angel Carias'
author = 'Angel Carias'
release = '1.1.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosectionlabel',
    'sphinx_design',
    'sphinx_copybutton'
]

templates_path = ['_templates']
exclude_patterns = []

copybutton_prompt_text = r'>>> |\.\.\. '
copybutton_prompt_is_regexp = True

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'furo'
html_static_path = ['_static']

# courtesy of https://stephencharlesweiss.com/regex-markdown-link
_mdlink_pattern = r'!?\[([^\]]*)?\]\(((https?:\/\/)?[A-Za-z0-9\:\/\. ]+)(\"(.+)\")?\)'

def docstring(app, what, name, obj, options, lines):
    # Some docstrings include Markdown links. This converts them to RST.
    for i, ln in enumerate(lines):
        lines[i] = re.sub(_mdlink_pattern, 
                          lambda mat: f"`{mat.group(1)} <{mat.group(2)}>`_", ln)

def setup(app):
    app.connect('autodoc-process-docstring', docstring)
