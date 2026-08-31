PYTHON = maze_env/bin/python3
PIP = maze_env/bin/pip
FLAKE8 = maze_env/bin/flake8
MYPY = maze_env/bin/mypy
PROJECT = mazegen/maze_generator.py \
		  a_maze_ing.py \
		  config_parser.py \
		  maze_display.py \

# Chemins pour le vendoring des librairies locales
LOCAL_LIBS_DIR = $(CURDIR)/libs
LOCAL_INCLUDE = $(LOCAL_LIBS_DIR)/usr/include
LOCAL_LIB_PATH = $(LOCAL_LIBS_DIR)/usr/lib/x86_64-linux-gnu

all: install mlx run

install:
	python3 -m venv maze_env
	$(PIP) install --upgrade pip
	$(PIP) install flake8 mypy pytest
	@echo "--------------------------------------------------"
	@echo "Python environment ready!"
	@echo "--------------------------------------------------"

mlx-download:
	@if [ "$$(uname -s)" = "Darwin" ]; then \
		if [ ! -d "mlx" ]; then \
			echo "Cloning MLX repository..."; \
			git clone https://github.com/42school/mlx_CLXV.git mlx; \
		else \
			echo "MLX repository already exists, skipping clone."; \
		fi \
	else \
		echo "Linux detected : mlx cloning ignored."; \
	fi

mlx: mlx-download
	@if [ "$$(uname -s)" = "Darwin" ]; then \
		echo "Configuring and compiling MLX for macOS..."; \
		$(MAKE) -C mlx BACKEND=appkit; \
		$(PIP) install mlx/mlx-*.whl --force-reinstall; \
	else \
		if ! ls mlx-*.whl > /dev/null 2>&1; then \
			echo "Error: mlx-*.whl cannot be found."; \
			echo "For school computers (Ubuntu 22.04 LTS), download the precompiled wheel from the project ressources on the intra and put it at the root of the project directory."; \
			exit 1; \
		fi; \
		echo "Installation of the precompiled mlx wheel for Linux..."; \
		$(PIP) install mlx-*.whl --force-reinstall; \
	fi

run:
	@if [ "$$(uname -s)" = "Linux" ]; then \
		LD_LIBRARY_PATH="$(LOCAL_LIB_PATH)" $(PYTHON) a_maze_ing.py config.txt; \
	else \
		$(PYTHON) a_maze_ing.py config.txt; \
	fi

debug:
	@if [ "$$(uname -s)" = "Linux" ]; then \
		LD_LIBRARY_PATH="$(LOCAL_LIB_PATH)" $(PYTHON) -m pdb a_maze_ing.py config.txt; \
	else \
		$(PYTHON) -m pdb a_maze_ing.py config.txt; \
	fi

clean:
	rm -rf mazegen/__pycache__ __pycache__ .mypy_cache src/__pycache__ $(LOCAL_LIBS_DIR) 
	@if [ -d "mlx" ]; then cd mlx && $(MAKE) clean; fi

fclean: clean
	rm -rf mlx maze_env

lint:
	$(FLAKE8) $(PROJECT)
	$(MYPY) --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs $(PROJECT)

lint-strict:
	$(FLAKE8) $(PROJECT)
	$(MYPY) --strict $(PROJECT)

re: fclean all

.PHONY: all install mlx-download mlx run debug clean fclean lint lint-strict