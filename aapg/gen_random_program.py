"""
    Module to generate random program based on configuration file
    Invoked from the gen subcommand of aapg
"""
import logging
import sys
import os
import configparser

def run(args):
    """ Entry point for generating new random assembly program
    
        Invoked from main.py

        Args:
            args: (namespace) Command line arguments parsed

        Returns:
            None
    """
    logger = logging.getLogger(__name__)
    logger.info("Command [GEN] invoked. Random program generation started")

    config_file_path = os.path.abspath(args.config_file)

    if not os.path.isfile(config_file_path):
        logger.error("{0} Not Found. Please supply existing config file".format(args.config_file))
        sys.exit(1)

    logger.info("Config file provided: {0}".format(config_file_path))
    config_args = configparser.ConfigParser()
    config_args.read(config_file_path)
