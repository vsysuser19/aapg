import pytest 
import os
import random
import numpy as np
from random import seed
from random import randint
from click.testing import CliRunner
from aapg.main import cli


list_of_files = ['aapg_cclass_rv64imafdc_illegal.yaml',
 'aapg_cclass_rv32imafc_bringup_s.yaml',
 'aapg_cclass_rv64imafdc_user_u.yaml',
 'aapg_cclass_rv64imafdc_exceptions_s.yaml',
 'aapg_cclass_rv32imac_bringup_u.yaml',
 'aapg_cclass_exceptions_s.yaml',
 'aapg_cclass_rv64imac_bringup_s.yaml',
 '.DS_Store',
 'aapg_cclass_rv32imaf_bringup_s.yaml',
 'aapg_cclass_rv64imafdc_bringup_u.yaml',
 'aapg_cclass_rv64ic_bringup_s.yaml',
 'aapg_cclass_rv64imafd_bringup_s.yaml',
 'aapg_cclass_rv32ic_bringup.yaml',
 'aapg_cclass_rv32imafc_bringup_u.yaml',
 'aapg_cclass_rv64imafdc_user_s.yaml',
 'aapg_cclass_rv32imafc_bringup.yaml',
 'aapg_cclass_config1.yaml',
 'aapg_cclass_rv64imafdc_exceptions_u.yaml',
 'aapg_cclass_rv32imac_bringup_s.yaml',
 'aapg_cclass_illegal.yaml',
 'aapg_cclass_exceptions_u.yaml',
 'aapg_cclass_rv64imac_bringup_u.yaml',
 'aapg_cclass_rv64imafdc_bringup.yaml',
 'aapg_cclass_rv64imafdc_hazards.yaml',
 'aapg_cclass_rv64imafdc_exceptions.yaml',
 'aapg_cclass_rv64ic_bringup_u.yaml',
 'aapg_cclass_rv64imafd_bringup_u.yaml',
 'aapg_cclass_rv64imafd_exceptions.yaml',
 'aapg_cclass_rv32imac_bringup.yaml',
 'aapg_cclass_rv32imaf_bringup_u.yaml',
 'aapg_cclass_rv64imafdc_bringup_s.yaml',
 'aapg_cclass_rv64imafd_bringup.yaml',
 'aapg_cclass_exceptions.yaml',
 'aapg_cclass_rv32ic_bringup_s.yaml',
 'aapg_cclass_rv32imaf_bringup.yaml',
 'aapg_cclass_rv64imafdc_illegal_u.yaml',
 'aapg_cclass_rv32imc_bringup_u.yaml',
 'aapg_cclass_rv64imafdc_branches1_u.yaml',
 'aapg_cclass_rv32imc_bringup.yaml',
 'aapg_cclass_illegal_s.yaml',
 'aapg_cclass_config1_u.yaml',
 'aapg_cclass_v_bringup_u.yaml',
 'aapg_cclass_rv64imc_bringup_u.yaml',
 'aapg_cclass_rv64imafd_exceptions_s.yaml',
 'aapg_cclass_rv64imc_bringup.yaml',
 'aapg_cclass_rv64imafdc_hazards_u.yaml',
 'aapg_cclass_rv64imafdc_illegal_s.yaml',
 'aapg_cclass_rv64imafdc_branches1.yaml',
 'aapg_cclass_rv32imc_bringup_s.yaml',
 'aapg_cclass_rv64imafdc_branches1_s.yaml',
 'aapg_cclass_v_bringup.yaml',
 'aapg_cclass_rv32ic_bringup_u.yaml',
 'aapg_cclass_rv64imafdc_user.yaml',
 'aapg_cclass_rv64imac_bringup.yaml',
 'aapg_cclass_rv64imafdc_hazards_s.yaml',
 'aapg_cclass_rv64ic_bringup.yaml',
 'aapg_cclass_illegal_u.yaml',
 'aapg_cclass_config1_s.yaml',
 'aapg_cclass_v_bringup_s.yaml',
 'aapg_cclass_rv64imc_bringup_s.yaml',
 'aapg_cclass_rv64imafd_exceptions_u.yaml']
list_of_files2 = ['aapg_cclass_rv64imafdc_illegal',
 'aapg_cclass_rv32imafc_bringup_s',
 'aapg_cclass_rv64imafdc_user_u',
 'aapg_cclass_rv64imafdc_exceptions_s',
 'aapg_cclass_rv32imac_bringup_u',
 'aapg_cclass_exceptions_s',
 'aapg_cclass_rv64imac_bringup_s',
 '.DS_',
 'aapg_cclass_rv32imaf_bringup_s',
 'aapg_cclass_rv64imafdc_bringup_u',
 'aapg_cclass_rv64ic_bringup_s',
 'aapg_cclass_rv64imafd_bringup_s',
 'aapg_cclass_rv32ic_bringup',
 'aapg_cclass_rv32imafc_bringup_u',
 'aapg_cclass_rv64imafdc_user_s',
 'aapg_cclass_rv32imafc_bringup',
 'aapg_cclass_config1',
 'aapg_cclass_rv64imafdc_exceptions_u',
 'aapg_cclass_rv32imac_bringup_s',
 'aapg_cclass_illegal',
 'aapg_cclass_exceptions_u',
 'aapg_cclass_rv64imac_bringup_u',
 'aapg_cclass_rv64imafdc_bringup',
 'aapg_cclass_rv64imafdc_hazards',
 'aapg_cclass_rv64imafdc_exceptions',
 'aapg_cclass_rv64ic_bringup_u',
 'aapg_cclass_rv64imafd_bringup_u',
 'aapg_cclass_rv64imafd_exceptions',
 'aapg_cclass_rv32imac_bringup',
 'aapg_cclass_rv32imaf_bringup_u',
 'aapg_cclass_rv64imafdc_bringup_s',
 'aapg_cclass_rv64imafd_bringup',
 'aapg_cclass_exceptions',
 'aapg_cclass_rv32ic_bringup_s',
 'aapg_cclass_rv32imaf_bringup',
 'aapg_cclass_rv64imafdc_illegal_u',
 'aapg_cclass_rv32imc_bringup_u',
 'aapg_cclass_rv64imafdc_branches1_u',
 'aapg_cclass_rv32imc_bringup',
 'aapg_cclass_illegal_s',
 'aapg_cclass_config1_u',
 'aapg_cclass_v_bringup_u',
 'aapg_cclass_rv64imc_bringup_u',
 'aapg_cclass_rv64imafd_exceptions_s',
 'aapg_cclass_rv64imc_bringup',
 'aapg_cclass_rv64imafdc_hazards_u',
 'aapg_cclass_rv64imafdc_illegal_s',
 'aapg_cclass_rv64imafdc_branches1',
 'aapg_cclass_rv32imc_bringup_s',
 'aapg_cclass_rv64imafdc_branches1_s',
 'aapg_cclass_v_bringup',
 'aapg_cclass_rv32ic_bringup_u',
 'aapg_cclass_rv64imafdc_user',
 'aapg_cclass_rv64imac_bringup',
 'aapg_cclass_rv64imafdc_hazards_s',
 'aapg_cclass_rv64ic_bringup',
 'aapg_cclass_illegal_u',
 'aapg_cclass_config1_s',
 'aapg_cclass_v_bringup_s',
 'aapg_cclass_rv64imc_bringup_s',
 'aapg_cclass_rv64imafd_exceptions_u']

seeds = []
seed(1)
for _ in range(100):
    value = randint(0, 1000)
    seeds.append(value)

@pytest.fixture
def runner():
    return CliRunner()

@pytest.mark.serial
def test_setup(runner):
    '''Testing setup option in serial mode'''
    result = runner.invoke(cli, ['setup','--setup_dir=work'])
    assert result.exit_code == 0

def aapg_cclass_rv64imafdc_illegal(runner):
    '''Testing aapg_cclass_rv64imafdc_illegal.yaml config file in parallel mode'''
    result = runner.invoke(cli, ['gen','--setup_dir=work','--output_dir=work1','--num_programs=5','--config_file=./../tests/cclass/{config_file}'.format(config_file=list_of_files[1]),'--asm_name={name}'.format(name=list_of_files2[1]),'--seed={gen_seed}'.format(gen_seed=seeds[1]),'--arch=rv64'])
    assert result.exit_code == 0

def aapg_cclass_rv32imafc_bringup_s(runner):
    '''Testing aapg_cclass_rv32imafc_bringup_s.yaml config file in parallel mode'''
    result = runner.invoke(cli, ['gen','--setup_dir=work','--output_dir=work1','--num_programs=5','--config_file=./../tests/cclass/{config_file}'.format(config_file=list_of_files[1]),'--asm_name={name}'.format(name=list_of_files2[1]),'--seed={gen_seed}'.format(gen_seed=seeds[1]),'--arch=rv32'])
    assert result.exit_code == 0

def aapg_cclass_rv64imafdc_user_u(runner):
    '''Testing aapg_cclass_rv64imafdc_user_u.yaml config file in parallel mode'''
    result = runner.invoke(cli, ['gen','--setup_dir=work','--output_dir=work1','--num_programs=5','--config_file=./../tests/cclass/{config_file}'.format(config_file=list_of_files[1]),'--asm_name={name}'.format(name=list_of_files2[1]),'--seed={gen_seed}'.format(gen_seed=seeds[1]),'--arch=rv64'])
    assert result.exit_code == 0

def aapg_cclass_rv64imafdc_exceptions_s(runner):
    '''Testing aapg_cclass_rv64imafdc_exceptions_s.yaml config file in parallel mode'''
    result = runner.invoke(cli, ['gen','--setup_dir=work','--output_dir=work1','--num_programs=5','--config_file=./../tests/cclass/{config_file}'.format(config_file=list_of_files[1]),'--asm_name={name}'.format(name=list_of_files2[1]),'--seed={gen_seed}'.format(gen_seed=seeds[1]),'--arch=rv64'])
    assert result.exit_code == 0

def aapg_cclass_rv32imac_bringup_u(runner):
    '''Testing aapg_cclass_rv32imac_bringup_u.yaml config file in parallel mode'''
    result = runner.invoke(cli, ['gen','--setup_dir=work','--output_dir=work1','--num_programs=5','--config_file=./../tests/cclass/{config_file}'.format(config_file=list_of_files[1]),'--asm_name={name}'.format(name=list_of_files2[1]),'--seed={gen_seed}'.format(gen_seed=seeds[1]),'--arch=rv32'])
    assert result.exit_code == 0

def aapg_cclass_exceptions_s(runner):
    '''Testing aapg_cclass_exceptions_s.yaml config file in parallel mode'''
    result = runner.invoke(cli, ['gen','--setup_dir=work','--output_dir=work1','--num_programs=5','--config_file=./../tests/cclass/{config_file}'.format(config_file=list_of_files[1]),'--asm_name={name}'.format(name=list_of_files2[1]),'--seed={gen_seed}'.format(gen_seed=seeds[1]),'--arch=rv64'])
    assert result.exit_code == 0

def aapg_cclass_rv64imac_bringup_s(runner):
    '''Testing aapg_cclass_rv64imac_bringup_s.yaml config file in parallel mode'''
    result = runner.invoke(cli, ['gen','--setup_dir=work','--output_dir=work1','--num_programs=5','--config_file=./../tests/cclass/{config_file}'.format(config_file=list_of_files[1]),'--asm_name={name}'.format(name=list_of_files2[1]),'--seed={gen_seed}'.format(gen_seed=seeds[1]),'--arch=rv64'])
    assert result.exit_code == 0

def .DS_(runner):
    '''Testing .DS_.yaml config file in parallel mode'''
    result = runner.invoke(cli, ['gen','--setup_dir=work','--output_dir=work1','--num_programs=5','--config_file=./../tests/cclass/{config_file}'.format(config_file=list_of_files[1]),'--asm_name={name}'.format(name=list_of_files2[1]),'--seed={gen_seed}'.format(gen_seed=seeds[1]),'--arch=rv64'])
    assert result.exit_code == 0

def aapg_cclass_rv32imaf_bringup_s(runner):
    '''Testing aapg_cclass_rv32imaf_bringup_s.yaml config file in parallel mode'''
    result = runner.invoke(cli, ['gen','--setup_dir=work','--output_dir=work1','--num_programs=5','--config_file=./../tests/cclass/{config_file}'.format(config_file=list_of_files[1]),'--asm_name={name}'.format(name=list_of_files2[1]),'--seed={gen_seed}'.format(gen_seed=seeds[1]),'--arch=rv32'])
    assert result.exit_code == 0

def aapg_cclass_rv64imafdc_bringup_u(runner):
    '''Testing aapg_cclass_rv64imafdc_bringup_u.yaml config file in parallel mode'''
    result = runner.invoke(cli, ['gen','--setup_dir=work','--output_dir=work1','--num_programs=5','--config_file=./../tests/cclass/{config_file}'.format(config_file=list_of_files[1]),'--asm_name={name}'.format(name=list_of_files2[1]),'--seed={gen_seed}'.format(gen_seed=seeds[1]),'--arch=rv64'])
    assert result.exit_code == 0

def aapg_cclass_rv64ic_bringup_s(runner):
    '''Testing aapg_cclass_rv64ic_bringup_s.yaml config file in parallel mode'''
    result = runner.invoke(cli, ['gen','--setup_dir=work','--output_dir=work1','--num_programs=5','--config_file=./../tests/cclass/{config_file}'.format(config_file=list_of_files[1]),'--asm_name={name}'.format(name=list_of_files2[1]),'--seed={gen_seed}'.format(gen_seed=seeds[1]),'--arch=rv64'])
    assert result.exit_code == 0

def aapg_cclass_rv64imafd_bringup_s(runner):
    '''Testing aapg_cclass_rv64imafd_bringup_s.yaml config file in parallel mode'''
    result = runner.invoke(cli, ['gen','--setup_dir=work','--output_dir=work1','--num_programs=5','--config_file=./../tests/cclass/{config_file}'.format(config_file=list_of_files[1]),'--asm_name={name}'.format(name=list_of_files2[1]),'--seed={gen_seed}'.format(gen_seed=seeds[1]),'--arch=rv64'])
    assert result.exit_code == 0

def aapg_cclass_rv32ic_bringup(runner):
    '''Testing aapg_cclass_rv32ic_bringup.yaml config file in parallel mode'''
    result = runner.invoke(cli, ['gen','--setup_dir=work','--output_dir=work1','--num_programs=5','--config_file=./../tests/cclass/{config_file}'.format(config_file=list_of_files[1]),'--asm_name={name}'.format(name=list_of_files2[1]),'--seed={gen_seed}'.format(gen_seed=seeds[1]),'--arch=rv32'])
    assert result.exit_code == 0

def aapg_cclass_rv32imafc_bringup_u(runner):
    '''Testing aapg_cclass_rv32imafc_bringup_u.yaml config file in parallel mode'''
    result = runner.invoke(cli, ['gen','--setup_dir=work','--output_dir=work1','--num_programs=5','--config_file=./../tests/cclass/{config_file}'.format(config_file=list_of_files[1]),'--asm_name={name}'.format(name=list_of_files2[1]),'--seed={gen_seed}'.format(gen_seed=seeds[1]),'--arch=rv32'])
    assert result.exit_code == 0

def aapg_cclass_rv64imafdc_user_s(runner):
    '''Testing aapg_cclass_rv64imafdc_user_s.yaml config file in parallel mode'''
    result = runner.invoke(cli, ['gen','--setup_dir=work','--output_dir=work1','--num_programs=5','--config_file=./../tests/cclass/{config_file}'.format(config_file=list_of_files[1]),'--asm_name={name}'.format(name=list_of_files2[1]),'--seed={gen_seed}'.format(gen_seed=seeds[1]),'--arch=rv64'])
    assert result.exit_code == 0

def aapg_cclass_rv32imafc_bringup(runner):
    '''Testing aapg_cclass_rv32imafc_bringup.yaml config file in parallel mode'''
    result = runner.invoke(cli, ['gen','--setup_dir=work','--output_dir=work1','--num_programs=5','--config_file=./../tests/cclass/{config_file}'.format(config_file=list_of_files[1]),'--asm_name={name}'.format(name=list_of_files2[1]),'--seed={gen_seed}'.format(gen_seed=seeds[1]),'--arch=rv32'])
    assert result.exit_code == 0

def aapg_cclass_config1(runner):
    '''Testing aapg_cclass_config1.yaml config file in parallel mode'''
    result = runner.invoke(cli, ['gen','--setup_dir=work','--output_dir=work1','--num_programs=5','--config_file=./../tests/cclass/{config_file}'.format(config_file=list_of_files[1]),'--asm_name={name}'.format(name=list_of_files2[1]),'--seed={gen_seed}'.format(gen_seed=seeds[1]),'--arch=rv64'])
    assert result.exit_code == 0

def aapg_cclass_rv64imafdc_exceptions_u(runner):
    '''Testing aapg_cclass_rv64imafdc_exceptions_u.yaml config file in parallel mode'''
    result = runner.invoke(cli, ['gen','--setup_dir=work','--output_dir=work1','--num_programs=5','--config_file=./../tests/cclass/{config_file}'.format(config_file=list_of_files[1]),'--asm_name={name}'.format(name=list_of_files2[1]),'--seed={gen_seed}'.format(gen_seed=seeds[1]),'--arch=rv64'])
    assert result.exit_code == 0

def aapg_cclass_rv32imac_bringup_s(runner):
    '''Testing aapg_cclass_rv32imac_bringup_s.yaml config file in parallel mode'''
    result = runner.invoke(cli, ['gen','--setup_dir=work','--output_dir=work1','--num_programs=5','--config_file=./../tests/cclass/{config_file}'.format(config_file=list_of_files[1]),'--asm_name={name}'.format(name=list_of_files2[1]),'--seed={gen_seed}'.format(gen_seed=seeds[1]),'--arch=rv32'])
    assert result.exit_code == 0

def aapg_cclass_illegal(runner):
    '''Testing aapg_cclass_illegal.yaml config file in parallel mode'''
    result = runner.invoke(cli, ['gen','--setup_dir=work','--output_dir=work1','--num_programs=5','--config_file=./../tests/cclass/{config_file}'.format(config_file=list_of_files[1]),'--asm_name={name}'.format(name=list_of_files2[1]),'--seed={gen_seed}'.format(gen_seed=seeds[1]),'--arch=rv64'])
    assert result.exit_code == 0

def aapg_cclass_exceptions_u(runner):
    '''Testing aapg_cclass_exceptions_u.yaml config file in parallel mode'''
    result = runner.invoke(cli, ['gen','--setup_dir=work','--output_dir=work1','--num_programs=5','--config_file=./../tests/cclass/{config_file}'.format(config_file=list_of_files[1]),'--asm_name={name}'.format(name=list_of_files2[1]),'--seed={gen_seed}'.format(gen_seed=seeds[1]),'--arch=rv64'])
    assert result.exit_code == 0

def aapg_cclass_rv64imac_bringup_u(runner):
    '''Testing aapg_cclass_rv64imac_bringup_u.yaml config file in parallel mode'''
    result = runner.invoke(cli, ['gen','--setup_dir=work','--output_dir=work1','--num_programs=5','--config_file=./../tests/cclass/{config_file}'.format(config_file=list_of_files[1]),'--asm_name={name}'.format(name=list_of_files2[1]),'--seed={gen_seed}'.format(gen_seed=seeds[1]),'--arch=rv64'])
    assert result.exit_code == 0

def aapg_cclass_rv64imafdc_bringup(runner):
    '''Testing aapg_cclass_rv64imafdc_bringup.yaml config file in parallel mode'''
    result = runner.invoke(cli, ['gen','--setup_dir=work','--output_dir=work1','--num_programs=5','--config_file=./../tests/cclass/{config_file}'.format(config_file=list_of_files[1]),'--asm_name={name}'.format(name=list_of_files2[1]),'--seed={gen_seed}'.format(gen_seed=seeds[1]),'--arch=rv64'])
    assert result.exit_code == 0

def aapg_cclass_rv64imafdc_hazards(runner):
    '''Testing aapg_cclass_rv64imafdc_hazards.yaml config file in parallel mode'''
    result = runner.invoke(cli, ['gen','--setup_dir=work','--output_dir=work1','--num_programs=5','--config_file=./../tests/cclass/{config_file}'.format(config_file=list_of_files[1]),'--asm_name={name}'.format(name=list_of_files2[1]),'--seed={gen_seed}'.format(gen_seed=seeds[1]),'--arch=rv64'])
    assert result.exit_code == 0

def aapg_cclass_rv64imafdc_exceptions(runner):
    '''Testing aapg_cclass_rv64imafdc_exceptions.yaml config file in parallel mode'''
    result = runner.invoke(cli, ['gen','--setup_dir=work','--output_dir=work1','--num_programs=5','--config_file=./../tests/cclass/{config_file}'.format(config_file=list_of_files[1]),'--asm_name={name}'.format(name=list_of_files2[1]),'--seed={gen_seed}'.format(gen_seed=seeds[1]),'--arch=rv64'])
    assert result.exit_code == 0

def aapg_cclass_rv64ic_bringup_u(runner):
    '''Testing aapg_cclass_rv64ic_bringup_u.yaml config file in parallel mode'''
    result = runner.invoke(cli, ['gen','--setup_dir=work','--output_dir=work1','--num_programs=5','--config_file=./../tests/cclass/{config_file}'.format(config_file=list_of_files[1]),'--asm_name={name}'.format(name=list_of_files2[1]),'--seed={gen_seed}'.format(gen_seed=seeds[1]),'--arch=rv64'])
    assert result.exit_code == 0

def aapg_cclass_rv64imafd_bringup_u(runner):
    '''Testing aapg_cclass_rv64imafd_bringup_u.yaml config file in parallel mode'''
    result = runner.invoke(cli, ['gen','--setup_dir=work','--output_dir=work1','--num_programs=5','--config_file=./../tests/cclass/{config_file}'.format(config_file=list_of_files[1]),'--asm_name={name}'.format(name=list_of_files2[1]),'--seed={gen_seed}'.format(gen_seed=seeds[1]),'--arch=rv64'])
    assert result.exit_code == 0

def aapg_cclass_rv64imafd_exceptions(runner):
    '''Testing aapg_cclass_rv64imafd_exceptions.yaml config file in parallel mode'''
    result = runner.invoke(cli, ['gen','--setup_dir=work','--output_dir=work1','--num_programs=5','--config_file=./../tests/cclass/{config_file}'.format(config_file=list_of_files[1]),'--asm_name={name}'.format(name=list_of_files2[1]),'--seed={gen_seed}'.format(gen_seed=seeds[1]),'--arch=rv64'])
    assert result.exit_code == 0

def aapg_cclass_rv32imac_bringup(runner):
    '''Testing aapg_cclass_rv32imac_bringup.yaml config file in parallel mode'''
    result = runner.invoke(cli, ['gen','--setup_dir=work','--output_dir=work1','--num_programs=5','--config_file=./../tests/cclass/{config_file}'.format(config_file=list_of_files[1]),'--asm_name={name}'.format(name=list_of_files2[1]),'--seed={gen_seed}'.format(gen_seed=seeds[1]),'--arch=rv32'])
    assert result.exit_code == 0

def aapg_cclass_rv32imaf_bringup_u(runner):
    '''Testing aapg_cclass_rv32imaf_bringup_u.yaml config file in parallel mode'''
    result = runner.invoke(cli, ['gen','--setup_dir=work','--output_dir=work1','--num_programs=5','--config_file=./../tests/cclass/{config_file}'.format(config_file=list_of_files[1]),'--asm_name={name}'.format(name=list_of_files2[1]),'--seed={gen_seed}'.format(gen_seed=seeds[1]),'--arch=rv32'])
    assert result.exit_code == 0

def aapg_cclass_rv64imafdc_bringup_s(runner):
    '''Testing aapg_cclass_rv64imafdc_bringup_s.yaml config file in parallel mode'''
    result = runner.invoke(cli, ['gen','--setup_dir=work','--output_dir=work1','--num_programs=5','--config_file=./../tests/cclass/{config_file}'.format(config_file=list_of_files[1]),'--asm_name={name}'.format(name=list_of_files2[1]),'--seed={gen_seed}'.format(gen_seed=seeds[1]),'--arch=rv64'])
    assert result.exit_code == 0

def aapg_cclass_rv64imafd_bringup(runner):
    '''Testing aapg_cclass_rv64imafd_bringup.yaml config file in parallel mode'''
    result = runner.invoke(cli, ['gen','--setup_dir=work','--output_dir=work1','--num_programs=5','--config_file=./../tests/cclass/{config_file}'.format(config_file=list_of_files[1]),'--asm_name={name}'.format(name=list_of_files2[1]),'--seed={gen_seed}'.format(gen_seed=seeds[1]),'--arch=rv64'])
    assert result.exit_code == 0

def aapg_cclass_exceptions(runner):
    '''Testing aapg_cclass_exceptions.yaml config file in parallel mode'''
    result = runner.invoke(cli, ['gen','--setup_dir=work','--output_dir=work1','--num_programs=5','--config_file=./../tests/cclass/{config_file}'.format(config_file=list_of_files[1]),'--asm_name={name}'.format(name=list_of_files2[1]),'--seed={gen_seed}'.format(gen_seed=seeds[1]),'--arch=rv64'])
    assert result.exit_code == 0

def aapg_cclass_rv32ic_bringup_s(runner):
    '''Testing aapg_cclass_rv32ic_bringup_s.yaml config file in parallel mode'''
    result = runner.invoke(cli, ['gen','--setup_dir=work','--output_dir=work1','--num_programs=5','--config_file=./../tests/cclass/{config_file}'.format(config_file=list_of_files[1]),'--asm_name={name}'.format(name=list_of_files2[1]),'--seed={gen_seed}'.format(gen_seed=seeds[1]),'--arch=rv32'])
    assert result.exit_code == 0

def aapg_cclass_rv32imaf_bringup(runner):
    '''Testing aapg_cclass_rv32imaf_bringup.yaml config file in parallel mode'''
    result = runner.invoke(cli, ['gen','--setup_dir=work','--output_dir=work1','--num_programs=5','--config_file=./../tests/cclass/{config_file}'.format(config_file=list_of_files[1]),'--asm_name={name}'.format(name=list_of_files2[1]),'--seed={gen_seed}'.format(gen_seed=seeds[1]),'--arch=rv32'])
    assert result.exit_code == 0

def aapg_cclass_rv64imafdc_illegal_u(runner):
    '''Testing aapg_cclass_rv64imafdc_illegal_u.yaml config file in parallel mode'''
    result = runner.invoke(cli, ['gen','--setup_dir=work','--output_dir=work1','--num_programs=5','--config_file=./../tests/cclass/{config_file}'.format(config_file=list_of_files[1]),'--asm_name={name}'.format(name=list_of_files2[1]),'--seed={gen_seed}'.format(gen_seed=seeds[1]),'--arch=rv64'])
    assert result.exit_code == 0

def aapg_cclass_rv32imc_bringup_u(runner):
    '''Testing aapg_cclass_rv32imc_bringup_u.yaml config file in parallel mode'''
    result = runner.invoke(cli, ['gen','--setup_dir=work','--output_dir=work1','--num_programs=5','--config_file=./../tests/cclass/{config_file}'.format(config_file=list_of_files[1]),'--asm_name={name}'.format(name=list_of_files2[1]),'--seed={gen_seed}'.format(gen_seed=seeds[1]),'--arch=rv32'])
    assert result.exit_code == 0

def aapg_cclass_rv64imafdc_branches1_u(runner):
    '''Testing aapg_cclass_rv64imafdc_branches1_u.yaml config file in parallel mode'''
    result = runner.invoke(cli, ['gen','--setup_dir=work','--output_dir=work1','--num_programs=5','--config_file=./../tests/cclass/{config_file}'.format(config_file=list_of_files[1]),'--asm_name={name}'.format(name=list_of_files2[1]),'--seed={gen_seed}'.format(gen_seed=seeds[1]),'--arch=rv64'])
    assert result.exit_code == 0

def aapg_cclass_rv32imc_bringup(runner):
    '''Testing aapg_cclass_rv32imc_bringup.yaml config file in parallel mode'''
    result = runner.invoke(cli, ['gen','--setup_dir=work','--output_dir=work1','--num_programs=5','--config_file=./../tests/cclass/{config_file}'.format(config_file=list_of_files[1]),'--asm_name={name}'.format(name=list_of_files2[1]),'--seed={gen_seed}'.format(gen_seed=seeds[1]),'--arch=rv32'])
    assert result.exit_code == 0

def aapg_cclass_illegal_s(runner):
    '''Testing aapg_cclass_illegal_s.yaml config file in parallel mode'''
    result = runner.invoke(cli, ['gen','--setup_dir=work','--output_dir=work1','--num_programs=5','--config_file=./../tests/cclass/{config_file}'.format(config_file=list_of_files[1]),'--asm_name={name}'.format(name=list_of_files2[1]),'--seed={gen_seed}'.format(gen_seed=seeds[1]),'--arch=rv64'])
    assert result.exit_code == 0

def aapg_cclass_config1_u(runner):
    '''Testing aapg_cclass_config1_u.yaml config file in parallel mode'''
    result = runner.invoke(cli, ['gen','--setup_dir=work','--output_dir=work1','--num_programs=5','--config_file=./../tests/cclass/{config_file}'.format(config_file=list_of_files[1]),'--asm_name={name}'.format(name=list_of_files2[1]),'--seed={gen_seed}'.format(gen_seed=seeds[1]),'--arch=rv64'])
    assert result.exit_code == 0

def aapg_cclass_v_bringup_u(runner):
    '''Testing aapg_cclass_v_bringup_u.yaml config file in parallel mode'''
    result = runner.invoke(cli, ['gen','--setup_dir=work','--output_dir=work1','--num_programs=5','--config_file=./../tests/cclass/{config_file}'.format(config_file=list_of_files[1]),'--asm_name={name}'.format(name=list_of_files2[1]),'--seed={gen_seed}'.format(gen_seed=seeds[1]),'--arch=rv64'])
    assert result.exit_code == 0

def aapg_cclass_rv64imc_bringup_u(runner):
    '''Testing aapg_cclass_rv64imc_bringup_u.yaml config file in parallel mode'''
    result = runner.invoke(cli, ['gen','--setup_dir=work','--output_dir=work1','--num_programs=5','--config_file=./../tests/cclass/{config_file}'.format(config_file=list_of_files[1]),'--asm_name={name}'.format(name=list_of_files2[1]),'--seed={gen_seed}'.format(gen_seed=seeds[1]),'--arch=rv64'])
    assert result.exit_code == 0

def aapg_cclass_rv64imafd_exceptions_s(runner):
    '''Testing aapg_cclass_rv64imafd_exceptions_s.yaml config file in parallel mode'''
    result = runner.invoke(cli, ['gen','--setup_dir=work','--output_dir=work1','--num_programs=5','--config_file=./../tests/cclass/{config_file}'.format(config_file=list_of_files[1]),'--asm_name={name}'.format(name=list_of_files2[1]),'--seed={gen_seed}'.format(gen_seed=seeds[1]),'--arch=rv64'])
    assert result.exit_code == 0

def aapg_cclass_rv64imc_bringup(runner):
    '''Testing aapg_cclass_rv64imc_bringup.yaml config file in parallel mode'''
    result = runner.invoke(cli, ['gen','--setup_dir=work','--output_dir=work1','--num_programs=5','--config_file=./../tests/cclass/{config_file}'.format(config_file=list_of_files[1]),'--asm_name={name}'.format(name=list_of_files2[1]),'--seed={gen_seed}'.format(gen_seed=seeds[1]),'--arch=rv64'])
    assert result.exit_code == 0

def aapg_cclass_rv64imafdc_hazards_u(runner):
    '''Testing aapg_cclass_rv64imafdc_hazards_u.yaml config file in parallel mode'''
    result = runner.invoke(cli, ['gen','--setup_dir=work','--output_dir=work1','--num_programs=5','--config_file=./../tests/cclass/{config_file}'.format(config_file=list_of_files[1]),'--asm_name={name}'.format(name=list_of_files2[1]),'--seed={gen_seed}'.format(gen_seed=seeds[1]),'--arch=rv64'])
    assert result.exit_code == 0

def aapg_cclass_rv64imafdc_illegal_s(runner):
    '''Testing aapg_cclass_rv64imafdc_illegal_s.yaml config file in parallel mode'''
    result = runner.invoke(cli, ['gen','--setup_dir=work','--output_dir=work1','--num_programs=5','--config_file=./../tests/cclass/{config_file}'.format(config_file=list_of_files[1]),'--asm_name={name}'.format(name=list_of_files2[1]),'--seed={gen_seed}'.format(gen_seed=seeds[1]),'--arch=rv64'])
    assert result.exit_code == 0

def aapg_cclass_rv64imafdc_branches1(runner):
    '''Testing aapg_cclass_rv64imafdc_branches1.yaml config file in parallel mode'''
    result = runner.invoke(cli, ['gen','--setup_dir=work','--output_dir=work1','--num_programs=5','--config_file=./../tests/cclass/{config_file}'.format(config_file=list_of_files[1]),'--asm_name={name}'.format(name=list_of_files2[1]),'--seed={gen_seed}'.format(gen_seed=seeds[1]),'--arch=rv64'])
    assert result.exit_code == 0

def aapg_cclass_rv32imc_bringup_s(runner):
    '''Testing aapg_cclass_rv32imc_bringup_s.yaml config file in parallel mode'''
    result = runner.invoke(cli, ['gen','--setup_dir=work','--output_dir=work1','--num_programs=5','--config_file=./../tests/cclass/{config_file}'.format(config_file=list_of_files[1]),'--asm_name={name}'.format(name=list_of_files2[1]),'--seed={gen_seed}'.format(gen_seed=seeds[1]),'--arch=rv32'])
    assert result.exit_code == 0

def aapg_cclass_rv64imafdc_branches1_s(runner):
    '''Testing aapg_cclass_rv64imafdc_branches1_s.yaml config file in parallel mode'''
    result = runner.invoke(cli, ['gen','--setup_dir=work','--output_dir=work1','--num_programs=5','--config_file=./../tests/cclass/{config_file}'.format(config_file=list_of_files[1]),'--asm_name={name}'.format(name=list_of_files2[1]),'--seed={gen_seed}'.format(gen_seed=seeds[1]),'--arch=rv64'])
    assert result.exit_code == 0

def aapg_cclass_v_bringup(runner):
    '''Testing aapg_cclass_v_bringup.yaml config file in parallel mode'''
    result = runner.invoke(cli, ['gen','--setup_dir=work','--output_dir=work1','--num_programs=5','--config_file=./../tests/cclass/{config_file}'.format(config_file=list_of_files[1]),'--asm_name={name}'.format(name=list_of_files2[1]),'--seed={gen_seed}'.format(gen_seed=seeds[1]),'--arch=rv64'])
    assert result.exit_code == 0

def aapg_cclass_rv32ic_bringup_u(runner):
    '''Testing aapg_cclass_rv32ic_bringup_u.yaml config file in parallel mode'''
    result = runner.invoke(cli, ['gen','--setup_dir=work','--output_dir=work1','--num_programs=5','--config_file=./../tests/cclass/{config_file}'.format(config_file=list_of_files[1]),'--asm_name={name}'.format(name=list_of_files2[1]),'--seed={gen_seed}'.format(gen_seed=seeds[1]),'--arch=rv32'])
    assert result.exit_code == 0

def aapg_cclass_rv64imafdc_user(runner):
    '''Testing aapg_cclass_rv64imafdc_user.yaml config file in parallel mode'''
    result = runner.invoke(cli, ['gen','--setup_dir=work','--output_dir=work1','--num_programs=5','--config_file=./../tests/cclass/{config_file}'.format(config_file=list_of_files[1]),'--asm_name={name}'.format(name=list_of_files2[1]),'--seed={gen_seed}'.format(gen_seed=seeds[1]),'--arch=rv64'])
    assert result.exit_code == 0

def aapg_cclass_rv64imac_bringup(runner):
    '''Testing aapg_cclass_rv64imac_bringup.yaml config file in parallel mode'''
    result = runner.invoke(cli, ['gen','--setup_dir=work','--output_dir=work1','--num_programs=5','--config_file=./../tests/cclass/{config_file}'.format(config_file=list_of_files[1]),'--asm_name={name}'.format(name=list_of_files2[1]),'--seed={gen_seed}'.format(gen_seed=seeds[1]),'--arch=rv64'])
    assert result.exit_code == 0

def aapg_cclass_rv64imafdc_hazards_s(runner):
    '''Testing aapg_cclass_rv64imafdc_hazards_s.yaml config file in parallel mode'''
    result = runner.invoke(cli, ['gen','--setup_dir=work','--output_dir=work1','--num_programs=5','--config_file=./../tests/cclass/{config_file}'.format(config_file=list_of_files[1]),'--asm_name={name}'.format(name=list_of_files2[1]),'--seed={gen_seed}'.format(gen_seed=seeds[1]),'--arch=rv64'])
    assert result.exit_code == 0

def aapg_cclass_rv64ic_bringup(runner):
    '''Testing aapg_cclass_rv64ic_bringup.yaml config file in parallel mode'''
    result = runner.invoke(cli, ['gen','--setup_dir=work','--output_dir=work1','--num_programs=5','--config_file=./../tests/cclass/{config_file}'.format(config_file=list_of_files[1]),'--asm_name={name}'.format(name=list_of_files2[1]),'--seed={gen_seed}'.format(gen_seed=seeds[1]),'--arch=rv64'])
    assert result.exit_code == 0

def aapg_cclass_illegal_u(runner):
    '''Testing aapg_cclass_illegal_u.yaml config file in parallel mode'''
    result = runner.invoke(cli, ['gen','--setup_dir=work','--output_dir=work1','--num_programs=5','--config_file=./../tests/cclass/{config_file}'.format(config_file=list_of_files[1]),'--asm_name={name}'.format(name=list_of_files2[1]),'--seed={gen_seed}'.format(gen_seed=seeds[1]),'--arch=rv64'])
    assert result.exit_code == 0

def aapg_cclass_config1_s(runner):
    '''Testing aapg_cclass_config1_s.yaml config file in parallel mode'''
    result = runner.invoke(cli, ['gen','--setup_dir=work','--output_dir=work1','--num_programs=5','--config_file=./../tests/cclass/{config_file}'.format(config_file=list_of_files[1]),'--asm_name={name}'.format(name=list_of_files2[1]),'--seed={gen_seed}'.format(gen_seed=seeds[1]),'--arch=rv64'])
    assert result.exit_code == 0

def aapg_cclass_v_bringup_s(runner):
    '''Testing aapg_cclass_v_bringup_s.yaml config file in parallel mode'''
    result = runner.invoke(cli, ['gen','--setup_dir=work','--output_dir=work1','--num_programs=5','--config_file=./../tests/cclass/{config_file}'.format(config_file=list_of_files[1]),'--asm_name={name}'.format(name=list_of_files2[1]),'--seed={gen_seed}'.format(gen_seed=seeds[1]),'--arch=rv64'])
    assert result.exit_code == 0

def aapg_cclass_rv64imc_bringup_s(runner):
    '''Testing aapg_cclass_rv64imc_bringup_s.yaml config file in parallel mode'''
    result = runner.invoke(cli, ['gen','--setup_dir=work','--output_dir=work1','--num_programs=5','--config_file=./../tests/cclass/{config_file}'.format(config_file=list_of_files[1]),'--asm_name={name}'.format(name=list_of_files2[1]),'--seed={gen_seed}'.format(gen_seed=seeds[1]),'--arch=rv64'])
    assert result.exit_code == 0

def aapg_cclass_rv64imafd_exceptions_u(runner):
    '''Testing aapg_cclass_rv64imafd_exceptions_u.yaml config file in parallel mode'''
    result = runner.invoke(cli, ['gen','--setup_dir=work','--output_dir=work1','--num_programs=5','--config_file=./../tests/cclass/{config_file}'.format(config_file=list_of_files[1]),'--asm_name={name}'.format(name=list_of_files2[1]),'--seed={gen_seed}'.format(gen_seed=seeds[1]),'--arch=rv64'])
    assert result.exit_code == 0