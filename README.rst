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
