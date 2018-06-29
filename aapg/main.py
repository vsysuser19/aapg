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

import aapg.gen_random_program
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
    
    subparsers = main_parser.add_subparsers(help = 'Available sub-commands')

    # Subparser: gen action
    gen_parser = subparsers.add_parser('gen', help = 'Generate a random program')
    gen_parser.add_argument('--config-file', action = 'store', default = 'config.ini', metavar = "", \
        help="Configuration file. Default: ./config.ini" )
    gen_parser.add_argument('--asm-name', action = 'store', default = 'out.asm', \
            help = 'Assembly output file name. Default: out.asm', metavar = "")
    gen_parser.add_argument('--output-dir', action='store', default = './build', \
            help = 'Output directory. Default: ./build', metavar = "")
    gen_parser.set_defaults(func = aapg.gen_random_program.run)

    return main_parser.parse_args()

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
    args = parse_cmdline_opts()
    setup_logging(args.verbose)
    logger = logging.getLogger()
    logger.handlers = []
    ch = logging.StreamHandler()
    ch.setFormatter(aapg.utils.ColoredFormatter())
    logger.addHandler(ch)
    logger.info("AAPG started")

    # Call the required function for the sub-command
    args.func(args)
