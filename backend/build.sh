#!/bin/bash
# Build script for Render deployment
# Installs setuptools and wheel before installing requirements

set -e  # Exit on error

echo "Upgrading pip..."
python -m pip install --upgrade pip

echo "Installing base requirements (setuptools, wheel)..."
pip install -r requirements-base.txt

echo "Installing requirements..."
pip install -r requirements.txt

echo "Build completed successfully!"

