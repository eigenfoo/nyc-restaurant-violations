.PHONY: help venv check-docstyle check-format check-style format lint
.DEFAULT_GOAL = help

PROJECT_DIR = src/
PYTHON = python
PIP = pip
CONDA = conda
SHELL = bash

help:
	@printf "Usage:\n"
	@grep -E '^[a-zA-Z_-]+:.*?# .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?# "}; {printf "\033[1;34mmake %-10s\033[0m%s\n", $$1, $$2}'

venv:  # Set up a Python virtual environment for development.
	@printf "Creating Python virtual environment...\n"
	rm -rf venv
	${PYTHON} -m venv venv
	( \
	source venv/bin/activate; \
	${PIP} install -U pip; \
	${PIP} install -r requirements.txt; \
	deactivate; \
	)
	@printf "\n\nVirtual environment created! \033[1;34mRun \`source venv/bin/activate\` to activate it.\033[0m\n\n\n"

check-docstyle:
	@printf "Checking documentation style...\n"
	pydocstyle ${PROJECT_DIR}
	@printf "\033[1;34mDocumentation style passes!\033[0m\n\n"

check-format:
	@printf "Checking code format...\n"
	black -t py36 --check ${PROJECT_DIR} tests/ setup.py conftest.py; \
  isort --check ${PROJECT_DIR} tests/ setup.py conftest.py;
	@printf "\033[1;34mFormatting passes!\033[0m\n\n"

check-style:
	@printf "Checking code style...\n"
	flake8
	@printf "\033[1;34mCode style passes!\033[0m\n\n"

format:  # Format code in-place using black.
	black ${PROJECT_DIR} tests/ setup.py conftest.py; \
  isort ${PROJECT_DIR} tests/ setup.py conftest.py;

lint: check-format check-style check-docstyle
