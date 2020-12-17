import pytest 
import os
import random
import numpy as np
from random import seed
from random import randint
from click.testing import CliRunner
from aapg.main import cli


list_of_files = ['aapg_cclass_rv64imafdc_illegal.yaml', 'aapg_eclass_rv32imac_bringup.yaml', 'aapg_cclass_rv32ic_bringup.yaml', 'aapg_eclass_config.yaml', 'aapg_eclass_rv32imac_user.yaml', 'aapg_cclass_rv32imafc_bringup.yaml', 'aapg_cclass_config1.yaml', 'aapg_cclass_illegal.yaml', 'aapg_cclass_rv64imafdc_bringup.yaml', 'aapg_cclass_rv64imafdc_hazards.yaml', 'aapg_cclass_rv64imafdc_exceptions.yaml', 'aapg_eclass_rv32imac_exceptions_user.yaml', 'aapg_cclass_rv64imafd_exceptions.yaml', 'aapg_eclass_bringup.yaml', 'aapg_cclass_rv32imac_bringup.yaml', 'aapg_cclass_rv64imafd_bringup.yaml', 'aapg_cclass_exceptions.yaml', 'aapg_eclass_rv64imac_bringup.yaml', 'aapg_cclass_rv32imaf_bringup.yaml', 'aapg_eclass_rv32imac_exceptions.yaml', 'aapg_cclass_rv32imc_bringup.yaml', 'aapg_cclass_rv64imc_bringup.yaml', 'aapg_igcar_bringup.yaml', 'aapg_eclass_rv64imac_exceptions.yaml', 'aapg_cclass_rv64imafdc_branches1.yaml', 'aapg_eclass_config2.yaml', 'aapg_eclass_rv64imac_exceptions_user.yaml', 'aapg_cclass_v_bringup.yaml', 'aapg_cclass_rv64imafdc_user.yaml', 'aapg_cclass_rv64imac_bringup.yaml', 'aapg_cclass_rv64ic_bringup.yaml']
list_of_files2 = ['aapg_cclass_rv64imafdc_illegal', 'aapg_eclass_rv32imac_bringup', 'aapg_cclass_rv32ic_bringup', 'aapg_eclass_config', 'aapg_eclass_rv32imac_user', 'aapg_cclass_rv32imafc_bringup', 'aapg_cclass_config1', 'aapg_cclass_illegal', 'aapg_cclass_rv64imafdc_bringup', 'aapg_cclass_rv64imafdc_hazards', 'aapg_cclass_rv64imafdc_exceptions', 'aapg_eclass_rv32imac_exceptions_user', 'aapg_cclass_rv64imafd_exceptions', 'aapg_eclass_bringup', 'aapg_cclass_rv32imac_bringup', 'aapg_cclass_rv64imafd_bringup', 'aapg_cclass_exceptions', 'aapg_eclass_rv64imac_bringup', 'aapg_cclass_rv32imaf_bringup', 'aapg_eclass_rv32imac_exceptions', 'aapg_cclass_rv32imc_bringup', 'aapg_cclass_rv64imc_bringup', 'aapg_igcar_bringup', 'aapg_eclass_rv64imac_exceptions', 'aapg_cclass_rv64imafdc_branches1', 'aapg_eclass_config2', 'aapg_eclass_rv64imac_exceptions_user', 'aapg_cclass_v_bringup', 'aapg_cclass_rv64imafdc_user', 'aapg_cclass_rv64imac_bringup', 'aapg_cclass_rv64ic_bringup']

seeds = []
seed(1)
for _ in range(30):
    value = randint(0, 1000)
    seeds.append(value)

@pytest.fixture
def runner():
    return CliRunner()

def test_setup(runner):
    '''Testing setup option in serial mode'''
    result = runner.invoke(cli, ['setup','--setup_dir=work'])
    assert result.exit_code == 0

def test_aapg_eclass_rv32imac_bringup(runner):
    '''Testing aapg_eclass_rv32imac_bringup.yaml config file in parallel mode'''
    result = runner.invoke(cli, ['gen','--setup_dir=work','--output_dir=work1','--num_programs=5','--config_file=./../tests/shakti_yaml_configs/{config_file}'.format(config_file=list_of_files[1]),'--asm_name={name}'.format(name=list_of_files2[1]),'--seed={gen_seed}'.format(gen_seed=seeds[1]),'--arch=rv32'])
    assert result.exit_code == 0

def test_aapg_cclass_rv32ic_bringup(runner):
    '''Testing aapg_cclass_rv32ic_bringup.yaml config file in parallel mode'''
    result = runner.invoke(cli, ['gen','--setup_dir=work','--output_dir=work1','--num_programs=5','--config_file=./../tests/shakti_yaml_configs/{config_file}'.format(config_file=list_of_files[2]),'--asm_name={name}'.format(name=list_of_files2[2]),'--seed={gen_seed}'.format(gen_seed=seeds[2]),'--arch=rv32'])
    assert result.exit_code == 0

def test_aapg_eclass_config(runner):
    '''Testing aapg_eclass_config.yaml config file in parallel mode'''
    result = runner.invoke(cli, ['gen','--setup_dir=work','--output_dir=work1','--num_programs=5','--config_file=./../tests/shakti_yaml_configs/{config_file}'.format(config_file=list_of_files[3]),'--asm_name={name}'.format(name=list_of_files2[3]),'--seed={gen_seed}'.format(gen_seed=seeds[3])])
    assert result.exit_code == 0

def test_aapg_eclass_rv32imac_user(runner):
    '''Testing aapg_eclass_rv32imac_user.yaml config file in parallel mode'''
    result = runner.invoke(cli, ['gen','--setup_dir=work','--output_dir=work1','--num_programs=5','--config_file=./../tests/shakti_yaml_configs/{config_file}'.format(config_file=list_of_files[4]),'--asm_name={name}'.format(name=list_of_files2[4]),'--seed={gen_seed}'.format(gen_seed=seeds[4]),'--arch=rv32'])
    assert result.exit_code == 0

def test_aapg_cclass_rv32imafc_bringup(runner):
    '''Testing aapg_cclass_rv32imafc_bringup.yaml config file in parallel mode'''
    result = runner.invoke(cli, ['gen','--setup_dir=work','--output_dir=work1','--num_programs=5','--config_file=./../tests/shakti_yaml_configs/{config_file}'.format(config_file=list_of_files[5]),'--asm_name={name}'.format(name=list_of_files2[5]),'--seed={gen_seed}'.format(gen_seed=seeds[5]),'--arch=rv32'])
    assert result.exit_code == 0

def test_aapg_cclass_config1(runner):
    '''Testing aapg_cclass_config1.yaml config file in parallel mode'''
    result = runner.invoke(cli, ['gen','--setup_dir=work','--output_dir=work1','--num_programs=5','--config_file=./../tests/shakti_yaml_configs/{config_file}'.format(config_file=list_of_files[6]),'--asm_name={name}'.format(name=list_of_files2[6]),'--seed={gen_seed}'.format(gen_seed=seeds[6])])
    assert result.exit_code == 0

def test_aapg_cclass_rv64imafdc_bringup(runner):
    '''Testing aapg_cclass_rv64imafdc_bringup.yaml config file in parallel mode'''
    result = runner.invoke(cli, ['gen','--setup_dir=work','--output_dir=work1','--num_programs=5','--config_file=./../tests/shakti_yaml_configs/{config_file}'.format(config_file=list_of_files[8]),'--asm_name={name}'.format(name=list_of_files2[8]),'--seed={gen_seed}'.format(gen_seed=seeds[7])])
    assert result.exit_code == 0

def test_aapg_cclass_rv64imafdc_hazards(runner):
    '''Testing cclass_rv64imafdc_hazards.yaml config file in parallel mode'''
    result = runner.invoke(cli, ['gen','--setup_dir=work','--output_dir=work1','--num_programs=5','--config_file=./../tests/shakti_yaml_configs/{config_file}'.format(config_file=list_of_files[9]),'--asm_name={name}'.format(name=list_of_files2[9]),'--seed={gen_seed}'.format(gen_seed=seeds[8])])
    assert result.exit_code == 0

def test_aapg_cclass_rv64imafdc_exceptions(runner):
    '''Testing cclass_rv64imafdc_exceptions.yaml config file in parallel mode'''
    result = runner.invoke(cli, ['gen','--setup_dir=work','--output_dir=work1','--num_programs=5','--config_file=./../tests/shakti_yaml_configs/{config_file}'.format(config_file=list_of_files[10]),'--asm_name={name}'.format(name=list_of_files2[10]),'--seed={gen_seed}'.format(gen_seed=seeds[9])])
    assert result.exit_code == 0

def test_aapg_eclass_rv32imac_exceptions_user(runner):
    '''Testing aapg_eclass_rv32imac_exceptions_user.yaml config file in parallel mode'''
    result = runner.invoke(cli, ['gen','--setup_dir=work','--output_dir=work1','--num_programs=5','--config_file=./../tests/shakti_yaml_configs/{config_file}'.format(config_file=list_of_files[11]),'--asm_name={name}'.format(name=list_of_files2[11]),'--seed={gen_seed}'.format(gen_seed=seeds[10]),'--arch=rv32'])
    assert result.exit_code == 0

def test_aapg_cclass_rv64imafd_exceptions(runner):
    '''Testing aapg_cclass_rv64imafd_exceptions.yaml config file in parallel mode'''
    result = runner.invoke(cli, ['gen','--setup_dir=work','--output_dir=work1','--num_programs=5','--config_file=./../tests/shakti_yaml_configs/{config_file}'.format(config_file=list_of_files[12]),'--asm_name={name}'.format(name=list_of_files2[12]),'--seed={gen_seed}'.format(gen_seed=seeds[11])])
    assert result.exit_code == 0

def test_aapg_eclass_bringup(runner):
    '''Testing aapg_eclass_bringup.yaml config file in parallel mode'''
    result = runner.invoke(cli, ['gen','--setup_dir=work','--output_dir=work1','--num_programs=5','--config_file=./../tests/shakti_yaml_configs/{config_file}'.format(config_file=list_of_files[13]),'--asm_name={name}'.format(name=list_of_files2[13]),'--seed={gen_seed}'.format(gen_seed=seeds[12])])
    assert result.exit_code == 0

def test_aapg_cclass_rv32imac_bringup(runner):
    '''Testing aapg_cclass_rv32imac_bringup.yaml config file in parallel mode'''
    result = runner.invoke(cli, ['gen','--setup_dir=work','--output_dir=work1','--num_programs=5','--config_file=./../tests/shakti_yaml_configs/{config_file}'.format(config_file=list_of_files[14]),'--asm_name={name}'.format(name=list_of_files2[14]),'--seed={gen_seed}'.format(gen_seed=seeds[13]),'--arch=rv32'])
    assert result.exit_code == 0

def test_aapg_cclass_rv64imafd_bringup(runner):
    '''Testing aapg_cclass_rv64imafd_bringup.yaml config file in parallel mode'''
    result = runner.invoke(cli, ['gen','--setup_dir=work','--output_dir=work1','--num_programs=5','--config_file=./../tests/shakti_yaml_configs/{config_file}'.format(config_file=list_of_files[15]),'--asm_name={name}'.format(name=list_of_files2[15]),'--seed={gen_seed}'.format(gen_seed=seeds[14])])
    assert result.exit_code == 0





