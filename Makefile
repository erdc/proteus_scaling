PLUNGING_SYSTEMS := $(wildcard systems/plunging_breakers/plunging_breakers_twp_navier_stokes_p_L_*)

NP := 16

all: results/plunging_superlu_log.txt results/plunging_asm_log.txt results/plunging_fieldsplit_asm_log.txt figures

figures: figures/marin_comparison.png figures/plunging_comparison.png

results/plunging_superlu_log.txt: $(PLUNGING_SYSTEMS) code/test_mat.py solvers/proteus_superlu.options
	@echo "plunging breakers in superlu"
	@mkdir -p results
	mpirun -np $(NP) python code/test_mat.py $(PLUNGING_SYSTEMS) -options_file solvers/proteus_superlu.options > results/plunging_superlu_log.txt

results/plunging_asm_log.txt: $(PLUNGING_SYSTEMS) code/test_mat.py solvers/proteus_asm.options
	@echo "plunging breakers in asm"
	@mkdir -p results
	mpirun -np $(NP) python code/test_mat.py $(PLUNGING_SYSTEMS) -options_file solvers/proteus_asm.options > results/plunging_asm_log.txt

results/plunging_fieldsplit_asm_log.txt: $(PLUNGING_SYSTEMS) code/test_mat.py solvers/fieldsplit_asm.options
	@echo "plunging breakers with fieldsplit asm"
	@mkdir -p results
	mpirun -np $(NP) python code/test_mat.py $(PLUNGING_SYSTEMS) -options_file solvers/fieldsplit_asm.options > results/plunging_fieldsplit_asm_log.txt

figures/marin_comparison.png figures/plunging_comparison.png: results/plunging_fieldsplit_asm_log.txt results/plunging_asm_log.txt results/marin_fieldsplit_asm_log.txt results/marin_proteus_asm_log.txt code/generate_figures.py
	@echo "creating marin and plunging comparison plots"
	@mkdir -p figures
	python code/generate_figures.py
