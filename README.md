# pypiwrap

![PyPI - Downloads per week](https://img.shields.io/pypi/dw/pypiwrap?style=flat-square)
![PyPI - Latest Release](https://img.shields.io/pypi/v/pypiwrap?style=flat-square)
![PyPI - Supported Python Versions](https://img.shields.io/pypi/pyversions/pypiwrap?style=flat-square)
![GitHub - License](https://img.shields.io/github/license/aescarias/pypiwrap?style=flat-square)

[Documentation](https://pypiwrap.rtfd.io/) · [PyPI](https://pypi.org/project/pypiwrap) · [Changelog](https://github.com/aescarias/pypiwrap/blob/main/CHANGELOG.md)

pypiwrap is an API wrapper for the Python Package Index (PyPI) providing interfaces for retrieving project information, releases and statistics from the [PyPI JSON API](https://docs.pypi.org/api/json/), the [Statistics API](https://docs.pypi.org/api/stats/), and the [Index API](https://docs.pypi.org/api/index-api/). pypiwrap also parses information from the [PyPI RSS feeds](https://docs.pypi.org/api/feeds/).

## Installation

pypiwrap requires Python 3.9 or later and can be installed with `pip`:

- `python3 -m pip install pypiwrap` (Linux/Mac)
- `py -3 -m pip install pypiwrap` (Windows)

## Examples

```py
import pypiwrap

# Fetching data from the PyPI API
with pypiwrap.PyPIClient() as pypi:
    project = pypi.get_project("requests")

    print(project.name)  # requests
    print(project.author)  # Kenneth Reitz
    print(project.summary)  # Python HTTP for Humans.

    stats = pypi.get_stats()
    print(stats.total_size.si)  # 24.61 TB


# Fetching data from the Index API
with pypiwrap.SimpleRepoClient() as repo:
    page = repo.get_project_page("requests")
    
    print(page.files[-1].url)  # https://files.pythonhosted.org/packages/63/70/[...]
    print(page.files[-1].size.si)  # 131.22 KB


# Fetching data from the RSS feeds
with pypiwrap.PyPIFeedClient() as rss:
    feed = rss.get_newest_packages()

    print(feed.title)  # PyPI newest packages

    for item in feed.items:
        print(item.title)  # ... added to PyPI
```
