# Deployment Guide

This guide covers different deployment options for the AI Microservices application.

## 🚀 Quick Start (Development)

### Prerequisites
- Python 3.8+
- Node.js 16+
- Git

### 1. Automated Setup
Run the setup script for your platform:

**Windows (PowerShell):**
```powershell
.\setup.ps1
```

**Linux/Mac:**
```bash
chmod +x setup.sh
./setup.sh
```

### 2. Manual Setup

#### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows

pip install -r requirements.txt
cp .env.example .env
# Edit .env with your configuration
```

#### Frontend
```bash
cd frontend
npm install
```

### 3. Start Services

**Terminal 1 - Backend:**
```bash
cd backend
python main.py
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

**Terminal 3 - Test (Optional):**
```bash
python test_api.py
```

## 🐳 Docker Deployment

### Option 1: Docker Compose (Recommended)

Create `docker-compose.yml`:
```yaml
version: '3.8'

services:
  backend:
    build: 
      context: ./backend
      dockerfile: Dockerfile
    ports:
      - "8000:8000"
    environment:
      - OLLAMA_BASE_URL=http://ollama:11434
    volumes:
      - ./backend/uploads:/app/uploads
    depends_on:
      - ollama

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    ports:
      - "3000:3000"
    depends_on:
      - backend

  ollama:
    image: ollama/ollama:latest
    ports:
      - "11434:11434"
    volumes:
      - ollama_data:/root/.ollama
    command: serve

volumes:
  ollama_data:
```

Create `backend/Dockerfile`:
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p uploads

EXPOSE 8000

CMD ["python", "main.py"]
```

Create `frontend/Dockerfile`:
```dockerfile
FROM node:16-alpine as build

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 3000

CMD ["nginx", "-g", "daemon off;"]
```

Deploy:
```bash
docker-compose up -d
```

### Option 2: Individual Docker Containers

**Backend:**
```bash
cd backend
docker build -t ai-microservices-backend .
docker run -p 8000:8000 -v $(pwd)/uploads:/app/uploads ai-microservices-backend
```

**Frontend:**
```bash
cd frontend
docker build -t ai-microservices-frontend .
docker run -p 3000:3000 ai-microservices-frontend
```

## ☁️ Cloud Deployment

### AWS Deployment

#### Using AWS EC2

1. **Launch EC2 Instance**
   - Choose Ubuntu 20.04 LTS
   - Instance type: t3.medium or larger
   - Open ports: 22, 80, 443, 3000, 8000

2. **Install Dependencies**
```bash
sudo apt update
sudo apt install -y python3 python3-pip nodejs npm git

# Install Docker (optional)
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker ubuntu
```

3. **Deploy Application**
```bash
git clone <your-repo>
cd AIMLPROJECT
chmod +x setup.sh
./setup.sh

# Start services with PM2
npm install -g pm2
pm2 start backend/main.py --name backend --interpreter python3
pm2 start "cd frontend && npm start" --name frontend
pm2 startup
pm2 save
```

#### Using AWS Lambda + API Gateway

Create `backend/lambda_handler.py`:
```python
from mangum import Mangum
from main import app

handler = Mangum(app)
```

Package and deploy using AWS SAM or Serverless Framework.

### Google Cloud Platform

#### Using Cloud Run

1. **Build and Push Container**
```bash
# Backend
gcloud builds submit --tag gcr.io/PROJECT-ID/ai-backend backend/

# Frontend
gcloud builds submit --tag gcr.io/PROJECT-ID/ai-frontend frontend/
```

2. **Deploy to Cloud Run**
```bash
gcloud run deploy ai-backend \
  --image gcr.io/PROJECT-ID/ai-backend \
  --platform managed \
  --port 8000

gcloud run deploy ai-frontend \
  --image gcr.io/PROJECT-ID/ai-frontend \
  --platform managed \
  --port 3000
```

### Microsoft Azure

#### Using Azure Container Instances

```bash
# Create resource group
az group create --name ai-microservices --location eastus

# Deploy backend
az container create \
  --resource-group ai-microservices \
  --name ai-backend \
  --image your-registry/ai-backend \
  --ports 8000 \
  --dns-name-label ai-backend-unique

# Deploy frontend
az container create \
  --resource-group ai-microservices \
  --name ai-frontend \
  --image your-registry/ai-frontend \
  --ports 3000 \
  --dns-name-label ai-frontend-unique
```

## 🔧 Production Configuration

### Environment Variables

**Backend (.env):**
```env
# Production settings
DEBUG=False
APP_HOST=0.0.0.0
APP_PORT=8000

# Security
CORS_ORIGINS=["https://yourdomain.com"]
SECRET_KEY=your-secret-key

# LLM Providers
OLLAMA_BASE_URL=http://ollama:11434
OPENROUTER_API_KEY=your-key
OPENAI_API_KEY=your-key

# Database (if using)
DATABASE_URL=postgresql://user:pass@host:port/db

# File storage
UPLOAD_FOLDER=/app/uploads
MAX_FILE_SIZE=10485760
```

**Frontend (.env.production):**
```env
VITE_API_BASE_URL=https://api.yourdomain.com
VITE_APP_TITLE=AI Microservices
```

### Nginx Configuration

Create `nginx.conf`:
```nginx
events {
    worker_connections 1024;
}

http {
    upstream backend {
        server backend:8000;
    }

    server {
        listen 80;
        server_name yourdomain.com;

        # Frontend
        location / {
            root /usr/share/nginx/html;
            try_files $uri $uri/ /index.html;
        }

        # Backend API
        location /api/ {
            proxy_pass http://backend;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        # Health check
        location /health {
            proxy_pass http://backend;
        }
    }
}
```

### SSL Certificate

Using Let's Encrypt:
```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com
```

## 📊 Monitoring and Logging

### Health Monitoring

Create `monitoring/healthcheck.py`:
```python
import requests
import time
import logging

ENDPOINTS = [
    "http://localhost:8000/health",
    "http://localhost:3000",
]

def check_health():
    for endpoint in ENDPOINTS:
        try:
            response = requests.get(endpoint, timeout=5)
            if response.status_code == 200:
                logging.info(f"✅ {endpoint} is healthy")
            else:
                logging.error(f"❌ {endpoint} returned {response.status_code}")
        except Exception as e:
            logging.error(f"❌ {endpoint} is unreachable: {e}")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    while True:
        check_health()
        time.sleep(60)  # Check every minute
```

### Log Management

For production, configure structured logging:

```python
import logging
from pythonjsonlogger import jsonlogger

# In main.py
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s'
)

# For JSON logging
logHandler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter()
logHandler.setFormatter(formatter)
logger = logging.getLogger()
logger.addHandler(logHandler)
```

## 🔒 Security Considerations

### Backend Security

1. **API Rate Limiting**
```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.post("/api/v1/summarize")
@limiter.limit("10/minute")
async def summarize_text(request: Request, ...):
    # Implementation
```

2. **Input Validation**
```python
from pydantic import validator

class SummarizationRequest(BaseModel):
    text: str
    
    @validator('text')
    def validate_text(cls, v):
        if len(v) > 50000:  # Limit text size
            raise ValueError('Text too long')
        return v
```

3. **CORS Configuration**
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],  # Specific domains
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)
```

### File Upload Security

```python
ALLOWED_EXTENSIONS = {'.pdf', '.docx', '.txt'}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

def validate_file(file: UploadFile):
    # Check file extension
    if not any(file.filename.endswith(ext) for ext in ALLOWED_EXTENSIONS):
        raise HTTPException(400, "Invalid file type")
    
    # Check file size
    if file.size > MAX_FILE_SIZE:
        raise HTTPException(400, "File too large")
```

## 🔧 Troubleshooting

### Common Issues

1. **Port Already in Use**
```bash
# Find and kill process using port
lsof -ti:8000 | xargs kill -9  # Linux/Mac
netstat -ano | findstr :8000   # Windows
```

2. **Ollama Connection Issues**
```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# Start Ollama
ollama serve

# Pull required model
ollama pull llama2
```

3. **Memory Issues**
```bash
# Monitor memory usage
htop  # Linux
top   # Mac
taskmgr  # Windows

# Limit model memory usage in Ollama
OLLAMA_HOST=0.0.0.0:11434 OLLAMA_KEEP_ALIVE=5m ollama serve
```

4. **Build Issues**
```bash
# Clear caches
npm cache clean --force
pip cache purge

# Reinstall dependencies
rm -rf node_modules package-lock.json
npm install

rm -rf venv
python -m venv venv
pip install -r requirements.txt
```

### Performance Tuning

1. **Backend Optimization**
```python
# Use async/await for I/O operations
# Implement connection pooling
# Cache frequently accessed data
# Use background tasks for heavy operations

from fastapi import BackgroundTasks

@app.post("/api/v1/process")
async def process_data(background_tasks: BackgroundTasks):
    background_tasks.add_task(heavy_processing_task)
    return {"message": "Processing started"}
```

2. **Frontend Optimization**
```javascript
// Code splitting
const LazyComponent = React.lazy(() => import('./Component'));

// Memoization
const MemoizedComponent = React.memo(Component);

// Virtual scrolling for large lists
// Image optimization
// Bundle size optimization
```

## 📈 Scaling

### Horizontal Scaling

1. **Load Balancer Configuration**
```nginx
upstream backend_pool {
    server backend1:8000;
    server backend2:8000;
    server backend3:8000;
}
```

2. **Database Scaling**
```python
# Use connection pooling
# Implement read replicas
# Consider caching layers (Redis)
```

3. **Kubernetes Deployment**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ai-backend
spec:
  replicas: 3
  selector:
    matchLabels:
      app: ai-backend
  template:
    metadata:
      labels:
        app: ai-backend
    spec:
      containers:
      - name: backend
        image: ai-microservices-backend:latest
        ports:
        - containerPort: 8000
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
```

This deployment guide should help you deploy the AI Microservices application in various environments, from development to production-scale cloud deployments.