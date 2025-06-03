# Incremental Document Processing with Ollama

This repository now includes an enhanced GitHub Actions workflow that processes documents incrementally, ensuring that progress is saved after each document and can be resumed if the job is interrupted.

## Key Features

### 1. Incremental Processing
- Documents are processed one by one
- After each document is analyzed, the results are immediately committed to the repository
- If the workflow is interrupted (e.g., due to the 6-hour GitHub Actions limit), progress is preserved

### 2. Duplicate Prevention
- The `processed_files.json` file tracks which documents have been analyzed with their file hashes
- Documents are only reprocessed if:
  - They are new (not in `processed_files.json`)
  - They have been modified (hash has changed)
  - Force reprocessing is enabled

### 3. Resumable Execution
- If a workflow run is canceled or times out, the next run will continue from where it left off
- Previously processed documents are skipped automatically
- No work is duplicated

## Workflow Configuration

### Automatic Triggers
- **Daily Schedule**: Runs at 2 AM UTC every day
- **File Changes**: Triggers when documents are added/modified in the `documents/` folder
- **Script Updates**: Triggers when the processor script is modified

### Manual Triggers
- **Workflow Dispatch**: Can be manually triggered from GitHub Actions tab
- **Force Reprocess**: Option to reprocess all documents (ignoring `processed_files.json`)

## Files Structure

```
├── .github/workflows/
│   └── process_documents_with_ollama.yml    # Main workflow file
├── scripts/
│   ├── fixed_ollama_processor.py            # Original processor
│   ├── incremental_ollama_processor.py      # Enhanced incremental processor
│   └── requirements.txt                     # Python dependencies
├── data/
│   ├── documents.json                       # Processed document metadata
│   └── processed_files.json                # Tracking of processed files
└── documents/                               # PDF documents to process
```

## How It Works

### 1. Document Discovery
The workflow scans the `documents/` folder for PDF files and compares them against `processed_files.json` to determine which files need processing.

### 2. Incremental Processing
For each document that needs processing:
1. Extract text content from the PDF
2. Analyze with Ollama (Mistral model) to generate metadata
3. Update `documents.json` with the new document entry
4. Update `processed_files.json` with the file hash
5. Commit and push changes to GitHub
6. Continue to the next document

### 3. Progress Tracking
Each commit message includes:
- The document filename that was processed
- The running count of processed documents
- Example: `"Process document: AI_Guide.pdf (15 processed)"`

### 4. Resumption Logic
When the workflow runs again:
1. Load `processed_files.json` to see what's already been done
2. Skip files that haven't changed since last processing
3. Only process new or modified files
4. Continue the incremental commit pattern

## Workflow Limits and Safety

### Time Limits
- Workflow timeout: 5 hours 50 minutes (under GitHub's 6-hour limit)
- Provides 10-minute buffer for cleanup and final operations

### Error Handling
- Individual document failures don't stop the entire workflow
- Failed documents are logged but processing continues
- Git operations are wrapped in error handling

### Resource Management
- Uses Ubuntu latest runner
- Python 3.11 environment
- Ollama with Mistral 7B model

## Usage Examples

### Manual Workflow Trigger
1. Go to GitHub Actions tab
2. Select "Process Documents with Ollama" workflow
3. Click "Run workflow"
4. Optionally enable "Force reprocess all documents"

### Adding New Documents
1. Add PDF files to the `documents/` folder
2. Commit and push changes
3. Workflow will automatically trigger and process new files

### Monitoring Progress
- Check the Actions tab for real-time logs
- Each document processing shows detailed progress
- Commit history shows individual document processing

## Benefits

### 1. Fault Tolerance
- No loss of work if workflow is interrupted
- Automatic resumption from last processed document
- Robust error handling for individual failures

### 2. Efficiency
- No duplicate processing of unchanged documents
- Fast startup for subsequent runs (skips processed files)
- Optimal resource usage

### 3. Transparency
- Clear commit history showing processing progress
- Detailed logging for troubleshooting
- Easy to track which documents have been processed

### 4. Flexibility
- Manual trigger with force reprocess option
- Automatic triggers for new documents
- Easy to modify processing parameters

## Troubleshooting

### Common Issues

**Workflow times out after 6 hours**
- This is expected for large document sets
- Next run will continue from where it left off
- Consider processing in smaller batches if needed

**Document processing fails**
- Check logs for specific error messages
- Individual failures don't stop the workflow
- Failed documents can be reprocessed by modifying them (changing hash)

**Git push failures**
- Usually due to concurrent modifications
- Workflow includes retry logic
- Manual intervention may be needed for conflicts

### Monitoring Commands

Check processing status:
```bash
# Count processed documents
jq length data/documents.json

# Count tracked files
jq length data/processed_files.json

# List recently processed files
git log --oneline --grep="Process document" -10
```

## Configuration Options

### Environment Variables
- `OLLAMA_MODEL`: Model to use (default: mistral:7b)
- `FORCE_REPROCESS`: Force reprocess all files (true/false)

### Workflow Inputs
- `force_reprocess`: Boolean input for manual workflow dispatch

This incremental approach ensures reliable, resumable document processing that can handle large document collections without losing progress due to GitHub Actions time limits.
