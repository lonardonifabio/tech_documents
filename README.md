# AI Document Library with Ollama Integration

An automated document processing system that uses Ollama with DeepSeek model to analyze PDF documents and generate metadata for a web-based document library.

## Features

- **Automated Document Processing**: Automatically processes PDF documents when added to the `documents/` folder
- **AI-Powered Analysis**: Uses Ollama with DeepSeek model for intelligent document analysis
- **GitHub Actions Integration**: Fully automated workflow triggered by document changes
- **Web Interface**: Clean, responsive web interface for browsing documents
- **Incremental Processing**: Only processes new or changed documents for efficiency

## How It Works

1. **Document Upload**: Add PDF documents to the `documents/` folder
2. **Automatic Trigger**: GitHub Actions detects changes and starts processing
3. **AI Analysis**: Ollama with DeepSeek model analyzes document content
4. **Metadata Generation**: Extracts title, summary, keywords, category, and difficulty
5. **Database Update**: Updates `data/documents.json` with new metadata
6. **Website Deployment**: Automatically builds and deploys the updated website

## Setup

### Prerequisites

- Node.js 18+
- Python 3.11+
- Ollama (for local development)

### Local Development

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd tech_documents
   ```

2. **Install dependencies**
   ```bash
   npm install
   pip install -r scripts/requirements.txt
   ```

3. **Install and setup Ollama** (for local testing)
   ```bash
   # Install Ollama
   curl -fsSL https://ollama.ai/install.sh | sh
   
   # Start Ollama
   ollama serve
   
   # Pull DeepSeek model
   ollama pull deepseek-r1:1.5b
   ```

4. **Process documents locally**
   ```bash
   npm run process-docs
   ```

5. **Start development server**
   ```bash
   npm run dev
   ```

### GitHub Actions Setup

The repository is configured with GitHub Actions that automatically:

1. **Triggers on document changes** in the `documents/` folder
2. **Installs Ollama** and the DeepSeek model
3. **Processes documents** using AI analysis
4. **Updates the database** with new metadata
5. **Builds and deploys** the website to GitHub Pages

No additional setup required - just push documents to the `documents/` folder!

## Project Structure

```
├── .github/workflows/
│   └── process-documents.yml    # GitHub Actions workflow
├── documents/                   # PDF documents to process
├── data/
│   ├── documents.json          # Generated document metadata
│   └── processed_files.json    # Processing state tracking
├── scripts/
│   ├── ollama_processor.py     # Main document processor
│   ├── test_ollama.py         # Ollama connectivity test
│   └── requirements.txt       # Python dependencies
├── src/                        # Website source code
├── components/                 # React components
└── dist/                      # Built website (auto-generated)
```

## Document Processing

The AI processor extracts and analyzes:

- **Title**: Clean, readable document title
- **Summary**: 2-3 sentence content summary
- **Keywords**: Relevant topic keywords
- **Category**: AI, Machine Learning, Data Science, etc.
- **Difficulty**: Beginner, Intermediate, or Advanced
- **Authors**: Document authors (if found)
- **Content Preview**: First portion of meaningful content

## Configuration

### Environment Variables

- `OLLAMA_MODEL`: Specify different Ollama model (default: `deepseek-r1:1.5b`)

### Model Options

The system is optimized for DeepSeek but can work with other Ollama models:
- `deepseek-r1:1.5b` (default, lightweight)
- `deepseek-r1:7b` (more capable, requires more resources)
- `llama2` (alternative option)

## Performance Optimization

- **Incremental Processing**: Only processes new/changed documents
- **Text Extraction Limits**: Analyzes first 3 pages for efficiency
- **Token Limits**: Truncates content to avoid model limits
- **Fallback Analysis**: Provides basic metadata if AI analysis fails
- **Lightweight Model**: Uses DeepSeek 1.5B for fast processing

## Troubleshooting

### Local Development

1. **Test Ollama connectivity**:
   ```bash
   python scripts/test_ollama.py
   ```

2. **Check available models**:
   ```bash
   ollama list
   ```

3. **Manual document processing**:
   ```bash
   python scripts/ollama_processor.py
   ```

### GitHub Actions

- Check the Actions tab for workflow logs
- Ensure the repository has GitHub Pages enabled
- Verify documents are in the correct `documents/` folder

## Contributing

1. Add PDF documents to the `documents/` folder
2. The system will automatically process and deploy changes
3. Monitor the GitHub Actions workflow for processing status

## License

This project is open source and available under the MIT License.
