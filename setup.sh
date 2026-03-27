#!/bin/bash

echo ""
echo "========================================="
echo "   FactoryLink Setup Script"
echo "========================================="
echo ""

# Check Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed."
    echo "Please install it from https://www.python.org/downloads/"
    exit 1
fi

echo "Found Python: $(python3 --version)"
echo ""

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv myvenv

# Activate it
echo "Activating virtual environment..."
source myvenv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt -q

# Create .env file
echo "Creating .env file..."
cat > .env << 'ENVFILE'
DATABASE_URL=postgresql://neondb_owner:npg_ARlY7QfNJu3I@ep-fancy-feather-agfppv25-pooler.c-2.eu-central-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require
SECRET_KEY=LbfSwTI7LleizG0Q6hkZcC6RpUOeby0h3CaANQ22edS
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
ENVFILE

echo ""
echo "========================================="
echo "   Setup complete!"
echo "========================================="
echo ""
echo "   Admin login:"
echo "   Email:    admin@factorylink.com"
echo "   Password: admin123"
echo ""

read -p "   Start the server now? (y/n): " answer
if [ "$answer" = "y" ] || [ "$answer" = "Y" ]; then
    echo ""
    echo "Starting server..."
    echo "Open your browser at: http://localhost:8000"
    echo "Press CTRL+C to stop"
    echo ""
    uvicorn main:app --reload
else
    echo ""
    echo "   To start later, run:"
    echo "   source myvenv/bin/activate"
    echo "   uvicorn main:app --reload"
    echo ""
    echo "   Then open: http://localhost:8000"
    echo ""
fi
