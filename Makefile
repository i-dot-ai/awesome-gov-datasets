# Python version and virtual environment
PYTHON := python3
VENV := venv
VENV_BIN := $(VENV)/bin

# Activate the virtual environment for each rule
# Detect the operating system
ifeq ($(OS),Windows_NT)
    ACTIVATE := $(VENV)\Scripts\activate
else
    ACTIVATE := . $(VENV_BIN)/activate
endif

# Phony targets
.PHONY: all setup validate readme clean

# Default target
all: setup validate readme clean

# Set up the virtual environment and install dependencies
setup:
	@echo "Setting up virtual environment..."
	@$(PYTHON) -m venv $(VENV)
	@$(ACTIVATE) && pip install --upgrade pip
	@$(ACTIVATE) && pip install -r requirements.txt

# Validate YAML files
validate:
	@echo "Validating YAML files..."
	@$(ACTIVATE) && python scripts/validate_yaml.py

# Generate test README
readme:
	@echo "Generating test README..."
	@$(ACTIVATE) && python scripts/generate_readme.py --output README_test.md

# Clean up generated files and virtual environment
clean:
	@echo "Cleaning up..."
	@rm -rf $(VENV) README_test.md
	@find . -type f -name '*.pyc' -delete
	@find . -type d -name '__pycache__' -delete

# Full test suite
full-test: setup validate readme
	@echo "Full test suite completed."