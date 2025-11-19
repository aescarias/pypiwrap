Features
========

The following is a list of PEPs, specs and APIs related to PyPI.

Note that some features in pypiwrap have been implemented according to the examples in the `PyPI API documentation <https://docs.pypi.org/api/>`_. Some aspects in the API have been implemented according to the issues & source code of the `Warehouse project <https://github.com/pypi/warehouse/>`_ powering PyPI.


PyPI/Warehouse APIs
-------------------

.. list-table:: APIs, feeds, and datasets
    :header-rows: 1

    * - Feature
      - Supported?
      - Notes
    * - `Index API <https://docs.pypi.org/api/index-api/>`_
      - Yes
      - See :class:`pypiwrap.client.SimpleRepoClient`.
    * - `PyPI JSON API <https://docs.pypi.org/api/json/>`_
      - Yes
      - See :meth:`pypiwrap.client.PyPIClient.get_project`.
    * - `Upload API <https://docs.pypi.org/api/upload/>`_
      - No
      -
    * - `Integrity API <https://docs.pypi.org/api/integrity/>`_
      - No
      -
    * - `Stats API <https://docs.pypi.org/api/stats/>`_
      - Yes
      - See :meth:`pypiwrap.client.PyPIClient.get_stats`.
    * - `BigQuery datasets <https://docs.pypi.org/api/bigquery/>`_
      - No
      -
    * - `RSS feeds <https://docs.pypi.org/api/feeds/>`_
      - Yes
      - See :class:`pypiwrap.client.PyPIFeedClient`.
    * - `Secret reporting API <https://docs.pypi.org/api/secrets/>`_
      - No
      - This API is designed for private use. There's currently no intention to implement it.


PEPs relating to PyPI
---------------------

.. list-table:: PEPs
    :header-rows: 1

    * - PEP
      - Supported?
      - Notes
    * - `PEP 503 - Simple Repository API <https://peps.python.org/pep-0503/>`_
      - Yes
      - pypiwrap will always use the JSON API. See PEP 691.
    * - `PEP 629 - Versioning PyPI's Simple API <https://peps.python.org/pep-0629/>`_
      - Yes
      - pypiwrap will verify the API version as recommended by this PEP.
    * - `PEP 691 - JSON-based Simple API for Python Package Indexes <https://peps.python.org/pep-0691/>`_
      - Yes
      - See :class:`pypiwrap.client.SimpleRepoClient`.
    * - `PEP 639 - Improving License Clarity with Better Package Metadata <https://peps.python.org/pep-0639/>`_
      - Yes
      - This PEP introduces the ``License-Expression`` and ``License-Files`` keys.
    * - `PEP 700 - Additional Fields for the Simple API for Package Indexes <https://peps.python.org/pep-0700/>`_
      - Yes
      - This PEP introduces version 1.1 of the Simple Repository API.
    * - `PEP 708 - Extending the Repository API to Mitigate Dependency Confusion Attacks <https://peps.python.org/pep-0708/#alternate-locations-metadata>`_
      - Yes
      - This PEP introduces the ``tracks`` and ``alternate-locations`` keys.
    * - `PEP 740 - Index support for digital attestations <https://peps.python.org/pep-0740/>`_
      - Partially
      - This PEP introduces provenance objects and attestations. Only the ``provenance`` field returned by the Simple Repository API is recognized.
    * - `PEP 792 - Project status markers in the simple index <https://peps.python.org/pep-0792/>`_
      - Yes
      - See :attr:`.Meta.project_status` and :attr:`.Meta.project_status_reason`.
