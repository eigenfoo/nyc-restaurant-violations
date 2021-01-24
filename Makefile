.PHONY: help venv lint format clean
.DEFAULT_GOAL = help

PROJECT_FILES = *.py
PYTHON = python
PIP = pip

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

lint:
	@printf "Checking code format...\n"
	black -t py36 --check ${PROJECT_FILES}
	isort --check ${PROJECT_FILES}
	@printf "\033[1;34mFormatting passes!\033[0m\n\n"

format:  # Format code in-place using black.
	black ${PROJECT_FILES}
	isort ${PROJECT_FILES}

clean:  # Clean project directories.
	rm -rf dist/ site/ pip-wheel-metadata/ __pycache__/ testing-report.html coverage.xml
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name "__pycache__" -delete
	find . -type f -name "*.pyc" -delete
