import datetime
import json
from xml.etree import ElementTree

from pypiwrap.objects import Project, PyPIFeed, Stats


def test_parse_pypi_project() -> None:
    with open("tests/data/pypi_flask.json") as fp:
        project = Project.from_json(json.load(fp))

        assert project.name == "Flask"
        assert project.file_urls[0].filename == "flask-3.1.0-py3-none-any.whl"
        assert project.file_urls[0].size.bytes == 102_979
        assert project.file_urls[0].upload_time_tz == datetime.datetime(
            2024, 11, 13, 18, 24, 36, 135982, tzinfo=datetime.timezone.utc
        )


def test_parse_pypi_stats() -> None:
    with open("tests/data/pypi_stats.json") as fp:
        stats = Stats.from_json(json.load(fp))

        assert stats.total_size.bytes == 24_847_924_802_983
        assert stats.top_packages["PySide2"].bytes == 20_246_295_405
        assert list(stats.top_packages)[-1] == "OpenVisus"


def test_parse_pypi_feeds() -> None:
    with open("tests/data/pypi_packages.xml") as fp:
        rss = ElementTree.fromstring(fp.read())
        channel = rss.find("channel")

        assert channel is not None

        feed = PyPIFeed.from_xml(channel)

        assert feed.title == "PyPI newest packages"
        assert feed.link == "https://pypi.org/"
        assert feed.items[2].guid == feed.items[2].link
        assert feed.items[2].published_raw == "Fri, 17 Jan 2025 21:48:37 GMT"
        assert feed.items[2].published == datetime.datetime(2025, 1, 17, 21, 48, 37)
