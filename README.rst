VALUE SERP for Python
=====================

A Python client library for fetching data from the `VALUE SERP <https://www.valueserp.com/>`_ API.

Documentation: https://python-valueserp.readthedocs.io/

Get started
-----------

1. Install:

.. code-block:: bash

   pip install python-valueserp

2. Use:

.. code-block:: python

   import valueserp

   creds = valueserp.Credentials('YOURAPIKEYHERE')
   google = valueserp.GoogleClient(creds)

   serp = google.web_search('seo', location='United Kingdom')
   results = serp.links

Disclaimer
----------

This is not an officially maintained library, and is neither owned by nor affiliated with VALUE SERP or Wildeer LLP.
