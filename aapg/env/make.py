makefile = '''
ASM_SRC_DIR := asm
COMMON_DIR := common
BIN_DIR := bin
OBJ_DIR := objdump
LOG_DIR := log

LINKER_SCRIPT := common/link.ld
INCLUDE_DIRS := common
CRT_FILE := common/crt.S
GCC_OPTS := -DPREALLOCATE=1 -mcmodel=medany -static -std=gnu99 -O2 -fno-common -fno-builtin-printf
LINKER_OPTIONS := -static -nostdlib -nostartfiles -lm -lgcc -T $(LINKER_SCRIPT)

SRC_FILES := $(wildcard $(ASM_SRC_DIR)/*.S)
BIN_FILES := $(patsubst $(ASM_SRC_DIR)/%.S, $(BIN_DIR)/%.riscv, $(SRC_FILES))
OBJ_FILES := $(patsubst $(ASM_SRC_DIR)/%.S, $(OBJ_DIR)/%.objdump, $(SRC_FILES))
LOG_FILES := $(patsubst $(ASM_SRC_DIR)/%.S, $(LOG_DIR)/%.log, $(SRC_FILES))

build: $(BIN_FILES)
\t$(info ==================== Build completed ====================)

$(BIN_DIR)/%.riscv: $(ASM_SRC_DIR)/%.S 
\triscv64-unknown-elf-gcc $(GCC_OPTS) -I $(INCLUDE_DIRS) -o $@ $< $(CRT_FILE) $(LINKER_OPTIONS)

objdump: $(OBJ_FILES)
\t$(info ==================== Objdump Completed ==================)

$(OBJ_DIR)/%.objdump: $(BIN_DIR)/%.riscv
\triscv64-unknown-elf-objdump -D $< > $@

run: $(LOG_FILES)
\t$(info ==================== Spike Run Completed ================)

$(LOG_DIR)/%.log: $(BIN_DIR)/%.riscv
\t spike -l $< 2> $@
clean: $(BIN_FILES)
\trm bin/*
\trm log/*
\trm objdump/*
'''
