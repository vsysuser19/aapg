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
    main_parser.add_argument('--verbose', action = 'store', default = 'WARNING', \
            help = 'debug | info | warning | error')
    
    subparsers = main_parser.add_subparsers(help = 'Sub-commands Help')

    # Subparser: gen action
    gen_parser = subparsers.add_parser('gen', help = 'Generate a random program')

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
        raise ValueError('Non-integer log_level associated with {}'.format(log_level))

    logging.basicConfig(level = numeric_level)

def execute():
    """ Entry point for the AAPG program
    
        Invoked by
        * console-scripts section in pip
        * python -m aapg.main
    """
    args = parse_cmdline_opts()
    setup_logging(args.verbose)
    
    logger = logging.getLogger(__name__)

    logger.info("AAPG started")
