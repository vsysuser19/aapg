"""
    Module to generate random program based on configuration file
    Invoked from the gen subcommand of aapg
"""
import logging
import sys
import os
from six.moves import configparser
import errno

import aapg.asm_writer
import aapg.program_generator
import aapg.utils

import datetime

logger = logging.getLogger(__name__)

def gen_random_program(ofile, args, arch, seed):
    """ Function to generate one random assembly program

        Args:
            ofile: Output file handler
            args: Configuration parser args obtained from (default) config.ini
    """

    # Instantiate AsmWriter
    writer = aapg.asm_writer.AsmWriter(ofile)

    # Header Section
    writer.comment(" Random Assembly Program Generated using aapg")
    writer.comment(" Generated at: {}".format(datetime.datetime.now().strftime("%H %T")))
    writer.comment(" Seed: {}".format(seed))
    writer.newline()
    writer.comment("include \"templates.S\"")
    writer.newline()
    writer.write('.text')
    writer.write('.align\t\t4')
    writer.write('.globl\t\tmain');
    writer.write('.type\t\tmain, @function');

    # Section instruction writer
    basic_generator = aapg.program_generator.BasicGenerator(args, arch, seed) 
    root_index = 0
    for index, line in enumerate(basic_generator):
        if line[0] == 'section':
            root_index = 0
            writer.write(line[1] + ":", indent = 0)
            logger.debug("Writing: " + " ".join(line[1]))
        elif line[0] == 'instruction':
            label = 'i' + '{0:010x}'.format(root_index)
            writer.write_inst(*line[1], label = label)
            root_index += 1
            logger.debug("Writing: " + " ".join(line[1]))
        elif line[0] == 'pseudo':
            label = 'i' + '{0:010x}'.format(root_index)
            writer.write_pseudo(*line[1], label = label)
            root_index += 1
            logger.debug("Writing: " + " ".join(line[1]))
        elif line[0] == 'branch':
            offset_string = line[1][-1]
            jump_backward = True if offset_string[0] == 'b' else False
            jump_length = int(offset_string[2:])
            label = '{:<11s}'.format('')

            if jump_backward:
                offset_label = 'i' + '{0:010x}'.format(root_index - jump_length) 
            else:
                offset_label = 'i' + '{0:010x}'.format(root_index + jump_length)

            writer.write('')
            writer.write('b' + '{0:010x}:'.format(root_index), indent = 0)
            for inst in line[1][:-1]:
                if offset_string in inst:
                    inst[-1] = offset_label
                writer.write_pseudo(*inst, indent = 4)
            writer.write('')

    writer.write('write_tohost:', indent = 0)
    writer.write_pseudo('li', 't5', '1')
    writer.write_pseudo('sw', 't5', 'tohost', 't4')
    writer.write('label: j label')
    writer.newline()

    # I-cache thrash
    writer.comment(" Cache thrashing routines")
    thrash_generator = aapg.program_generator.ThrashGenerator('i-cache', args)

    writer.write('i_cache_thrash:', indent = 0)

    for line in thrash_generator:
        if line is None:
            continue

        if line[0] == 'instruction':
            writer.write_inst(*line[1], indent = 4)
        elif line[0] == 'instructions':
            for inst in line[1]:
                writer.write_inst(*inst, indent = 4)
        elif line[0] == 'label_instructions':
            writer.write_inst(*line[2][0], label = line[1])
            for inst in line[2][1:]:
                writer.write_pseudo(*inst, indent = 4)
        elif line[0] == 'label':
            writer.write_inst(*line[2], label = line[1])
        elif line[0] == 'byte':
            writer.write_inst(*line[1], indent = 4)

    writer.newline()

    # Data section writer
    writer.write('.data')
    writer.write('.align 4')
    writer.write('.globl data')
    writer.write('data:', indent = 0)

    data_generator = aapg.program_generator.DataGenerator(args)
    for line in data_generator:
        writer.write_inst(*line)

    # Completed
    logger.info("Program generation completed")

def run(args, index):
    """ Entry point for generating new random assembly program
    
        Invoked from main.py

        Args:
            args: (namespace) Command line arguments parsed

        Returns:
            None
    """
    config_file_path = os.path.abspath(args.config_file)
    config_file_name = os.path.basename(config_file_path.rstrip(os.sep))

    output_dir = os.path.abspath(args.output_dir)
    output_asm_name = args.asm_name

    logger.info("Command [GEN] invoked. Random program generation started")
    logger.info("Config file path: {0}".format(config_file_path))

    # Check if valid config file provided
    if not os.path.isfile(config_file_path):
        logger.error("Config file not found. Please supply existing config file")
        sys.exit(1)

    logger.info("Config filename: {0}".format(config_file_name))
    config_args = configparser.ConfigParser()
    config_args.read(config_file_path)

    logger.info("Output directory selected: {0}".format(output_dir))
    try:
        os.makedirs(output_dir)
    except OSError as e:
        if e.errno == errno.EEXIST:
            logger.warn("Output directory exists")

    # Configure output file and run the program generator
    output_file_path = os.path.join(output_dir, output_asm_name + '_{:05d}'.format(index) + '.S')
    logger.info("Output file path: {0}".format(output_file_path))

    if os.path.isfile(output_file_path):
        logger.warn('Output file exists. Overwriting')

    with open(output_file_path, 'w') as output_file:
        seed_def = int.from_bytes(os.urandom(8), byteorder = 'big')
        seed = seed_def if args.seed is None else int(args.seed)
        gen_random_program(output_file, config_args, args.arch, seed)
