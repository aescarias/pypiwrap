# pypiwrap

![PyPi - Downloads](https://img.shields.io/pypi/dw/pypiwrap?style=flat-square)
![PyPI](https://img.shields.io/pypi/v/pypiwrap?style=flat-square)
![GitHub](https://img.shields.io/github/license/aescarias/pypiwrap?style=flat-square)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pypiwrap?style=flat-square)

A simple API wrapper for the Python Package Index (PyPI), including a simple interface to get project and release data.

- [Documentation](https://aescarias.github.io/pypiwrap)
- [PyPI](https://pypi.org/project/pypiwrap)

## Installation

**Python 3.7 or higher is required.**

Install `pypiwrap` through `pip`:

- On Linux/macOS, `python3 -m pip install pypiwrap`
- On Windows, `py -3 -m pip install pypiwrap`

## Example

```py
import pypiwrap

wrap = pypiwrap.PyPIClient()
project = wrap.get_project("requests")

print(project.name) # requests
print(project.author) # Kenneth Reitz
print(project.summary) # Python HTTP for Humans.
```
