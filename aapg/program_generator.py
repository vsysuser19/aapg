"""
    Module that contains random program generators

    Each program generator is a state machine that
    generates one instruction at a time. Each object
    creates a generator which can be iterated over
"""
from six.moves import queue
from six.moves import configparser
import logging

import aapg.utils
import aapg.isa_funcs
import aapg.args_generator
import aapg.asm_templates

import random
import os
import sys

random.seed(os.urandom(128))

""" Setup the logger """
logger = logging.getLogger(__name__)

class BasicGenerator(object):
    """ Basic Generator to generate random instructions """

    def __init__(self, args, arch):
        logger.debug("Created instance of BasicGenerator")

        # Instantiate local variables
        self.q = queue.Queue()
        self.total_instructions = int(args.get('general', 'total_instructions'))
        self.inst_dist = None
        self.regfile = {}
        self.instructions_togen = 0
        self.args = args
        self.end_sections = False
        self.recursion_enabled = args.getboolean('recursion-options', 'recursion-enable')
        self.access_sections_enabled = args.getboolean('access-sections', 'enable')
        self.arch = arch

        # Setup the register file
        self.init_regfile(args.get('general', 'regs_not_use'))

        # Read the instruction distribution
        try:
            self.compute_instruction_distribution(args.items('isa-instruction-distribution'))
            logger.debug("Instruction distribution received")
            for k in self.inst_dist:
                logger.debug("{0} - {1}".format(k, self.inst_dist[k]))
        except configparser.NoSectionError as e:
            logger.error("Instruction distribution not specified.")
            logger.error("Check if your config file has the [isa-instruction-distribution] section")
            sys.exit(1)

        # Create Pre-lude
        logger.info("Creating Prelude")
        self.add_prelude()

        # Add recursion call
        if self.recursion_enabled:
            self.add_recursion_call()

        # Log debug messages
        logger.debug("Total instructions: {0}".format(self.total_instructions))
        logger.debug("Total instructions to generate: {0}".format(self.instructions_togen))

    def __iter__(self):
        return self

    def __next__(self):
        if self.total_instructions != 0:
            self.generate_next_instruction()

        if self.q.empty():
            if self.recursion_enabled:
                self.add_recursion_sections()
                self.recursion_enabled = False
            else:
                raise StopIteration('Instructions over')

        return self.q.get()
    
    def next(self):
        """Python 2 compat"""
        return self.__next__()

    def generate_next_instruction(self):
        # Check if total number of required instructions have been generated
        if self.total_instructions == 0:
            logger.info("Total number of instructions required generated")
            return

        # Select a random instruction
        if self.instructions_togen > 0:
            next_inst_found = False
            while not next_inst_found:
                isa_ext = random.choice(list(self.inst_dist.keys()))

                if self.inst_dist[isa_ext] > 0:
                    if self.access_sections_enabled:
                        if isa_ext in ['rv32i.data', 'rv64i.data']:
                            if self.arch == 'rv32':
                                next_inst = aapg.isa_funcs.get_random_inst_from_set('bounded-access-rv32')
                            elif self.arch == 'rv64':
                                next_inst = aapg.isa_funcs.get_random_inst_from_set('bounded-access-rv64')
                            self.inst_dist[isa_ext] -= 1
                            self.instructions_togen -= 1

                            insts_to_put = aapg.args_generator.gen_bounded_access_args(next_inst, self.regfile, self.args.items('access-sections'))
                            self.q.put(('pseudo', insts_to_put[0]))
                            self.q.put(('instruction', insts_to_put[1]))
                            return

                    next_inst = aapg.isa_funcs.get_random_inst_from_set(isa_ext)
                    self.inst_dist[isa_ext] -= 1
                    next_inst_found = True

            next_inst_with_args = aapg.args_generator.gen_args(next_inst, self.regfile, self.arch)
            self.q.put(('instruction', next_inst_with_args))
            self.instructions_togen -= 1

        # Decrement total number of instructions
        self.total_instructions -= 1
        return

    def compute_instruction_distribution(self, args):
        """ Function to compute fraction of instructions per ISA extension """

        # Dictionary to store the values of each instruction distribution
        cd = {}

        # Count relative values of instruction set
        # config format - rel_<inst_set>_instructions
        for item in args:
            isa_index = item[0].split('_')[1]
            if float(item[1]) > 0.0:
                cd[isa_index] = float(item[1])

        # Normalize them
        total_sum = sum(list([float(k) for k in cd.values()]))
        for k in cd:
            instr_count = int(cd[k]*self.total_instructions/total_sum)
            cd[k] = int(cd[k]*self.total_instructions/total_sum)

        self.inst_dist = cd
        self.total_instructions = sum(self.inst_dist.values())
        self.instructions_togen = self.total_instructions

    def init_regfile(self, not_used_reg_string):
        """ Initialize the register file """
        not_used_regs = [(x[0], int(x[1:])) for x in not_used_reg_string.strip("'").split(',')]
        for i in range(32):
            reg = ('x', i)
            if reg not in not_used_regs:
                self.regfile[('x', i)] = 0
        for i in range(32):
            reg = ('f', i)
            if reg not in not_used_regs:
                self.regfile[('f', i)] = 0

    def add_prelude(self):
        """Add the prelude instructions to the queue to be written"""
        args = {'stack_size': 32}
        self.q.put(('section', 'main'))
        self.total_instructions += 1
        for instruction in aapg.asm_templates.prelude_template(args):
            self.q.put(('instruction', instruction))
            self.total_instructions += 1

    def add_recursion_sections(self):
        """Add user-defined templates"""
        recursion_template_enabled = self.recursion_enabled
        logger.info("Recursion Enabled? {}".format(recursion_template_enabled))

        if recursion_template_enabled:
            recurse_sections = aapg.asm_templates.recurse_sections()
            for section in recurse_sections:
                self.q.put(('section', '.' + section))
                for instruction in recurse_sections[section]:
                    self.q.put(('pseudo', instruction))

        return

    def add_recursion_call(self):
        """ Add a recursion call """
        recursion_depth = self.args.getint('recursion-options', 'recursion-depth')
        self.q.put(('instruction', ('li', 'a0', str(recursion_depth))))
        self.q.put(('instruction', ('call', 'recurse')))
        self.total_instructions += 2
        logger.debug("Added recursion call")
        return

class DataGenerator(object):
    """ Object to generate the data section """

    def __init__(self, args):
        """ Initialize the data generator """
        logger.debug("Data generator instantiated")

        # Read the args
        data_size = int(args.getint('data-section', 'size'))
        
        # Log configured args
        logger.info("Data section size: {} KB".format(data_size))

        # Local variables
        self.num_dwords = data_size * 1024 / 64
        logger.debug("Num dwords: {}".format(self.num_dwords))

    def __iter__(self):
        return self

    def __next__(self):
        if self.num_dwords == 0:
            raise StopIteration("Data Section Generated")
        else:
            self.num_dwords -= 1
            value = random.randint(0, 1<<64)
            address = ('.dword', "{0:#0{1}x}".format(value, 18))
            return address
