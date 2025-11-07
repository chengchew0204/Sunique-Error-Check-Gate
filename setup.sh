#!/bin/bash

# Setup script for InFlow Error Check Gate

echo "Setting up InFlow Error Check Gate..."

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Create logs directory if it doesn't exist
echo "Creating logs directory..."
mkdir -p logs

# Check if .env file exists
if [ ! -f .env ]; then
    echo "Creating .env file from .env.example..."
    if [ -f .env.example ]; then
        cp .env.example .env
        echo "Please edit .env file with your configuration."
    else
        echo "Warning: .env.example not found. Please create .env file manually."
    fi
else
    echo ".env file already exists."
fi

echo ""
echo "Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env file with your API credentials"
echo "2. Run: source venv/bin/activate"
echo "3. Run: python app/main.py"
echo "4. In another terminal, run: ngrok http 8000"
echo "5. Subscribe to InFlow webhooks using the ngrok URL"
echo ""

