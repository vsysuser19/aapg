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

""" Setup the logger """
logger = logging.getLogger(__name__)

class BasicGenerator(object):
    """ Basic Generator to generate random instructions """

    def __init__(self, args):
        logger.debug("Created instance of BasicGenerator")

        # Instantiate local variables
        self.q = queue.Queue()
        self.total_instructions = int(args.get('general', 'total_instructions'))

        # Log debug messages
        logger.debug("Configuration parameters received")
        logger.debug("total_instructions: {0}".format(self.total_instructions))

    def __iter__(self):
        return self

    def __next__(self):
        self.pre_inst_gen()

        if self.q.empty():
            raise StopIteration('Instructions are over')

        return self.q.get()

    def pre_inst_gen(self):
        if self.total_instructions > 0:
            self.q.put('inst')

        self.total_instructions -= 1
