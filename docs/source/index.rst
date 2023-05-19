.. pypiwrap documentation master file, created by
   sphinx-quickstart on Sat Sep 10 22:28:46 2022.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to pypiwrap
=================== 

``pypiwrap`` is a simple API wrapper for the Python Package Index (PyPI) registry. 

It provides an interface to the JSON API, the Simple API, and the Stats API.
It allows users to quickly get information about projects on PyPI.

.. toctree::
   :maxdepth: 2
   :caption: Reference
   
   Client <reference/client>
   Exceptions <reference/exceptions>
   PyPI Objects <reference/objects/pypi>
   Simple Objects <reference/objects/simple>
   Utils <reference/utils>


Installation
------------

**At least Python 3.7 or higher is required.** 

Install ``pypiwrap`` through ``pip``:

.. tab-set::

   .. tab-item:: Linux/MacOS

      .. code-block:: sh

         python3 -m pip install pypiwrap

   .. tab-item:: Windows

      .. code-block:: sh

         py -3 -m pip install pypiwrap


.. tip::
   If you plan to work with other packages along ``pypiwrap``, we recommend you do so in a virtual environment so as to isolate
   it from other existing packages in the system.

Quickstart
----------

``pypiwrap`` provides two base interfaces for interacting with PyPI:

* :class:`~pypiwrap.client.SimpleClient` allows access to data from 
  the PyPI Simple Repository.  
* :class:`~pypiwrap.client.PyPIClient` allows access to data from
  the PyPI website itself.

**Example 1: Information about a project**

.. code-block:: python

   import pypiwrap

   wrap = pypiwrap.PyPIClient()
   proj = wrap.get_project("requests")
   print(f"{proj.name} by {proj.author}") # requests by Kenneth Reitz

**Example 2: Getting a distribution file for a project**

.. code-block:: python

   import pypiwrap

   wrap = pypiwrap.SimpleClient()
   proj = wrap.get_page("requests")

   print(proj.files[-1].url)

More detailed documentation is included in the :ref:`Client Reference`.

.. toctree::
   :maxdepth: 2
   :caption: Links
   :hidden:

   Github <https://github.com/aescarias/pypiwrap>
   PyPI <https://pypi.org/project/pypiwrap>

Indices
-------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

