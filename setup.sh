#!/bin/bash

echo ""
echo "========================================="
echo "   FactoryLink Setup Script"
echo "========================================="
echo ""

# Install uv if not already installed
if ! command -v uv &> /dev/null; then
    echo "Installing uv (Python package manager)..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    # Add uv to PATH for this session
    export PATH="$HOME/.cargo/bin:$HOME/.local/bin:$PATH"
    echo "uv installed successfully."
else
    echo "uv already installed: $(uv --version)"
fi

echo ""

# Create .env file
echo "Creating .env file..."
cat > .env << 'ENVFILE'
DATABASE_URL=postgresql://neondb_owner:npg_ARlY7QfNJu3I@ep-fancy-feather-agfppv25-pooler.c-2.eu-central-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require
SECRET_KEY=LbfSwTI7LleizG0Q6hkZcC6RpUOeby0h3CaANQ22edS
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
ENVFILE

# Install Python 3.12 and all dependencies automatically
echo "Installing Python 3.12 and dependencies..."
echo "(This may take a minute on first run)"
uv sync

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
    uv run uvicorn main:app --reload
else
    echo ""
    echo "   To start later, run:"
    echo "   uv run uvicorn main:app --reload"
    echo ""
    echo "   Then open: http://localhost:8000"
    echo ""
fi
