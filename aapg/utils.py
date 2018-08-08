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
total_instructions = 200
regs_not_use = x1,x2

# ---------------------------------------------------------------------------------
# Distribution of instructions according to ISA extensions
# Specify the relative frequency of each set 
# E.g. : A relative frequency of 1 each means each instruction will be 
# generated equal number of times in the total instructions. Specify 0 to disable.
# ---------------------------------------------------------------------------------
[isa-instruction-distribution]
rel_sys = 1
rel_rv32i.ctrl = 1
rel_rv32i.compute = 1
rel_rv32i.data = 1
rel_rv32i.fence = 1
rel_rv64i.compute = 0
rel_rv64i.data = 0
rel_rv32m = 1
rel_rv64m = 0
rel_rv32a = 1
rel_rv64a = 0
rel_rv32f = 1
rel_rv64f = 0
rel_rv32d = 1
rel_rv64d = 0
rel_rv32c = 0
rel_rv64c = 0

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
size = 8

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
enable = true
section1 = 0x80000000,0x90000000
'''
def print_sample_config():
    """
        Print sample config.ini
    """
    with open('config.ini', 'w') as f:
        f.write(config_sample.strip('\n'))
