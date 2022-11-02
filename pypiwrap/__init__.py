"""
pypiwrap
A Python API wrapper for the PyPi package registry.
"""
from .client import Client

__name__ = "pypiwrap"
__author__ = 'Angel Carias'
__license__ = 'MIT'
__version__ = '0.3.0'

JSON_URL = "https://pypi.org/pypi"
STATS_URL = "https://pypi.org/stats"
SIMPLE_URL = "https://pypi.org/simple"

CONTENT_TYPE = "application/vnd.pypi.simple.v1+json"
