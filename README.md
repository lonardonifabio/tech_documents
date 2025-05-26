# AI & Data Science Document Library

An automated document processing system that creates summaries of uploaded documents and displays them in a searchable web interface.

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
│   └── global_trends_in_ai_governance.pdf
├── data/
│   └── documents.json           # Processed document metadata and summaries
├── src/
│   └── index.html              # Main web interface
├── scripts/
│   ├── process_documents.py    # Document processing script
│   ├── build.py               # Build script
│   └── requirements.txt       # Python dependencies
├── components/
│   └── DocumentLibrary.jsx    # React component (alternative implementation)
├── start_server.py            # Easy server startup script
└── README.md                  # This file
```

## 🔧 How It Works

1. **Document Upload**: Add PDF files to the `documents/` folder
2. **Processing**: The Python scripts process documents and extract:
   - Filename and metadata
   - AI-generated summary
   - Keywords
   - Category classification
   - Difficulty level
3. **Storage**: Processed data is stored in `data/documents.json`
4. **Display**: The web interface loads and displays all documents with search/filter capabilities

## 🌐 Web Interface Features

- **Search**: Search by filename, summary content, or keywords
- **Filtering**: Filter by category and difficulty level
- **Responsive Design**: Works on desktop and mobile devices
- **Direct Links**: Click "Visualizza →" to view documents on GitHub
- **Real-time Updates**: Automatically shows document count and status

## 🐛 Issues Fixed

### Previous Problems:
1. **CORS Policy Issues**: Browser couldn't load files when opening HTML directly
2. **Incorrect File Paths**: Fetch requests used wrong relative paths
3. **Malformed URLs**: GitHub links had syntax errors
4. **Missing Error Handling**: No feedback when documents failed to load

### Solutions Implemented:
1. **Embedded JavaScript**: Moved all JS code inline to avoid CORS issues
2. **Multiple Path Fallbacks**: Try different relative paths to find documents.json
3. **Fixed Template Literals**: Corrected GitHub URL generation
4. **Enhanced Error Handling**: Added loading states and error messages
5. **Local Server Script**: Created easy-to-use server startup script

## 📊 Document Data Format

Each document in `documents.json` contains:
```json
{
  "id": "unique_hash",
  "filename": "document.pdf",
  "filepath": "documents/document.pdf",
  "upload_date": "2025-05-26T15:11:48.897460",
  "file_size": 22812101,
  "summary": "AI-generated summary",
  "keywords": ["AI", "Data Science"],
  "category": "General",
  "difficulty": "Intermediate",
  "content_preview": "First few lines of content..."
}
```

## 🔄 Adding New Documents

1. Add PDF files to the `documents/` folder
2. Run the processing script (if automated processing is set up)
3. Refresh the web interface to see new documents

## 🛠️ Technical Details

- **Frontend**: React 18 with Tailwind CSS
- **Backend**: Python HTTP server
- **Data Format**: JSON
- **Document Processing**: Python with PDF extraction
- **Deployment**: GitHub Pages compatible

## 📝 Notes

- The system is designed to work both locally and on GitHub Pages
- All external dependencies are loaded via CDN for simplicity
- The interface is fully responsive and mobile-friendly
- Search is case-insensitive and searches across multiple fields

## 🎯 Current Status

✅ **Working Features:**
- Document display and rendering
- Search functionality
- Category and difficulty filtering
- Responsive design
- GitHub integration
- Local server setup

🔄 **Future Enhancements:**
- Automated document processing on upload
- More advanced search capabilities
- Document preview functionality
- Batch upload support
