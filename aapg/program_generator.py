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
        self.current_access_section = None
        self.end = False

        # Create the data_access sections
        access_sections = args.items('access-sections')
        self.access_sections = []
        for item in access_sections:
            bounds = item[1].split(',')
            lower_bound = int(bounds[0], 16)
            upper_bound = int(bounds[1], 16)
            read_write = bounds[2]
            self.access_sections.append((lower_bound, upper_bound, read_write))

        # Seeding the PRNG generator
        random.seed(self.seed)
        aapg.args_generator.set_seed_args_gen(self.seed)
        aapg.isa_funcs.set_seed_isa_funcs(self.seed)

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

        # Setup the register file
        self.init_regfile(args.get('general', 'regs_not_use'))

        # Add a call to the pre-program macro
        logger.info("Adding pre-program macro")

        # Create Pre-lude
        logger.info("Creating Prelude")
        self.add_prelude()

        # Set SP to a legal range
        self.add_memory_instruction(random_gen = False)

        # Log debug messages
        logger.debug("Total instructions: {0}".format(self.total_instructions))
        logger.debug("Total instructions to generate: {0}".format(self.instructions_togen))

        # Branch control
        self.insts_since_last_branch = 0
        if 'rv32i.ctrl' in self.inst_dist:
            self.branch_bwd_prob = args.get('branch-control', 'backward-probability')
        self.q.put(('instruction', ['li', 't6', '0']))
        self.total_instructions += 1

        # Setup the user function call 
        self.user_calls_dict = {x[0] : ('f', int(x[1])) for x in args.items('user-functions') if int(x[1]) > 0}
        self.user_calls_dict['i_cache_thrash'] = ('f', args.getint('i-cache', 'num_calls'))
        
        ecause_filtered = list(filter(lambda x: int(x[1]) > 0, args.items('exception-generation')))

        for ecause in ecause_filtered:
            self.user_calls_dict[ecause[0]] = ('m', int(ecause[1]))

        keys = ' '.join(self.user_calls_dict.keys())

        logger.info('User functions received {}'.format(keys))

        # Add recursion call
        if self.recursion_enabled:
            self.user_calls_dict['.recurse'] = int(args.get(
                    'recursion-options', 'recursion-calls'))

    def __iter__(self):
        return self

    def __next__(self):
        if self.total_instructions != 0:
            self.generate_next_instruction()

        if self.q.empty():
            if not self.end:
                self.q.put(('instruction_nolabel', ('post_program_macro', )))
                self.q.put(('pseudo', ['j', 'write_tohost']))
                self.total_instructions += 2
                self.end = True
            elif self.recursion_enabled:
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

        # Randomly add a user-defined call
        temp_dict = self.user_calls_dict
        self.user_calls_dict = {x:temp_dict[x] for x in temp_dict if temp_dict[x][1] > 0}
        user_defined_total_calls = sum(map(lambda x: x[1], self.user_calls_dict.values()))
        logger.debug('User calls left {}'.format(user_defined_total_calls))

        if user_defined_total_calls > 0 and random.random() > 0.8:
            logger.debug('Adding a user call')

            # Select the user call
            user_call = random.choice(list(self.user_calls_dict.keys()))

            # Check if function call or macro
            if self.user_calls_dict[user_call][0] == 'f':
                self.q.put(('instruction', ('call', user_call)))
            else:
                self.q.put(('instruction', (user_call, )))
            self.user_calls_dict[user_call] = (self.user_calls_dict[user_call][0], self.user_calls_dict[user_call][1] - 1)
            return
            

        # Select a random instruction
        if self.instructions_togen > 0:
            next_inst_found = False
            while not next_inst_found:

                # If we have crossed a certain threshold from the
                # previous branch instruction, generate a branch
                # instruction possibly, otherwise omit the key
                if 'rv32i.ctrl' in self.inst_dist:
                    if self.insts_since_last_branch > self.min_insts_threshold:
                        isa_ext = 'rv32i.ctrl'
                    else:
                        isa_ext = random.choice(list(self.inst_dist_nobranch.keys()))
                else:
                    isa_ext = random.choice(list(self.inst_dist.keys()))

                if self.inst_dist[isa_ext] > 0:
                    next_inst = aapg.isa_funcs.get_random_inst_from_set(isa_ext)
                    self.inst_dist[isa_ext] -= 1

                    if isa_ext != 'rv32i.ctrl':
                        self.insts_since_last_branch += 1

                    next_inst_found = True

            # if memory_insts, randomly displace sp
            if next_inst[0] in aapg.isa_funcs.memory_insts:
                self.add_memory_instruction()
                next_inst = tuple([next_inst[0], next_inst[1], 'sp', next_inst[3]])

                # check data section and replace lw with sw
                if next_inst[0][0] != 'c':
                    if self.current_access_section[2] == 'w':
                        if 'l' in next_inst[0]:
                            next_inst_op = next_inst[0].replace('l', 's', 1)
                            next_inst = (next_inst_op,) + next_inst[1:]
                            logger.debug("Load to write section. Rewriting")
                    if self.current_access_section[2] == 'r':
                        if 's' in next_inst[0]:
                            next_inst_op = next_inst[0].replace('s', 'l', 1)
                            next_inst = (next_inst_op,) + next_inst[1:]
                            logger.debug("Store to read section. Rewriting")
                elif next_inst[0][0] == 'c':
                    if self.current_access_section[2] == 'w':
                        if 'l' in next_inst[0]:
                            next_inst_op = next_inst[0].replace('l', 's', 1)
                            next_inst = (next_inst_op,) + next_inst[1:]
                            logger.debug("Load to write section. Rewriting")
                    if self.current_access_section[2] == 'r':
                        if 's' in next_inst[0] and 'l' not in next_inst[0]:
                            next_inst_op = next_inst[0].replace('s', 'l', 1)
                            next_inst = (next_inst_op,) + next_inst[1:]
                            logger.debug("Store to read section. Rewriting")


            # if control instruction
            if isa_ext == 'rv32i.ctrl':
                next_insts = aapg.args_generator.gen_branch_args(
                        next_inst,
                        self.regfile,
                        self.arch,
                        insts_total = self.ref_total_instructions,
                        insts_left = self.instructions_togen,
                        insts_since = self.insts_since_last_branch,
                        bwd_prob = self.branch_bwd_prob
                )

                self.q.put(('branch', next_insts))
                # Reset the counters
                self.insts_since_last_branch = 0
                self.instructions_togen -= 1
                self.total_instructions -= 1
                return

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
        self.inst_dist_nobranch = {k:cd[k] for k in self.inst_dist if k != 'rv32i.ctrl'}
        if 'rv32i.ctrl' in self.inst_dist:
            self.min_insts_threshold = int(sum(self.inst_dist_nobranch.values())/self.inst_dist['rv32i.ctrl']) - 1
            logger.info("Branch threshold: {}".format(self.min_insts_threshold))
        else:
            self.min_insts_threshold = 0
        self.total_instructions = sum(self.inst_dist.values())
        self.instructions_togen = self.total_instructions

    def init_regfile(self, not_used_reg_string):
        """ Initialize the register file """
        not_used_regs = [(x[0], int(x[1:])) for x in not_used_reg_string.strip("'").split(',')]

        if 'rv32i.ctrl' in self.inst_dist:
            not_used_regs.append(('x', 31))

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
        self.q.put(('instruction_nolabel', ('pre_program_macro', )))
        self.total_instructions += 2
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
        self.q.put(('instruction', ('call', '.recurse')))
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
            self.total_instructions += 1
            self.current_access_section = access_section

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

    def next(self):
        """Python 2 compat"""
        return self.__next__()

    def __next__(self):
        if self.num_dwords == 0:
            raise StopIteration("Data Section Generated")
        else:
            self.num_dwords -= 1
            value = random.randint(0, 1<<64)
            address = ('.dword', "{0:#0{1}x}".format(value, 18))
            return address

class ThrashGenerator(object):
    """ Object to generate the data section """

    def __init__(self, cache_type, args):
        """ Initialize the data generator """
        logger.debug("Thrash generator instantiated")

        # Read the args
        self.num_bytes_per_block = int(args.getint(cache_type, 'num_bytes_per_block'))
        self.num_blocks = int(args.getint(cache_type, 'num_blocks'))
        self.num_cycles = int(args.getint(cache_type, 'num_cycles'))
        
        # Log configured args
        logger.info("Cache thrasher type: {}".format(cache_type))
        logger.info("Number of bytes per block: {}".format(self.num_bytes_per_block))
        logger.info("Number of blocks: {}".format(self.num_blocks))
        logger.info("Number of cycles: {}".format(self.num_cycles))

        # Local variables
        self.return_address_moved = False
        self.finished = False

        # Local counters
        self.block_index = 0
        self.byte_index = 0

    def __iter__(self):
        return self

    def next(self):
        """Python 2 compat"""
        return self.__next__()

    def __next__(self):
        if self.finished:
            raise StopIteration("Thrashing section generated")

        if not self.return_address_moved:
            self.return_address_moved = True
            # Move the return address from x1 into x31
            insts = [
                ('addi', 'x31', 'x1', '0'),
                ('li', 'x20', '{}'.format(self.num_cycles))]

            insts_left = int((self.num_bytes_per_block - 8) / 4)
            if insts_left > 0:
                insts.extend([('addi', 'x0', 'x0', '0')] * insts_left)
            return ('instructions', insts)

        # Creating the i-cache instructions
        if self.block_index < (2 * self.num_blocks):
            if self.byte_index == 0:
                self.byte_index = 2
                return (
                    'label',
                    'it' + '{0:09x}'.format(self.block_index),
                    ('j', 'it' + '{0:09x}'.format(self.block_index + 1)))

            elif self.byte_index > 0 and self.byte_index < self.num_bytes_per_block:
                self.byte_index += 1
                value = random.randint(0, (1<<8) - 1)
                data = ('byte',('.byte', "{0:#0{1}x}".format(value, 4)))
                return data
            elif self.byte_index == self.num_bytes_per_block:
                self.byte_index = 0
                self.block_index += 1
        elif self.block_index == 2*self.num_blocks:
            self.finished = True
            return (
                'label_instructions',
                'it' + '{0:09x}'.format(self.block_index),
                [
                    ('addi', 'x20', 'x20', '-1'),
                    ('bnez', 'x20', 'it' + '{0:09x}'.format(0)),
                    ('jr', 'x31')
                ])
