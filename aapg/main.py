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
import click

import aapg.gen_random_program
import aapg.env.templates
# curdir = os.getcwd()
# os.chdir('aapg')
# import gen_random_program
# from gen_random_program import gen_config_files
# os.chdir(curdir)
import aapg.env.env_setup
import aapg.utils
from aapg.__init__ import __version__ as version

from multiprocessing import Process

#class TestClass:



# Version read
VERSION = '(' + version + ')' + ' Automated Assembly Program Generator - aapg'

# def parse_cmdline_opts():
#     """ Setup the cmdline parser

#         Main parser args
#         and subparsers setup here

#         Args:
#             None

#         Returns:
#             args: (dict) Command line arguments
#     """
#     # Main Parser
#     main_parser = argparse.ArgumentParser(prog = 'aapg', description = 'Automated Assembly Program Generator for RISC-V')
#     main_parser.add_argument('--version', action = 'version', version = VERSION)
#     main_parser.add_argument('--verbose', action = 'store', default = 'info', \
#             help = 'debug | info | warning | error', metavar = "")
    
#     subparsers = main_parser.add_subparsers(help = 'Available sub-commands', dest='command')

#     # Subparser: gen action
#     gen_parser = subparsers.add_parser('gen', help = 'Generate a random program')
#     gen_parser.add_argument('--num-programs', action = 'store', default = 1, type = int, dest = "num_programs", help = 'Number of programs to generate | Default = 1',
#             metavar = '')
#     gen_parser.add_argument('--config-file', action = 'store', default = 'config.yaml', metavar = "", \
#         help="Configuration file. Default: ./config.yaml" )
#     gen_parser.add_argument('--asm-name', action = 'store', default = 'out', \
#             help = 'Assembly output file name. Default: out.asm', metavar = "")
#     gen_parser.add_argument('--setup-dir', action='store', default = '.', \
#             help = 'Setup directory of env files. Default ./', metavar = "")
#     gen_parser.add_argument('--output-dir', action='store', default = '.', \
#             help = 'Output directory for generated programs. Default: ./asm', metavar = "")
#     gen_parser.add_argument('--arch', action='store', default = 'rv64', \
#             help = 'Target architecture. Default: rv64', metavar = "")
#     gen_parser.add_argument('--seed', action='store',\
#             help = 'Seed to regenerate test.', metavar = "")
#     gen_parser.add_argument('--linker-only', action='store_true', help = 'Generate link.ld only')

#     # Subparset: setup
#     # Setup the current directory to build all asms
#     setup_parser = subparsers.add_parser('setup', help = 'Setup the current dir')
#     setup_parser.add_argument('--setup-dir', action='store', default='.', help = 'Output directory for setup files. Default = ./', metavar = "")

#     return (main_parser.parse_args(), main_parser)


@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    if ctx.invoked_subcommand is None:
        click.echo('Either provide build or gen command')
    elif ctx.invoked_subcommand == 'version':
        click.echo('Checking version...')
    elif ctx.invoked_subcommand == 'gen':
        click.echo('gen Invoked %s' % ctx.invoked_subcommand)
    elif ctx.invoked_subcommand == 'setup':
        click.echo('setup invoked %s' % ctx.invoked_subcommand)
    elif ctx.invoked_subcommand == 'clean':
        click.echo('clean invoked %s' % ctx.invoked_subcommand)


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

# def execute():
#     """ Entry point for the AAPG program
    
#         Invoked by
#         * console-scripts section in pip
#         * python -m aapg.main
#     """
#     args, parser = parse_cmdline_opts()
#     setup_logging(args.verbose)
#     logger = logging.getLogger()
#     logger.handlers = []
#     ch = logging.StreamHandler()
#     ch.setFormatter(aapg.utils.ColoredFormatter())
#     logger.addHandler(ch)
#     logger.info("aapg started")

#     # Call the required function for the sub-command
#     if args.command == 'gen':
#         logger.info("Command received: gen")
#         logger.info("Number of programs to generate: {}".format(args.num_programs))

#         # If linker-only true, then generate linker and quit
#         logger.info("Linker script generation started")
#         aapg.gen_random_program.gen_config_files(args)
#         logger.info("Linker script generation completed")
#         if args.linker_only:
#             logger.info("linker-only option selected. Exiting aapg")
#             sys.exit(0)

#         # Generate the asm programs
#         process_list = []
#         for index in range(args.num_programs):
#             logger.info("Program number: {} started".format(index))
#             p = Process(target = aapg.gen_random_program.run, args = (args, index))
#             p.start()
#             process_list.append(p)

#         for p in process_list:
#             p.join()

#         for p in process_list:
#             if p.exitcode == 1:
#                 sys.exit(1)

#         sys.exit(0)

#     elif args.command == 'setup':
#         logger.info("Command received: setup")
#         aapg.env.env_setup.setup_build(args.setup_dir)
#         aapg.utils.print_sample_config(args.setup_dir)
#         logger.info("Setup directory built in {}".format(os.path.abspath(args.setup_dir)))
#     else:
#         logger.error("No command received")

class myClass:
    def __init__(self,num_programs,config_file,asm_name,setup_dir,output_dir,arch,seed,linker_only):
        self.num_programs = num_programs
        self.config_file = config_file
        self.asm_name = asm_name
        self.setup_dir = setup_dir
        self.output_dir = output_dir
        self.arch = arch
        self.seed = seed
        self.linker_only = linker_only

@cli.command()
@click.option('--num_programs', default=1, help='Number of programs to be generated')
@click.option('--config_file', default ='./config.yaml', help='Configuration file. Default: ./config.yaml')
@click.option('--asm_name', default ='out', help='Assembly output file name. Default: out.asm')
@click.option('--setup_dir', default ='work', help='Setup directory of env files. Default ./')
@click.option('--output_dir', default ='work', help='Output directory for generated programs. Default: ./asm')
@click.option('--arch', default ='rv64', help='Target architecture. Default: rv64')
@click.option('--seed', help='Seed to regenerate test.')
@click.option('--linker_only', is_flag='True',help='Generate link.ld only',default='False')
def gen(num_programs,config_file,asm_name,setup_dir,output_dir,arch,seed,linker_only):
    args = myClass(num_programs,config_file,asm_name,setup_dir,output_dir,arch,seed,linker_only)
    setup_logging('info')
    logger = logging.getLogger()
    logger.handlers = []
    ch = logging.StreamHandler()
    ch.setFormatter(aapg.utils.ColoredFormatter())
    logger.addHandler(ch)
    logger.info("aapg started")
    click.echo('The subcommand gen')
    logger.info("Command received: gen")
    logger.info("Number of programs to generate: {}".format(args.num_programs))

    # If linker-only true, then generate linker and quit
    logger.info("Linker script generation started")
    aapg.gen_random_program.gen_config_files(args)
    logger.info("Linker script generation completed")
    if args.linker_only:
        logger.info("linker-only option selected. Exiting aapg")
        sys.exit(0)

    process_list = []
    for index in range(args.num_programs):
        logger.info("Program number: {} started".format(index))
        p = Process(target = aapg.gen_random_program.run, args = (args, index))
        p.start()
        process_list.append(p)

    for p in process_list:
        p.join()

    for p in process_list:
        if p.exitcode == 1:
            sys.exit(1)

    sys.exit(0)

@cli.command()
@click.option('--setup_dir', default ='work', help='Setup directory of env files. Default ./')
def setup(setup_dir):
    setup_logging('info')
    logger = logging.getLogger()
    logger.handlers = []
    ch = logging.StreamHandler()
    ch.setFormatter(aapg.utils.ColoredFormatter())
    logger.addHandler(ch)
    logger.info("aapg started")
    logger.info("Command received: setup")
    aapg.env.env_setup.setup_build(setup_dir)
    aapg.utils.print_sample_config(setup_dir)
    logger.info("Setup directory built in {}".format(os.path.abspath(setup_dir)))

@cli.command()
def version():
    setup_logging('info')
    logger = logging.getLogger()
    logger.info(VERSION)
    

@cli.command()
@click.option('--setup_dir', default ='work', help='Setup directory of env files. Default ./')
@click.option('--output_dir', default ='work', help='Output directory for generated programs. Default: ./asm')
def clean(setup_dir,output_dir):
    setup_logging('info')
    logger = logging.getLogger()
    logger.info('Cleaning setup files....')
    # if setup_dir != '.':
    #     if os.path.isdir(setup_dir):
    #         os.system('rm -r {setup_dir}'.format(setup_dir=setup_dir))
    #     else:
    #         logger.info('The provided setup directory does not exist')
    # else:
    #     if os.path.exists('bin'):
    #         os.system('rm -r bin')
    #     if os.path.exists('common'):
    #         os.system('rm -r common')
    #     if os.path.exists('log'):
    #         os.system('rm -r log')
    #     if os.path.exists('objdump'):
    #         os.system('rm -r objdump')
    #     if os.path.exists('Makefile'):
    #         os.system('rm -r Makefile')
    #     if os.path.exists('asm'):
    #         os.system('rm -r asm')
        
    #     yaml_files = []
    #     ini_files = []
    #     for file in os.listdir("."):
    #         if file.endswith(".yaml"):
    #             yaml_files.append(file)
    #         if file.endswith(".ini"):
    #             ini_files.append(file)

    #     for item in yaml_files:
    #         os.system('rm -r {yaml_file}'.format(yaml_file=item))
    #     for item in ini_files:
    #         os.system('rm -r {ini_file}'.format(ini_file=item))

    # logger.info('Cleaning gen files...')
    # if output_dir != '.':
    #     if os.path.isdir(output_dir):
    #         os.system('rm -r {output_dir}'.format(output_dir=output_dir))
    #     else:
    #         logger.info('The provided output directory does not exist')

    # else:
    #     if os.path.exists('asm'):
    #         os.system('rm -r asm')

    if os.path.isdir(setup_dir):
        os.system('rm -r {setup_dir}'.format(setup_dir=setup_dir))
    else:
        if setup_dir=='work':
            logger.info('The default setup directory "work" does not exist')
        else:
            logger.info('The given setup directory does not exist!')

    if setup_dir != output_dir:
        logger.info('Cleaning gen files....')
        if os.path.isdir(output_dir):
            os.system('rm -r {output_dir}'.format(output_dir=output_dir))
        else:
            logger.info('Default output directory "work" does not exist. \n Maybe gen command was not run? \n Maybe setup_dir and output_dir are same?')

    logger.info('Finished cleaning')


if __name__ == '__main__':
    cli()
