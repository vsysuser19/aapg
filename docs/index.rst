.. aapg documentation master file, created by
   sphinx-quickstart on Sat Jun 30 00:23:12 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

AAPG - Documentation
====================
Automated Assembly Program Generator (``aapg``) is a tool
that is intended to generate random RISC-V programs
to test RISC-V cores.

``aapg`` works by reading the required configuration for
the random program from a configuration file which specifies
various controls and generates a random program.
For a full list of features refer to :ref:`feature-list`.

Quickstart
----------
To get started quickly, we first need to install ``aapg`` using the following command,

.. code-block:: python

    pip install aapg

Now navigate to a directory where you want to store
the random assembly program. We need to setup a config file
for ``aapg`` to read the configuration from.

.. code-block:: bash

    touch config.ini
    echo "[general]" >> config.init
    echo "total_instructions = 1200" >> config.ini

Refer to :ref:`config-ref` for complete details
about writing a configuration file.
Once the ``config.ini`` has been created we can run ``aapg``
using the following command.

.. code-block:: bash
    
    aapg gen 

You should find your random program generated in
``build/out.asm`` in your current directory. By default,
``aapg`` expects the configuration file to be ``config.ini``
and the output file to be ``build/out.asm`` in the directory
that ``aapg`` was run in.

Read the :ref:`user-guide` for more details.

.. _feature-list:

Feature List
------------
Currently, ``aapg`` supports the following controls for
random program generation.

    * Total number of instructions

Table of Contents
-----------------

.. toctree::
   :maxdepth: 2

   installation
   user-guide
   config-ref

