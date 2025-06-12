# Document Chat Setup Guide

This guide explains how to set up the new document chat feature with Ollama/Mistral integration.

## Features Added

✅ **Third Column Layout**: Added a chat interface as a third column in the document preview modal
✅ **Ollama Integration**: Direct integration with local Ollama service
✅ **Document Context**: AI has access to document metadata (title, summary, key concepts, etc.)
✅ **Model Selection**: Support for multiple Ollama models
✅ **Performance Optimized**: Designed for GitHub Spaces free tier

## Architecture

```
┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
│   Metadata      │ │   PDF Preview   │ │   AI Chat       │
│   (Left)        │ │   (Center)      │ │   (Right)       │
│                 │ │                 │ │                 │
│ • Title         │ │ • PDF Viewer    │ │ • Chat Messages │
│ • Authors       │ │ • Zoom Controls │ │ • Input Field   │
│ • Summary       │ │ • Navigation    │ │ • Model Select  │
│ • Key Concepts  │ │                 │ │ • Connection    │
│ • Keywords      │ │                 │ │   Status        │
│ • Category      │ │                 │ │                 │
│ • Download      │ │                 │ │                 │
└─────────────────┘ └─────────────────┘ └─────────────────┘
```

## Setup Instructions

### 1. Install Ollama

**For GitHub Spaces (Recommended):**
```bash
# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Start Ollama service
ollama serve &

# Pull Mistral model (lightweight for free tier)
ollama pull mistral:7b-instruct
```

**For Local Development:**
```bash
# macOS
brew install ollama

# Linux
curl -fsSL https://ollama.ai/install.sh | sh

# Windows
# Download from https://ollama.ai/download
```

### 2. Start Ollama Service

```bash
# Start the Ollama service (runs on port 11434 by default)
ollama serve
```

### 3. Pull AI Models

**Recommended models for GitHub Spaces free tier:**
```bash
# Lightweight models (recommended for free tier)
ollama pull mistral:7b-instruct    # ~4GB - Good balance of performance/size
ollama pull llama3.2:3b           # ~2GB - Fastest, smaller responses
ollama pull phi3:mini             # ~2GB - Microsoft's efficient model

# Larger models (if you have more resources)
ollama pull llama3.1:8b           # ~5GB - Better quality responses
ollama pull codellama:7b          # ~4GB - Good for technical documents
```

### 4. Environment Configuration

Create a `.env` file in your project root:
```env
# Ollama Configuration
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_DEFAULT_MODEL=mistral:7b-instruct

# GitHub Spaces Configuration (if deploying)
GITHUB_SPACES=true
```

### 5. GitHub Spaces Deployment

Create `.github/workflows/deploy.yml`:
```yaml
name: Deploy to GitHub Spaces
on:
  push:
    branches: [ main ]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: '18'
      - run: npm install
      - run: npm run build
      - name: Setup Ollama
        run: |
          curl -fsSL https://ollama.ai/install.sh | sh
          ollama serve &
          sleep 10
          ollama pull mistral:7b-instruct
```

## Performance Optimizations

### For GitHub Spaces Free Tier:

1. **Model Selection**: Use smaller models (3B-7B parameters)
2. **Response Limits**: Max 500 tokens per response
3. **Context Management**: Keep only last 10 messages in conversation
4. **Connection Pooling**: Reuse Ollama connections
5. **Error Handling**: Graceful fallbacks when service is unavailable

### Memory Usage:
- **mistral:7b-instruct**: ~4GB RAM
- **llama3.2:3b**: ~2GB RAM  
- **phi3:mini**: ~2GB RAM

## Usage

1. **Open Document**: Click on any document in the library
2. **View Layout**: See the new three-column layout
3. **Start Chatting**: Use the chat interface on the right
4. **Ask Questions**: The AI has context about the document
5. **Model Selection**: Choose different models from the dropdown

### Example Questions:
- "What are the main topics covered in this document?"
- "Can you explain the key concepts mentioned?"
- "What is the main conclusion or takeaway?"
- "Who is the target audience for this document?"
- "Summarize the methodology described"

## Troubleshooting

### Common Issues:

**1. "Ollama Not Connected" Warning**
```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# Start Ollama if not running
ollama serve
```

**2. Model Not Found**
```bash
# List available models
ollama list

# Pull required model
ollama pull mistral:7b-instruct
```

**3. Memory Issues on GitHub Spaces**
- Use smaller models (3B parameters)
- Reduce max_tokens in responses
- Clear chat history frequently

**4. CORS Issues**
```bash
# Start Ollama with CORS enabled
OLLAMA_ORIGINS="*" ollama serve
```

## API Endpoints

The chat feature uses these Ollama API endpoints:

- `GET /api/tags` - List available models
- `POST /api/chat` - Send chat messages
- `GET /api/version` - Check Ollama version

## Security Considerations

- Ollama runs locally, no data sent to external services
- Document content is processed locally
- Chat history is stored in browser memory only
- No persistent storage of conversations

## Performance Monitoring

Monitor these metrics for optimal performance:

- **Response Time**: < 5 seconds per message
- **Memory Usage**: < 8GB total
- **Model Load Time**: < 30 seconds
- **Connection Status**: Green indicator in chat header

## Contributing

To extend the chat functionality:

1. **Add New Models**: Update `availableModels` in `DocumentChat.tsx`
2. **Custom Prompts**: Modify `getDocumentContext()` method
3. **UI Improvements**: Update chat interface styling
4. **Performance**: Optimize message handling and context management

## Support

For issues or questions:
1. Check Ollama is running: `ollama serve`
2. Verify model is installed: `ollama list`
3. Check browser console for errors
4. Ensure sufficient memory is available
