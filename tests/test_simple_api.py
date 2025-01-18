import json

import pytest

from pypiwrap.client import SimpleRepoClient
from pypiwrap.exceptions import UnexpectedVersionWarning, UnsupportedVersionError
from pypiwrap.objects import IndexPage, ProjectPage


def test_parse_index_page() -> None:
    with open("tests/data/simple_repo_index_page.json") as fp:
        index_json = json.load(fp)

    page = IndexPage.from_json(index_json)

    assert page.meta.api_version == "1.3"


def test_parse_project_page() -> None:
    with open("tests/data/simple_repo_colorama_page.json") as fp:
        project_json = json.load(fp)

    page = ProjectPage.from_json(project_json)

    assert page.meta.api_version == "1.3"
    assert page.name == "colorama"
    assert page.files[4].yanked
    assert page.files[4].filename == "colorama-0.4.2-py2.py3-none-any.whl"


def test_check_version_mismatch() -> None:
    with SimpleRepoClient() as client:
        with pytest.warns(UnexpectedVersionWarning):
            client._verify_api_version("1.25")

        with pytest.raises(UnsupportedVersionError):
            client._verify_api_version("10.0")
