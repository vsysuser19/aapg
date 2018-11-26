XLEN ?= 64
TARGET ?= unknown-elf
RISCVPREFIX=riscv${XLEN}-${TARGET}
ASM_SRC_DIR := asm
COMMON_DIR := common
BIN_DIR := bin
OBJ_DIR := objdump
LOG_DIR := log
ISA ?= rv64imafd
ABI ?= lp64

LINKER_SCRIPT := common/link.ld
INCLUDE_DIRS := common
CRT_FILE := common/crt.S
TEMPLATE_FILE := common/templates.S
GCC_OPTS := -march=$(ISA) -mabi=$(ABI) -DPREALLOCATE=1 -mcmodel=medany -static -std=gnu99 -O2 -fno-common -fno-builtin-printf
LINKER_OPTIONS := -static -nostdlib -nostartfiles -lm -lgcc -T $(LINKER_SCRIPT)

SRC_FILES := $(wildcard $(ASM_SRC_DIR)/*.S)
BIN_FILES := $(patsubst $(ASM_SRC_DIR)/%.S, $(BIN_DIR)/%.riscv, $(SRC_FILES))
OBJ_FILES := $(patsubst $(ASM_SRC_DIR)/%.S, $(OBJ_DIR)/%.objdump, $(SRC_FILES))
LOG_FILES := $(patsubst $(ASM_SRC_DIR)/%.S, $(LOG_DIR)/%.log, $(SRC_FILES))


all: build objdump run
	$(info ==================== Complete Build Finished =============)

build: $(BIN_FILES)
	$(info ==================== Build completed ====================)
	$(info )

$(BIN_DIR)/%.riscv: $(ASM_SRC_DIR)/%.S 
	$(info ==================== Compiling asm to binary ============)
	${RISCVPREFIX}-gcc $(GCC_OPTS) -I $(INCLUDE_DIRS) -o $@ $< $(CRT_FILE) $(LINKER_OPTIONS)

objdump: $(OBJ_FILES)
	$(info ==================== Objdump Completed ==================)
	$(info )

$(OBJ_DIR)/%.objdump: $(BIN_DIR)/%.riscv
	$(info ==================== Disassembling binary ===============)
	${RISCVPREFIX}-objdump -D $< > $@

run: $(LOG_FILES)
	$(info ==================== Spike Run Completed ================)
	$(info )

$(LOG_DIR)/%.log: $(BIN_DIR)/%.riscv
	$(info ==================== Simulating binary on Spike =========)
	 spike -l $< 2> $@


.PHONY: clean
clean:
	rm bin/*
	rm log/*
	rm objdump/*
