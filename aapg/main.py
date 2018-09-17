"""
    Automatic Assembly Program Generator (AAPG)

    Main module of AAPG that deals with
        * Parsing command line arguments
        * Reading configuration
        * Initiating the program generation
"""
import logging
import argparse
import os
import io
import sys
import subprocess

import aapg.gen_random_program
import aapg.env.env_setup
import aapg.utils

# Version read
VERSION = None
here = os.path.abspath(os.path.dirname(__file__))
with io.open(os.path.join(here, '__version__.py')) as f:
    VERSION = f.read()

def parse_cmdline_opts():
    """ Setup the cmdline parser

        Main parser args
        and subparsers setup here

        Args:
            None

        Returns:
            args: (dict) Command line arguments
    """
    # Main Parser
    main_parser = argparse.ArgumentParser(prog = 'aapg', description = 'Automated Assembly Program Generator for RISC-V')
    main_parser.add_argument('--version', action = 'version', version = VERSION)
    main_parser.add_argument('--verbose', action = 'store', default = 'info', \
            help = 'debug | info | warning | error', metavar = "")
    main_parser.add_argument('--num-programs', action = 'store', default = 1, type = int, dest = "num_programs", help = 'Number of programs to generate | Default = 1',
            metavar = '')
    
    subparsers = main_parser.add_subparsers(help = 'Available sub-commands', dest='command')

    # Subparser: gen action
    gen_parser = subparsers.add_parser('gen', help = 'Generate a random program')
    gen_parser.add_argument('--config-file', action = 'store', default = 'config.ini', metavar = "", \
        help="Configuration file. Default: ./config.ini" )
    gen_parser.add_argument('--asm-name', action = 'store', default = 'out', \
            help = 'Assembly output file name. Default: out.asm', metavar = "")
    gen_parser.add_argument('--output-dir', action='store', default = './asm', \
            help = 'Output directory for generated programs. Default: ./asm', metavar = "")
    gen_parser.add_argument('--arch', action='store', default = 'rv64', \
            help = 'Target architecture. Default: rv64', metavar = "")
    gen_parser.add_argument('--seed', action='store',\
            help = 'Seed to regenerate test.', metavar = "")

    # Subparser: sample
    sample_parser = subparsers.add_parser('sample', help = 'Generate a sample config.ini')

    # Subparset: setup
    # Setup the current directory to build all asms
    setup_parser = subparsers.add_parser('setup', help = 'Simulate a random program')

    return (main_parser.parse_args(), main_parser)

def setup_logging(log_level):
    """Setup logging

        Verbosity decided on user input

        Args:
            log_level: (str) User defined log level

        Returns:
            None
    """
    numeric_level = getattr(logging, log_level.upper(), None)

    if not isinstance(numeric_level, int):
        print("\033[91mInvalid log level passed. Please select from debug | info | warning | error\033[0m")
        sys.exit(1)

    logging.basicConfig(level = numeric_level)

def execute():
    """ Entry point for the AAPG program
    
        Invoked by
        * console-scripts section in pip
        * python -m aapg.main
    """
    args, parser = parse_cmdline_opts()
    setup_logging(args.verbose)
    logger = logging.getLogger()
    logger.handlers = []
    ch = logging.StreamHandler()
    ch.setFormatter(aapg.utils.ColoredFormatter())
    logger.addHandler(ch)
    logger.info("aapg started")

    # Call the required function for the sub-command
    if args.command == 'gen':
        logger.info("Command received: gen")
        logger.info("Number of programs to generate: {}".format(args.num_programs))
        for index in range(args.num_programs):
            logger.info("Program number: {} started".format(index))
            aapg.gen_random_program.run(args, index)
    elif args.command == 'setup':
        logger.info("Command received: setup")
        aapg.env.env_setup.setup_build()
        aapg.utils.print_sample_config()
        logger.info("Sample config written to config.ini")
    else:
        logger.error("No command received")

if __name__ == '__main__':
    execute()
