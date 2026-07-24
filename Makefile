.PHONY: \
	all \
	clean \
	edit \
	install \
	lab \
	lint \
	py \
	rename \
	run \
	test \

### Default target(s)
all: test run

sandbox: lint
	uv run src/hier/sandbox.py

### Edit files
edit:
	gvim -p src/hier/*.py

### Clean up generated files
clean:
	uv clean
	rm -fr .ruff_cache .venv

### Install this tool locally
install:
	uv tool install --upgrade .

### Run Jupyter lab
lab:
	JUPYTER_CONFIG_DIR=etc uv run jupyter lab --notebook-dir=etc/notebooks

### Perform static analysis
lint:
	uv run ruff check --select I --fix src test
	uv run ruff format src test
	uv run ruff check src test --fix
	uv run ty check src test

### Open a Python shell
py:
	PYTHONSTARTUP= uv run ipython --profile-dir=./etc/ipython

### Rename the project
rename:
	uv run etc/set_project_name.py

### Run unit tests
test: lint
	PYTHONBREAKPOINT="pudb.set_trace" uv run pytest -vv

### Run the project
run: lint
	uv run hier --version
	@echo ""
	@echo "================================================================================"
	@echo ""
	uv run hier --help
	@echo ""
	@echo "================================================================================"
	@echo ""
	uv run hier src
	@for sample in samples/*; do \
		echo ""; \
		echo "================================================================================"; \
		echo ""; \
		echo "$$sample"; \
		uv run hier $$sample; \
	done
