# Document Automation System

This project now includes an automated document processing system that will automatically detect new PDF files in the `documents/` folder and update the website accordingly.

## How It Works

The system monitors the `documents/` folder for:
- **New PDF files** - Automatically added to the website
- **Modified PDF files** - Re-processed and updated
- **Deleted PDF files** - Automatically removed from the website

## Quick Start

### 1. Add New Documents
Simply copy any PDF files into the `documents/` folder. The system will automatically:
- Generate metadata for each document
- Update `data/documents.json`
- Update `dist/data/documents.json` 
- Make the documents visible on the website

### 2. Update Documents Database
Run one of these commands to process documents:

```bash
# Single scan for changes
npm run update-docs

# Continuous monitoring (checks every 10 seconds)
npm run watch-docs

# Force reprocess all documents
npm run process-docs
```

### 3. Build the Website
The build process now automatically updates documents before building:

```bash
# This will update documents AND build the site
npm run build

# Development server
npm run dev
```

## Available Scripts

| Script | Command | Description |
|--------|---------|-------------|
| `npm run update-docs` | `python scripts/auto_update.py` | Scan once for document changes |
| `npm run watch-docs` | `python scripts/auto_update.py --watch` | Continuously monitor for changes |
| `npm run process-docs` | `python scripts/simple_processor.py` | Force reprocess all documents |
| `npm run build` | `python scripts/auto_update.py && vite build` | Update docs and build site |
| `npm run dev` | `vite` | Start development server |

## File Structure

```
tech_documents/
├── documents/           # PDF files go here
├── data/
│   ├── documents.json   # Document metadata
│   └── processed_files.json  # Tracking file hashes
├── dist/data/
│   └── documents.json   # Copy for the website
└── scripts/
    ├── auto_update.py   # Smart document processor
    └── simple_processor.py  # Basic document processor
```

## How to Add New Documents

1. **Copy PDF files** to the `documents/` folder
2. **Run update command**: `npm run update-docs`
3. **Check the website** - new documents should appear automatically

## Troubleshooting

### Documents not showing on website?
1. Check if `data/documents.json` exists and contains your documents
2. Check if `dist/data/documents.json` exists and is up to date
3. Run `npm run update-docs` to force an update
4. Rebuild the site with `npm run build`

### Want to reprocess all documents?
```bash
# Delete the tracking file and reprocess everything
rm data/processed_files.json
npm run process-docs
```

### Continuous monitoring
For development, you can run continuous monitoring:
```bash
npm run watch-docs
```
This will check for changes every 10 seconds and automatically update the documents database.

## Technical Details

- **File tracking**: Uses MD5 hashes to detect file changes
- **Duplicate prevention**: Won't reprocess unchanged files
- **Automatic cleanup**: Removes deleted files from the database
- **Dual output**: Updates both `data/` and `dist/data/` directories
- **Error handling**: Gracefully handles missing files and directories

The system is designed to be robust and handle edge cases like:
- Files being added while the system is running
- Files being deleted or moved
- Corrupted or unreadable PDF files
- Network interruptions during processing
