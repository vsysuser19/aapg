"""
    Functions to setup the environment for building the generated asm
"""
import logging
import os

import aapg.env.prelude
import aapg.env.encoding
import aapg.env.linker
import aapg.env.make

logger = logging.getLogger(__name__)

def setup_build():
    """ Setup the build directory
        This command does the following steps
        * Create the common directory and put crt.S and encoding.h there
        * Create a top level Makefile to make the programs
    """

    logger.info("Build setup started")


    dirs = ['common', 'bin', 'log', 'objdump']
    common_dir = dirs[0]

    prelude_file = 'crt.S'
    encoding_file = 'encoding.h'
    linker_file = 'link.ld'
    make_file = 'Makefile'

    # Create the common directory 
    for dirname in dirs:
        try:
            os.makedirs(dirname)
        except FileExistsError as e:
            logger.warning('Folder exists. Not overwriting {}'.format(e))

    # Put the files in common
    with open(os.path.join(common_dir, prelude_file), 'w') as f:
        f.write(aapg.env.prelude.crt_asm.strip('\n'))

    with open(os.path.join(common_dir, encoding_file), 'w') as f:
        f.write(aapg.env.encoding.encoding_header.strip('\n'))

    with open(os.path.join(common_dir, linker_file), 'w') as f:
        f.write(aapg.env.linker.linker_script.strip('\n'))

    with open(os.path.join(make_file), 'w') as f:
        f.write(aapg.env.make.makefile.strip('\n'))
