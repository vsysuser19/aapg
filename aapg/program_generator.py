"""
    Module that contains random program generators

    Each program generator is a state machine that
    generates one instruction at a time. Each object
    creates a generator which can be iterated over
"""
from six.moves import queue
import logging

import aapg.utils
import aapg.isa_funcs
import aapg.args_generator

import random
import os

random.seed(os.urandom(128))

""" Setup the logger """
logger = logging.getLogger(__name__)

class BasicGenerator(object):
    """ Basic Generator to generate random instructions """

    def __init__(self, args):
        logger.debug("Created instance of BasicGenerator")

        # Instantiate local variables
        self.q = queue.Queue()
        self.total_instructions = int(args.get('general', 'total_instructions'))
        self.inst_dist = None
        self.regfile = {}

        # Setup the generator
        self.compute_instruction_distribution(args.items('isa-instruction-distribution'))
        self.init_regfile()

        # Log debug messages
        logger.debug("Total_instructions: {0}".format(self.total_instructions))
        logger.debug("Instruction distribution received")
        for k in self.inst_dist:
            logger.debug("{0} - {1}".format(k, self.inst_dist[k]))

    def __iter__(self):
        return self

    def __next__(self):
        self.generate_next_instruction()

        if self.q.empty():
            raise StopIteration('Instructions are over')

        return self.q.get()

    def generate_next_instruction(self):

        # Check if total number of required instructions have been generated
        if self.total_instructions == 0:
            logger.info("Total number of instructions required generated")
            return

        # Select a random instruction
        next_inst_found = False
        while not next_inst_found:
            isa_ext = random.choice(list(self.inst_dist.keys()))
            if self.inst_dist[isa_ext] > 0:
                next_inst = aapg.isa_funcs.get_random_inst_from_set(isa_ext)
                self.inst_dist[isa_ext] -= 1
                next_inst_found = True

        next_inst_with_args = aapg.args_generator.gen_args(next_inst, self.regfile)
        self.q.put(next_inst_with_args)

        # Decrement total number of instructions
        self.total_instructions -= 1

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

    def init_regfile(self):
        """ Initialize the register file """
        for i in range(32):
            self.regfile[('x', i)] = 0
        for i in range(32):
            self.regfile[('f', i)] = 0
