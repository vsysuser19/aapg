"""
    Automatic Assembly Program Generator (AAPG)

    Module of AAPG that deals with
        * Checking if signature file is created
        * Parsing signature file
        * Appending parseg signature file to test
        * Appending test function to template.S
"""
import logging
import argparse
import os
import io
import sys
import subprocess
import click
import yaml
import fileinput
from glob import glob

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

def format_sig(sig_file):
    """Format Signature

        Function to parse the generated signature files and return as list
    """
    f = open(sig_file,'r')
    #to_write = ['\t.data','\t.align 1','\t.globl ref_signature','ref_signature:']
    to_write = []
    while(True):
        line = f.readline()
        if not line:
            break
        write_line2,write_line1 = line[0:16],line[16:32]
        write_line1 = '.dword 0x'+write_line1
        write_line2 = '.dword 0x'+write_line2
        to_write.append(write_line1)
        to_write.append(write_line2)
    f.close()
    return to_write

def add_function_call(test_file):
    for line in fileinput.input(test_file, inplace=True):
        if "post_program_macro" in line:
            if "#" not in line:
                print("call check_sign_func\n", end='')
                print(line, end='')
        else:
            print(line, end='')


def add_self_check(output_dir,config_file):
    """Add Self Check

        Function to execute the makefile, extract signature and append to test

        Args:

    """
    setup_logging('info')
    logger = logging.getLogger()

    logger.info('Executing Makefile to generate signature dump \n')


    assembly = [y for x in os.walk(os.path.join(output_dir,'asm')) for y in glob(os.path.join(x[0], '*.S'))]

    test_file = None
    template_file = None
    for file in assembly:
        if "template.S" not in file:
            test_file = file
        elif "template.S" in file:
            template_file = file

    # Calculate the size of the signature section
    conf = yaml.safe_load(open(os.path.join(output_dir,config_file)))
    signature_start = None
    signature_end = None
    try:
        signature_section = conf['access-sections']['begin_signature']
        signature = signature_section.split(',')
        signature_start = int(signature[0],16)
        signature_end = int(signature[1],16)
    except:
        logger.error("Can not find `begin_signature` section in config file.")
        sys.exit(0)

    length = int((signature_end - signature_start)/8)
    logger.info("Size of signature section is {}".format(str(length)))
    length = length - 1

    func_to_add = """
.globl check_sign_func        
check_sign_func:
li t0, {}*REGBYTES
loop_label:
  la      sp, begin_signature
  add     sp, sp, t0
  LREG    t1, 0*REGBYTES(sp)

  la      sp, ref_signature
  add     sp, sp, t0
  LREG    t2, 0*REGBYTES(sp)

  bne     t1, t2, fail
  addi    t0, t0, -1*REGBYTES
  bgtz    t0, loop_label
pass:
  la      sp, begin_signature
  addi    sp, sp, 0 
  addi    t1, x0, 1
  SREG    t1, 0*REGBYTES(sp)
  ret
fail:
  la      sp, begin_signature
  addi    sp, sp, 0 
  addi    t1, x0, 0
  SREG    t1, 0*REGBYTES(sp)
  ret
    """.format(str(length))

    logger.info("Adding validation function to template file")

    check_function = func_to_add.split("\n")
    f = open(template_file,'a+')
    f.writelines(["%s\n" % item  for item in check_function])
    f.close()

    to_write1 = ['\t.data','\t.align 1','\t.globl ref_signature','ref_signature:']
    f = open(test_file,'a+')
    f.writelines(["%s\n" % item  for item in to_write1])
    f.close()
    
    # Execute MakeFile
    os.system("cd {};make".format(output_dir))

    # Check if signature file exists
    signature = [y for x in os.walk(output_dir) for y in glob(os.path.join(x[0], '*.dump.sign'))]
    if not signature:
        logger.error("Signature File was not created; Check if signature section is present in config/assembly")
        sys.exit(0)
    to_write = format_sig(signature[0])
    

    logger.info("Adding signature to the test file")

    f = open(test_file,'a+')
    f.writelines(["%s\n" % item  for item in to_write])
    f.close()

    logger.info("Adding function call to test file")

    add_function_call(test_file)    
    os.system("cd {};make clean".format(output_dir))