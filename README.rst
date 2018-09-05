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

Next, create a working directory for your project,

.. code-block:: bash
    mkdir ~/aapg-samples 
    cd ~/aapg-samples

We need to setup a config file
for ``aapg`` to read the configuration from.

.. code-block:: bash

    aapg sample

A sample ``config.ini`` file should be created in your local directory.

Now we setup the build environment by typing,

.. code-block:: bash

    aapg setup

This creates the folders for the outputs of each step that is compiling the assembly to machine code, dumping a disassemly and then running the simulator on spike (riscv-isa-sim).

Once the previous steps have been completed, we can run ``aapg``
using the following command.

.. code-block:: bash
    
    aapg gen 

By default, ``aapg`` generates 64 bit programs. To generate 32 bit programs, you have to run,

.. code-block:: bash
    aapg gen --arch rv32

You should find your random program generated in
``build/out.asm`` in your current directory. By default,
``aapg`` expects the configuration file to be ``config.ini``
and the output file to be ``build/out.asm`` in the directory
that ``aapg`` was run in. To build the programs and run them on Spike,

.. code-block:: bash

    make

Alternatively for compiling using the 32-bit toolchain, you can type,

.. code-block:: bash
    make XLEN=32

You can check the logfiles in the ``log`` directory and the disassembled code in ``objdump`` directory.

A sample config.ini with all options can be found in the ```samples``` directory. 

Developing
----------
If you want to develop aapg features and test them on your system, install aapg using the following command - 

.. code-block:: python

   sudo python3 setup.py develop

This will create the command line tool ``aapg`` and any changes you make in the source will reflect in the command line tool. 

Feature List
------------
Currently, ``aapg`` supports the following controls for
random program generation.

* Total number of instructions
* Recursion template with recursion parameters
* Percentage distribution of ISA instructions - RV32/64 IMAFDC

License
-------
Copyright (c) 2013-2018, IIT Madras
All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

*  Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
*  Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
*  Neither the name of IIT Madras  nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE. 
