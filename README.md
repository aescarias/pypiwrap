# pypiwrap

A simple wrapper for interfacing with PyPi (Python Package Index) APIs.

**Documentation:** [PyPiWrap Wiki](https://github.com/angelCarias/pypiwrap/wiki)

## Installation

The simplest way to install PyPiWrap is via PIP:

```s
pip install pypiwrap
```

Verify that PyPiWrap has been installed correctly by importing it in any Python file or shell:

```py
>>> import pypiwrap
>>> 
```

## Examples

### Example 1 - Package information

```py
import pypiwrap.apis as pypiapis
package = pypiapis.data.PackageInfo("requests")
print(f"{package.name} by {package.author}")
print(package.summary)
```

```s
requests by Kenneth Reitz
Python HTTP for Humans.
```

### Example 2 - Package release information

```py
import pypiwrap.apis as pypiapis
releases = pypiapis.data.ReleaseInfo("dotenv")
print(releases.version_data)
```

```py
{
    '0.0.1': [File(name='dotenv-0.0.1.tar.gz', type='sdist', size='6.46 KB', url='...')],
    '0.0.2': [File(name='dotenv-0.0.2.tar.gz', type='sdist', size='6.73 KB', url='...')],
    '0.0.4': [File(name='dotenv-0.0.4.tar.gz', type='sdist', size='1.97 KB', url='...')],
    '0.0.5': [File(name='dotenv-0.0.5.tar.gz', type='sdist', size='2.42 KB', url='...')]
}
```

### Example 3 - PyPi statistics

```py
import pypiwrap.apis as pypiapis
stats = pypiapis.stats.Statistics().stats
print(stats.total_packages_size_readable)
```

```py
'7.09 TB'
```
