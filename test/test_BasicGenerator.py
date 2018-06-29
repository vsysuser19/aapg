"""
    Testing BasicGenerator class from program_generator module
"""
import pytest

from aapg.program_generator import BasicGenerator

class TestBasicGenerator(object):
    def test_constructor_exists(self):
        """ Check if constructor is working """
        args = {}
        basic_generator = BasicGenerator(args)
        assert isinstance(basic_generator, BasicGenerator)

    def test_raises_StopIteration_on_empty(self):
        """ Check if it stops iteration properly """
        args = {}
        basic_generator = BasicGenerator(args)
        with pytest.raises(StopIteration):
            next(basic_generator)

    def test_correct_num_instructions_generated(self):
        """ Check generated number of instructions """
