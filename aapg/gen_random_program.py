"""
    Module to generate random program based on configuration file
    Invoked from the gen subcommand of aapg
"""
import logging
import sys
import os
from six.moves import configparser
import errno
import re
import random
import pytz

import aapg.asm_writer
import aapg.program_generator
import aapg.utils
import aapg.env
from aapg.__init__ import __version__ as version

import datetime

logger = logging.getLogger(__name__)

ecause00 = '''.macro ecause00'''
ecause01 = '''.macro ecause01'''
ecause02 = '''.macro ecause02'''
ecause03 = '''.macro ecause03'''
ecause04 = '''.macro ecause04'''
ecause05 = '''.macro ecause05'''
ecause06 = '''.macro ecause06'''
ecause07 = '''.macro ecause07'''
ecause08 = '''.macro ecause08'''
ecause09 = '''.macro ecause09'''
ecause10 = '''.macro ecause10'''
ecause11 = '''.macro ecause11'''
ecause12 = '''.macro ecause12'''
ecause13 = '''.macro ecause13'''
ecause14 = '''.macro ecause14'''

#List of registers that must not be used if Branch is enabled
no_use_regs = []
ecause00_r = []
ecause01_r = []
ecause02_r = []
ecause03_r = []
ecause04_r = []
ecause05_r = []
ecause06_r = []
ecause07_r = []
ecause08_r = []
ecause09_r = []
ecause10_r = []
ecause11_r = []
ecause12_r = []
ecause13_r = []
ecause14_r = []


def init_global_wth_seed(seed):
  random.seed(seed)
  reg1 = random.randint(0,29) + 1
  reg2 = random.randint(0,27)
  if reg1 == 11 or reg1 == 2:
    reg1=reg1+1
  if (reg1 == reg2):
    reg2=reg2+1
  if (reg2 == 11 or reg2 == 2):
    reg2=reg2+1

  no_use_regs.append(reg1)
  no_use_regs.append(reg2)

  ecause00_r = ['''
  .macro ecause00
  # stack push
  addi sp, sp, -2*REGBYTES
  SREG a1,  1*REGBYTES(sp)
  SREG x{reg1},  2*REGBYTES(sp)
    
  # exception
  la x{reg1}, 2f
  la a1, 1f
    1:
  jr 2(x{reg1})
    2: 
  nop
  nop
  # stack pop
  LREG a1, 1*REGBYTES(sp)
  LREG x{reg1}, 2*REGBYTES(sp)
  addi sp, sp, 1*REGBYTES
  .endm
  '''.format(reg1=reg1,reg2=reg2),
    '''  
  .macro ecause00
  # stack push
  addi sp, sp, -3*REGBYTES
  SREG a1, 1*REGBYTES(sp)
  SREG x{reg1}, 2*REGBYTES(sp)
  SREG x{reg2}, 3*REGBYTES(sp)
    
  # exception
  la x{reg1}, 2f
  la a1, 1f
  1:
  jalr x{reg2}, 2(x{reg1})
  2:
  nop
  nop
  # stack pop
  LREG a1, 1*REGBYTES(sp)
  LREG x{reg1}, 2*REGBYTES(sp)
  LREG x{reg2}, 3*REGBYTES(sp)
  addi sp, sp, 3*REGBYTES

  .endm
  '''.format(reg1=str(reg1),reg2=str(reg2))]


  reg1 = random.randint(0,29) + 1
  reg2 = random.randint(0,27)
  if reg1 == 11 or reg1 == 2:
    reg1=reg1+1
  if (reg1 == reg2):
    reg2=reg2+1
  if (reg2 == 11 or reg2 == 2):
    reg2=reg2+1
  no_use_regs.append(reg1)
  no_use_regs.append(reg2)
  ecause01_r = [
  '''
  .macro ecause01
  # stack push
  addi sp, sp, -1*REGBYTES
  SREG a1,  1*REGBYTES(sp)
    
  # exception
  la a1, 1f
    1:
  jr x0

  # stack pop
  LREG a1,  1*REGBYTES(sp)
  addi sp, sp,  1*REGBYTES
  .endm
  '''.format(reg1=reg1,reg2=reg2),
    '''
  .macro ecause01
  # stack push
  addi sp, sp, -2*REGBYTES
  SREG a1,  1*REGBYTES(sp)
  SREG x{reg1},  2*REGBYTES(sp)
    
  # exception
  la a1, 1f
    1:
  jalr x{reg1}, x0
    
  # stack pop
  LREG a1,  1*REGBYTES(sp)
  LREG x{reg1},  2*REGBYTES(sp)
  addi sp, sp,  2*REGBYTES
  .endm
  '''.format(reg1=reg1,reg2=reg2),
    '''
  .macro ecause01
  # stack push
  addi sp, sp, -2*REGBYTES
  SREG a1,  1*REGBYTES(sp)
  SREG x{reg1},  2*REGBYTES(sp)
    
  # exception
  la a1, 1f
  li x{reg1}, 0
    1: 
  jr x{reg1}

  # stack pop
  LREG a1,  1*REGBYTES(sp)
  LREG x{reg1},  2*REGBYTES(sp)
  addi sp, sp,  2*REGBYTES
  .endm
  '''.format(reg1=reg1,reg2=reg2),
    '''
  .macro ecause01
  # stack push
  addi sp, sp, -3*REGBYTES
  SREG a1,  1*REGBYTES(sp)
  SREG x{reg1},  2*REGBYTES(sp)
  SREG x{reg2},  3*REGBYTES(sp)
    
  # exception
  la a1, 1f
  li x{reg1}, 0
    1: 
  jalr x{reg2}, x{reg1}

  # stack pop
  LREG a1,  1*REGBYTES(sp)
  LREG x{reg1},  2*REGBYTES(sp)
  LREG x{reg2},  3*REGBYTES(sp)
  addi sp, sp,  3*REGBYTES
    
  .endm
  '''.format(reg1=reg1,reg2=reg2)
  ]

  ecause02_r=[
  '''
  .macro ecause02
  .word 0x4B04183B
  .endm
  '''
  ]

  ecause03_r=[
  '''
  .macro ecause03
  ebreak
  .endm
  '''
  ]


  reg1 = random.randint(0,29) + 1
  reg2 = random.randint(0,27)
  if reg1 == 11 or reg1 == 2:
    reg1=reg1+1
  if (reg1 == reg2):
    reg2=reg2+1
  if (reg2 == 11 or reg2 == 2):
    reg2=reg2+1
  no_use_regs.append(reg1)
  no_use_regs.append(reg2)
  ecause04_r = [
  '''
  .macro ecause04
  # stack push
  addi sp, sp, -1*REGBYTES
  SREG x{reg2},  1*REGBYTES(sp)
    
  #exception
  LREG x{reg2}, 1(sp)

  # stack pop
  LREG x{reg2}, 1*REGBYTES(sp)
  addi sp, sp, 1*REGBYTES
  .endm
  '''.format(reg1=reg1,reg2=reg2),
    '''
  .macro ecause04
  # stack push
  addi sp, sp, -1*REGBYTES
  SREG x{reg2},  1*REGBYTES(sp)
    
  #exception
  LREG x{reg2}, 2(sp)

  # stack pop
  LREG x{reg2}, 1*REGBYTES(sp)
  addi sp, sp, 1*REGBYTES
  .endm
  '''.format(reg1=reg1,reg2=reg2),
    '''
  .macro ecause04
  # stack push
  addi sp, sp, -1*REGBYTES
  SREG x{reg2},  1*REGBYTES(sp)
    
  #exception
  LREG x{reg2}, 3(sp)

  # stack pop
  LREG x{reg2}, 1*REGBYTES(sp)
  addi sp, sp, 1*REGBYTES
  .endm
  '''.format(reg1=reg1,reg2=reg2),
    '''
  .macro ecause04
  # stack push
  addi sp, sp, -1*REGBYTES
  SREG x{reg2},  1*REGBYTES(sp)
    
  #exception
  LREGU x{reg2}, 1(sp)

  # stack pop
  LREG x{reg2}, 1*REGBYTES(sp)
  addi sp, sp, 1*REGBYTES
  .endm
  '''.format(reg1=reg1,reg2=reg2),
    '''
  .macro ecause04
  # stack push
  addi sp, sp, -1*REGBYTES
  SREG x{reg2},  1*REGBYTES(sp)
    
  #exception
  LREGU x{reg2}, 2(sp)

  # stack pop
  LREG x{reg2}, 1*REGBYTES(sp)
  addi sp, sp, 1*REGBYTES
  .endm
  '''.format(reg1=reg1,reg2=reg2),
    '''
  .macro ecause04
  # stack push
  addi sp, sp, -1*REGBYTES
  SREG x{reg2},  1*REGBYTES(sp)
    
  #exception
  LREGU x{reg2}, 3(sp)

  # stack pop
  LREG x{reg2}, 1*REGBYTES(sp)
  addi sp, sp, 1*REGBYTES
  .endm
  '''.format(reg1=reg1,reg2=reg2),
    '''
  .macro ecause04
  # stack push
  addi sp, sp, -1*REGBYTES
  SREG x{reg2},  1*REGBYTES(sp)
    
  #exception
  lw x{reg2}, 1(sp)

  # stack pop
  LREG x{reg2}, 1*REGBYTES(sp)
  addi sp, sp, 1*REGBYTES
  .endm
  '''.format(reg1=reg1,reg2=reg2),
    '''
  .macro ecause04
  # stack push
  addi sp, sp, -1*REGBYTES
  SREG x{reg2},  1*REGBYTES(sp)
    
  #exception
  lw x{reg2}, 2(sp)

  # stack pop
  LREG x{reg2}, 1*REGBYTES(sp)
  addi sp, sp, 1*REGBYTES
  .endm
  '''.format(reg1=reg1,reg2=reg2),
    '''
  .macro ecause04
  # stack push
  addi sp, sp, -1*REGBYTES
  SREG x{reg2},  1*REGBYTES(sp)
    
  #exception
  lw x{reg2}, 3(sp)

  # stack pop
  LREG x{reg2}, 1*REGBYTES(sp)
  addi sp, sp, 1*REGBYTES
  .endm
  '''.format(reg1=reg1,reg2=reg2),
    '''
  .macro ecause04
  # stack push
  addi sp, sp, -1*REGBYTES
  SREG x{reg2},  1*REGBYTES(sp)
    
  #exception
  lh x{reg2}, 1(sp)

  # stack pop
  LREG x{reg2}, 1*REGBYTES(sp)
  addi sp, sp, 1*REGBYTES
  .endm
  '''.format(reg1=reg1,reg2=reg2),
    '''
  .macro ecause04
  # stack push
  addi sp, sp, -1*REGBYTES
  SREG x{reg2},  1*REGBYTES(sp)
    
  #exception
  lh x{reg2}, 3(sp)

  # stack pop
  LREG x{reg2}, 1*REGBYTES(sp)
  addi sp, sp, 1*REGBYTES
  .endm
  '''.format(reg1=reg1,reg2=reg2),
    '''
  .macro ecause04
  # stack push
  addi sp, sp, -1*REGBYTES
  SREG x{reg2},  1*REGBYTES(sp)
    
  #exception
  lhu x{reg2}, 1(sp)

  # stack pop
  LREG x{reg2}, 1*REGBYTES(sp)
  addi sp, sp, 1*REGBYTES
  .endm
  '''.format(reg1=reg1,reg2=reg2),
    '''
  .macro ecause04
  # stack push
  addi sp, sp, -1*REGBYTES
  SREG x{reg2},  1*REGBYTES(sp)
    
  #exception
  lhu x{reg2}, 3(sp)

  # stack pop
  LREG x{reg2}, 1*REGBYTES(sp)
  addi sp, sp, 1*REGBYTES
  .endm
  '''.format(reg1=reg1,reg2=reg2),
    '''
  .macro ecause04
  # stack push
  addi sp, sp, -2*REGBYTES
  SREG x{reg1},  1*REGBYTES(sp)
  SREG x{reg2},  2*REGBYTES(sp)
    
  #exception
  mv x{reg1}, sp
  LREG x{reg2}, 1(x{reg1})

  # stack pop
  LREG x{reg1},  1*REGBYTES(sp)
  LREG x{reg2},  2*REGBYTES(sp)
  addi sp, sp, 2*REGBYTES
  .endm
  '''.format(reg1=reg1,reg2=reg2),
    '''
  .macro ecause04
  # stack push
  addi sp, sp, -2*REGBYTES
  SREG x{reg1},  1*REGBYTES(sp)
  SREG x{reg2},  2*REGBYTES(sp)
    
  #exception
  mv x{reg1}, sp
  LREG x{reg2}, 2(x{reg1})

  # stack pop
  LREG x{reg1},  1*REGBYTES(sp)
  LREG x{reg2},  2*REGBYTES(sp)
  addi sp, sp, 2*REGBYTES
  .endm
  '''.format(reg1=reg1,reg2=reg2),
    '''
  .macro ecause04
  # stack push
  addi sp, sp, -2*REGBYTES
  SREG x{reg1},  1*REGBYTES(sp)
  SREG x{reg2},  2*REGBYTES(sp)
    
  #exception
  mv x{reg1}, sp
  LREG x{reg2}, 3(x{reg1})

  # stack pop
  LREG x{reg1},  1*REGBYTES(sp)
  LREG x{reg2},  2*REGBYTES(sp)
  addi sp, sp, 2*REGBYTES
  .endm
  '''.format(reg1=reg1,reg2=reg2),
    '''
  .macro ecause04
  # stack push
  addi sp, sp, -2*REGBYTES
  SREG x{reg1},  1*REGBYTES(sp)
  SREG x{reg2},  2*REGBYTES(sp)
    
  #exception
  mv x{reg1}, sp
  LREGU x{reg2}, 1(x{reg1})

  # stack pop
  LREG x{reg1},  1*REGBYTES(sp)
  LREG x{reg2},  2*REGBYTES(sp)
  addi sp, sp, 2*REGBYTES
  .endm
  '''.format(reg1=reg1,reg2=reg2),
    '''
  .macro ecause04
  # stack push
  addi sp, sp, -2*REGBYTES
  SREG x{reg1},  1*REGBYTES(sp)
  SREG x{reg2},  2*REGBYTES(sp)
    
  #exception
  mv x{reg1}, sp
  LREGU x{reg2}, 2(x{reg1})

  # stack pop
  LREG x{reg1},  1*REGBYTES(sp)
  LREG x{reg2},  2*REGBYTES(sp)
  addi sp, sp, 2*REGBYTES
  .endm
  '''.format(reg1=reg1,reg2=reg2),
    '''
  .macro ecause04
  # stack push
  addi sp, sp, -2*REGBYTES
  SREG x{reg1},  1*REGBYTES(sp)
  SREG x{reg2},  2*REGBYTES(sp)
    
  #exception
  mv x{reg1}, sp
  LREGU x{reg2}, 3(x{reg1})

  # stack pop
  LREG x{reg1},  1*REGBYTES(sp)
  LREG x{reg2},  2*REGBYTES(sp)
  addi sp, sp, 2*REGBYTES
  .endm
  '''.format(reg1=reg1,reg2=reg2),
    '''
  .macro ecause04
  # stack push
  addi sp, sp, -2*REGBYTES
  SREG x{reg1},  1*REGBYTES(sp)
  SREG x{reg2},  2*REGBYTES(sp)
    
  #exception
  mv x{reg1}, sp
  lw x{reg2}, 1(x{reg1})

  # stack pop
  LREG x{reg1},  1*REGBYTES(sp)
  LREG x{reg2},  2*REGBYTES(sp)
  addi sp, sp, 2*REGBYTES
  .endm
  '''.format(reg1=reg1,reg2=reg2),
    '''
  .macro ecause04
  # stack push
  addi sp, sp, -2*REGBYTES
  SREG x{reg1},  1*REGBYTES(sp)
  SREG x{reg2},  2*REGBYTES(sp)
    
  #exception
  mv x{reg1}, sp
  lw x{reg2}, 2(x{reg1})

  # stack pop
  LREG x{reg1},  1*REGBYTES(sp)
  LREG x{reg2},  2*REGBYTES(sp)
  addi sp, sp, 2*REGBYTES
  .endm
  '''.format(reg1=reg1,reg2=reg2),
    '''
  .macro ecause04
  # stack push
  addi sp, sp, -2*REGBYTES
  SREG x{reg1},  1*REGBYTES(sp)
  SREG x{reg2},  2*REGBYTES(sp)
    
  #exception
  mv x{reg1}, sp
  lw x{reg2}, 3(x{reg1})

  # stack pop
  LREG x{reg1},  1*REGBYTES(sp)
  LREG x{reg2},  2*REGBYTES(sp)
  addi sp, sp, 2*REGBYTES
  .endm
  '''.format(reg1=reg1,reg2=reg2),
    '''
  .macro ecause04
  # stack push
  addi sp, sp, -2*REGBYTES
  SREG x{reg1},  1*REGBYTES(sp)
  SREG x{reg2},  2*REGBYTES(sp)
    
  #exception
  mv x{reg1}, sp
  lh x{reg2}, 1(x{reg1})

  # stack pop
  LREG x{reg1},  1*REGBYTES(sp)
  LREG x{reg2},  2*REGBYTES(sp)
  addi sp, sp, 2*REGBYTES
  .endm
  '''.format(reg1=reg1,reg2=reg2),
    '''
  .macro ecause04
  # stack push
  addi sp, sp, -2*REGBYTES
  SREG x{reg1},  1*REGBYTES(sp)
  SREG x{reg2},  2*REGBYTES(sp)
    
  #exception
  mv x{reg1}, sp
  lh x{reg2}, 3(x{reg1})

  # stack pop
  LREG x{reg1},  1*REGBYTES(sp)
  LREG x{reg2},  2*REGBYTES(sp)
  addi sp, sp, 2*REGBYTES
  .endm
  '''.format(reg1=reg1,reg2=reg2),
    '''
  .macro ecause04
  # stack push
  addi sp, sp, -2*REGBYTES
  SREG x{reg1},  1*REGBYTES(sp)
  SREG x{reg2},  2*REGBYTES(sp)
    
  #exception
  mv x{reg1}, sp
  lhu x{reg2}, 1(x{reg1})

  # stack pop
  LREG x{reg1},  1*REGBYTES(sp)
  LREG x{reg2},  2*REGBYTES(sp)
  addi sp, sp, 2*REGBYTES
  .endm
  '''.format(reg1=reg1,reg2=reg2),
    '''
  .macro ecause04
  # stack push
  addi sp, sp, -2*REGBYTES
  SREG x{reg1},  1*REGBYTES(sp)
  SREG x{reg2},  2*REGBYTES(sp)
    
  #exception
  mv x{reg1}, sp
  lhu x{reg2}, 3(x{reg1})

  # stack pop
  LREG x{reg1},  1*REGBYTES(sp)
  LREG x{reg2},  2*REGBYTES(sp)
  addi sp, sp, 2*REGBYTES
  .endm
  '''.format(reg1=reg1,reg2=reg2),
    '''
  .macro ecause04
  # stack push
  addi sp, sp, -2*REGBYTES
  SREG x{reg1},  1*REGBYTES(sp)
  SREG x{reg2},  2*REGBYTES(sp)
    
  #exception
  mv x{reg1}, sp
  li x{reg2}, 1
  mul x{reg1}, x{reg1}, x{reg2}
  LREG x{reg2}, 1(x{reg1})
  mul x{reg1}, x{reg1}, x{reg2}

  # stack pop
  LREG x{reg1},  1*REGBYTES(sp)
  LREG x{reg2},  2*REGBYTES(sp)
  addi sp, sp, 2*REGBYTES
  .endm
  '''.format(reg1=reg1,reg2=reg2),
    '''
  .macro ecause04
  # stack push
  addi sp, sp, -2*REGBYTES
  SREG x{reg1},  1*REGBYTES(sp)
  SREG x{reg2},  2*REGBYTES(sp)
    
  #exception
  mv x{reg1}, sp
  li x{reg2}, 1
  mul x{reg1}, x{reg1}, x{reg2}
  LREG x{reg2}, 2(x{reg1})
  mul x{reg1}, x{reg1}, x{reg2}

  # stack pop
  LREG x{reg1},  1*REGBYTES(sp)
  LREG x{reg2},  2*REGBYTES(sp)
  addi sp, sp, 2*REGBYTES
  .endm
  '''.format(reg1=reg1,reg2=reg2),
    '''
  .macro ecause04
  # stack push
  addi sp, sp, -2*REGBYTES
  SREG x{reg1},  1*REGBYTES(sp)
  SREG x{reg2},  2*REGBYTES(sp)
    
  #exception
  mv x{reg1}, sp
  li x{reg2}, 1
  mul x{reg1}, x{reg1}, x{reg2}
  LREG x{reg2}, 3(x{reg1})
  mul x{reg1}, x{reg1}, x{reg2}

  # stack pop
  LREG x{reg1},  1*REGBYTES(sp)
  LREG x{reg2},  2*REGBYTES(sp)
  addi sp, sp, 2*REGBYTES
  .endm
  '''.format(reg1=reg1,reg2=reg2),
    '''
  .macro ecause04
  # stack push
  addi sp, sp, -2*REGBYTES
  SREG x{reg1},  1*REGBYTES(sp)
  SREG x{reg2},  2*REGBYTES(sp)
    
  #exception
  mv x{reg1}, sp
  li x{reg2}, 1
  mul x{reg1}, x{reg1}, x{reg2}
  LREGU x{reg2}, 1(x{reg1})
  mul x{reg1}, x{reg1}, x{reg2}

  # stack pop
  LREG x{reg1},  1*REGBYTES(sp)
  LREG x{reg2},  2*REGBYTES(sp)
  addi sp, sp, 2*REGBYTES
  .endm
  '''.format(reg1=reg1,reg2=reg2),
    '''
  .macro ecause04
  # stack push
  addi sp, sp, -2*REGBYTES
  SREG x{reg1},  1*REGBYTES(sp)
  SREG x{reg2},  2*REGBYTES(sp)
    
  #exception
  mv x{reg1}, sp
  li x{reg2}, 1
  mul x{reg1}, x{reg1}, x{reg2}
  LREGU x{reg2}, 2(x{reg1})
  mul x{reg1}, x{reg1}, x{reg2}

  # stack pop
  LREG x{reg1},  1*REGBYTES(sp)
  LREG x{reg2},  2*REGBYTES(sp)
  addi sp, sp, 2*REGBYTES
  .endm
  '''.format(reg1=reg1,reg2=reg2),
    '''
  .macro ecause04
  # stack push
  addi sp, sp, -2*REGBYTES
  SREG x{reg1},  1*REGBYTES(sp)
  SREG x{reg2},  2*REGBYTES(sp)
    
  #exception
  mv x{reg1}, sp
  li x{reg2}, 1
  mul x{reg1}, x{reg1}, x{reg2}
  LREGU x{reg2}, 3(x{reg1})
  mul x{reg1}, x{reg1}, x{reg2}

  # stack pop
  LREG x{reg1},  1*REGBYTES(sp)
  LREG x{reg2},  2*REGBYTES(sp)
  addi sp, sp, 2*REGBYTES
  .endm
  '''.format(reg1=reg1,reg2=reg2),
    '''
  .macro ecause04
  # stack push
  addi sp, sp, -2*REGBYTES
  SREG x{reg1},  1*REGBYTES(sp)
  SREG x{reg2},  2*REGBYTES(sp)
    
  #exception
  mv x{reg1}, sp
  li x{reg2}, 1
  mul x{reg1}, x{reg1}, x{reg2}
  lw x{reg2}, 1(x{reg1})
  mul x{reg1}, x{reg1}, x{reg2}

  # stack pop
  LREG x{reg1},  1*REGBYTES(sp)
  LREG x{reg2},  2*REGBYTES(sp)
  addi sp, sp, 2*REGBYTES
  .endm
  '''.format(reg1=reg1,reg2=reg2),
    '''
  .macro ecause04
  # stack push
  addi sp, sp, -2*REGBYTES
  SREG x{reg1},  1*REGBYTES(sp)
  SREG x{reg2},  2*REGBYTES(sp)
    
  #exception
  mv x{reg1}, sp
  li x{reg2}, 1
  mul x{reg1}, x{reg1}, x{reg2}
  lw x{reg2}, 2(x{reg1})
  mul x{reg1}, x{reg1}, x{reg2}

  # stack pop
  LREG x{reg1},  1*REGBYTES(sp)
  LREG x{reg2},  2*REGBYTES(sp)
  addi sp, sp, 2*REGBYTES
  .endm
  '''.format(reg1=reg1,reg2=reg2),
    '''
  .macro ecause04
  # stack push
  addi sp, sp, -2*REGBYTES
  SREG x{reg1},  1*REGBYTES(sp)
  SREG x{reg2},  2*REGBYTES(sp)
    
  #exception
  mv x{reg1}, sp
  li x{reg2}, 1
  mul x{reg1}, x{reg1}, x{reg2}
  lw x{reg2}, 3(x{reg1})
  mul x{reg1}, x{reg1}, x{reg2}

  # stack pop
  LREG x{reg1},  1*REGBYTES(sp)
  LREG x{reg2},  2*REGBYTES(sp)
  addi sp, sp, 2*REGBYTES
  .endm
  '''.format(reg1=reg1,reg2=reg2),
    '''
  .macro ecause04
  # stack push
  addi sp, sp, -2*REGBYTES
  SREG x{reg1},  1*REGBYTES(sp)
  SREG x{reg2},  2*REGBYTES(sp)
    
  #exception
  mv x{reg1}, sp
  li x{reg2}, 1
  mul x{reg1}, x{reg1}, x{reg2}
  lh x{reg2}, 1(x{reg1})
  mul x{reg1}, x{reg1}, x{reg2}

  # stack pop
  LREG x{reg1},  1*REGBYTES(sp)
  LREG x{reg2},  2*REGBYTES(sp)
  addi sp, sp, 2*REGBYTES
  .endm
  '''.format(reg1=reg1,reg2=reg2),
    '''
  .macro ecause04
  # stack push
  addi sp, sp, -2*REGBYTES
  SREG x{reg1},  1*REGBYTES(sp)
  SREG x{reg2},  2*REGBYTES(sp)
    
  #exception
  mv x{reg1}, sp
  li x{reg2}, 1
  mul x{reg1}, x{reg1}, x{reg2}
  lh x{reg2}, 3(x{reg1})
  mul x{reg1}, x{reg1}, x{reg2}

  # stack pop
  LREG x{reg1},  1*REGBYTES(sp)
  LREG x{reg2},  2*REGBYTES(sp)
  addi sp, sp, 2*REGBYTES
  .endm
  '''.format(reg1=reg1,reg2=reg2),
    '''
  .macro ecause04
  # stack push
  addi sp, sp, -2*REGBYTES
  SREG x{reg1},  1*REGBYTES(sp)
  SREG x{reg2},  2*REGBYTES(sp)
    
  #exception
  mv x{reg1}, sp
  li x{reg2}, 1
  mul x{reg1}, x{reg1}, x{reg2}
  lhu x{reg2}, 1(x{reg1})
  mul x{reg1}, x{reg1}, x{reg2}

  # stack pop
  LREG x{reg1},  1*REGBYTES(sp)
  LREG x{reg2},  2*REGBYTES(sp)
  addi sp, sp, 2*REGBYTES
  .endm
  '''.format(reg1=reg1,reg2=reg2),
    '''
  .macro ecause04
  # stack push
  addi sp, sp, -2*REGBYTES
  SREG x{reg1},  1*REGBYTES(sp)
  SREG x{reg2},  2*REGBYTES(sp)
    
  #exception
  mv x{reg1}, sp
  li x{reg2}, 1
  mul x{reg1}, x{reg1}, x{reg2}
  lhu x{reg2}, 3(x{reg1})
  mul x{reg1}, x{reg1}, x{reg2}

  # stack pop
  LREG x{reg1},  1*REGBYTES(sp)
  LREG x{reg2},  2*REGBYTES(sp)
  addi sp, sp, 2*REGBYTES
  .endm
  '''.format(reg1=reg1,reg2=reg2)
  ]

  reg1 = random.randint(0,29) + 1
  reg2 = random.randint(0,27)
  if reg1 == 11 or reg1 == 2:
    reg1=reg1+1
  if (reg1 == reg2):
    reg2=reg2+1
  if (reg2 == 11 or reg2 == 2):
    reg2=reg2+1
  no_use_regs.append(reg1)
  no_use_regs.append(reg2)
  ecause05_r = [
  '''
  .macro ecause05
  # stack push
  addi sp, sp, -1*REGBYTES
  SREG x{reg1},  1*REGBYTES(sp)
    
  # exception 
  li x{reg1}, 0
  LREG x{reg1}, (x{reg1})
    
  # stack pop
  LREG x{reg1},  1*REGBYTES(sp)
  addi sp, sp,  1*REGBYTES
  .endm
  '''.format(reg1=reg1,reg2=reg2),
    '''
  .macro ecause05
  # exception
  LREG x0, (x0)
  .endm
  '''.format(reg1=reg1,reg2=reg2),
    '''
  .macro ecause05
  # stack push
  addi sp, sp, -1*REGBYTES
  SREG x{reg1},  1*REGBYTES(sp)
    
  # exception 
  li x{reg1}, 0
  LREG x{reg1}, (x{reg1})
    
  # stack pop
  LREG x{reg1},  1*REGBYTES(sp)
  addi sp, sp,  1*REGBYTES
  .endm
  '''.format(reg1=reg1,reg2=reg2),
    '''
  .macro ecause05
  # stack push
  addi sp, sp, -1*REGBYTES
  SREG x{reg1},  1*REGBYTES(sp)
    
  # exception 
  li x{reg1}, 0
  LREGU x{reg1}, (x{reg1})
    
  # stack pop
  LREG x{reg1},  1*REGBYTES(sp)
  addi sp, sp,  1*REGBYTES
  .endm
  '''.format(reg1=reg1,reg2=reg2),
    '''
  .macro ecause05
  # exception
  LREGU x0, (x0)
  .endm
  '''.format(reg1=reg1,reg2=reg2),
    '''
  .macro ecause05
  # stack push
  addi sp, sp, -1*REGBYTES
  SREG x{reg1},  1*REGBYTES(sp)
    
  # exception 
  li x{reg1}, 0
  LREGU x{reg1}, (x{reg1})
    
  # stack pop
  LREG x{reg1},  1*REGBYTES(sp)
  addi sp, sp,  1*REGBYTES
  .endm
  '''.format(reg1=reg1,reg2=reg2),
    # ------------------------------------
    '''
  .macro ecause05
  # stack push
  addi sp, sp, -1*REGBYTES
  SREG x{reg1},  1*REGBYTES(sp)
    
  # exception 
  li x{reg1}, 0
  lw x{reg1}, (x{reg1})
    
  # stack pop
  LREG x{reg1},  1*REGBYTES(sp)
  addi sp, sp,  1*REGBYTES
  .endm
  '''.format(reg1=reg1,reg2=reg2),
    '''
  .macro ecause05
  # exception
  lw x0, (x0)
  .endm
  '''.format(reg1=reg1,reg2=reg2),
    '''
  .macro ecause05
  # stack push
  addi sp, sp, -1*REGBYTES
  SREG x{reg1},  1*REGBYTES(sp)
    
  # exception 
  li x{reg1}, 0
  lw x{reg1}, (x{reg1})
    
  # stack pop
  LREG x{reg1},  1*REGBYTES(sp)
  addi sp, sp,  1*REGBYTES
  .endm
  '''.format(reg1=reg1,reg2=reg2),
  # ------------------------------------
    '''
  .macro ecause05
  # stack push
  addi sp, sp, -1*REGBYTES
  SREG x{reg1},  1*REGBYTES(sp)
    
  # exception 
  li x{reg1}, 0
  lh x{reg1}, (x{reg1})
    
  # stack pop
  LREG x{reg1},  1*REGBYTES(sp)
  addi sp, sp,  1*REGBYTES
  .endm
  '''.format(reg1=reg1,reg2=reg2),
    '''
  .macro ecause05
  # exception
  lh x0, (x0)
  .endm
  '''.format(reg1=reg1,reg2=reg2),
    '''
  .macro ecause05
  # stack push
  addi sp, sp, -1*REGBYTES
  SREG x{reg1},  1*REGBYTES(sp)
    
  # exception 
  li x{reg1}, 0
  lw x{reg1}, (x{reg1})
    
  # stack pop
  LREG x{reg1},  1*REGBYTES(sp)
  addi sp, sp,  1*REGBYTES
  .endm
  '''.format(reg1=reg1,reg2=reg2),
    # ------------------------------------
    '''
  .macro ecause05
  # stack push
  addi sp, sp, -1*REGBYTES
  SREG x{reg1},  1*REGBYTES(sp)
    
  # exception 
  li x{reg1}, 0
  lhu x{reg1}, (x{reg1})
    
  # stack pop
  LREG x{reg1},  1*REGBYTES(sp)
  addi sp, sp,  1*REGBYTES
  .endm
  '''.format(reg1=reg1,reg2=reg2),
    '''
  .macro ecause05
  # exception
  lhu x0, (x0)
  .endm
  '''.format(reg1=reg1,reg2=reg2),
    '''
  .macro ecause05
  # stack push
  addi sp, sp, -1*REGBYTES
  SREG x{reg1},  1*REGBYTES(sp)
    
  # exception 
  li x{reg1}, 0
  lhu x{reg1}, (x{reg1})
    
  # stack pop
  LREG x{reg1},  1*REGBYTES(sp)
  addi sp, sp,  1*REGBYTES
  .endm
  '''.format(reg1=reg1,reg2=reg2),
    # ------------------------------------
    '''
  .macro ecause05
  # stack push
  addi sp, sp, -1*REGBYTES
  SREG x{reg1},  1*REGBYTES(sp)
    
  # exception 
  li x{reg1}, 0
  lb x{reg1}, (x{reg1})
    
  # stack pop
  LREG x{reg1},  1*REGBYTES(sp)
  addi sp, sp,  1*REGBYTES
  .endm
  '''.format(reg1=reg1,reg2=reg2),
    '''
  .macro ecause05
  # exception
  lb x0, (x0)
  .endm
  '''.format(reg1=reg1,reg2=reg2),
    '''
  .macro ecause05
  # stack push
  addi sp, sp, -1*REGBYTES
  SREG x{reg1},  1*REGBYTES(sp)
    
  # exception 
  li x{reg1}, 0
  lb x{reg1}, (x{reg1})
    
  # stack pop
  LREG x{reg1},  1*REGBYTES(sp)
  addi sp, sp,  1*REGBYTES
  .endm
  '''.format(reg1=reg1,reg2=reg2),
    # ------------------------------------
    '''
  .macro ecause05
  # stack push
  addi sp, sp, -1*REGBYTES
  SREG x{reg1},  1*REGBYTES(sp)
    
  # exception 
  li x{reg1}, 0
  lbu x{reg1}, (x{reg1})
    
  # stack pop
  LREG x{reg1},  1*REGBYTES(sp)
  addi sp, sp,  1*REGBYTES
  .endm
  '''.format(reg1=reg1,reg2=reg2),
    '''
  .macro ecause05
  # exception
  lbu x0, (x0)
  .endm
  '''.format(reg1=reg1,reg2=reg2),
    '''
  .macro ecause05
  # stack push
  addi sp, sp, -1*REGBYTES
  SREG x{reg1},  1*REGBYTES(sp)
    
  # exception 
  li x{reg1}, 0
  lbu x{reg1}, (x{reg1})
    
  # stack pop
  LREG x{reg1},  1*REGBYTES(sp)
  addi sp, sp,  1*REGBYTES
  .endm
  '''.format(reg1=reg1,reg2=reg2)
  ]

  reg1 = random.randint(0,29) + 1
  reg2 = random.randint(0,27)
  if reg1 == 11 or reg1 == 2:
    reg1=reg1+1
  if (reg1 == reg2):
    reg2=reg2+1
  if (reg2 == 11 or reg2 == 2):
    reg2=reg2+1
  no_use_regs.append(reg1)
  no_use_regs.append(reg2)
  ecause06_r = [
  '''
  .macro ecause06
  # stack push
  addi sp, sp, -1*REGBYTES
  SREG x{reg2},  1*REGBYTES(sp)
    
  #exception
  SREG x{reg2}, 1(sp)

  # stack pop
  LREG x{reg2}, 1*REGBYTES(sp)
  addi sp, sp, 1*REGBYTES
  .endm
  '''.format(reg1=reg1,reg2=reg2),
    '''
  .macro ecause06
  # stack push
  addi sp, sp, -1*REGBYTES
  SREG x{reg2},  1*REGBYTES(sp)
    
  #exception
  SREG x{reg2}, 2(sp)

  # stack pop
  LREG x{reg2}, 1*REGBYTES(sp)
  addi sp, sp, 1*REGBYTES
  .endm
  '''.format(reg1=reg1,reg2=reg2),
    '''
  .macro ecause06
  # stack push
  addi sp, sp, -1*REGBYTES
  SREG x{reg2},  1*REGBYTES(sp)
    
  #exception
  SREG x{reg2}, 3(sp)

  # stack pop
  LREG x{reg2}, 1*REGBYTES(sp)
  addi sp, sp, 1*REGBYTES
  .endm
  '''.format(reg1=reg1,reg2=reg2),
    '''
  .macro ecause06
  # stack push
  addi sp, sp, -1*REGBYTES
  SREG x{reg2},  1*REGBYTES(sp)
    
  #exception
  sw x{reg2}, 1(sp)

  # stack pop
  LREG x{reg2}, 1*REGBYTES(sp)
  addi sp, sp, 1*REGBYTES
  .endm
  '''.format(reg1=reg1,reg2=reg2),
    '''
  .macro ecause06
  # stack push
  addi sp, sp, -1*REGBYTES
  SREG x{reg2},  1*REGBYTES(sp)
    
  #exception
  sw x{reg2}, 2(sp)

  # stack pop
  LREG x{reg2}, 1*REGBYTES(sp)
  addi sp, sp, 1*REGBYTES
  .endm
  '''.format(reg1=reg1,reg2=reg2),
    '''
  .macro ecause06
  # stack push
  addi sp, sp, -1*REGBYTES
  SREG x{reg2},  1*REGBYTES(sp)
    
  #exception
  sw x{reg2}, 3(sp)

  # stack pop
  LREG x{reg2}, 1*REGBYTES(sp)
  addi sp, sp, 1*REGBYTES
  .endm
  '''.format(reg1=reg1,reg2=reg2),
    '''
  .macro ecause06
  # stack push
  addi sp, sp, -1*REGBYTES
  SREG x{reg2},  1*REGBYTES(sp)
    
  #exception
  sh x{reg2}, 1(sp)

  # stack pop
  LREG x{reg2}, 1*REGBYTES(sp)
  addi sp, sp, 1*REGBYTES
  .endm
  '''.format(reg1=reg1,reg2=reg2),
    '''
  .macro ecause06
  # stack push
  addi sp, sp, -1*REGBYTES
  SREG x{reg2},  1*REGBYTES(sp)
    
  #exception
  sh x{reg2}, 3(sp)

  # stack pop
  LREG x{reg2}, 1*REGBYTES(sp)
  addi sp, sp, 1*REGBYTES
  .endm
  '''.format(reg1=reg1,reg2=reg2),
    '''
  .macro ecause06
  # stack push
  addi sp, sp, -2*REGBYTES
  SREG x{reg1},  1*REGBYTES(sp)
  SREG x{reg2},  2*REGBYTES(sp)
    
  #exception
  mv x{reg1}, sp
  LREG x{reg2}, 1(x{reg1})

  # stack pop
  LREG x{reg1},  1*REGBYTES(sp)
  LREG x{reg2},  2*REGBYTES(sp)
  addi sp, sp, 2*REGBYTES
  .endm
  '''.format(reg1=reg1,reg2=reg2),
    '''
  .macro ecause06
  # stack push
  addi sp, sp, -2*REGBYTES
  SREG x{reg1},  1*REGBYTES(sp)
  SREG x{reg2},  2*REGBYTES(sp)
    
  #exception
  mv x{reg1}, sp
  SREG x{reg2}, 2(x{reg1})

  # stack pop
  LREG x{reg1},  1*REGBYTES(sp)
  LREG x{reg2},  2*REGBYTES(sp)
  addi sp, sp, 2*REGBYTES
  .endm
  '''.format(reg1=reg1,reg2=reg2),
    '''
  .macro ecause06
  # stack push
  addi sp, sp, -2*REGBYTES
  SREG x{reg1},  1*REGBYTES(sp)
  SREG x{reg2},  2*REGBYTES(sp)
    
  #exception
  mv x{reg1}, sp
  SREG x{reg2}, 3(x{reg1})

  # stack pop
  LREG x{reg1},  1*REGBYTES(sp)
  LREG x{reg2},  2*REGBYTES(sp)
  addi sp, sp, 2*REGBYTES
  .endm
  '''.format(reg1=reg1,reg2=reg2),
    '''
  .macro ecause06
  # stack push
  addi sp, sp, -2*REGBYTES
  SREG x{reg1},  1*REGBYTES(sp)
  SREG x{reg2},  2*REGBYTES(sp)
    
  #exception
  mv x{reg1}, sp
  sw x{reg2}, 1(x{reg1})

  # stack pop
  LREG x{reg1},  1*REGBYTES(sp)
  LREG x{reg2},  2*REGBYTES(sp)
  addi sp, sp, 2*REGBYTES
  .endm
  '''.format(reg1=reg1,reg2=reg2),
    '''
  .macro ecause06
  # stack push
  addi sp, sp, -2*REGBYTES
  SREG x{reg1},  1*REGBYTES(sp)
  SREG x{reg2},  2*REGBYTES(sp)
    
  #exception
  mv x{reg1}, sp
  sw x{reg2}, 2(x{reg1})

  # stack pop
  LREG x{reg1},  1*REGBYTES(sp)
  LREG x{reg2},  2*REGBYTES(sp)
  addi sp, sp, 2*REGBYTES
  .endm
  '''.format(reg1=reg1,reg2=reg2),
    '''
  .macro ecause06
  # stack push
  addi sp, sp, -2*REGBYTES
  SREG x{reg1},  1*REGBYTES(sp)
  SREG x{reg2},  2*REGBYTES(sp)
    
  #exception
  mv x{reg1}, sp
  sw x{reg2}, 3(x{reg1})

  # stack pop
  LREG x{reg1},  1*REGBYTES(sp)
  LREG x{reg2},  2*REGBYTES(sp)
  addi sp, sp, 2*REGBYTES
  .endm
  '''.format(reg1=reg1,reg2=reg2),
    '''
  .macro ecause06
  # stack push
  addi sp, sp, -2*REGBYTES
  SREG x{reg1},  1*REGBYTES(sp)
  SREG x{reg2},  2*REGBYTES(sp)
    
  #exception
  mv x{reg1}, sp
  sh x{reg2}, 1(x{reg1})

  # stack pop
  LREG x{reg1},  1*REGBYTES(sp)
  LREG x{reg2},  2*REGBYTES(sp)
  addi sp, sp, 2*REGBYTES
  .endm
  '''.format(reg1=reg1,reg2=reg2),
    '''
  .macro ecause06
  # stack push
  addi sp, sp, -2*REGBYTES
  SREG x{reg1},  1*REGBYTES(sp)
  SREG x{reg2},  2*REGBYTES(sp)
    
  #exception
  mv x{reg1}, sp
  sh x{reg2}, 3(x{reg1})

  # stack pop
  LREG x{reg1},  1*REGBYTES(sp)
  LREG x{reg2},  2*REGBYTES(sp)
  addi sp, sp, 2*REGBYTES
  .endm
  '''.format(reg1=reg1,reg2=reg2),

    '''
  .macro ecause06
  # stack push
  addi sp, sp, -2*REGBYTES
  SREG x{reg1},  1*REGBYTES(sp)
  SREG x{reg2},  2*REGBYTES(sp)
    
  #exception
  mv x{reg1}, sp
  li x{reg2}, 1
  mul x{reg1}, x{reg1}, x{reg2}
  SREG x{reg2}, 1(x{reg1})
  mul x{reg1}, x{reg1}, x{reg2}

  # stack pop
  LREG x{reg1},  1*REGBYTES(sp)
  LREG x{reg2},  2*REGBYTES(sp)
  addi sp, sp, 2*REGBYTES
  .endm
  '''.format(reg1=reg1,reg2=reg2),
    '''
  .macro ecause06
  # stack push
  addi sp, sp, -2*REGBYTES
  SREG x{reg1},  1*REGBYTES(sp)
  SREG x{reg2},  2*REGBYTES(sp)
    
  #exception
  mv x{reg1}, sp
  li x{reg2}, 1
  mul x{reg1}, x{reg1}, x{reg2}
  SREG x{reg2}, 2(x{reg1})
  mul x{reg1}, x{reg1}, x{reg2}

  # stack pop
  LREG x{reg1},  1*REGBYTES(sp)
  LREG x{reg2},  2*REGBYTES(sp)
  addi sp, sp, 2*REGBYTES
  .endm
  '''.format(reg1=reg1,reg2=reg2),
    '''
  .macro ecause06
  # stack push
  addi sp, sp, -2*REGBYTES
  SREG x{reg1},  1*REGBYTES(sp)
  SREG x{reg2},  2*REGBYTES(sp)
    
  #exception
  mv x{reg1}, sp
  li x{reg2}, 1
  mul x{reg1}, x{reg1}, x{reg2}
  SREG x{reg2}, 3(x{reg1})
  mul x{reg1}, x{reg1}, x{reg2}

  # stack pop
  LREG x{reg1},  1*REGBYTES(sp)
  LREG x{reg2},  2*REGBYTES(sp)
  addi sp, sp, 2*REGBYTES
  .endm
  '''.format(reg1=reg1,reg2=reg2),
    '''
  .macro ecause06
  # stack push
  addi sp, sp, -2*REGBYTES
  SREG x{reg1},  1*REGBYTES(sp)
  SREG x{reg2},  2*REGBYTES(sp)
    
  #exception
  mv x{reg1}, sp
  li x{reg2}, 1
  mul x{reg1}, x{reg1}, x{reg2}
  sw x{reg2}, 1(x{reg1})
  mul x{reg1}, x{reg1}, x{reg2}

  # stack pop
  LREG x{reg1},  1*REGBYTES(sp)
  LREG x{reg2},  2*REGBYTES(sp)
  addi sp, sp, 2*REGBYTES
  .endm
  '''.format(reg1=reg1,reg2=reg2),
    '''
  .macro ecause06
  # stack push
  addi sp, sp, -2*REGBYTES
  SREG x{reg1},  1*REGBYTES(sp)
  SREG x{reg2},  2*REGBYTES(sp)
    
  #exception
  mv x{reg1}, sp
  li x{reg2}, 1
  mul x{reg1}, x{reg1}, x{reg2}
  sw x{reg2}, 2(x{reg1})
  mul x{reg1}, x{reg1}, x{reg2}

  # stack pop
  LREG x{reg1},  1*REGBYTES(sp)
  LREG x{reg2},  2*REGBYTES(sp)
  addi sp, sp, 2*REGBYTES
  .endm
  '''.format(reg1=reg1,reg2=reg2),
    '''
  .macro ecause06
  # stack push
  addi sp, sp, -2*REGBYTES
  SREG x{reg1},  1*REGBYTES(sp)
  SREG x{reg2},  2*REGBYTES(sp)
    
  #exception
  mv x{reg1}, sp
  li x{reg2}, 1
  mul x{reg1}, x{reg1}, x{reg2}
  sw x{reg2}, 3(x{reg1})
  mul x{reg1}, x{reg1}, x{reg2}

  # stack pop
  LREG x{reg1},  1*REGBYTES(sp)
  LREG x{reg2},  2*REGBYTES(sp)
  addi sp, sp, 2*REGBYTES
  .endm
  '''.format(reg1=reg1,reg2=reg2),
    '''
  .macro ecause06
  # stack push
  addi sp, sp, -2*REGBYTES
  SREG x{reg1},  1*REGBYTES(sp)
  SREG x{reg2},  2*REGBYTES(sp)
    
  #exception
  mv x{reg1}, sp
  li x{reg2}, 1
  mul x{reg1}, x{reg1}, x{reg2}
  sh x{reg2}, 1(x{reg1})
  mul x{reg1}, x{reg1}, x{reg2}

  # stack pop
  LREG x{reg1},  1*REGBYTES(sp)
  LREG x{reg2},  2*REGBYTES(sp)
  addi sp, sp, 2*REGBYTES
  .endm
  '''.format(reg1=reg1,reg2=reg2),
    '''
  .macro ecause06
  # stack push
  addi sp, sp, -2*REGBYTES
  SREG x{reg1},  1*REGBYTES(sp)
  SREG x{reg2},  2*REGBYTES(sp)
    
  #exception
  mv x{reg1}, sp
  li x{reg2}, 1
  mul x{reg1}, x{reg1}, x{reg2}
  sh x{reg2}, 3(x{reg1})
  mul x{reg1}, x{reg1}, x{reg2}

  # stack pop
  LREG x{reg1},  1*REGBYTES(sp)
  LREG x{reg2},  2*REGBYTES(sp)
  addi sp, sp, 2*REGBYTES
  .endm
  '''.format(reg1=reg1,reg2=reg2)
  ]

  reg1 = random.randint(0,29) + 1
  reg2 = random.randint(0,27)
  if reg1 == 11 or reg1 == 2:
    reg1=reg1+1
  if (reg1 == reg2):
    reg2=reg2+1
  if (reg2 == 11 or reg2 == 2):
    reg2=reg2+1
  no_use_regs.append(reg1)
  no_use_regs.append(reg2)
  ecause07_r = [
  '''
  .macro ecause07
  # stack push
  addi sp, sp, -1*REGBYTES
  SREG x{reg1},  1*REGBYTES(sp)
    
  # exception 
  li x{reg1}, 0
  SREG x{reg1}, (x{reg1})
    
  # stack pop
  LREG x{reg1},  1*REGBYTES(sp)
  addi sp, sp,  1*REGBYTES
  .endm
  '''.format(reg1=reg1,reg2=reg2),
    '''
  .macro ecause07
  # exception
  SREG x0, (x0)
  .endm
  '''.format(reg1=reg1,reg2=reg2),
    '''
  .macro ecause07
  # stack push
  addi sp, sp, -1*REGBYTES
  SREG x{reg1},  1*REGBYTES(sp)
    
  # exception 
  li x{reg1}, 0
  SREG x{reg1}, (x{reg1})
    
  # stack pop
  LREG x{reg1},  1*REGBYTES(sp)
  addi sp, sp,  1*REGBYTES
  .endm
  '''.format(reg1=reg1,reg2=reg2),
    # ------------------------------------
    '''
  .macro ecause07
  # stack push
  addi sp, sp, -1*REGBYTES
  SREG x{reg1},  1*REGBYTES(sp)
    
  # exception 
  li x{reg1}, 0
  sw x{reg1}, (x{reg1})
    
  # stack pop
  LREG x{reg1},  1*REGBYTES(sp)
  addi sp, sp,  1*REGBYTES
  .endm
  '''.format(reg1=reg1,reg2=reg2),
    '''
  .macro ecause07
  # exception
  sw x0, (x0)
  .endm
  '''.format(reg1=reg1,reg2=reg2),
    '''
  .macro ecause07
  # stack push
  addi sp, sp, -1*REGBYTES
  SREG x{reg1},  1*REGBYTES(sp)
    
  # exception 
  li x{reg1}, 0
  sw x{reg1}, (x{reg1})
    
  # stack pop
  LREG x{reg1},  1*REGBYTES(sp)
  addi sp, sp,  1*REGBYTES
  .endm
  '''.format(reg1=reg1,reg2=reg2),
  # ------------------------------------
    '''
  .macro ecause07
  # stack push
  addi sp, sp, -1*REGBYTES
  SREG x{reg1},  1*REGBYTES(sp)
    
  # exception 
  li x{reg1}, 0
  sh x{reg1}, (x{reg1})
    
  # stack pop
  LREG x{reg1},  1*REGBYTES(sp)
  addi sp, sp,  1*REGBYTES
  .endm
  '''.format(reg1=reg1,reg2=reg2),
    '''
  .macro ecause07
  # exception
  sh x0, (x0)
  .endm
  '''.format(reg1=reg1,reg2=reg2),
    '''
  .macro ecause07
  # stack push
  addi sp, sp, -1*REGBYTES
  SREG x{reg1},  1*REGBYTES(sp)
    
  # exception 
  li x{reg1}, 0
  sh x{reg1}, (x{reg1})
    
  # stack pop
  LREG x{reg1},  1*REGBYTES(sp)
  addi sp, sp,  1*REGBYTES
  .endm
  '''.format(reg1=reg1,reg2=reg2),
    # ------------------------------------
    '''
  .macro ecause07
  # stack push
  addi sp, sp, -1*REGBYTES
  SREG x{reg1},  1*REGBYTES(sp)
    
  # exception 
  li x{reg1}, 0
  sb x{reg1}, (x{reg1})
    
  # stack pop
  LREG x{reg1},  1*REGBYTES(sp)
  addi sp, sp,  1*REGBYTES
  .endm
  '''.format(reg1=reg1,reg2=reg2),
    '''
  .macro ecause07
  # exception
  sb x0, (x0)
  .endm
  '''.format(reg1=reg1,reg2=reg2),
    '''
  .macro ecause07
  # stack push
  addi sp, sp, -1*REGBYTES
  SREG x{reg1},  1*REGBYTES(sp)
    
  # exception 
  li x{reg1}, 0
  sb x{reg1}, (x{reg1})
    
  # stack pop
  LREG x{reg1},  1*REGBYTES(sp)
  addi sp, sp,  1*REGBYTES
  .endm
  '''.format(reg1=reg1,reg2=reg2)
  ]

  ecause08_r = [
  '''
  # Env call from U-mode
  .macro ecause08
  .endm
  '''
  ]
  ecause09_r = [
  '''
  # Env call from S-mode
  .macro ecause09
  .endm
  '''
  ]
  ecause10_r = [
  '''
  # Reserved
  .macro ecause10
  .endm
  '''
  ]

  ecause11_r = [
  '''
  # Env call from M-mode
  .macro ecause11
  ecall
  .endm
  '''
  ]

  ecause12_r = [
  '''
  # Instruction page fault
  .macro ecause12
  .endm
  '''
  ]

  ecause13_r = [
  '''
  # Load page fault
  .macro ecause13
  .endm
  '''
  ]

  ecause14_r = [
  '''
  # Reserved
  .macro ecause14
  .endm
  '''
  ]
  ecause15_r = [
  '''
  # Store/AMO page fault
  .macro ecause15
  .endm
  '''
  ]

  return (ecause00_r,ecause01_r,ecause02_r,ecause03_r,ecause04_r,ecause05_r,ecause06_r,ecause07_r,ecause08_r,ecause09_r,ecause10_r,ecause11_r,ecause12_r,ecause13_r,ecause14_r,ecause15_r)


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

def gen_random_program(ofile, args, arch, seed, no_headers):
    """ Function to generate one random assembly program

        Args:
            ofile: Output file handler
            args: Configuration parser args obtained from (default) config.ini
    """

    # Instantiate AsmWriter
    writer = aapg.asm_writer.AsmWriter(ofile)

    # Header Section
    writer.comment(" Random Assembly Program Generated using aapg")
    writer.comment(" Generated at: {}".format(datetime.datetime.now(pytz.timezone('GMT')).strftime("%Y-%m-%d %H:%M GMT")))
    writer.comment(" Seed: {}".format(seed))
    writer.newline()
    writer.comment("include \"templates.S\"")
    writer.newline()
    writer.comment("aapg version: {}".format(version))
    writer.newline()
    if(no_headers):
      try:
        writer.comment(" Generated by user: {}".format(os.getlogin()))
      except:
        writer.comment(" Generated by user: Unknown")
      writer.comment(" Arguments:")
      config_sections = args.sections()
      for section in config_sections:
        options = args.options(section)
        writer.comment("  {}:".format(section))
        for option in options:
          writer.comment("    {option}: {value}".format(option=option,value = str(args.get(section,option)).replace('\n','\t')))

    writer.newline()
    writer.write('.text')
    writer.write('.align\t\t4')
    writer.write('.globl\t\tmain');
    writer.write('.type\t\tmain, @function');

    # Section instruction writer
    basic_generator = aapg.program_generator.BasicGenerator(args, arch, seed, no_use_regs) 
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
            writer.write_pseudo(*line[1], label = label, indent = 4)
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
        elif line[0] == 'instruction_nolabel':
            writer.write_inst(*line[1], label = "", indent = 4)
            logger.debug("Writing: " + " ".join(line[1]))

    if args.getboolean('general', 'default_program_exit'):
        writer.newline()
        writer.write('write_tohost:', indent = 0)
        writer.write_pseudo('li', 't5', '1', indent = 4)
        writer.write_pseudo('sw', 't5', 'tohost', 't4', indent = 4)
        writer.write('label: j label', indent = 4)
        writer.newline()

    # I-cache thrash
    if args.getint('i-cache', 'num_calls') > 0:
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


    # Create the required data sections
    writer.newline()
    access_sections = args.items('access-sections')

    for index, section in enumerate(access_sections):
        section_name = section[0]
        section_start, section_end = section[1].split(',')[:2]

        if (index + 1) == len(access_sections):
            # Last section
            section_size = int(section_end, 16) - int(section_start, 16)
        else:
            next_section_start = access_sections[index+1][1].split(',')[0]
            section_size = int(next_section_start, 16) - int(section_start, 16)

        writer.write('.data')
        writer.write('.align 1')
        writer.write('.globl ' + section_name)
        writer.write(section_name + ':', indent = 0)

        data_generator = aapg.program_generator.DataGenerator(section_size)
        for line in data_generator:
            writer.write_inst(*line)

        writer.newline()

    writer.write('.align 4; .global end_signature; end_signature:', indent=0)
    # Completed
    logger.info("Program generation completed")

def gen_config_files(args):
    """ generate the linker file based on the configuration """ 
    # traslates yaml to ini file
    
    perl_file = os.path.join(args.setup_dir,"common","illegal.pl")
    outfile = os.path.join(args.setup_dir,"common","illegal_insts.txt")
    seed_def = int.from_bytes(os.urandom(8), byteorder = 'big')
    if args.seed == None:
      args.seed = seed_def
    
    perl_seed = str(args.seed)
    temp_seed = args.seed
    random.seed(args.seed)
      

    (ecause00_r,ecause01_r,ecause02_r,ecause03_r,ecause04_r,ecause05_r,ecause06_r,ecause07_r,ecause08_r,ecause09_r,ecause10_r,ecause11_r,ecause12_r,ecause13_r,ecause14_r,ecause15_r) = init_global_wth_seed(temp_seed)
    perl_cmd = "perl {infile} {outfile} {seed}".format(infile=perl_file,outfile=outfile,seed=perl_seed)

    try:
      os.system(perl_cmd)
      ecause02_r = []
      ill_insts = open(outfile,'r')
      ecause02_append_str = """
.macro ecause02
replace_word
.endm
      """
      while(True):
        line = ill_insts.readline()
        if not line:
          break
        line = line.replace("\n","")
        ins = ecause02_append_str.replace('replace_word',line)
        ecause02_r.append(ins)
    except:
      logger.info('perl script not run')
    import yaml
    ppm_avail = True

    if args.output_dir=='work':
      if not os.path.exists('{output_dir}/asm'.format(output_dir=args.output_dir)):
          os.makedirs('{output_dir}/asm'.format(output_dir=args.output_dir))
    else:
      if not os.path.exists('{output_dir}'.format(output_dir=args.output_dir)):
          os.makedirs('{output_dir}'.format(output_dir=args.output_dir))

    if os.path.isfile(args.config_file):
      load_path = args.config_file
    else:
      load_path = os.path.join(args.setup_dir,args.config_file)
    logger.info(load_path)
    config_yaml = yaml.safe_load(open(load_path))
    config_name = os.path.basename(load_path.rstrip(os.sep))
    config_name = config_name.strip('yaml')
    
    #os.path.basename(output_file_path2.rstrip(os.sep))
    config_ini = config_name +'ini'
    config_ini = os.path.join(args.output_dir,config_ini)
    logger.info('Creating a config file as : '+ config_ini)

    ###########################################################################################

    logger.debug(config_ini)
    logger.info(config_ini)
    f = open(config_ini,"w")
    for key in config_yaml:
        f.write('['+key+']'+'\n')
        for innerkey in config_yaml[key]:
            f.write(str(innerkey)+' = '+str(config_yaml[key][innerkey])+'\n')
    f.close()


    # Read the config file
    config_file_path = os.path.abspath(config_ini)
    config_file_name = os.path.basename(config_file_path.rstrip(os.sep))
    logger.info(config_file_path)

    # Setup the output dir
    common_dir = os.path.join(os.path.abspath(args.setup_dir), 'common')
    if args.output_dir=='work':
      ld_file_path = os.path.join(args.output_dir,'asm')
    else:
      ld_file_path = args.output_dir
    if args.asm_name == 'out':
      link_ldfile = os.path.join(ld_file_path, args.asm_name + '_' + config_file_name.strip('ini')[:-1] + '_00000.ld')
    else:
      if args.num_programs==1:
        link_ldfile = os.path.join(ld_file_path, args.asm_name+'.ld')
      else:
        link_ldfile = os.path.join(ld_file_path, args.asm_name+'_00000.ld')
    crt_file = os.path.join(common_dir, 'crt.S')

    # Check if valid config file provided
    if not os.path.isfile(config_file_path):
        logger.error("Config file not found. Please supply existing config file")
        sys.exit(1)

    # Read the program config
    config_args = configparser.ConfigParser()
    config_args.read(config_file_path)

    # Configure linker template
    linker_template = aapg.env.linker.linker_script.strip()

    # Perform the linker script substitutions
    start_address = config_args.get('general', 'code_start_address')
    linker_template = re.sub(r"<!start_address!>", start_address, linker_template)

    data_section_string = ""

    start_address = config_args.items('access-sections')[0][1].split(',')[0]
    data_section_string += ". = {};\n  ".format(start_address)

    # Generate data sections
    data_section_names = map(lambda x: x[0], config_args.items('access-sections'))
    data_section_strings = list(map(lambda x: "*({}*)".format(x), data_section_names))
    data_section_string += '.data : {{ {0} }}'.format(" ".join(data_section_strings))

    linker_template = re.sub(r"<!data_section!>", data_section_string, linker_template)

    tohost_section_pattern = r"<!\[tohost\]([\s\S]*)!>"
    tohost_string = re.search(tohost_section_pattern, linker_template).group(1)
    if config_args.getboolean('general', 'default_program_exit'):
        repl_string = tohost_string
    else:
        repl_string = ""

    linker_template = re.sub(tohost_section_pattern, repl_string, linker_template)

    

    with open(link_ldfile, 'w') as f:
        f.write(linker_template)

    # Configure the crt.S
    crt_template = aapg.env.prelude.crt_asm.strip()
    section_name = config_args.items('access-sections')[0][0]
    crt_template = re.sub(r"<!data_section!>", section_name, crt_template)

    # Add the config.ini as rodata
    config_contents = ""
    with open(config_file_path, 'rb') as config_file:
        bytes_var = config_file.read(8)

        while bytes_var != b'':
            # Append the dwords to contents
            if len(bytes_var) == 8:
                config_contents += "\t.dword 0x{}\n".format(bytes_var.hex())
            else:
                for b in bytes_var:
                    config_contents += "\t.byte {}\n".format(hex(b))
            # Next chunk read
            bytes_var = config_file.read(8)

    crt_template = re.sub(r"<!rodata_config!>", config_contents, crt_template)

    with open(crt_file, 'w') as f:
        f.write(crt_template)

    # Generate Template files
    dirs = ['common', 'bin', 'log', 'objdump','asm']
    num_ecause00 = 0
    num_ecause01 = 0
    num_ecause02 = 0
    num_ecause03 = 0
    num_ecause04 = 0
    num_ecause05 = 0
    num_ecause06 = 0
    num_ecause07 = 0
    num_ecause08 = 0
    num_ecause09 = 0
    num_ecause10 = 0
    num_ecause11 = 0
    num_ecause12 = 0
    num_ecause13 = 0
    num_ecause14 = 0
    num_ecause15 = 0

    test_entry_macro = '''
.macro test_entry_macro
.endm'''

    user_functions = '''
# User defined functions to be called
    '''

    pre_program_macro = '''
.macro pre_program_macro
.endm'''

    post_program_macro = '''
.macro post_program_macro
.endm'''

    pre_branch_macro = '''
.macro pre_branch_macro
.endm'''
      
    post_branch_macro = '''
.macro post_branch_macro
.endm'''


    if os.path.isfile(args.config_file):
      conf_path = args.config_file
    else:
      conf_path = os.path.join(args.setup_dir,args.config_file)
    a_yaml_file = open(conf_path)
    parsed_yaml_file = yaml.load(a_yaml_file, Loader=yaml.FullLoader)
    if 'priv-mode' in parsed_yaml_file.keys():
      for key,value in parsed_yaml_file['priv-mode'].items():
        if key == 'mode' and value == 'u':
          #ppm_avail = False # Making sure that pre-program-macro is not overwritten
          test_entry_macro = '''
.macro test_entry_macro
// Enter user mode.
    la t0, 123f
    csrw mepc, t0
    li t0, MSTATUS_MPP
    csrc mstatus, t0
    li t5, (MSTATUS_MPP & -MSTATUS_MPP) * PRV_U
    csrs mstatus, t5
    mret
 .endm
        '''
        elif key == 'mode' and value == 's':
          #ppm_avail = False # Making sure that pre-program-macro is not overwritten
          test_entry_macro = '''
.macro test_entry_macro
# Enter supervisor mode.
    la t0, 123f
    csrw mepc , t0
    li t0, MSTATUS_MPP
    csrc mstatus, t0
    li t5, (MSTATUS_MPP & -MSTATUS_MPP) * PRV_S
    csrs mstatus, t5
    mret
 .endm
        '''

    if 'user-functions' in parsed_yaml_file.keys():
      for key,value in parsed_yaml_file['user-functions'].items():
        Dict = eval(value)
        user_functions = user_functions + '''
.globl {func_name}        
{func_name}:
{func_body}
  ret'''.format(func_name=key,func_body=list(Dict.values())[0])
    if 'program-macro' in parsed_yaml_file.keys():
      for key,value in parsed_yaml_file['program-macro'].items():
      	if key == 'pre_program_macro':
      		check = re.search("ecause", value)
      		if not check:
      			pre_program_macro = '''.macro pre_program_macro\n'''+ value +'''\n .endm'''
      		else:
      			check_num00 = re.search("00", value)
      			check_num01 = re.search("01", value)
      			check_num02 = re.search("02", value)
      			check_num03 = re.search("03", value)
      			check_num04 = re.search("04", value)
      			check_num05 = re.search("05", value)
      			check_num06 = re.search("06", value)
      			check_num07 = re.search("07", value)
      			check_num08 = re.search("08", value)
      			check_num09 = re.search("09", value)
      			check_num10 = re.search("10", value)
      			check_num11 = re.search("11", value)
      			check_num12 = re.search("12", value)
      			check_num13 = re.search("13", value)
      			check_num14 = re.search("14", value)
      			check_num15 = re.search("15", value)
      			if check_num00:
      				to_write = ecause00_r[random.randint(0,len(ecause00_r)-1)]
      				to_write = to_write.splitlines(True)
      				to_write = to_write[2:-1]
      				output = '''.macro pre_program_macro\n'''
      				for to_write_ctr in range(len(to_write)):
      					output = output+to_write[to_write_ctr]
      				output = output + '''\n .endm'''
      				pre_program_macro = output
      			elif check_num01:
      				to_write = ecause01_r[random.randint(0,len(ecause01_r)-1)]
      				to_write = to_write.splitlines(True)
      				to_write = to_write[2:-1]
      				output = '''.macro pre_program_macro\n'''
      				for to_write_ctr in range(len(to_write)):
      					output = output+to_write[to_write_ctr]
      				output = output + '''\n .endm'''
      				pre_program_macro = output
      			elif check_num02:
      				to_write = ecause02_r[random.randint(0,len(ecause02_r)-1)]
      				to_write = to_write.splitlines(True)
      				to_write = to_write[2:-1]
      				output = '''.macro pre_program_macro\n'''
      				for to_write_ctr in range(len(to_write)):
      					output = output+to_write[to_write_ctr]
      				output = output + '''\n .endm'''
      				pre_program_macro = output
      			elif check_num03:
      				to_write = ecause03_r[random.randint(0,len(ecause03_r)-1)]
      				to_write = to_write.splitlines(True)
      				to_write = to_write[2:-1]
      				output = '''.macro pre_program_macro\n'''
      				for to_write_ctr in range(len(to_write)):
      					output = output+to_write[to_write_ctr]
      				output = output + '''\n .endm'''
      				pre_program_macro = output
      			elif check_num04:
      				to_write = ecause04_r[random.randint(0,len(ecause04_r)-1)]
      				to_write = to_write.splitlines(True)
      				to_write = to_write[2:-1]
      				output = '''.macro pre_program_macro\n'''
      				for to_write_ctr in range(len(to_write)):
      					output = output+to_write[to_write_ctr]
      				output = output + '''\n .endm'''
      				pre_program_macro = output
      			elif check_num05:
      				to_write = ecause05_r[random.randint(0,len(ecause05_r)-1)]
      				to_write = to_write.splitlines(True)
      				to_write = to_write[2:-1]
      				output = '''.macro pre_program_macro\n'''
      				for to_write_ctr in range(len(to_write)):
      					output = output+to_write[to_write_ctr]
      				output = output + '''\n .endm'''
      				pre_program_macro = output
      			elif check_num06:
      				to_write = ecause06_r[random.randint(0,len(ecause06_r)-1)]
      				to_write = to_write.splitlines(True)
      				to_write = to_write[2:-1]
      				output = '''.macro pre_program_macro\n'''
      				for to_write_ctr in range(len(to_write)):
      					output = output+to_write[to_write_ctr]
      				output = output + '''\n .endm'''
      				pre_program_macro = output
      			elif check_num07:
      				to_write = ecause07_r[random.randint(0,len(ecause07_r)-1)]
      				to_write = to_write.splitlines(True)
      				to_write = to_write[2:-1]
      				output = '''.macro pre_program_macro\n'''
      				for to_write_ctr in range(len(to_write)):
      					output = output+to_write[to_write_ctr]
      				output = output + '''\n .endm'''
      				pre_program_macro = output
      			elif check_num08:
      				to_write = ecause08_r[random.randint(0,len(ecause08_r)-1)]
      				to_write = to_write.splitlines(True)
      				to_write = to_write[2:-1]
      				output = '''.macro pre_program_macro\n'''
      				for to_write_ctr in range(len(to_write)):
      					output = output+to_write[to_write_ctr]
      				output = output + '''\n .endm'''
      				pre_program_macro = output
      			elif check_num09:
      				to_write = ecause09_r[random.randint(0,len(ecause09_r)-1)]
      				to_write = to_write.splitlines(True)
      				to_write = to_write[2:-1]
      				output = '''.macro pre_program_macro\n'''
      				for to_write_ctr in range(len(to_write)):
      					output = output+to_write[to_write_ctr]
      				output = output + '''\n .endm'''
      				pre_program_macro = output
      			elif check_num10:
      				to_write = ecause10_r[random.randint(0,len(ecause10_r)-1)]
      				to_write = to_write.splitlines(True)
      				to_write = to_write[2:-1]
      				output = '''.macro pre_program_macro\n'''
      				for to_write_ctr in range(len(to_write)):
      					output = output+to_write[to_write_ctr]
      				output = output + '''\n .endm'''
      				pre_program_macro = output
      			elif check_num11:
      				to_write = ecause11_r[random.randint(0,len(ecause11_r)-1)]
      				to_write = to_write.splitlines(True)
      				to_write = to_write[2:-1]
      				output = '''.macro pre_program_macro\n'''
      				for to_write_ctr in range(len(to_write)):
      					output = output+to_write[to_write_ctr]
      				output = output + '''\n .endm'''
      				pre_program_macro = output
      			elif check_num12:
      				to_write = ecause12_r[random.randint(0,len(ecause12_r)-1)]
      				to_write = to_write.splitlines(True)
      				to_write = to_write[2:-1]
      				output = '''.macro pre_program_macro\n'''
      				for to_write_ctr in range(len(to_write)):
      					output = output+to_write[to_write_ctr]
      				output = output + '''\n .endm'''
      				pre_program_macro = output
      			elif check_num13:
      				to_write = ecause13_r[random.randint(0,len(ecause13_r)-1)]
      				to_write = to_write.splitlines(True)
      				to_write = to_write[2:-1]
      				output = '''.macro pre_program_macro\n'''
      				for to_write_ctr in range(len(to_write)):
      					output = output+to_write[to_write_ctr]
      				output = output + '''\n .endm'''
      				pre_program_macro = output
      			elif check_num14:
      				to_write = ecause14_r[random.randint(0,len(ecause14_r)-1)]
      				to_write = to_write.splitlines(True)
      				to_write = to_write[2:-1]
      				output = '''.macro pre_program_macro\n'''
      				for to_write_ctr in range(len(to_write)):
      					output = output+to_write[to_write_ctr]
      				output = output + '''\n .endm'''
      				pre_program_macro = output
      			elif check_num15:
      				to_write = ecause15_r[random.randint(0,len(ecause15_r)-1)]
      				to_write = to_write.splitlines(True)
      				to_write = to_write[2:-1]
      				output = '''.macro pre_program_macro\n'''
      				for to_write_ctr in range(len(to_write)):
      					output = output+to_write[to_write_ctr]
      				output = output + '''\n .endm'''
      				pre_program_macro = output
      	if key == 'post_program_macro':
      		check = re.search("ecause", value)
      		if not check:
      			post_program_macro = '''.macro post_program_macro\n'''+ value +'''\n .endm'''
      		else:
      			check_num00 = re.search("00", value)
      			check_num01 = re.search("01", value)
      			check_num02 = re.search("02", value)
      			check_num03 = re.search("03", value)
      			check_num04 = re.search("04", value)
      			check_num05 = re.search("05", value)
      			check_num06 = re.search("06", value)
      			check_num07 = re.search("07", value)
      			check_num08 = re.search("08", value)
      			check_num09 = re.search("09", value)
      			check_num10 = re.search("10", value)
      			check_num11 = re.search("11", value)
      			check_num12 = re.search("12", value)
      			check_num13 = re.search("13", value)
      			check_num14 = re.search("14", value)
      			check_num15 = re.search("15", value)
      			if check_num00:
      				to_write = ecause00_r[random.randint(0,len(ecause00_r)-1)]
      				to_write = to_write.splitlines(True)
      				to_write = to_write[2:-1]
      				output = '''.macro post_program_macro\n'''
      				for to_write_ctr in range(len(to_write)):
      					output = output+to_write[to_write_ctr]
      				output = output + '''\n .endm'''
      				post_program_macro = output
      			elif check_num01:
      				to_write = ecause01_r[random.randint(0,len(ecause01_r)-1)]
      				to_write = to_write.splitlines(True)
      				to_write = to_write[2:-1]
      				output = '''.macro post_program_macro\n'''
      				for to_write_ctr in range(len(to_write)):
      					output = output+to_write[to_write_ctr]
      				output = output + '''\n .endm'''
      				post_program_macro = output
      			elif check_num02:
      				to_write = ecause02_r[random.randint(0,len(ecause02_r)-1)]
      				to_write = to_write.splitlines(True)
      				to_write = to_write[2:-1]
      				output = '''.macro post_program_macro\n'''
      				for to_write_ctr in range(len(to_write)):
      					output = output+to_write[to_write_ctr]
      				output = output + '''\n .endm'''
      				post_program_macro = output
      			elif check_num03:
      				to_write = ecause03_r[random.randint(0,len(ecause03_r)-1)]
      				to_write = to_write.splitlines(True)
      				to_write = to_write[2:-1]
      				output = '''.macro post_program_macro\n'''
      				for to_write_ctr in range(len(to_write)):
      					output = output+to_write[to_write_ctr]
      				output = output + '''\n .endm'''
      				post_program_macro = output
      			elif check_num04:
      				to_write = ecause04_r[random.randint(0,len(ecause04_r)-1)]
      				to_write = to_write.splitlines(True)
      				to_write = to_write[2:-1]
      				output = '''.macro post_program_macro\n'''
      				for to_write_ctr in range(len(to_write)):
      					output = output+to_write[to_write_ctr]
      				output = output + '''\n .endm'''
      				post_program_macro = output
      			elif check_num05:
      				to_write = ecause05_r[random.randint(0,len(ecause05_r)-1)]
      				to_write = to_write.splitlines(True)
      				to_write = to_write[2:-1]
      				output = '''.macro post_program_macro\n'''
      				for to_write_ctr in range(len(to_write)):
      					output = output+to_write[to_write_ctr]
      				output = output + '''\n .endm'''
      				post_program_macro = output
      			elif check_num06:
      				to_write = ecause06_r[random.randint(0,len(ecause06_r)-1)]
      				to_write = to_write.splitlines(True)
      				to_write = to_write[2:-1]
      				output = '''.macro post_program_macro\n'''
      				for to_write_ctr in range(len(to_write)):
      					output = output+to_write[to_write_ctr]
      				output = output + '''\n .endm'''
      				post_program_macro = output
      			elif check_num07:
      				to_write = ecause07_r[random.randint(0,len(ecause07_r)-1)]
      				to_write = to_write.splitlines(True)
      				to_write = to_write[2:-1]
      				output = '''.macro post_program_macro\n'''
      				for to_write_ctr in range(len(to_write)):
      					output = output+to_write[to_write_ctr]
      				output = output + '''\n .endm'''
      				post_program_macro = output
      			elif check_num08:
      				to_write = ecause08_r[random.randint(0,len(ecause08_r)-1)]
      				to_write = to_write.splitlines(True)
      				to_write = to_write[2:-1]
      				output = '''.macro post_program_macro\n'''
      				for to_write_ctr in range(len(to_write)):
      					output = output+to_write[to_write_ctr]
      				output = output + '''\n .endm'''
      				post_program_macro = output
      			elif check_num09:
      				to_write = ecause09_r[random.randint(0,len(ecause09_r)-1)]
      				to_write = to_write.splitlines(True)
      				to_write = to_write[2:-1]
      				output = '''.macro post_program_macro\n'''
      				for to_write_ctr in range(len(to_write)):
      					output = output+to_write[to_write_ctr]
      				output = output + '''\n .endm'''
      				post_program_macro = output
      			elif check_num10:
      				to_write = ecause10_r[random.randint(0,len(ecause10_r)-1)]
      				to_write = to_write.splitlines(True)
      				to_write = to_write[2:-1]
      				output = '''.macro post_program_macro\n'''
      				for to_write_ctr in range(len(to_write)):
      					output = output+to_write[to_write_ctr]
      				output = output + '''\n .endm'''
      				post_program_macro = output
      			elif check_num11:
      				to_write = ecause11_r[random.randint(0,len(ecause11_r)-1)]
      				to_write = to_write.splitlines(True)
      				to_write = to_write[2:-1]
      				output = '''.macro post_program_macro\n'''
      				for to_write_ctr in range(len(to_write)):
      					output = output+to_write[to_write_ctr]
      				output = output + '''\n .endm'''
      				post_program_macro = output
      			elif check_num12:
      				to_write = ecause12_r[random.randint(0,len(ecause12_r)-1)]
      				to_write = to_write.splitlines(True)
      				to_write = to_write[2:-1]
      				output = '''.macro post_program_macro\n'''
      				for to_write_ctr in range(len(to_write)):
      					output = output+to_write[to_write_ctr]
      				output = output + '''\n .endm'''
      				post_program_macro = output
      			elif check_num13:
      				to_write = ecause13_r[random.randint(0,len(ecause13_r)-1)]
      				to_write = to_write.splitlines(True)
      				to_write = to_write[2:-1]
      				output = '''.macro post_program_macro\n'''
      				for to_write_ctr in range(len(to_write)):
      					output = output+to_write[to_write_ctr]
      				output = output + '''\n .endm'''
      				post_program_macro = output
      			elif check_num14:
      				to_write = ecause14_r[random.randint(0,len(ecause14_r)-1)]
      				to_write = to_write.splitlines(True)
      				to_write = to_write[2:-1]
      				output = '''.macro post_program_macro\n'''
      				for to_write_ctr in range(len(to_write)):
      					output = output+to_write[to_write_ctr]
      				output = output + '''\n .endm'''
      				post_program_macro = output
      			elif check_num15:
      				to_write = ecause15_r[random.randint(0,len(ecause15_r)-1)]
      				to_write = to_write.splitlines(True)
      				to_write = to_write[2:-1]
      				output = '''.macro post_program_macro\n'''
      				for to_write_ctr in range(len(to_write)):
      					output = output+to_write[to_write_ctr]
      				output = output + '''\n .endm'''
      				post_program_macro = output
      	if key == 'pre_branch_macro':
      		check = re.search("ecause", value)
      		if not check:
      			pre_branch_macro = '''.macro pre_branch_macro\n'''+ value +'''\n .endm'''
      		else:
      			check_num00 = re.search("00", value)
      			check_num01 = re.search("01", value)
      			check_num02 = re.search("02", value)
      			check_num03 = re.search("03", value)
      			check_num04 = re.search("04", value)
      			check_num05 = re.search("05", value)
      			check_num06 = re.search("06", value)
      			check_num07 = re.search("07", value)
      			check_num08 = re.search("08", value)
      			check_num09 = re.search("09", value)
      			check_num10 = re.search("10", value)
      			check_num11 = re.search("11", value)
      			check_num12 = re.search("12", value)
      			check_num13 = re.search("13", value)
      			check_num14 = re.search("14", value)
      			check_num15 = re.search("15", value)
      			if check_num00:
      				to_write = ecause00_r[random.randint(0,len(ecause00_r)-1)]
      				to_write = to_write.splitlines(True)
      				to_write = to_write[2:-1]
      				output = '''.macro pre_branch_macro\n'''
      				for to_write_ctr in range(len(to_write)):
      					output = output+to_write[to_write_ctr]
      				output = output + '''\n .endm'''
      				pre_branch_macro = output
      			elif check_num01:
      				to_write = ecause01_r[random.randint(0,len(ecause01_r)-1)]
      				to_write = to_write.splitlines(True)
      				to_write = to_write[2:-1]
      				output = '''.macro pre_branch_macro\n'''
      				for to_write_ctr in range(len(to_write)):
      					output = output+to_write[to_write_ctr]
      				output = output + '''\n .endm'''
      				pre_branch_macro = output
      			elif check_num02:
      				to_write = ecause02_r[random.randint(0,len(ecause02_r)-1)]
      				to_write = to_write.splitlines(True)
      				to_write = to_write[2:-1]
      				output = '''.macro pre_branch_macro\n'''
      				for to_write_ctr in range(len(to_write)):
      					output = output+to_write[to_write_ctr]
      				output = output + '''\n .endm'''
      				pre_branch_macro = output
      			elif check_num03:
      				to_write = ecause03_r[random.randint(0,len(ecause03_r)-1)]
      				to_write = to_write.splitlines(True)
      				to_write = to_write[2:-1]
      				output = '''.macro pre_branch_macro\n'''
      				for to_write_ctr in range(len(to_write)):
      					output = output+to_write[to_write_ctr]
      				output = output + '''\n .endm'''
      				pre_branch_macro = output
      			elif check_num04:
      				to_write = ecause04_r[random.randint(0,len(ecause04_r)-1)]
      				to_write = to_write.splitlines(True)
      				to_write = to_write[2:-1]
      				output = '''.macro pre_branch_macro\n'''
      				for to_write_ctr in range(len(to_write)):
      					output = output+to_write[to_write_ctr]
      				output = output + '''\n .endm'''
      				pre_branch_macro = output
      			elif check_num05:
      				to_write = ecause05_r[random.randint(0,len(ecause05_r)-1)]
      				to_write = to_write.splitlines(True)
      				to_write = to_write[2:-1]
      				output = '''.macro pre_branch_macro\n'''
      				for to_write_ctr in range(len(to_write)):
      					output = output+to_write[to_write_ctr]
      				output = output + '''\n .endm'''
      				pre_branch_macro = output
      			elif check_num06:
      				to_write = ecause06_r[random.randint(0,len(ecause06_r)-1)]
      				to_write = to_write.splitlines(True)
      				to_write = to_write[2:-1]
      				output = '''.macro pre_branch_macro\n'''
      				for to_write_ctr in range(len(to_write)):
      					output = output+to_write[to_write_ctr]
      				output = output + '''\n .endm'''
      				pre_branch_macro = output
      			elif check_num07:
      				to_write = ecause07_r[random.randint(0,len(ecause07_r)-1)]
      				to_write = to_write.splitlines(True)
      				to_write = to_write[2:-1]
      				output = '''.macro pre_branch_macro\n'''
      				for to_write_ctr in range(len(to_write)):
      					output = output+to_write[to_write_ctr]
      				output = output + '''\n .endm'''
      				pre_branch_macro = output
      			elif check_num08:
      				to_write = ecause08_r[random.randint(0,len(ecause08_r)-1)]
      				to_write = to_write.splitlines(True)
      				to_write = to_write[2:-1]
      				output = '''.macro pre_branch_macro\n'''
      				for to_write_ctr in range(len(to_write)):
      					output = output+to_write[to_write_ctr]
      				output = output + '''\n .endm'''
      				pre_branch_macro = output
      			elif check_num09:
      				to_write = ecause09_r[random.randint(0,len(ecause09_r)-1)]
      				to_write = to_write.splitlines(True)
      				to_write = to_write[2:-1]
      				output = '''.macro pre_branch_macro\n'''
      				for to_write_ctr in range(len(to_write)):
      					output = output+to_write[to_write_ctr]
      				output = output + '''\n .endm'''
      				pre_branch_macro = output
      			elif check_num10:
      				to_write = ecause10_r[random.randint(0,len(ecause10_r)-1)]
      				to_write = to_write.splitlines(True)
      				to_write = to_write[2:-1]
      				output = '''.macro pre_branch_macro\n'''
      				for to_write_ctr in range(len(to_write)):
      					output = output+to_write[to_write_ctr]
      				output = output + '''\n .endm'''
      				pre_branch_macro = output
      			elif check_num11:
      				to_write = ecause11_r[random.randint(0,len(ecause11_r)-1)]
      				to_write = to_write.splitlines(True)
      				to_write = to_write[2:-1]
      				output = '''.macro pre_branch_macro\n'''
      				for to_write_ctr in range(len(to_write)):
      					output = output+to_write[to_write_ctr]
      				output = output + '''\n .endm'''
      				pre_branch_macro = output
      			elif check_num12:
      				to_write = ecause12_r[random.randint(0,len(ecause12_r)-1)]
      				to_write = to_write.splitlines(True)
      				to_write = to_write[2:-1]
      				output = '''.macro pre_branch_macro\n'''
      				for to_write_ctr in range(len(to_write)):
      					output = output+to_write[to_write_ctr]
      				output = output + '''\n .endm'''
      				pre_branch_macro = output
      			elif check_num13:
      				to_write = ecause13_r[random.randint(0,len(ecause13_r)-1)]
      				to_write = to_write.splitlines(True)
      				to_write = to_write[2:-1]
      				output = '''.macro pre_branch_macro\n'''
      				for to_write_ctr in range(len(to_write)):
      					output = output+to_write[to_write_ctr]
      				output = output + '''\n .endm'''
      				pre_branch_macro = output
      			elif check_num14:
      				to_write = ecause14_r[random.randint(0,len(ecause14_r)-1)]
      				to_write = to_write.splitlines(True)
      				to_write = to_write[2:-1]
      				output = '''.macro pre_branch_macro\n'''
      				for to_write_ctr in range(len(to_write)):
      					output = output+to_write[to_write_ctr]
      				output = output + '''\n .endm'''
      				pre_branch_macro = output
      			elif check_num15:
      				to_write = ecause15_r[random.randint(0,len(ecause15_r)-1)]
      				to_write = to_write.splitlines(True)
      				to_write = to_write[2:-1]
      				output = '''.macro pre_branch_macro\n'''
      				for to_write_ctr in range(len(to_write)):
      					output = output+to_write[to_write_ctr]
      				output = output + '''\n .endm'''
      				pre_branch_macro = output
      	if key == 'post_branch_macro':
      		check = re.search("ecause", value)
      		if not check:
      			post_branch_macro = '''.macro post_branch_macro\n'''+ value +'''\n .endm'''
      		else:
      			check_num00 = re.search("00", value)
      			check_num01 = re.search("01", value)
      			check_num02 = re.search("02", value)
      			check_num03 = re.search("03", value)
      			check_num04 = re.search("04", value)
      			check_num05 = re.search("05", value)
      			check_num06 = re.search("06", value)
      			check_num07 = re.search("07", value)
      			check_num08 = re.search("08", value)
      			check_num09 = re.search("09", value)
      			check_num10 = re.search("10", value)
      			check_num11 = re.search("11", value)
      			check_num12 = re.search("12", value)
      			check_num13 = re.search("13", value)
      			check_num14 = re.search("14", value)
      			check_num15 = re.search("15", value)
      			if check_num00:
      				to_write = ecause00_r[random.randint(0,len(ecause00_r)-1)]
      				to_write = to_write.splitlines(True)
      				to_write = to_write[2:-1]
      				output = '''.macro post_branch_macro\n'''
      				for to_write_ctr in range(len(to_write)):
      					output = output+to_write[to_write_ctr]
      				output = output + '''\n .endm'''
      				post_branch_macro = output
      			elif check_num01:
      				to_write = ecause01_r[random.randint(0,len(ecause01_r)-1)]
      				to_write = to_write.splitlines(True)
      				to_write = to_write[2:-1]
      				output = '''.macro post_branch_macro\n'''
      				for to_write_ctr in range(len(to_write)):
      					output = output+to_write[to_write_ctr]
      				output = output + '''\n .endm'''
      				post_branch_macro = output
      			elif check_num02:
      				to_write = ecause02_r[random.randint(0,len(ecause02_r)-1)]
      				to_write = to_write.splitlines(True)
      				to_write = to_write[2:-1]
      				output = '''.macro post_branch_macro\n'''
      				for to_write_ctr in range(len(to_write)):
      					output = output+to_write[to_write_ctr]
      				output = output + '''\n .endm'''
      				post_branch_macro = output
      			elif check_num03:
      				to_write = ecause03_r[random.randint(0,len(ecause03_r)-1)]
      				to_write = to_write.splitlines(True)
      				to_write = to_write[2:-1]
      				output = '''.macro post_branch_macro\n'''
      				for to_write_ctr in range(len(to_write)):
      					output = output+to_write[to_write_ctr]
      				output = output + '''\n .endm'''
      				post_branch_macro = output
      			elif check_num04:
      				to_write = ecause04_r[random.randint(0,len(ecause04_r)-1)]
      				to_write = to_write.splitlines(True)
      				to_write = to_write[2:-1]
      				output = '''.macro post_branch_macro\n'''
      				for to_write_ctr in range(len(to_write)):
      					output = output+to_write[to_write_ctr]
      				output = output + '''\n .endm'''
      				post_branch_macro = output
      			elif check_num05:
      				to_write = ecause05_r[random.randint(0,len(ecause05_r)-1)]
      				to_write = to_write.splitlines(True)
      				to_write = to_write[2:-1]
      				output = '''.macro post_branch_macro\n'''
      				for to_write_ctr in range(len(to_write)):
      					output = output+to_write[to_write_ctr]
      				output = output + '''\n .endm'''
      				post_branch_macro = output
      			elif check_num06:
      				to_write = ecause06_r[random.randint(0,len(ecause06_r)-1)]
      				to_write = to_write.splitlines(True)
      				to_write = to_write[2:-1]
      				output = '''.macro post_branch_macro\n'''
      				for to_write_ctr in range(len(to_write)):
      					output = output+to_write[to_write_ctr]
      				output = output + '''\n .endm'''
      				post_branch_macro = output
      			elif check_num07:
      				to_write = ecause07_r[random.randint(0,len(ecause07_r)-1)]
      				to_write = to_write.splitlines(True)
      				to_write = to_write[2:-1]
      				output = '''.macro post_branch_macro\n'''
      				for to_write_ctr in range(len(to_write)):
      					output = output+to_write[to_write_ctr]
      				output = output + '''\n .endm'''
      				post_branch_macro = output
      			elif check_num08:
      				to_write = ecause08_r[random.randint(0,len(ecause08_r)-1)]
      				to_write = to_write.splitlines(True)
      				to_write = to_write[2:-1]
      				output = '''.macro post_branch_macro\n'''
      				for to_write_ctr in range(len(to_write)):
      					output = output+to_write[to_write_ctr]
      				output = output + '''\n .endm'''
      				post_branch_macro = output
      			elif check_num09:
      				to_write = ecause09_r[random.randint(0,len(ecause09_r)-1)]
      				to_write = to_write.splitlines(True)
      				to_write = to_write[2:-1]
      				output = '''.macro post_branch_macro\n'''
      				for to_write_ctr in range(len(to_write)):
      					output = output+to_write[to_write_ctr]
      				output = output + '''\n .endm'''
      				post_branch_macro = output
      			elif check_num10:
      				to_write = ecause10_r[random.randint(0,len(ecause10_r)-1)]
      				to_write = to_write.splitlines(True)
      				to_write = to_write[2:-1]
      				output = '''.macro post_branch_macro\n'''
      				for to_write_ctr in range(len(to_write)):
      					output = output+to_write[to_write_ctr]
      				output = output + '''\n .endm'''
      				post_branch_macro = output
      			elif check_num11:
      				to_write = ecause11_r[random.randint(0,len(ecause11_r)-1)]
      				to_write = to_write.splitlines(True)
      				to_write = to_write[2:-1]
      				output = '''.macro post_branch_macro\n'''
      				for to_write_ctr in range(len(to_write)):
      					output = output+to_write[to_write_ctr]
      				output = output + '''\n .endm'''
      				post_branch_macro = output
      			elif check_num12:
      				to_write = ecause12_r[random.randint(0,len(ecause12_r)-1)]
      				to_write = to_write.splitlines(True)
      				to_write = to_write[2:-1]
      				output = '''.macro post_branch_macro\n'''
      				for to_write_ctr in range(len(to_write)):
      					output = output+to_write[to_write_ctr]
      				output = output + '''\n .endm'''
      				post_branch_macro = output
      			elif check_num13:
      				to_write = ecause13_r[random.randint(0,len(ecause13_r)-1)]
      				to_write = to_write.splitlines(True)
      				to_write = to_write[2:-1]
      				output = '''.macro post_branch_macro\n'''
      				for to_write_ctr in range(len(to_write)):
      					output = output+to_write[to_write_ctr]
      				output = output + '''\n .endm'''
      				post_branch_macro = output
      			elif check_num14:
      				to_write = ecause14_r[random.randint(0,len(ecause14_r)-1)]
      				to_write = to_write.splitlines(True)
      				to_write = to_write[2:-1]
      				output = '''.macro post_branch_macro\n'''
      				for to_write_ctr in range(len(to_write)):
      					output = output+to_write[to_write_ctr]
      				output = output + '''\n .endm'''
      				post_branch_macro = output
      			elif check_num15:
      				to_write = ecause15_r[random.randint(0,len(ecause15_r)-1)]
      				to_write = to_write.splitlines(True)
      				to_write = to_write[2:-1]
      				output = '''.macro post_branch_macro\n'''
      				for to_write_ctr in range(len(to_write)):
      					output = output+to_write[to_write_ctr]
      				output = output + '''\n .endm'''
      				post_branch_macro = output
                

    for key,value in parsed_yaml_file['exception-generation'].items():
      if key == 'ecause00':
        num_ecause00 = value
      if key == 'ecause01':
        num_ecause01 = value
      if key == 'ecause02':
        num_ecause02 = value
      if key == 'ecause03':
        num_ecause03 = value
      if key == 'ecause04':
        num_ecause04 = value
      if key == 'ecause05':
        num_ecause05 = value
      if key == 'ecause06':
        num_ecause06 = value
      if key == 'ecause07':
        num_ecause07 = value
      if key == 'ecause08':
        num_ecause08 = value
      if key == 'ecause09':
        num_ecause09 = value
      if key == 'ecause10':
        num_ecause10 = value
      if key == 'ecause11':
        num_ecause11 = value
      if key == 'ecause12':
        num_ecause12 = value
      if key == 'ecause13':
        num_ecause13 = value
      if key == 'ecause14':
        num_ecause14 = value
      if key == 'ecause15':
        num_ecause15 = value

    for i in range(args.num_programs):
        if args.asm_name =='out':
          templates_file = '{test_name}_{config_name}_{num}_template.S'.format(test_name=args.asm_name,config_name=config_file_name.strip('ini')[:-1],num='{:05d}'.format(i))
        else:
          if args.num_programs==1:
            templates_file = '{test_name}_template.S'.format(test_name=args.asm_name)
          else:
            templates_file = '{test_name}_{num}_template.S'.format(test_name=args.asm_name,config_name=config_file_name.strip('ini')[:-1],num='{:05d}'.format(i))
        if args.output_dir=="work":
          out_dir = os.path.join(args.output_dir,dirs[4])
        else:
          out_dir = args.output_dir
        
        for key,value in parsed_yaml_file['switch-priv-modes'].items():
          if key=='switch_modes' and value ==True:
            write = aapg.env.templates.templates_asm[1]
            break
          else:
            write = aapg.env.templates.templates_asm[0]
        write = write + test_entry_macro + "\n"
        write = write + pre_program_macro + "\n"
        write = write + post_program_macro + "\n"
        write = write + pre_branch_macro + "\n"
        write = write + post_branch_macro + "\n"
        write = write + user_functions + "\n"
        for i in range(num_ecause00):
          x = ecause00_r[random.randint(0,len(ecause00_r)-1)]
          x = x.replace(ecause00,ecause00+'''_{:05d}'''.format(i))
          write = write + x

        for i in range(num_ecause01):
          x = ecause01_r[random.randint(0,len(ecause01_r)-1)]
          x = x.replace(ecause01,ecause01+'''_{:05d}'''.format(i))
          write = write + x

        for i in range(num_ecause02):
          x = ecause02_r[random.randint(0,len(ecause02_r)-1)]
          x = x.replace(ecause02,ecause02+'''_{:05d}'''.format(i))
          write = write + x

        for i in range(num_ecause03):
          x = ecause03_r[random.randint(0,len(ecause03_r)-1)]
          x = x.replace(ecause03,ecause03+'''_{:05d}'''.format(i))
          write = write + x

        for i in range(num_ecause04):
          x = ecause04_r[random.randint(0,len(ecause04_r)-1)]
          x = x.replace(ecause04,ecause04+'''_{:05d}'''.format(i))
          write = write + x

        for i in range(num_ecause05):
          x = ecause05_r[random.randint(0,len(ecause05_r)-1)]
          x = x.replace(ecause05,ecause05+'''_{:05d}'''.format(i))
          write = write + x

        for i in range(num_ecause06):
          x = ecause06_r[random.randint(0,len(ecause06_r)-1)]
          x = x.replace(ecause06,ecause06+'''_{:05d}'''.format(i))
          write = write + x

        for i in range(num_ecause07):
          x = ecause07_r[random.randint(0,len(ecause07_r)-1)]
          x = x.replace(ecause07,ecause07+'''_{:05d}'''.format(i))
          write = write + x

        for i in range(num_ecause08):
          x = ecause08_r[random.randint(0,len(ecause08_r)-1)]
          x = x.replace(ecause08,ecause08+'''_{:05d}'''.format(i))
          write = write + x

        for i in range(num_ecause09):
          x = ecause09_r[random.randint(0,len(ecause09_r)-1)]
          x = x.replace(ecause09,ecause09+'''_{:05d}'''.format(i))
          write = write + x

        for i in range(num_ecause10):
          x = ecause10_r[random.randint(0,len(ecause10_r)-1)]
          x = x.replace(ecause10,ecause10+'''_{:05d}'''.format(i))
          write = write + x

        for i in range(num_ecause11):
          x = ecause11_r[random.randint(0,len(ecause11_r)-1)]
          x = x.replace(ecause11,ecause11+'''_{:05d}'''.format(i))
          write = write + x

        for i in range(num_ecause12):
          x = ecause12_r[random.randint(0,len(ecause12_r)-1)]
          x = x.replace(ecause12,ecause12+'''_{:05d}'''.format(i))
          write = write + x

        for i in range(num_ecause13):
          x = ecause13_r[random.randint(0,len(ecause13_r)-1)]
          x = x.replace(ecause13,ecause13+'''_{:05d}'''.format(i))
          write = write + x

        for i in range(num_ecause14):
          x = ecause14_r[random.randint(0,len(ecause14_r)-1)]
          x = x.replace(ecause14,ecause14+'''_{:05d}'''.format(i))
          write = write + x

        with open(os.path.join(out_dir, templates_file), 'w') as f:
            f.write(write.strip('\n'))

    #first_template_name = '{output_dir}/asm/{test_name}_{config_name}_00000_template.S'.format(output_dir=args.output_dir,test_name=args.asm_name,config_name=config_file_name.strip('ini')[:-1])
    if args.num_programs > 1:
        for i in range(1,args.num_programs):
            os.system('cp {link_ldfile} {new_file_name}'.format(link_ldfile=link_ldfile,new_file_name=link_ldfile[:-8]+'{:05d}'.format(i)+'.ld'))
            #os.system('cp {first_template_name} {new_template_name}'.format(first_template_name=first_template_name,new_template_name=first_template_name[:-16]+'{:05d}'.format(i)+'_template.S'))

    return args.seed


def run(args, index):
    """ Entry point for generating new random assembly program
    
        Invoked from main.py

        Args:
            args: (namespace) Command line arguments parsed

        Returns:
            None
    """
    # config_name = args.config_file
    # config_name = config_name.strip('.yaml')

    if os.path.isfile(args.config_file):
      load_path = args.config_file
    else:
      load_path = os.path.join(args.setup_dir,args.config_file)

    config_name = os.path.basename(load_path.rstrip(os.sep))
    config_name = config_name.strip('yaml')

    config_ini = config_name +'ini'
    #test = os.path.join(args.setup_dir,config_ini)
    config_file_path = os.path.join(args.output_dir,config_ini)

    config_file_name = os.path.basename(config_file_path.rstrip(os.sep))

    asm_prefix = config_file_name.strip('ini')[:-1]

    if args.output_dir=='work':
      output_dir = os.path.join(os.path.abspath(args.output_dir), 'asm')
    else:
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
    if output_asm_name == 'out':
      output_file_path = os.path.join(output_dir, output_asm_name + '_' + asm_prefix + '_{:05d}'.format(index) + '.S')
      output_file_path2 = os.path.join(output_dir, output_asm_name + '_' + asm_prefix + '_{:05d}'.format(index) + '.S')
    else:
      if args.num_programs == 1:
        output_file_path = os.path.join(output_dir, output_asm_name + '.S')
        output_file_path2 = os.path.join(output_dir, output_asm_name + '_' + asm_prefix + '_{:05d}'.format(index) + '.S')
      else:
        output_file_path = os.path.join(output_dir, output_asm_name + '_{:05d}'.format(index) + '.S')
        output_file_path2 = os.path.join(output_dir, output_asm_name + '_' + asm_prefix + '_{:05d}'.format(index) + '.S')

    logger.info("Output file path: {0}".format(output_file_path))

    if os.path.isfile(output_file_path):
        logger.warn('Output file exists. Overwriting')

    with open(output_file_path, 'w') as output_file:
        seed_def = int.from_bytes(os.urandom(8), byteorder = 'big')
        seed = seed_def if args.seed is None else int(args.seed)
        gen_random_program(output_file, config_args, args.arch, seed, args.no_headers)

    line_add = os.path.basename(output_file_path.rstrip(os.sep))
    line_add = line_add[:-2]+'_template.S'


    with open(output_file_path,'r') as output_file:
      lines = output_file.readlines()

    
    lines[4] = '#include "{template}"\n'.format(template=line_add)

    with open(output_file_path, "w") as outfile:
      outfile.write("".join(lines))

