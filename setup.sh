#!/bin/bash

# Exit on error
set -e

echo "Setting up development environment..."

# Create Python virtual environment if it doesn't exist
if [ ! -d "api/.venv" ]; then
    echo "Creating Python virtual environment..."
    cd api
    python -m venv .venv
    cd ..
fi

# Activate virtual environment
source api/.venv/bin/activate

# Install Python development dependencies
echo "Installing Python development dependencies..."
pip install black flake8 pre-commit

# Install pre-commit hooks
echo "Installing pre-commit hooks..."
pre-commit install

echo "Setup complete! You can now use:"
echo "  - black: for Python code formatting"
echo "  - flake8: for Python code linting"
echo "  - pre-commit: hooks will run automatically on commit"