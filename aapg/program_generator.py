"""
    Module that contains random program generators

    Each program generator is a state machine that
    generates one instruction at a time. Each object
    creates a generator which can be iterated over

    #TODO: Inheritance
"""
from six.moves import queue
import logging

import aapg.utils
import aapg.opcodes

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

        # Setup the generator
        self.compute_instruction_distribution(args.items('isa-instruction-distribution'))

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
                next_inst = aapg.opcodes.get_random_inst_from_set(isa_ext)
                self.inst_dist[isa_ext] -= 1
                next_inst_found = True

        # Process the args for the instruction
        self.process_args(next_inst)

        self.q.put(next_inst)

        # Decrement total number of instructions
        self.total_instructions -= 1

    def compute_instruction_distribution(self, args):
        """ Function to compute fraction of instructions per ISA extension """
        cd = {}

        # Count relative values of instruction set
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
