# AI & Data Science Document Library

An automated document processing system that creates summaries of uploaded documents and displays them in a searchable web interface.

Click this link: https://lonardonifabio.github.io/tech_documents/dist/src/index.html 

## 🚀 Quick Start

### Option 1: Using the Python Server Script (Recommended)
```bash
python start_server.py
```
This will automatically:
- Start a local HTTP server on port 8000
- Open your browser to the document library
- Display all processed documents

### Option 2: Manual Server Start
```bash
python -m http.server 8000
```
Then open your browser to: `http://localhost:8000/src/index.html`

## 📁 Project Structure

```
tech_documents/
├── documents/                    # PDF documents to be processed
│   └── *.pdf                    # AI and Data Science documents
├── dist/data/
│   ├── documents.json           # Processed document metadata and summaries
│   └── processed_files.json    # Track processed files to avoid reprocessing
├── src/
│   ├── index.html              # Main web interface
│   └── js/
│       ├── app.js              # Standalone React app
│       └── translations.js     # Multilingual support
├── scripts/
│   ├── process_documents.py    # Document processing script
│   ├── build.py               # Build script for deployment
│   └── requirements.txt       # Python dependencies
├── components/
│   └── DocumentLibrary.jsx    # React component (alternative implementation)
├── start_server.py            # Easy server startup script
├── package.json               # Node.js dependencies
├── vite.config.js            # Vite configuration
└── README.md                  # This file
```

## 🔧 How It Works

1. **Document Upload**: Add PDF files to the `documents/` folder
2. **Processing**: The Python scripts process documents and extract:
   - Filename and metadata
   - AI-generated summary using Llama2
   - Keywords extraction
   - Category classification
   - Difficulty level assessment
   - Author and title extraction
- Intelligent duplicate prevention system

3. **Storage**: Processed data is stored in `dist/data/documents.json`
4. **Display**: The web interface loads and displays all documents with search/filter capabilities

## 🌐 Web Interface Features

- **Multilingual Support**: Switch between English and Italian
- **Advanced Search**: Search by filename, title, summary content, authors, or keywords
- **Smart Filtering**: Filter by category and difficulty level
- **Responsive Design**: Works perfectly on desktop and mobile devices
- **Direct Links**: Click "View →" to access documents on GitHub
- **Real-time Updates**: Automatically shows document count and status
- **Document Previews**: Visual file type indicators and category badges
- **Expandable Summaries**: Show more/less functionality for long summaries

## 🤖 AI-Powered Processing

The system uses **Llama2** AI model to automatically:
- Generate intelligent summaries
- Extract relevant keywords
- Classify documents by category
- Assess difficulty levels
- Extract titles and authors from document content

## 🛠️ Setup and Installation

### Prerequisites
- Python 3.8+
- Ollama with Llama2 model (for document processing)
- Node.js (optional, for Vite development)

### Installation Steps
1. Clone the repository
2. Install Python dependencies:
   ```bash
   pip install -r scripts/requirements.txt
   ```
3. Install Ollama and pull Llama2:
   ```bash
   ollama pull llama2:7b
   ```
4. Add PDF documents to the `documents/` folder
5. Process documents:
   ```bash
   python scripts/process_documents.py
   ```
6. Start the server:
   ```bash
   python start_server.py
   ```

## 🔄 Adding New Documents

1. Add PDF files to the `documents/` folder
2. Run the processing script:
   ```bash
   python scripts/process_documents.py
   ```
3. Refresh the web interface to see new documents

The system automatically tracks processed files and only processes new or changed documents.

## 🔒 Duplicate Prevention System

The document processing system includes an intelligent duplicate prevention mechanism that ensures documents are not reprocessed unnecessarily:

### How It Works
- **File Tracking**: Each processed document's MD5 hash is stored in `dist/data/processed_files.json`
- **Change Detection**: Before processing, the system calculates the current file hash and compares it with stored hashes
- **Smart Skipping**: Documents with matching hashes are automatically skipped
- **Cross-Platform Compatibility**: Path normalization handles Windows (\) and Unix (/) path separators

### Benefits
- ⚡ **Faster Processing**: Skip already processed documents
- 💾 **Resource Efficiency**: Save computational resources and time
- 🔄 **Incremental Updates**: Only process new or modified documents
- 🛡️ **Data Integrity**: Prevent duplicate entries in the database

### File Structure
```json
{
  "documents/document1.pdf": "abc123def456...",
  "documents/document2.pdf": "789xyz012..."
}
```

### Testing
You can test the duplicate prevention system by running:
```bash
python scripts/test_results.py
```
This will show which documents are being skipped and which would be processed.

## 📊 Document Data Format

Each document in `documents.json` contains:
```json
{
  "id": "unique_hash",
  "filename": "document.pdf",
  "title": "Extracted or AI-generated title",
  "authors": ["Author 1", "Author 2"],
  "filepath": "documents/document.pdf",
  "upload_date": "2025-05-26T15:11:48.897460",
  "file_size": 22812101,
  "summary": "AI-generated summary",
  "keywords": ["AI", "Machine Learning", "Data Science"],
  "category": "Machine Learning",
  "difficulty": "Intermediate",
  "content_preview": "First 500 characters of content..."
}
```
## 🚀 Deployment

### GitHub Pages
1. Run the build script:
   ```bash
   python scripts/build.py
   ```
2. Deploy the `dist/` folder to GitHub Pages

### Local Development with Vite
```bash
npm install
npm run dev
```

## 🛠️ Technical Details

- **Frontend**: React 18 with Tailwind CSS
- **Backend**: Python HTTP server
- **AI Processing**: Ollama with Llama2
- **Data Format**: JSON
- **Document Processing**: LangChain with PDF extraction
- **Deployment**: GitHub Pages compatible
- **Build Tool**: Vite (optional)

## 🔍 Search Capabilities

The search functionality includes:
- **Full-text search** across titles, summaries, and content
- **Author search** by name
- **Keyword matching** with intelligent filtering
- **Category filtering** with dynamic options
- **Difficulty level filtering**
- **Case-insensitive search** for better user experience

## 📝 Development Notes

- All external dependencies are loaded via CDN for simplicity
- The interface is fully responsive and mobile-friendly
- Search is optimized for performance with large document collections
- The system handles file changes automatically (reprocessing only when needed)
- Error handling includes graceful fallbacks for missing data

## 🎯 Current Status

✅ **Working Features:**
- Document display and rendering
- AI-powered document processing
- Advanced search functionality
- Category and difficulty filtering
- Multilingual interface (EN/IT)
- Responsive design
- GitHub integration
- Local server setup
- Automatic file change detection
- Author and title extraction

🔄 **Future Enhancements:**
- Support for more document formats (DOCX, TXT)
- Advanced AI models for better categorization
- Document preview functionality
- Batch upload support
- User authentication and personal libraries
- Document tagging system
- Export functionality

## 🐛 Troubleshooting

### Common Issues:

1. **Documents not loading**: Check that `dist/data/documents.json` exists and is valid JSON
2. **Processing fails**: Ensure Ollama is running and Llama2 model is available
3. **Server won't start**: Check if port 8000 is already in use
4. **Search not working**: Verify document data structure matches expected format

### Debug Mode:
Open browser developer tools to see console logs for detailed error information.

## 📄 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.
