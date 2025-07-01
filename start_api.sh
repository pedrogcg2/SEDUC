#!/bin/bash
# SEDUC API Startup Script

echo "Starting SEDUC API..."
echo "Make sure your PostgreSQL database is running and configured."

# Check if virtual environment exists
if [ -d "venv" ]; then
    echo "Activating virtual environment..."
    source venv/bin/activate
fi

# Run the API
python run.py 