.. sqla-filter documentation master file, created by
   sphinx-quickstart on Mon Sep  3 15:34:27 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

=========================================================
sqla-filters: A library to filter your sqlachemy queries.
=========================================================

.. image:: https://img.shields.io/pypi/v/sqla-filters.svg
    :target: https://pypi.org/project/sqla-filters/

.. image:: https://img.shields.io/pypi/l/sqla-filters.svg
    :target: https://pypi.org/project/sqla-filters/

.. image:: https://img.shields.io/pypi/wheel/sqla-filters.svg
    :target: https://pypi.org/project/sqla-filters/

.. image:: https://img.shields.io/pypi/pyversions/sqla-filters.svg
    :target: https://pypi.org/project/sqla-filters/

.. image:: https://img.shields.io/discord/479781351051100170.svg?logo=discord
    :target: https://discord.gg/eQ4Mtc8

.. toctree::
   :maxdepth: 2
   :caption: Contents:


.. warning::
    This project is not ready for production so use it carefully because it's not stable.

Introduction
------------

.. _DFS: https://en.wikipedia.org/wiki/Depth-first_search
.. _Sqlalchemy: https://www.sqlalchemy.org/
.. _Discord: https://discord.gg/eQ4Mtc8

The purpose of this library is to provide a simple way to filter queries generated with `Sqlalchemy`_. To filter a query a tree is generated.
When the filter function is called the tree is traversed (`DFS`_) and the filter function of each sub node is called
until all nodes are scanned.

The default format for the tree generation is the ``JSON`` format. It's included in the
package.

Other formats will be supported in the future. You can also create your own parser to generate
the three from the format you want (:ref:`here <sqla-filters-plugins-cyopp>`).

=====
Guide
=====

User Guide
----------

.. toctree::
    :maxdepth: 1

    user/nodes
    user/tree

Developer Guide
---------------

.. toctree::
    :maxdepth: 1

    dev/plugins

==================
Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
