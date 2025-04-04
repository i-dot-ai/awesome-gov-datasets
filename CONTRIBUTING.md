# Contributing to Awesome UK Government Datasets

Thank you for your interest in contributing to the Awesome UK Government Datasets project! This document provides guidelines and instructions for contributing.

## Accepting a Dataset

Rather than attempting to catalog every available government dataset, the aim is to carefully select the most valuable and accessible ones that serve the needs of most users. Our focus is on quality over quantity, ensuring that each dataset included here offers meaningful value for analysis, research, or application development. As such, while we welcome submissions, we maintain selective criteria for including new datasets to preserve the collection's utility and manageability. If you are unsure, we recommend opening an issue to check if a dataset is suitable before making a PR.

## Adding a New Dataset

1. Install the necessary dependencies: `make setup`
2. Create a new YAML file in the appropriate `datasets/` topic folder (or create a new topic folder if needed).
3. Name the file using the dataset name in lowercase, replacing spaces with underscores (e.g., `population_estimates.yaml`).
4. Follow the YAML specification in `dataset-spec.yaml`.
5. Run the validation script to ensure your YAML file is correct: `make validate`
6. Run the script to build a test version of the README: `make readme`
7. Commit and push your changes to your branch.
8. Open a pull request to merge your changes into the main branch.
8. The GitHub Action will automatically update the README with your new dataset when your pull request has changes.

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
