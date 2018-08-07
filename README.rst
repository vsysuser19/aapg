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

A sample config.ini with all options can be found in the ```samples``` directory. 

Feature List
------------
Currently, ``aapg`` supports the following controls for
random program generation.

    * Total number of instructions

License
-------

Copyright (c) 2013-2018, IIT Madras
All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

*  Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
*  Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
*  Neither the name of IIT Madras  nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE. 


What it does
=============
This tool is used to generate random assembly programs. Currently AAPG supports generating instructions from the I, M, A, F, D for RV32 or RV64 extensions of the ISA.

The tool initializes the data section with random memory. The generated assembly program contains a predifined sequence of 38 instructions which sets the stack pointer, global pointer and initializes all the registers with random values. 

The tool also provides capabilities to run the generated assembly program on shakti-mod-spike. This shakti-mod-spike generates an instruction dump file: spike.dump.

The tool can further integrate an external RTL binary to execute the assembly program. The RTL binary should also create a rtl.dump file similar to that spike.dump. The tool compares these two dump files for correctness.

The user can configure the tool to provide a directed randomness using the configuration file. For eg. the tool can be configured to generate nested loops with pre-defined depth, iterations, numbers of nests, etc. It can also configure the percentage of floating and integer operations. 

Requirements
=============
- Python 3
- shakti-mod-spike is you want to perform comparison with RTL.
- The directory structure needs to be maintained

Usage
=============
1. First modify the config.py based on your requirements.
2. To generate only assembly program run the following command. Outputs will be in result/test# folder.

         $ ./make.py gen_only
         
4. To generate assembly programs and execute on riscv vanilla spike run the following command. This assumes that spike exists in the your $PATH

        $ ./make.py spike

5. To generate assembly programs and execute on shakti-mod-spike run the following:

        $ ./make.py modspike
        
6. To generate assembly, run on modspike, run on RTL binary and compare results run the following command. Currently this assumes that the RTL binary is named "out" and is present in $SHAKTI_C_HOME/bin, where $SHAKTI_C_HOME is any environment variable.

        $ ./make.py

8. All the generated tests will be in result/test# folder.
