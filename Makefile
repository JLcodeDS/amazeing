PYTHON = maze_env/bin/python3
PIP = maze_env/bin/pip
FLAKE8 = maze_env/bin/flake8
MYPY = maze_env/bin/mypy

all: install

install:
	python3 -m venv maze_env
	$(PIP) install --upgrade pip
	$(PIP) install flake8 mypy
	@echo "--------------------------------------------------"
	@echo "Python environment ready!"
	@echo "Run 'cd mlx && ./configure.sh' if not done"
	@echo "then write 'make mlx' to compile MLX."
	@echo "--------------------------------------------------"

mlx:
	cd mlx && make
	$(PIP) install mlx/mlx-*.whl

run:
	$(PYTHON) a_maze_ing.py config.txt

debug:
	$(PYTHON) -m pdb a_maze_ing.py config.txt

clean:
	rm -rf maze_env __pycache__ .mypy_cache src/__pycache__
	cd mlx && make clean

lint:
	$(FLAKE8) .
	$(MYPY) --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs .

lint-strict:
	$(FLAKE8) .
	$(MYPY) --strict .

.PHONY: all install mlx run debug clean lint lint-strict