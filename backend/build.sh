#!/bin/bash
# Build script for Render deployment
# Installs setuptools and wheel before installing requirements

set -e  # Exit on error

echo "=== Starting build process ==="
echo "Python version: $(python --version)"
echo "Pip version: $(pip --version)"

echo "=== Upgrading pip and installing build tools ==="
python -m pip install --upgrade pip
pip install --upgrade 'setuptools>=69.0.0' 'wheel>=0.43.0' --no-cache-dir

echo "=== Verifying setuptools installation ==="
python -c "import setuptools; print(f'setuptools version: {setuptools.__version__}')" || {
    echo "ERROR: setuptools not available!"
    exit 1
}

echo "=== Installing requirements ==="
pip install -r requirements.txt --no-cache-dir

echo "=== Build completed successfully ==="

