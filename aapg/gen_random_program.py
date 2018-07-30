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

logger = logging.getLogger(__name__)

def gen_random_program(ofile, args):
    """ Function to generate one random assembly program

        Args:
            ofile: Output file handler
            args: Configuration parser args obtained from (default) config.ini
    """

    # Instantiate AsmWriter
    writer = aapg.asm_writer.AsmWriter(ofile)

    # Header Section
    writer.comment("Random Assembly Program Generated using AAPG")
    writer.write('.text')
    writer.write('.align\t\t1')
    writer.write('.globl\t\tmain');
    writer.write('.type\t\tmain, @function');

    # Section main
    writer.write('main:', indent = 0)

    # Section instruction writer
    basic_generator = aapg.program_generator.BasicGenerator(args) 
    for line in basic_generator:
        if line[0] == 'section_heading':
            writer.write(line[1], indent = 0)
        elif line[0] == 'instruction':
            writer.write_inst(*line[1])

    # Jump to return address
    writer.write_inst('jr', 'ra')

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
    output_file_path = os.path.join(output_dir, output_asm_name + '_{:05d}'.format(index) + '.s')
    logger.info("Output file path: {0}".format(output_file_path))

    if os.path.isfile(output_file_path):
        logger.warn('Output file exists. Overwriting')

    with open(output_file_path, 'w') as output_file:
        gen_random_program(output_file, config_args)
