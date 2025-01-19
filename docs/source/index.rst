.. pypiwrap documentation master file, created by
   sphinx-quickstart on Sat Sep 10 22:28:46 2022.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

pypiwrap
========

pypiwrap is an API wrapper for the Python Package Index (PyPI), providing interfaces for the JSON API, the Stats API, the Index API, and the PyPI RSS feeds.

For more information on supported features, see :ref:`Features`.

Installation
------------

pypiwrap requires Python 3.9 or higher.

.. tab-set::

   .. tab-item:: Linux/MacOS

      .. code-block:: sh

         python3 -m pip install pypiwrap

   .. tab-item:: Windows

      .. code-block:: sh

         py -3 -m pip install pypiwrap


.. tip::
   If you plan to work with other packages along ``pypiwrap``, we recommend you do so in a virtual environment so as to isolate it from other existing packages in the system.

Quickstart
----------

pypiwrap provides three clients for interacting with PyPI:

* :class:`~pypiwrap.client.SimpleRepoClient` allows access to data from the Simple Repository API (also known as the Index API).
* :class:`~pypiwrap.client.PyPIClient` allows access to data from the PyPI JSON API.
* :class:`~pypiwrap.client.PyPIFeedClient` allows access to data from the PyPI RSS feeds.

Examples
--------

Example 1: Fetching details about a project.

.. code-block:: python

   import pypiwrap

   with pypiwrap.PyPIClient() as pypi:
       project = pypi.get_project("requests")
       print(f"{project.name} by {project.author}")  # requests by Kenneth Reitz

Example 2: Getting the latest distribution file for a project.

.. code-block:: python

   import pypiwrap

   with pypiwrap.SimpleRepoClient() as repo:
       project = repo.get_project_page("requests")
      
       print(project.files[-1].url)  # https://files.pythonhosted.org/packages/63/70/[...]

Example 3: Fetching the latest releases feed for a package.

.. code-block:: python

   import pypiwrap

   with pypiwrap.PyPIFeedClient() as rss:
       feed = rss.get_latest_releases_for_project("Django")

       for item in feed.items:
           print(f"{item.title} was released on {item.published:%A, %B %d, %Y}")
           print(item.link)
           print()

More documentation can be found in the :ref:`Client reference`.

Table of Contents
-----------------

.. toctree:: 
   :maxdepth: 2
   :caption: Guides

   Features <guides/features>

.. toctree::
   :maxdepth: 2
   :caption: API Reference

   Client <reference/client>
   Exceptions <reference/exceptions>
   PyPI Objects <reference/objects/pypi>
   RSS Objects <reference/objects/rss>
   Simple Repository Objects <reference/objects/simple_repo>
   Utilities <reference/utils>

.. toctree::
   :maxdepth: 2
   :caption: Links
   :hidden:

   Github <https://github.com/aescarias/pypiwrap>
   PyPI <https://pypi.org/project/pypiwrap>
   Changelog <https://github.com/aescarias/pypiwrap/blob/main/CHANGELOG.md>

Indices
-------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

