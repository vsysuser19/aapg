'''
    Module to generate the arguments for the instructions
'''
import aapg.isa_funcs
import aapg.mappings
import random
import os

# Module Initialization
random.seed(os.urandom(256))
registers = aapg.mappings.registers_int
register_mapping = aapg.mappings.register_mapping_int

def gen_args(instruction, regfile):
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

    # Check if instruction is floating point
    if aapg.isa_funcs.is_floating_point(instr_name):
        gen_floating_point_args(instruction, regfile)

    # Iterate over the args
    final_inst = [instr_name,]

    # Check for rd
    if 'rd' in instr_args:
        register = random.choice(registers)
        regfile[register] += 1
        final_inst.append(register_mapping[register])

    if 'rs1' in instr_args:
        register = random.choice(registers)
        regfile[register] += 1
        final_inst.append(register_mapping[register])

    if 'rs2' in instr_args:
        register = random.choice(registers)
        regfile[register] += 1
        final_inst.append(register_mapping[register])

    if 'imm12' in instr_args or 'imm12hi' in instr_args or 'imm12lo' in instr_args:
        imm12_val = random.randint(-8192, 8191)
        final_inst.append(str(imm12_val))

    if 'imm20' in instr_args:
        imm20_val = random.randint(-(2<<20), 2<<20 - 1)
        final_inst.append(str(imm20_val))

    return tuple(final_inst)
