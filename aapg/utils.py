"""
    Helpers for different functions
"""
import logging

class ColoredFormatter(logging.Formatter):
    """
        Class to create a log output which is colored based on level.
    """
    def __init__(self, *args, **kwargs):
        super(ColoredFormatter, self).__init__(*args, **kwargs)
        self.colors = {
                'DEBUG' : '\033[94m',
                'INFO'  : '\033[92m',
                'WARNING' : '\033[93m',
                'ERROR' : '\033[91m',
        }

        self.reset = '\033[0m'

    def format(self, record):
        msg = str(record.msg)
        level_name = str(record.levelname)
        name = str(record.name)
        color_prefix = self.colors[level_name]
        return '{0}{1:<9s} - {2:<25s} : {3}{4}'.format(
                color_prefix,
                '[' + level_name + ']',
                name,
                msg,
                self.reset)

''' Sample Config File '''
config_sample = '''
# Sample config.ini file to generate a random program
# using aapg (Automated Assembly Program Generator)

# Each section commands a behaviour of aapg
# and inline comments in each section will explain the
# usage

# ---------------------------------------------------------------------------------
# General directives to aapg
# Options:
#       total_instructions: Approximate number of instructions to be generated
#                           by aapg. Actual may vary.
#       regs_not_use:       Comma separated list of RISC-V registers to not use for
#                           reading/writing in the random generated instructions
# ---------------------------------------------------------------------------------
[general]
total_instructions = 1000
regs_not_use = x1,x2
user_trap_handler = false

# ---------------------------------------------------------------------------------
# Distribution of instructions according to ISA extensions
# Specify the relative frequency of each set 
# E.g. : A relative frequency of 1 each means each instruction will be 
# generated equal number of times in the total instructions. Specify 0 to disable.
# ---------------------------------------------------------------------------------
[isa-instruction-distribution]
rel_sys = 0
rel_rv32i.ctrl = 0
rel_rv32i.compute = 0
rel_rv32i.data = 0
rel_rv32i.fence = 0
rel_rv64i.compute = 0
rel_rv64i.data = 0
rel_rv32m = 0
rel_rv64m = 0
rel_rv32a = 0
rel_rv64a = 0
rel_rv32f = 0
rel_rv64f = 0
rel_rv32d = 0
rel_rv64d = 0

# Compressed instructions

rel_rvc.ctrl = 0
rel_rvc.compute = 1
rel_rvc.sp = 0
rel_rvc.data = 1
rel_rvc.fdata = 1

rel_rv32c.compute = 1
rel_rv32c.ctrl = 0
rel_rv32c.fdata = 1

rel_rv64c.compute = 1
rel_rv64c.data = 1

[branch-control]
backward-probability = 0.5

# ---------------------------------------------------------------------------------
# Recursion options
# Options:
#       recursion_enable:   Generate the template for recursion or not
#       recursion_depth:    Number of times the recursive function is called
# ---------------------------------------------------------------------------------
[recursion-options]
recursion-enable = false
recursion-depth = 10

# ---------------------------------------------------------------------------------
# Data section options
# Options:
#       size: Size of data section in KB (kilobytes)
# ---------------------------------------------------------------------------------
[data-section]
size = 1000

# ---------------------------------------------------------------------------------
# Data access sections
# Specify which regions of memory will be accessed by the random program
# Options:
#       enable:         Force all memory accesses instructions to only load/store
#                       to the specified list of address sections
#                       
# Section Template: Specify legal access zones using the following template
#       section_name =  section_low,section_high (HEX)     
# ---------------------------------------------------------------------------------
[access-sections]
section1 = 0x8001f000,0x8003a000,rw

# ---------------------------------------------------------------------------------
# User template sections
# Allows users to specify call to a custom function with number of times to call
# User should ensure that function does not modify 
#                       
# Section Template: Specify user template function calls with the number of times
#       function_name = number_of_times
# ---------------------------------------------------------------------------------
[user-functions]
_test = 0

# ---------------------------------------------------------------------------------
# Instruction Cache and Data-Cache Thrashing
# ---------------------------------------------------------------------------------
[i-cache]
num_calls = 10
num_bytes_per_block = 16
num_blocks = 8
num_cycles = 10

# ---------------------------------------------------------------------------------
# Exception generation
# ---------------------------------------------------------------------------------
[exception-generation]
ecause00 = 0
ecause01 = 0
ecause02 = 0
ecause03 = 10
ecause04 = 0
ecause05 = 0
ecause06 = 0
ecause07 = 0
ecause08 = 0
ecause09 = 0
ecause10 = 0
ecause11 = 0
ecause12 = 0
ecause13 = 0
ecause14 = 0
'''
def print_sample_config():
    """
        Print sample config.ini
    """
    with open('config.ini', 'w') as f:
        f.write(config_sample.strip('\n'))
