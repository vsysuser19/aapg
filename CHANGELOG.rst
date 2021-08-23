CHANGELOG
=========

This project adheres to `Semantic Versioning <https://semver.org/spec/v2.0.0.html>`_.

[2.2.6] - 2021-08-23
  - Encapsulating RVTEST_FPENABLE macro in templates under `#ifdef __riscv_flen`

[2.2.5] - 2021-08-15
  - Fixed alignment of `1f` label after floating point init code to 4 bytes.
  - Moved changelog to rst format
  - fixed ci to automatically deploy tags
  - fixed setup.cfg for bumpversion usage
  - removed stale `__version__.py` file.

[2.2.4] - 2021-07-28
  - Ecause02 perl script generated .word and .half based on opcode
  - Replace 0x0 with 0xff as the default illegal opcode
  - Update Custom Trap handler to check inst size even for illegal

[2.2.3] - 2021-07-19
  - Ecause02 perl script not generating illegal instructions

[2.2.2] - 2021-05-06
  - User function grouping at end of test
  - Switching Modes and Self Checking set to be mutually exclusive

[2.2.1] - 2021-04-26
  - Test master runner tag  

[2.2.0] - 2021-04-22
  - Support for self checking test  
  - Support for dynamic ISA and MARCH in makefile based on config  

[2.1.2] - 2021-03-23
  - custom_trap_handler forced to begin at 4 boundary as required by the spec

[2.1.1] - 2021-02-23
  - tohost alignment issue  
  - Support for multiple tests in CI/CD runner

[2.1.0] - 2021-02-19
  - Support for delegation  
  - Support for Floating point rounding modes

[2.0.0] - 2021-02-13
  - Support for test entry privledge mode  
  - Support for Switching Privledge modes
  - Support for CSR access Sections
  - Dynamic random ecause value generation    
  - Exception and Program macro definition support in config file  
  - Branch Block size in Branch Control Section  

[1.0.2] - 2019-12-18
  - version

[1.0.1] - 2019-12-17
  - ci yaml change to not have old configs

[1.0.0] - 2019-12-17
  - aapg with yaml configs
