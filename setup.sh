#!/bin/bash
set -e

echo "Setting up Sri Lanka Tourist Attractions app..."

# Create virtual environment with uv
uv venv .venv
echo "Virtual environment created at .venv"

# Activate and install dependencies
source .venv/bin/activate
uv pip install \
    "fastapi>=0.110.0" \
    "uvicorn[standard]>=0.27.0" \
    "sqlalchemy>=2.0.0" \
    "jinja2>=3.1.0" \
    "python-multipart>=0.0.9" \
    "bcrypt>=4.0.0" \
    "itsdangerous>=2.1.2"

# Create required directories
mkdir -p static/uploads
mkdir -p static/css

echo ""
echo "Setup complete!"
echo ""
echo "To start the app:"
echo "  source .venv/bin/activate"
echo "  uvicorn main:app --reload"
echo ""
echo "Then open http://localhost:8000 in your browser."
