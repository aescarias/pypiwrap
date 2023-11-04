.. pypiwrap documentation master file, created by
   sphinx-quickstart on Sat Sep 10 22:28:46 2022.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

pypiwrap
========

``pypiwrap`` is a simple API wrapper for the Python Package Index (PyPI). 

It provides interfaces to the **JSON and Stats API** and the **Simple API**.
It allows users to quickly fetch information about projects on PyPI or any compatible
repositories.

Installation
------------

**At least Python 3.7 or higher is required.** 

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

``pypiwrap`` provides two clients for interacting with PyPI:

* :class:`~pypiwrap.client.SimpleClient` allows access to data from 
  the PyPI Simple Repository.  
* :class:`~pypiwrap.client.PyPIClient` allows access to data from
  the PyPI website itself.

**Example 1: Fetching details about a project**

.. code-block:: python

   import pypiwrap

   with pypiwrap.PyPIClient() as wrap:
      proj = wrap.get_project("requests")
      print(f"{proj.name} by {proj.author}") # requests by Kenneth Reitz

**Example 2: Getting the latest distribution file for a project**

.. code-block:: python

   import pypiwrap

   wrap = pypiwrap.SimpleClient()
   proj = wrap.get_page("requests")

   print(proj.files[-1].url)

More documentation can be found in the :ref:`Client Reference`.

.. toctree::
   :maxdepth: 2
   :caption: Reference
   
   Client <reference/client>
   Exceptions <reference/exceptions>
   PyPI Objects <reference/objects/pypi>
   Simple Objects <reference/objects/simple>
   Utils <reference/utils>

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

