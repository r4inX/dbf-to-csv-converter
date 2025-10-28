# Contributing to DBF to CSV Converter

We love your input! We want to make contributing as easy and transparent as possible.

## Development Process

1. **Fork the repo** and create your branch from `master`
2. **Install development dependencies**: `pip install -r requirements-dev.txt`
3. **Make your changes**
4. **Add tests** for your changes
5. **Run the test suite**: `pytest`
6. **Ensure code quality**: `black dbf2csv.py && flake8 dbf2csv.py`
7. **Commit your changes** with a clear commit message
8. **Push to your fork** and submit a pull request

## Setting Up Development Environment

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/dbf-to-csv-converter.git
cd dbf-to-csv-converter

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Install pre-commit hooks (optional but recommended)
pre-commit install
```

## Running Tests

```bash
# Run all tests
pytest

# Run tests with coverage
pytest --cov=dbf2csv

# Run specific test file
pytest tests/test_dbf2csv.py

# Run with verbose output
pytest -v
```

## Code Style

We use several tools to maintain code quality:

- **Black** for code formatting
- **flake8** for linting
- **isort** for import sorting
- **mypy** for type checking (optional)

```bash
# Format code
black dbf2csv.py check_csv.py test_encoding.py

# Check formatting
black --check dbf2csv.py

# Lint code
flake8 dbf2csv.py

# Sort imports
isort dbf2csv.py

# Type checking
mypy dbf2csv.py --ignore-missing-imports
```

## Testing Guidelines

- Write tests for all new functionality
- Ensure existing tests still pass
- Include edge cases and error conditions
- Test with different Python versions locally if possible
- Mock external dependencies (like actual DBF files) in unit tests

## Pull Request Process

1. **Update documentation** if you're changing functionality
2. **Add tests** for new features or bug fixes
3. **Ensure all tests pass** locally
4. **Update the README.md** if needed
5. **Write a clear PR description** explaining your changes
6. **Link to any related issues**

## Bug Reports

When filing an issue, please include:

- **Python version** and operating system
- **Complete error message** and stack trace
- **Steps to reproduce** the issue
- **Sample input file** (if possible, without sensitive data)
- **Expected vs actual behavior**

## Feature Requests

We welcome feature requests! Please:

- **Check existing issues** to avoid duplicates
- **Clearly describe the use case** and problem you're solving
- **Provide examples** of how the feature would be used
- **Consider backwards compatibility**

## Code of Conduct

This project follows the [Contributor Covenant Code of Conduct](https://www.contributor-covenant.org/version/2/1/code_of_conduct/).

## Questions?

Feel free to open an issue with the "question" label if you need help or clarification on anything!