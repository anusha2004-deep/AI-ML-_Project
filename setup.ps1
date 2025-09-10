# AI Microservices Setup Script for Windows

Write-Host "Setting up AI Microservices project..." -ForegroundColor Green

# Backend setup
Write-Host "Setting up backend..." -ForegroundColor Yellow
Set-Location backend

# Create virtual environment if it doesn't exist
if (-not (Test-Path "venv")) {
    Write-Host "Creating Python virtual environment..." -ForegroundColor Blue
    python -m venv venv
}

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Blue
& "venv\Scripts\Activate.ps1"

# Install Python dependencies
Write-Host "Installing Python dependencies..." -ForegroundColor Blue
pip install -r requirements.txt

# Setup environment file
if (-not (Test-Path ".env")) {
    Write-Host "Creating environment file..." -ForegroundColor Blue
    Copy-Item ".env.example" ".env"
    Write-Host "Please edit .env file with your API keys and configuration" -ForegroundColor Magenta
}

# Create uploads directory
if (-not (Test-Path "uploads")) {
    New-Item -ItemType Directory -Path "uploads"
}

Set-Location ..

# Frontend setup
Write-Host "Setting up frontend..." -ForegroundColor Yellow
Set-Location frontend

# Install Node.js dependencies
Write-Host "Installing Node.js dependencies..." -ForegroundColor Blue
npm install

Set-Location ..

Write-Host ""
Write-Host "Setup complete! Next steps:" -ForegroundColor Green
Write-Host ""
Write-Host "1. Backend:" -ForegroundColor Yellow
Write-Host "   - Edit backend\.env with your configuration"
Write-Host "   - Install and start Ollama (optional): https://ollama.ai/"
Write-Host "   - Start backend: cd backend && python main.py"
Write-Host ""
Write-Host "2. Frontend:" -ForegroundColor Yellow
Write-Host "   - Start frontend: cd frontend && npm run dev"
Write-Host ""
Write-Host "3. Access the application:" -ForegroundColor Yellow
Write-Host "   - API: http://localhost:8000"
Write-Host "   - Frontend: http://localhost:3000"
Write-Host "   - API Docs: http://localhost:8000/docs"
Write-Host ""
Write-Host "For Ollama setup, run: .\backend\setup_ollama.ps1" -ForegroundColor Cyan