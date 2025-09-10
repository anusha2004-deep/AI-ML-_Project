# AI Microservices with Flowise + LangChain

A comprehensive AI microservices platform built with FastAPI, LangChain, and React, providing text summarization, document Q&A, and personalized learning path generation capabilities.

## 🚀 Features

### Core AI Services
- **Text Summarization**: Generate concise summaries from long texts using multiple LLM providers
- **Document Q&A**: Upload documents (PDF, DOCX, TXT) and ask intelligent questions about their content
- **Learning Path Generation**: Create personalized learning paths based on goals, background, and preferences

### Technical Capabilities
- **Multiple LLM Providers**: Support for Ollama (local), OpenRouter, and OpenAI
- **Document Processing**: Advanced text extraction and vector embedding for document analysis
- **RESTful APIs**: Well-documented FastAPI endpoints with automatic OpenAPI documentation
- **Modern Frontend**: React-based dashboard with intuitive user interface
- **Batch Processing**: Handle multiple requests efficiently
- **File Management**: Secure document upload, processing, and management

## 🏗️ Architecture

```
├── backend/                 # FastAPI backend
│   ├── api/                # API route handlers
│   ├── services/           # Business logic services
│   ├── models/             # Pydantic models and schemas
│   ├── uploads/            # Document storage
│   └── main.py             # Application entry point
├── frontend/               # React frontend
│   ├── src/
│   │   ├── components/     # Reusable UI components
│   │   ├── pages/          # Main application pages
│   │   └── services/       # API client services
└── AI_Microservices_API.postman_collection.json
```

## 🛠️ Setup and Installation

### Prerequisites

- Python 3.8+
- Node.js 16+
- Git

### Backend Setup

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd AIMLPROJECT
   ```

2. **Set up Python environment**
   ```bash
   cd backend
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**
   ```bash
   # Copy environment template
   copy .env.example .env  # Windows
   cp .env.example .env    # Linux/Mac
   ```

5. **Edit `.env` file with your configuration**
   ```env
   # LLM Configuration
   OLLAMA_BASE_URL=http://localhost:11434
   OLLAMA_MODEL=llama2
   
   # OpenRouter Configuration (Optional)
   OPENROUTER_API_KEY=your_openrouter_api_key_here
   
   # OpenAI Configuration (Optional)
   OPENAI_API_KEY=your_openai_api_key_here
   
   # Application Settings
   APP_HOST=0.0.0.0
   APP_PORT=8000
   DEBUG=True
   ```

### Frontend Setup

1. **Navigate to frontend directory**
   ```bash
   cd ../frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Create environment configuration (optional)**
   ```bash
   # Create .env file if needed
   echo "VITE_API_BASE_URL=http://localhost:8000" > .env
   ```

### Ollama Setup (Recommended)

1. **Install Ollama**
   - Visit [https://ollama.ai/](https://ollama.ai/) and download for your OS
   - Or use the setup scripts provided:
     ```bash
     # Windows PowerShell
     .\setup_ollama.ps1
     
     # Linux/Mac
     ./setup_ollama.sh
     ```

2. **Start Ollama and pull a model**
   ```bash
   ollama serve
   ollama pull llama2
   ```

## 🚀 Running the Application

### Start Backend Server
```bash
cd backend
python main.py
```
The API server will start at `http://localhost:8000`

### Start Frontend Development Server
```bash
cd frontend
npm run dev
```
The frontend will be available at `http://localhost:3000`

## 📚 API Documentation

### Interactive Documentation
Once the backend is running, visit:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

### API Endpoints

#### General Endpoints
- `GET /` - API information and available endpoints
- `GET /health` - Health check and provider status

#### Text Summarization
- `POST /api/v1/summarize` - Summarize text
- `GET /api/v1/summarize/providers` - Get available providers
- `POST /api/v1/summarize/batch` - Batch summarization

#### Document Q&A
- `POST /api/v1/upload-document` - Upload document
- `POST /api/v1/qa` - Ask question
- `GET /api/v1/documents` - List documents
- `DELETE /api/v1/documents/{id}` - Delete document
- `POST /api/v1/qa/batch` - Batch Q&A

#### Learning Path
- `POST /api/v1/learning-path` - Generate learning path
- `GET /api/v1/learning-path/templates` - Get templates
- `POST /api/v1/learning-path/evaluate` - Evaluate progress

### Example Requests

#### Text Summarization
```bash
curl -X POST "http://localhost:8000/api/v1/summarize" \
     -H "Content-Type: application/json" \
     -d '{
       "text": "Your long text here...",
       "max_length": 150,
       "provider": "ollama"
     }'
```

#### Document Q&A
```bash
# Upload document
curl -X POST "http://localhost:8000/api/v1/upload-document" \
     -F "file=@document.pdf"

# Ask question
curl -X POST "http://localhost:8000/api/v1/qa" \
     -H "Content-Type: application/json" \
     -d '{
       "question": "What is the main topic?",
       "document_ids": ["doc-id-here"],
       "provider": "ollama"
     }'
```

## 🧪 Testing with Postman

1. **Import the collection**
   - Open Postman
   - Import `AI_Microservices_API.postman_collection.json`

2. **Set environment variables**
   - Create new environment
   - Add variable: `base_url = http://localhost:8000`

3. **Test endpoints**
   - Start with "Health Check"
   - Try "Summarize Text" with sample data
   - Upload a document and test Q&A

## 🔧 Configuration Options

### LLM Providers

#### Ollama (Local, Recommended)
- **Pros**: Free, private, fast, works offline
- **Cons**: Requires local installation
- **Setup**: Install Ollama and pull models

#### OpenRouter
- **Pros**: Access to multiple models, easy setup
- **Cons**: Requires API key, costs money
- **Setup**: Get API key from OpenRouter

#### OpenAI
- **Pros**: High-quality responses
- **Cons**: More expensive, requires API key
- **Setup**: Get API key from OpenAI

### File Upload Limits
- **Maximum file size**: 10MB (configurable via `MAX_FILE_SIZE`)
- **Supported formats**: PDF, DOCX, TXT
- **Storage location**: `./uploads` (configurable via `UPLOAD_FOLDER`)

## 🎯 Usage Examples

### Text Summarization
1. Navigate to `/summarization`
2. Paste your text (minimum 50 characters)
3. Adjust summary length and select provider
4. Click "Generate Summary"
5. Copy or download the result

### Document Q&A
1. Navigate to `/qa`
2. Upload a document (PDF, DOCX, or TXT)
3. Wait for processing to complete
4. Select documents for Q&A context
5. Ask questions about the content
6. Export Q&A session if needed

### Learning Path Generation
1. Navigate to `/learning-path`
2. Add learning goals with proficiency levels
3. Provide background information
4. Select learning style and duration
5. Generate personalized learning path
6. Download the complete plan

## 🚨 Troubleshooting

### Common Issues

#### Backend Won't Start
- Check Python version (3.8+ required)
- Verify all dependencies are installed
- Check if port 8000 is available
- Review environment variables in `.env`

#### Ollama Connection Failed
- Ensure Ollama is running: `ollama serve`
- Check if model is available: `ollama list`
- Verify Ollama URL in `.env`

#### Frontend Issues
- Check Node.js version (16+ required)
- Clear npm cache: `npm cache clean --force`
- Delete `node_modules` and reinstall

#### Document Upload Fails
- Check file size (max 10MB)
- Verify file format (PDF, DOCX, TXT only)
- Ensure upload directory is writable

### Logs and Debugging
- Backend logs: Check console output where server is running
- Frontend logs: Open browser developer tools
- API errors: Check response details in Network tab

## 🌟 Advanced Features

### Batch Processing
- Process multiple texts for summarization
- Ask multiple questions simultaneously
- Efficient resource utilization

### Provider Fallback
- Automatic fallback to available providers
- Graceful error handling
- Provider status monitoring

### Progress Tracking
- Learning path progress evaluation
- Personalized recommendations
- Achievement tracking

## 🛡️ Security Considerations

- File type validation for uploads
- File size limits to prevent abuse
- Input sanitization for text processing
- CORS configuration for frontend access

## 📈 Performance Optimization

- Vector database caching for documents
- Efficient text chunking strategies
- Parallel processing for batch operations
- Resource pooling for LLM connections

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

If you encounter any issues or have questions:

1. Check the troubleshooting section above
2. Review the API documentation at `/docs`
3. Check existing issues in the repository
4. Create a new issue with detailed information

## 🔮 Future Enhancements

- [ ] Multi-language support
- [ ] Advanced document analysis
- [ ] Real-time collaboration features
- [ ] Mobile-responsive design improvements
- [ ] Integration with more LLM providers
- [ ] Advanced learning analytics
- [ ] Export to various formats
- [ ] User authentication and profiles

---

**Made with ❤️ using FastAPI, LangChain, and React**