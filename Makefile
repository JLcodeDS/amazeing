PYTHON = maze_env/bin/python3
PIP = maze_env/bin/pip
FLAKE8 = maze_env/bin/flake8
MYPY = maze_env/bin/mypy

# Chemins pour le vendoring des librairies locales
LOCAL_LIBS_DIR = $(CURDIR)/libs
LOCAL_INCLUDE = $(LOCAL_LIBS_DIR)/usr/include
LOCAL_LIB_PATH = $(LOCAL_LIBS_DIR)/usr/lib/x86_64-linux-gnu

all: install mlx

install:
	python3 -m venv maze_env
	$(PIP) install --upgrade pip
	$(PIP) install flake8 mypy
	@echo "--------------------------------------------------"
	@echo "Python environment ready!"
	@echo "--------------------------------------------------"

mlx-download:
	@if [ ! -d "mlx" ]; then \
		echo "Cloning MLX repository..."; \
		git clone https://github.com/42school/mlx_CLXV.git mlx; \
	else \
		echo "MLX repository already exists, skipping clone."; \
	fi

vendor-libs:
	@if [ "$$(uname -s)" = "Linux" ]; then \
		echo "Downloading local X11 libraries for Linux..."; \
		mkdir -p $(LOCAL_LIBS_DIR); \
		cd $(LOCAL_LIBS_DIR) && apt download libxcb-keysyms1 libxcb-keysyms1-dev; \
		cd $(LOCAL_LIBS_DIR) && dpkg -x libxcb-keysyms1_*.deb .; \
		cd $(LOCAL_LIBS_DIR) && dpkg -x libxcb-keysyms1-dev_*.deb .; \
		cd $(LOCAL_LIBS_DIR) && rm -f *.deb; \
		echo "Local libraries ready in $(LOCAL_LIBS_DIR)"; \
	else \
		echo "Running on macOS, skipping local Linux libraries extraction."; \
	fi

mlx: mlx-download vendor-libs
	@if [ "$$(uname -s)" = "Linux" ]; then \
		echo "Configuring and compiling MLX with local X11 libraries..."; \
		cd mlx && export C_INCLUDE_PATH="$(LOCAL_INCLUDE)" && export LIBRARY_PATH="$(LOCAL_LIB_PATH)" && $(MAKE) BACKEND=xcb; \
	else \
		echo "Configuring and compiling MLX for macOS..."; \
		cd mlx && $(MAKE); \
	fi
	$(PIP) install mlx/mlx-*.whl --force-reinstall

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
	rm -rf maze_env __pycache__ .mypy_cache src/__pycache__ $(LOCAL_LIBS_DIR)
	@if [ -d "mlx" ]; then cd mlx && $(MAKE) clean; fi

fclean: clean
	rm -rf mlx

lint:
	$(FLAKE8) .
	$(MYPY) --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs .

lint-strict:
	$(FLAKE8) .
	$(MYPY) --strict .

.PHONY: all install mlx-download vendor-libs mlx run debug clean fclean lint lint-strict