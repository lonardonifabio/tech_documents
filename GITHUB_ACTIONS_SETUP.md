# GitHub Actions Automation Setup

This project is now configured to automatically process documents and deploy the website using GitHub Actions whenever you add new PDF files to the `documents/` folder.

## How It Works

### Automatic Processing
1. **Add PDF files** to the `documents/` folder
2. **Commit and push** to the main/master branch
3. **GitHub Actions automatically**:
   - Processes all new/changed PDF files
   - Updates `documents.json` with metadata
   - Builds the website
   - Deploys to GitHub Pages
   - Commits the updated database back to the repository

### Workflow Files

#### `.github/workflows/deploy-site.yml`
Main workflow that runs on every push to main/master branch:
- Sets up Python and Node.js environments
- Installs dependencies
- Processes documents using `scripts/auto_update.py`
- Builds the website with Vite
- Deploys to GitHub Pages
- Commits updated database files

#### `.github/workflows/process-documents.yml`
Specialized workflow that only runs when files in `documents/` folder change:
- Lighter weight processing
- Focuses specifically on document changes
- Good for testing document processing

## Setup Instructions

### 1. Enable GitHub Pages
1. Go to your repository settings
2. Navigate to "Pages" section
3. Set source to "GitHub Actions"
4. Save the settings

### 2. Repository Permissions
Make sure your repository has the following permissions:
- **Actions**: Enabled (for running workflows)
- **Pages**: Enabled (for deployment)
- **Contents**: Write access (for committing updated files)

### 3. Branch Protection (Optional)
If you want to protect your main branch:
1. Go to Settings → Branches
2. Add a branch protection rule for `main`
3. Enable "Restrict pushes that create files"
4. Allow GitHub Actions to bypass restrictions

## Usage

### Adding New Documents
```bash
# 1. Add PDF files to documents folder
cp new_document.pdf documents/

# 2. Commit and push
git add documents/new_document.pdf
git commit -m "Add new document: new_document.pdf"
git push origin main
```

### Manual Triggering
You can manually trigger the workflow:
1. Go to "Actions" tab in your repository
2. Select "Build and Deploy Site"
3. Click "Run workflow"
4. Choose the branch and click "Run workflow"

### Monitoring Progress
1. Go to "Actions" tab in your repository
2. Click on the latest workflow run
3. Monitor the progress of each step
4. Check logs for any errors

## What Gets Automated

### Document Processing
- ✅ Automatic PDF detection
- ✅ Metadata extraction (title, file size, upload date)
- ✅ Database updates (`data/documents.json`)
- ✅ Duplicate prevention (hash-based)
- ✅ Deleted file cleanup

### Website Deployment
- ✅ Automatic building with Vite
- ✅ GitHub Pages deployment
- ✅ Cache optimization
- ✅ Error handling

### Repository Updates
- ✅ Auto-commit updated database files
- ✅ Proper commit messages
- ✅ Skip CI on auto-commits (prevents loops)

## File Structure After Automation

```
your-repo/
├── .github/workflows/
│   ├── deploy-site.yml          # Main deployment workflow
│   └── process-documents.yml    # Document-specific workflow
├── documents/                   # PDF files (you add here)
├── data/
│   ├── documents.json          # Auto-generated database
│   └── processed_files.json    # Auto-generated tracking
├── dist/                       # Auto-generated build output
│   ├── index.html
│   └── data/documents.json     # Copy for website
└── scripts/
    └── auto_update.py          # Document processor
```

## Troubleshooting

### Workflow Fails
1. Check the Actions tab for error details
2. Common issues:
   - Missing dependencies
   - Permission errors
   - Invalid PDF files
   - Network timeouts

### Documents Not Showing
1. Check if workflow completed successfully
2. Verify `data/documents.json` was updated
3. Check GitHub Pages deployment status
4. Clear browser cache

### Permission Errors
1. Ensure repository has proper permissions
2. Check if branch protection rules are blocking
3. Verify GitHub token has necessary scopes

### Manual Recovery
If something goes wrong, you can manually run:
```bash
# Locally process documents
npm run update-docs

# Build and test locally
npm run build
npm run preview

# Force push if needed
git add data/ dist/
git commit -m "Manual update"
git push
```

## Advanced Configuration

### Customizing Workflows
Edit `.github/workflows/deploy-site.yml` to:
- Change trigger conditions
- Modify build steps
- Add additional processing
- Change deployment targets

### Environment Variables
You can add secrets/variables in repository settings:
- `GITHUB_TOKEN` (automatically provided)
- Custom API keys for enhanced processing
- Deployment configurations

### Monitoring
Set up notifications:
1. Repository Settings → Notifications
2. Enable workflow notifications
3. Configure email/Slack alerts

## Benefits

### For Users
- ✅ **Zero manual work** - just add PDFs and push
- ✅ **Instant updates** - website updates automatically
- ✅ **Always in sync** - database always matches files
- ✅ **Error recovery** - automatic retry and error handling

### For Developers
- ✅ **Consistent processing** - same environment every time
- ✅ **Version control** - all changes tracked in git
- ✅ **Scalable** - handles any number of documents
- ✅ **Maintainable** - clear separation of concerns

This automation ensures your document library website stays up-to-date automatically whenever you add new research papers, documents, or resources to your collection!
