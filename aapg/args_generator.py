'''
    Module to generate the arguments for the instructions
'''
import aapg.isa_funcs
import aapg.mappings
import random
import os
import logging
import sys

logger = logging.getLogger(__name__)

def set_seed_args_gen(seed):
    """ Set the global seed """
    random.seed(seed)

def gen_branch_args(instruction, regfile, arch, *args, **kwargs):
    """ Generate the args for branch instructions """
    instr_name = instruction[0]

    # Forward or backward jump
    backward = random.random() < float(kwargs['bwd_prob'])

    # Taken or not taken
    taken = random.random() < 0.5

    # Number of steps to jump
    try:
        num_steps = random.randint(5, kwargs['insts_since'] - 5)
    except ValueError as e:
        logger.error("Number of instructions required for branch threshold to low")
        logger.error("Increase count of non-branch instructions")
        sys.exit(1)

    # if forward and number of insts not sufficient, switch to bwd
    if not backward and num_steps > kwargs['insts_left'] - 5:
        backward = True

    # Generate the args
    offset_string = '{0},{1}'.format('b' if backward else 'f', num_steps)

    if instr_name == 'beq':
        pre_insts = []
        if backward:
            if taken:
                pre_insts.append(['li', 'x30', '11'])
                pre_insts.append(['addi', 'x31', 'x31', '1'])
            else:
                pre_insts.append(['li', 'x30', '0'])
        else:
            if taken:
                pre_insts.append(['li', 'x30', '10'])
            else:
                pre_insts.append(['li', 'x30', '0'])
        pre_insts.append(['pre_branch_macro'])
        pre_insts.append(['beq', 'x31', 'x30', offset_string]) 
        pre_insts.append(['post_branch_macro'])
        pre_insts.append(['li', 'x31', '10'])

        pre_insts.append(offset_string)
        return pre_insts
    elif instr_name == 'bne':
        pre_insts = []
        if backward:
            if taken:
                pre_insts.append(['li', 'x30', '12'])
                pre_insts.append(['addi', 'x31', 'x31', '1'])
            else:
                pre_insts.append(['li', 'x30', '10'])
        else:
            if taken:
                pre_insts.append(['li', 'x30', '11'])
                pre_insts.append(['li', 'x31', '10']) 
            else:
                pre_insts.append(['li', 'x30', '10'])
                pre_insts.append(['li', 'x31', '10'])
        pre_insts.append(['pre_branch_macro'])
        pre_insts.append(['bne', 'x31', 'x30', offset_string]) 
        pre_insts.append(['post_branch_macro'])
        pre_insts.append(['li', 'x31', '10'])

        pre_insts.append(offset_string)
        return pre_insts
    elif instr_name == 'blt' or instr_name == 'bltu':
        pre_insts = []
        if backward:
            if taken:
                pre_insts.append(['li', 'x30', '12'])
                pre_insts.append(['addi', 'x31', 'x31', '1'])
            else:
                pre_insts.append(['li', 'x30', '9'])
        else:
            if taken:
                pre_insts.append(['li', 'x30', '12'])
                pre_insts.append(['li', 'x31', '10']) 
            else:
                pre_insts.append(['li', 'x30', '9'])
                pre_insts.append(['li', 'x31', '10'])
        pre_insts.append(['pre_branch_macro'])
        pre_insts.append(['blt', 'x31', 'x30', offset_string]) 
        pre_insts.append(['post_branch_macro'])
        pre_insts.append(['li', 'x31', '10'])

        pre_insts.append(offset_string)
        return pre_insts
    elif instr_name == 'bge' or instr_name == 'bgeu':
        pre_insts = []
        if backward:
            if taken:
                pre_insts.append(['li', 'x30', '12'])
                pre_insts.append(['addi', 'x31', 'x31', '1'])
            else:
                pre_insts.append(['li', 'x30', '9'])
        else:
            if taken:
                pre_insts.append(['li', 'x30', '11'])
                pre_insts.append(['li', 'x31', '10']) 
            else:
                pre_insts.append(['li', 'x30', '9'])
                pre_insts.append(['li', 'x31', '10'])
        pre_insts.append(['pre_branch_macro'])
        pre_insts.append(['bge', 'x30', 'x31', offset_string]) 
        pre_insts.append(['post_branch_macro'])
        pre_insts.append(['li', 'x31', '10'])
        pre_insts.append(offset_string)
        return pre_insts
    elif instr_name == 'jal':
        pre_insts = []
        if backward:
            if taken:
                pre_insts.append(['li', 'x30', '12'])
                pre_insts.append(['addi', 'x31', 'x31', '1'])
                pre_insts.append(['beq', 'x31', 'x30', '1f'])
                pre_insts.append(['jal', 'x10', offset_string])
                pre_insts.append(['1: li x31, 10'])
            else:
                pre_insts.append(['li', 'x30', '10'])
                pre_insts.append(['beq', 'x31', 'x30', '1f'])
                pre_insts.append(['jal', 'x10', offset_string])
                pre_insts.append(['1: li x31, 10'])
        else:
            pre_insts.append(['jal', 'x10', offset_string])
        pre_insts.append(offset_string)
        return pre_insts
    elif instr_name == 'jalr':
        pre_insts = []
        if backward:
            if taken:
                pre_insts.append(['li', 'x30', '12'])
                pre_insts.append(['addi', 'x31', 'x31', '1'])
                pre_insts.append(['beq', 'x31', 'x30', '1f'])
                pre_insts.append(['la', 'x30', offset_string])
                pre_insts.append(['jalr', 'x10', 'x30', '0'])
                pre_insts.append(['1: li x31, 10'])
            else:
                pre_insts.append(['li', 'x30', '10'])
                pre_insts.append(['beq', 'x31', 'x30', '1f'])
                pre_insts.append(['la', 'x30', offset_string])
                pre_insts.append(['jalr', 'x10', 'x30', '0'])
                pre_insts.append(['1: li x31, 10'])
        else:
            pre_insts.append(['la', 'x30', offset_string])
            pre_insts.append(['jalr', 'x10', 'x30', '0'])
        pre_insts.append(offset_string)
        return pre_insts

def gen_memory_inst_offset(instr_name):
    """ Generate load/store offset for the instruction """
    if instr_name in ['ld', 'sd', 'fld', 'fsd']:
        return random.choice(range(-2048, 2047, 8))
    if instr_name in ['lw', 'lwu', 'sw', 'flw', 'fsw']:
        return random.choice(range(-2048, 2047, 4))
    if instr_name in ['lh', 'lhu', 'sh']:
        return random.choice(range(-2048, 2047, 2))
    if instr_name in ['lb', 'lbu', 'sb']:
        return random.choice(range(-2048, 2047))

def gen_args(instruction, regfile, arch, *args, **kwargs):
    '''
        Function to generate the args for a given instruction

        Args:
            instruction: tuple of (inst_name, *args)
            regfile: value of the registers

        Returns:
            instruction_with_args: (inst_name, arg_strings)
    '''
    instr_name = instruction[0]
    instr_args = instruction[1:]

    # Creating the registers
    registers_comp = [x for x in regfile if x[1] in range(8,16) and x[0] == 'x']
    registers_comp_float = [x for x in regfile if x[1] in range(8,16) and x[0] == 'f']
    registers_int = [x for x in regfile if x[0] == 'x'] 
    registers_float = [x for x in regfile if x[0] == 'f']
    register_mapping = aapg.mappings.register_mapping_int
    register_mapping_float = aapg.mappings.register_mapping_float

    # Iterate over the args
    final_inst = [instr_name,]

    for arg in instr_args:

        if arg == 'rd':
            register = random.choice(registers_int)
            regfile[register] += 1
            final_inst.append(register_mapping[register])
            continue

        if arg == 'rs1':
            register = random.choice(registers_int)
            regfile[register] += 1
            final_inst.append(register_mapping[register])
            continue

        if arg == 'rs2':
            register = random.choice(registers_int)
            regfile[register] += 1
            final_inst.append(register_mapping[register])
            continue

        if arg in ['imm12', 'uimm12']:

            # Check if memory_inst
            if instr_name in aapg.isa_funcs.memory_insts:
                imm12_val = gen_memory_inst_offset(instr_name)

            else:
                if arg == 'uimm12':
                    imm12_val = random.randint(0,4095)
                else:
                    imm12_val = random.randint(-2048, 2047)

            final_inst.append(str(imm12_val))
            continue

        if arg == 'imm5':
            final_inst.append(str(random.randint(-16, 15)))
            continue

        if arg == 'uimm5':
            final_inst.append(str(random.randint(0,31)))
            continue

        if arg == 'uimm6':
            final_inst.append(str(random.randint(0,63)))
            continue

        if arg == 'imm6':
            final_inst.append(str(random.randint(- 1<<5, 1<<5 - 1)))

        if arg == 'imm20':
            final_inst.append(str(random.randint(0, 1<<20)))
            continue

        if arg == 'shamt':
            if arch == 'rv32':
                final_inst.append(str(random.randint(0, 31)))
            elif arch == 'rv64':
                final_inst.append(str(random.randint(0, 63)))
            continue

        if arg == 'shamtw':
            final_inst.append(str(random.randint(0, 31)))
            continue

        # Floating point instructions
        if arg == 'rdf':
            register = random.choice(registers_float)
            regfile[register] += 1
            final_inst.append(register_mapping_float[register])
            continue

        if arg == 'rs1f':
            register = random.choice(registers_float)
            regfile[register] += 1
            final_inst.append(register_mapping_float[register])
            continue

        if arg == 'rs2f':
            register = random.choice(registers_float)
            regfile[register] += 1
            final_inst.append(register_mapping_float[register])
            continue

        if arg == 'rs3f':
            register = random.choice(registers_float)
            regfile[register] += 1
            final_inst.append(register_mapping_float[register])
            continue

        # Compressed
        if arg == 'rdprime':
            register = random.choice(registers_comp)
            regfile[register] += 1
            final_inst.append(register_mapping[register])
            continue

        if arg == 'rsprime1':
            register = random.choice(registers_comp)
            regfile[register] += 1
            final_inst.append(register_mapping[register])
            continue

        if arg == 'rsprime2':
            register = random.choice(registers_comp)
            regfile[register] += 1
            final_inst.append(register_mapping[register])
            continue

        if arg == 'nzuimm8':
            final_inst.append(str(4*random.randint(0, 1<<8 - 1)))
            continue

        if arg == 's8uimm6':
            final_inst.append(str(8*random.randint(0, 1<<6 - 1)))
            continue

        if arg == 's4uimm6':
            final_inst.append(str(4*random.randint(0, 1<<6 - 1)))
            continue

        if arg == 'imm8':
            final_inst.append(str(random.randint(- 1 << 7, 1 << 7 - 1)))
            continue

        if arg == 'nzimm6':
            final_inst.append(str(random.randint(- 1<<5, 1<<5 - 1)))
            continue

        if arg == 'nzuimm6':
            final_inst.append(str(random.randint(1, 1<<6 - 1)))
            continue

        if arg == 'nzuimm5':
            final_inst.append(str(random.randint(1, 1 << 5 - 1)))
            continue

        if arg == 's16imm6':
            final_inst.append((str(16*random.randint(-1 <<5, 1<<5 - 1))))
            continue

        if arg == 'sp':
            final_inst.append('sp')
            continue

        if arg == 's8uimm5':
            final_inst.append(str(8*random.randint(0, 1<<5 -1)))
            continue 

        if arg == 's4uimm5':
            final_inst.append(str(4*random.randint(0, 1<<5 -1)))
            continue

        if arg == 'rdprimef':
            register = random.choice(registers_comp_float)
            regfile[register] += 1
            final_inst.append(register_mapping_float[register])
            continue

        if arg == 'rsprime1f':
            register = random.choice(registers_comp_float)
            regfile[register] += 1
            final_inst.append(register_mapping_float[register])
            continue

        if arg == 'rsprime2f':
            register = random.choice(registers_comp_float)
            regfile[register] += 1
            final_inst.append(register_mapping_float[register])
            continue

        if arg == 'rd_rs1_prime':
            register = random.choice(registers_comp)
            regfile[register] += 1
            reg_map = register_mapping[register]
            final_inst.append(reg_map)
            final_inst.append(reg_map)
            continue

        if arg == 'rd_rs1':
            register = random.choice(registers_comp)
            regfile[register] += 1
            reg_map = register_mapping[register]
            final_inst.append(reg_map)
            final_inst.append(reg_map)
            continue

        if arg == 'imm11':
            final_inst.append(str(random.randint(- 1<<10, 1<<10 - 1)))
            continue

        if arg == 'x1':
            final_inst.append(register_mapping[('x', 1)])
            continue
        
        if arg == 'x0':
            final_inst.append(register_mapping[('x', 0)])
            continue

        if arg == 'const0':
            final_inst.append('0')
            continue

    if final_inst[0] in aapg.isa_funcs.comp_insts:
        final_inst[0] = aapg.isa_funcs.comp_insts_subs[final_inst[0]]
        
    return tuple(final_inst)

def gen_atomic_args(instruction, regfile, arch, *args, **kwargs):
    """ Generate args for atomic insts"""

    instr_name = instruction[0]
    instr_args = instruction[1:]

    # Creating the registers
    registers_int = [x for x in regfile if x[0] == 'x'] 
    register_mapping = aapg.mappings.register_mapping_int
    
    final_inst = [instr_name,]
    # Updating the args
    for arg in instr_args:

        if arg == 'rd':
            register = random.choice(registers_int)
            regfile[register] += 1
            final_inst.append(register_mapping[register])

        if arg == 'rs1':
            register = random.choice(registers_int)
            regfile[register] += 1
            final_inst.append(register_mapping[register])

        if arg == 'rs2':
            final_inst.append('sp')

    # Iterate over the args

    return final_inst
