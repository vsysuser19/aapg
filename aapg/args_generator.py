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

def gen_bounded_access_args(instruction, regfile, args):
    """ Generate a load or store to a specific address range """

    # Register file setup
    registers_int = [x for x in regfile if x[0] == 'x'] 
    registers_float = [x for x in regfile if x[0] == 'f']
    register_mapping = aapg.mappings.register_mapping_int
    register_mapping_float = aapg.mappings.register_mapping_float

    # Create valid sections
    sections_dict = {k : tuple(map(lambda x: int(x,16), v.split(',')))
            for k,v in args if k != 'enable'}

    # Choose random address
    section = random.choice(list(sections_dict.keys()))
    upper, lower = sections_dict[section]
    addr = random.randint(upper, lower)

    # Setup constants
    instr_name = instruction[0]
    instr_args = instruction[1:]

    final_inst = [instr_name,]

    for arg in instr_args:
        if arg == 'rd':
            register = random.choice(registers_int)
            regfile[register] += 1
            final_inst.append(register_mapping[register])
            continue

        if arg == 'rdf':
            register = random.choice(registers_float)
            regfile[register] += 1
            final_inst.append(register_mapping_float[register])
            continue

        if arg == 'rt':
            register = ('x', 31)
            regfile[register] += 1
            final_inst.append(register_mapping[register])
            continue

    # Return the tuple
    return (
        ('li', 't6', "{0:#0{1}x}".format(addr, 18)),
        tuple(final_inst) + ('0', )
    )

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

    if instr_name in aapg.isa_funcs.ctrl_insts:

        # Extract branch limits
        if kwargs is not None:
            total = int(kwargs['total'] if 'total' in kwargs else 0)
            current = int(kwargs['current'] if 'current' in kwargs else 0)

        rs1, rs2 = tuple(map(register_mapping.__getitem__, random.sample(registers_int, 2)))

        if random.random() < 1.0:
            try:
                jump_target = random.randint(0, total - current - 1)
            except ValueError as e:
                return ['addi', 'zero', 'zero', '0']
            bimm12 = 'i{0:010x}'.format(jump_target)

        final_inst.extend([rs1, rs2, bimm12])
        return final_inst

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
