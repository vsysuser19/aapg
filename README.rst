Advanced Assembly Program Generator
===================================
Automated Assembly Program Generator (``aapg``) is a tool 
that is intended to generate random RISC-V programs
to test RISC-V cores.

Quickstart
----------
To get started, we first need to install ``aapg`` using the following command,

.. code-block:: python

    pip install aapg

Now navigate to a directory where you want to store
the random assembly program. We need to setup a config file
for ``aapg`` to read the configuration from.

.. code-block:: bash

    touch config.ini
    echo "[general]" >> config.init
    echo "total_instructions = 1200" >> config.ini

Once the ``config.ini`` has been created we can run ``aapg``
using the following command.

.. code-block:: bash
    
    aapg gen 

You should find your random program generated in
``build/out.asm`` in your current directory. By default,
``aapg`` expects the configuration file to be ``config.ini``
and the output file to be ``build/out.asm`` in the directory
that ``aapg`` was run in.

Feature List
------------
Currently, ``aapg`` supports the following controls for
random program generation.

    * Total number of instructions

License
-------
Copyright <YEAR> <COPYRIGHT HOLDER>

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.