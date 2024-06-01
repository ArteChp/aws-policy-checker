
# Makefile for running unit tests and other tasks

.PHONY: help test clean coverage lint build docs

# Default target: show help
help:
	@echo "Usage:"
	@echo "  make init      - Install packages"
	@echo "  make test      - Run unit tests with pytest"
	@echo "  make clean     - Clean up generated files"
	@echo "  make coverage  - Run tests and generate coverage report"
	@echo "  make lint      - Check code style with flake8"
	@echo "  make build     - Build the project"
	@echo "  make docs      - Generate documentation"

init:
	pip install -r requirements.txt

# Run unit tests using pytest
test:
	python3 -m pytest tests

# Clean up generated files
clean:
	find . -type f -name '*.pyc' -delete
	find . -type d -name '__pycache__' -exec rm -r {} +
	rm -rf .pytest_cache .coverage htmlcov build dist *.egg-info

# Generate coverage report using pytest-cov
coverage:
	pytest --cov=code --cov-report=html

# Check code style using flake8
lint:
	flake8 code tests

# Build the project
build:
	python3 setup.py sdist bdist_wheel

# Generate documentation
docs:
	sphinx-build -b html docs/source docs/build
