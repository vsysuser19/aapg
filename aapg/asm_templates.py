"""
    Module to store pre-defined templates
"""

def prelude_template(args):
    stack_size = args['stack_size']
    return [
	('addi', 'sp', '-{}'.format(stack_size)),
	('sd', 's0', '{}(sp)'.format(stack_size - 8)),
	('addi', 's0', 'sp', '{}'.format(stack_size))
    ]
