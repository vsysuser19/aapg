"""
    Module to generate random program based on configuration file
    Invoked from the gen subcommand of aapg
"""
import logging
import sys
import os
import configparser

def gen_random_program(ofile, args):
    """ Function to generate one random assembly program
    """

def run(args):
    """ Entry point for generating new random assembly program
    
        Invoked from main.py

        Args:
            args: (namespace) Command line arguments parsed

        Returns:
            None
    """
    logger = logging.getLogger(__name__)

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
    except FileExistsError as e:
        logger.warn("Output directory exists")

    # Configure output file and run the program generator
    output_file_path = os.path.join(output_dir, output_asm_name)
    logger.info("Output file path: {0}".format(output_file_path))

    if os.path.isfile(output_file_path):
        logger.warn('Output file exists. Overwriting')

    with open(output_file_path, 'w') as output_file:
        gen_random_program(output_file, config_args)
