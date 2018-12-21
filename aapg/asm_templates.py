"""
    Module to store pre-defined templates
"""

def prelude_template(args):
    stack_size = args['stack_size']
    return [
    ]

def recurse_sections(depth):
    return {
        'recurse_init': [
            ('li', 'a0', '{}'.format(depth))
        ],
        'recurse': [
            ('addi', 'sp', 'sp', '-32'),
            ('sw', 'ra', '28(sp)'),
            ('sw', 's0', '24(sp)'),
            ('addi', 's0', 'sp', '32'),
            ('sw', 'a0', '-20(s0)'),
            ('lw', 'a5', '-20(s0)'),
            ('bnez', 'a5', '.recurse.L4'),
            ('li', 'a5', '0'),
            ('j', '.recurse.L3')
        ],
        'recurse.L4': [
            ('lw', 'a5', '-20(s0)'),
            ('addi', 'a5', 'a5', '-1'),
            ('mv', 'a0', 'a5'),
            ('call', '.recurse')
        ],
        'recurse.L3': [
            ('mv', 'a0', 'a5'),
            ('LREGU', 'ra', '28(sp)'),
            ('LREGU', 's0', '24(sp)'),
            ('addi', 'sp', 'sp', '32'),
            ('jr',  'ra')
        ]
    }
