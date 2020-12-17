#!/usr/bin/env python
# coding: utf-8

# In[18]:


import os
import re


# In[2]:


os.system('aapg setup')


# In[ ]:



with os.scandir('cclass/') as entries:         
         for entry in entries:
            config_file = str(entry.name)
            print(config_file)
            config_file = 'cclass/'+config_file
            os.system(' cp $config_file work/config.yaml')
            os.system(' aapg gen')
            os.system(' cd work; riscv64-unknown-elf-gcc -march=rv64imafd -mabi=lp64 -DPREALLOCATE=1 -mcmodel=medany -static -std=gnu99 -O2 -fno-common -fno-builtin-printf -I common -o bin/out_00000.riscv asm/out_config_00000.S common/crt.S -static -nostdlib -nostartfiles -lm -lgcc -T asm/out_config_00000.ld')
            os.system(' cd work; spike -l --isa=rv64imafd bin/out_00000.riscv 2> log/out_00000.log')
            os.system(' head -n 200 work/log/out_00000.log')
            
    
        


# In[ ]:




