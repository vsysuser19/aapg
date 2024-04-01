"""
    Testing BasicGenerator class from program_generator module
"""
import pytest
import configparser

from aapg.program_generator import BasicGenerator

@pytest.fixture
def confargs():
    args = configparser.ConfigParser()
    args['general'] = {}
    args['general']['total_instructions'] =  '100'
    args['isa-instruction-distribution'] = {}
    args['isa-instruction-distribution']['rel_rv32i.ctrl_instructions'] = '10'
    return args

class TestBasicGenerator(object):

    @staticmethod
    def test_constructor_exists():
        """ Check if constructor is working """
        basic_generator = BasicGenerator(confargs())
        assert isinstance(basic_generator, BasicGenerator)

    @staticmethod
    def test_raises_StopIteration_on_empty():
        """ Check if it stops iteration properly """
        args = confargs()
        args['general']['total_instructions'] = '0'
        basic_generator = BasicGenerator(args)
        with pytest.raises(StopIteration):
            next(basic_generator)

    @staticmethod
    def test_correct_num_instructions_generated():
        """ Check generated number of instructions """
        basic_generator = BasicGenerator(confargs())
        instruction_counter = 0
        with pytest.raises(StopIteration):
            while True:
                next(basic_generator)
                instruction_counter += 1

        assert instruction_counter == 100
