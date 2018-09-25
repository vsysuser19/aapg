templates_asm = '''
.globl _test
_test:
    ret

.macro pre_branch_macro
.endm

.macro post_branch_macro
.endm
'''
