"""
    Module to store pre-defined templates
"""

def prelude_template(args):
    stack_size = args['stack_size']
    return [
	('addi', 'sp', 'sp', '-{}'.format(stack_size)),
	('sd', 's0', 'sp', '{}'.format(stack_size - 8)),
	('addi', 's0', 'sp', '{}'.format(stack_size))
    ]

def recurse_sections():
    return {
        'recurse': [
            ('addi', 'sp', 'sp', '-32'),
            ('sd', 'ra', '24(sp)'),
            ('sd', 's0', '16(sp)'),
            ('addi', 's0', 'sp', '32'),
            ('mv', 'a5', 'a0'),
            ('sw', 'a5', '-20(s0)'),
            ('lw', 'a5', '-20(s0)'),
            ('sext.w', 'a5', 'a5'),
            ('bnez', 'a5', '.recurse.L4'),
            ('li', 'a5', '0'),
            ('j', '.recurse.L3')
        ],
        'recurse.L4': [
            ('lw', 'a5', '-20(s0)'),
            ('addiw', 'a5', 'a5', '-1'),
            ('sext.w', 'a5', 'a5'),
            ('mv', 'a0', 'a5'),
            ('call', 'recurse')
        ],
        'recurse.L3': [
            ('mv', 'a0', 'a5'),
            ('ld', 'ra', '24(sp)'),
            ('ld', 's0', '16(sp)'),
            ('addi', 'sp', 'sp', '32'),
            ('jr',  'ra')
        ]
    }
