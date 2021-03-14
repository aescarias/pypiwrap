import setuptools
import re

with open('pypiwrap\__init__.py') as f:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE).group(1)

with open("README.md", "r") as f:
    readme = f.read()

print("Setup for pypiwrap version: ", version)

deps = ["requests"]

setuptools.setup(
    name="pypiwrap",
    packages=["pypiwrap", r"pypiwrap\apis"],
    author="Tekgar",
    license="MIT",
    license_file="LICENSE",
    author_email=None,
    version=version,
    description="A simple wrapper for interfacing with PyPi APIs.",
    long_description=readme,
    long_description_content_type="text/markdown",
    python_requires=">=3.6",
    url="https://github.com/angelCarias/pypiwrap",
    download_url="https://github.com/angelCarias/pypiwrap/archive/v0.1.0.tar.gz",
)