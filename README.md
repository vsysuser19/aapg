# AAPG for RISC-V ISA
(Automatic Assembly Program Generator for RISC-V ISA )

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
    > ./make.py gen_only
3. To generate assembly programs and execute on riscv vanilla spike run the following command. This assumes that spike exists in the your $PATH
    > ./make.py spike
4. To generate assembly programs and execute on shakti-mod-spike run the following:
    > ./make.py modspike
6. To generate assembly, run on modspike, run on RTL binary and compare results run the following command. Currently this assumes that the RTL binary is named "out" and is present in $SHAKTI_C_HOME/bin, where $SHAKTI_C_HOME is any environment variable.
    > ./make.py

8. All the generated tests will be in result/test# folder.
9. The seed for each random test is taken from the randomSeed.txt. Users can modify this file as per
their requirements.
