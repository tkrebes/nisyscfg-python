===========  ===============================================================================================================================
Info         Python bindings for NI System Configuration. See `GitHub <https://github.com/tkrebes/nisyscfg-python/>`_ for the latest source.
Author       National Instruments
===========  ===============================================================================================================================

Status
======
.. image:: https://travis-ci.org/tkrebes/nisyscfg-python.svg?branch=master
    :target: https://travis-ci.org/tkrebes/nisyscfg-python

About
=====

The **nisyscfg** package contains an API (Application Programming Interface)
for interacting with NI System Configuration. The package is implemented in Python.
This package was created by NI. The package is implemented as a complex, highly
object-oriented wrapper around the NI System Configuration C API using the
`ctypes <https://docs.python.org/2/library/ctypes.html>`_ Python library.

**nisyscfg** supports only the Windows and Linux operating systems.

**nisyscfg** supports CPython 2.7, 3.4+.

Installation
============

Running **nisyscfg** requires the NI System Configuration Runtime. Visit the
`ni.com/downloads <http://www.ni.com/downloads/>`_ to download the latest version
of NI System Configuration.

You also can download the project source and run::

  $ python setup.py install

.. _usage-section:

Usage
=====
The following is a basic example of using an **nisyscfg.Session** object.

.. code-block:: python

  >>> import nisyscfg
  >>> with nisyscfg.Session() as session:
  >>>     # Print user aliases for all NI devices in the local system
  >>>     for resource in session.find_hardware(IsPresent=True, IsNIProduct=True, IsDevice=True):
  >>>         print(resource.ExpertUserAlias[0])
