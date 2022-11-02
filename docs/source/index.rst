.. pypiwrap documentation master file, created by
   sphinx-quickstart on Sat Sep 10 22:28:46 2022.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to pypiwrap
=================== 

``pypiwrap`` is a simple Python API wrapper for the Python Package Index 
(PyPi) registry. 

It allows users to quickly get information about projects on PyPi.

.. toctree::
   :maxdepth: 2
   :caption: Reference
   
   Client <reference/client>
   Exceptions <reference/exceptions>
   Objects <reference/objects>
   Utils <reference/utils>


Installation
------------

``pypiwrap`` is installed like any other package, through ``pip``

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

The main interface for the API is the :class:`pypiwrap.client.Client` class. An example is shown below.

.. code-block:: python

   import pypiwrap

   wrap = pypiwrap.Client()
   proj = wrap.get_project("requests")
   print(proj.name, proj.author)


More detailed documentation is included in the :ref:`Client Reference`.

.. toctree::
   :maxdepth: 2
   :caption: Links
   :hidden:

   Github <https://github.com/aescarias/pypiwrap>
   PyPi <https://pypi.org/project/pypiwrap>

Indices
-------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

