templates_asm = '''
#if __riscv_xlen == 64
  #define LREG ld
  #define SREG sd
  #define REGBYTES 8
  #define FMV fmv.d.x
#else
  # define LREG lw
  # define SREG sw
  # define REGBYTES 4
  # define FMV fmv.w.x
#endif

# User defined functions to be called
.globl _test
_test:
    ret

# Instructions to be inserted before and after the program
.macro pre_program_macro
.endm

.macro post_program_macro
.endm

# Instructions to be inserted before and after branch
.macro pre_branch_macro
.endm

.macro post_branch_macro
.endm

############################
### Exception generation ###
############################

# Instruction address misaligned
.macro ecause00
.endm

# Instruction access fault
.macro ecause01
li x15, -10
jr x15
.endm

# Illegal Instruction
.macro ecause02
.word 0x01239239812981
.endm

# Breakpoint
.macro ecause03
ebreak
.endm

# Load address misaligned
.macro ecause04
LREG x0, (REGBYTES-2)(sp)
.endm

# Load access fault
.macro ecause05
.endm

# Store/AMO address misaligned
.macro ecause06
SREG x0, (REGBYTES-2)(sp)
.endm

# Store/AMO access fault
.macro ecause07
.endm

# Env call from U-mode
.macro ecause08
.endm

# Env call from S-mode
.macro ecause09
.endm

# Reserved
.macro ecause10
.endm

# Env call from M-mode
.macro ecause11
ecall
.endm

# Instruction page fault
.macro ecause12
.endm

# Load page fault
.macro ecause13
.endm

# Reserved
.macro ecause14
.endm

# Store/AMO page fault
.macro ecause15
.endm
'''
