# Contributing to Awesome UK Government Datasets

Thank you for your interest in contributing to the Awesome UK Government Datasets project! This document provides guidelines and instructions for contributing.

## Adding a New Dataset

1. Create a new YAML file in the appropriate topic folder (or create a new folder if needed).
2. Name the file using the dataset name in lowercase, replacing spaces with underscores (e.g., `population_estimates.yaml`).
3. Follow the YAML specification in `dataset-spec.yaml`.
4. Run the validation script to ensure your YAML file is correct:
   ```
   python validate_yaml.py
   ```
5. Commit and push your changes.
6. The GitHub Action will automatically update the README with your new dataset.

## Development Setup and Running Tests

We use a Makefile to manage our development processes. Here are the main commands you'll need:

1. Set up the development environment:
   ```
   make setup
   ```
   This creates a virtual environment and installs all necessary dependencies.

2. Individual commands:
   - Validate YAML files: `make validate`
   - Generate test README: `make readme`

4. Clean up generated files and virtual environment:
   ```
   make clean
   ```

Always run the full test suite before submitting a pull request:
```
make clean && make full-test
```

This ensures your changes pass all checks and tests.

## Questions?

If you have any questions or need further clarification, please open an issue in the repository.

Thank you for your contribution!