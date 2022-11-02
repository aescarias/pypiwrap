# pypiwrap

![PyPi - Downloads](https://img.shields.io/pypi/dw/pypiwrap?style=flat-square)
![PyPI](https://img.shields.io/pypi/v/pypiwrap?style=flat-square)
![GitHub](https://img.shields.io/github/license/aescarias/pypiwrap?style=flat-square)
![Lines of code](https://img.shields.io/tokei/lines/github/aescarias/pypiwrap?style=flat-square)

A simple API wrapper for the Python Package Index (PyPi).

It includes a minimal interface for users to get information about Python packages.

## Installation

Install `pypiwrap` via `pip` by using `pip install pypiwrap` or equivalent methods.

## Example

```py
import pypiwrap

wrap = pypiwrap.Client()
project = wrap.get_project("requests")

print(project.name) # requests
print(project.author) # Kenneth Reitz
print(project.summary) # Python HTTP for Humans.
```
