#!/bin/bash

echo "Setting up AI Microservices project..."

# Backend setup
echo "Setting up backend..."
cd backend

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Setup environment file
if [ ! -f ".env" ]; then
    echo "Creating environment file..."
    cp .env.example .env
    echo "Please edit .env file with your API keys and configuration"
fi

# Create uploads directory
mkdir -p uploads

cd ..

# Frontend setup
echo "Setting up frontend..."
cd frontend

# Install Node.js dependencies
echo "Installing Node.js dependencies..."
npm install

cd ..

echo ""
echo "Setup complete! Next steps:"
echo ""
echo "1. Backend:"
echo "   - Edit backend/.env with your configuration"
echo "   - Install and start Ollama (optional): https://ollama.ai/"
echo "   - Start backend: cd backend && python main.py"
echo ""
echo "2. Frontend:"
echo "   - Start frontend: cd frontend && npm run dev"
echo ""
echo "3. Access the application:"
echo "   - API: http://localhost:8000"
echo "   - Frontend: http://localhost:3000"
echo "   - API Docs: http://localhost:8000/docs"
echo ""
echo "For Ollama setup, run: ./backend/setup_ollama.sh"