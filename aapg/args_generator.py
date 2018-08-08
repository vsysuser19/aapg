'''
    Module to generate the arguments for the instructions
'''
import aapg.isa_funcs
import aapg.mappings
import random
import os
import logging

# Module Initialization
random.seed(os.urandom(256))

logger = logging.getLogger(__name__)

def gen_args(instruction, regfile, arch='rv64'):
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
