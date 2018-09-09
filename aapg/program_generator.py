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

""" Setup the logger """
logger = logging.getLogger(__name__)

class BasicGenerator(object):
    """ Basic Generator to generate random instructions """

    def __init__(self, args, arch, seed):
        logger.debug("Created instance of BasicGenerator")

        # Instantiate local variables
        self.q = queue.Queue()
        self.total_instructions = int(args.get('general', 'total_instructions'))
        self.ref_total_instructions = self.total_instructions
        self.inst_dist = None
        self.regfile = {}
        self.instructions_togen = 0
        self.args = args
        self.end_sections = False
        self.recursion_enabled = args.getboolean('recursion-options', 'recursion-enable')
        self.arch = arch
        self.seed = seed
        
        # Create the data_access sections
        access_sections = args.items('access-sections')
        self.access_sections = []
        for item in access_sections:
            bounds = item[1].split(',')
            lower_bound = int(bounds[0], 16)
            upper_bound = int(bounds[1], 16)
            self.access_sections.append((lower_bound, upper_bound))

        # Seeding the PRNG generator
        random.seed(self.seed)
        aapg.args_generator.set_seed_args_gen(self.seed)
        aapg.isa_funcs.set_seed_isa_funcs(self.seed)

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

        # Set SP to a legal range
        self.add_memory_instruction(random_gen = False)

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
                    next_inst = aapg.isa_funcs.get_random_inst_from_set(isa_ext)
                    self.inst_dist[isa_ext] -= 1
                    next_inst_found = True

            # if memory_insts randomly displace sp
            if next_inst[0] in aapg.isa_funcs.memory_insts:
                self.add_memory_instruction()
                next_inst = tuple([next_inst[0], next_inst[1], 'sp', next_inst[3]])

            # Create args for next instruction
            next_inst_with_args = aapg.args_generator.gen_args(
                    next_inst,
                    self.regfile,
                    self.arch,
                    total = self.ref_total_instructions,
                    current = self.instructions_togen)

            # Put the instruction
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

    def add_memory_instruction(self, random_gen = True):
        """ Add a memory instruction
            With a certain percentage, move the stack pointer within the accepted
            access sections and then check the instruction type and create the
            offset
        """
        if random.random() < 0.2 or random_gen == False:
            # Select a random access section
            access_section = random.choice(self.access_sections)
            sp_address = random.randint(access_section[0] + 2048, access_section[1] - 2048)

            # Align to 64 bits
            sp_address = int(sp_address/8)*8
            self.q.put(('instruction', ['li', 'sp', hex(sp_address)]))


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
