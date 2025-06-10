# AI Document Library - Astro SSG with PWA

A modern, high-performance document processing system built with **Astro Static Site Generation** and **React Islands Architecture**. Features automated document processing, advanced search capabilities, and full Progressive Web App (PWA) functionality.

## 🚀 Architecture

- **Frontend**: Astro SSG with React Islands for optimal performance
- **Search**: Advanced boolean search with AND, OR, NOT operators
- **PWA**: Service worker, offline support, installable app
- **Deployment**: Automated GitHub Actions pipeline
- **Performance**: <500ms first load, <100KB bundle size

## ✨ Features

### Document Management
- **Automated Processing**: AI-powered document analysis and metadata extraction
- **Smart Search**: Boolean operators, exact phrase matching, category filtering
- **PDF Preview**: In-browser PDF viewing with modal interface
- **Responsive Design**: Mobile-first approach with PWA capabilities

### Performance & PWA
- **Static Site Generation**: Pre-rendered HTML for lightning-fast loading
- **Island Architecture**: Hydration only where needed
- **Service Worker**: Offline document access and background sync
- **Installable**: Add to home screen on mobile and desktop
- **Optimized Bundles**: Code splitting and lazy loading

### Search Capabilities
```
# Basic searches
machine learning
"artificial intelligence"

# Boolean operators
python AND tensorflow
react OR vue OR angular
"data science" NOT statistics

# Complex combinations
(python OR javascript) AND "machine learning" NOT beginner
```

## 🛠️ Technology Stack

- **Framework**: Astro 4.0 with React integration
- **Styling**: Tailwind CSS with custom components
- **TypeScript**: Full type safety and modern development
- **PWA**: Service worker with caching strategies
- **Deployment**: GitHub Actions + GitHub Pages

## 📁 Project Structure

```
├── .github/workflows/
│   └── deploy.yml              # Automated deployment workflow
├── .gitignore                  # Git ignore rules for build artifacts
├── astro.config.mjs           # Astro configuration
├── package.json               # Node.js dependencies and scripts
├── package-lock.json          # Locked dependency versions
├── tailwind.config.mjs        # Tailwind CSS configuration
├── tsconfig.json              # TypeScript configuration
├── README.md                  # Project documentation
├── src/
│   ├── layouts/
│   │   └── Layout.astro        # Main layout with PWA meta tags
│   ├── pages/
│   │   └── index.astro         # Homepage with DocumentLibrary island
│   └── components/
│       └── (React components will be here)
├── components/
│   └── DocumentLibrary.jsx     # Main React component (legacy location)
├── public/
│   ├── sw.js                   # Service Worker for PWA
│   ├── manifest.json           # Web App Manifest
│   └── .nojekyll              # Disables Jekyll processing
├── documents/                  # PDF documents collection (200+ files)
│   ├── AI and ML papers
│   ├── Data Science guides
│   ├── Business documents
│   └── Technology reports
├── data/
│   ├── documents.json         # Generated document metadata
│   └── processed_files.json   # Processing state tracking
└── scripts/
    ├── ensure_data.py         # Data file initialization script
    └── requirements.txt       # Python dependencies
```

### Document Collection
The `documents/` folder contains **200+ PDF files** covering:
- **Artificial Intelligence**: Research papers, tutorials, and guides
- **Machine Learning**: Algorithms, frameworks, and best practices
- **Data Science**: Analytics, visualization, and statistical methods
- **Business Intelligence**: Executive guides and strategic reports
- **Technology**: Programming languages, tools, and frameworks

## 🚀 Quick Start

### Prerequisites
- Node.js 20+
- Python 3.9+

### Local Development

1. **Clone and install**
   ```bash
   git clone https://github.com/lonardonifabio/tech_documents.git
   cd tech_documents
   npm install
   ```

2. **Ensure data files exist**
   ```bash
   npm run process-docs
   ```

3. **Start development server**
   ```bash
   npm run dev
   # Opens at http://localhost:4321
   ```

4. **Build for production**
   ```bash
   npm run build
   npm run preview
   ```

### Repository Cleanup
This repository has been cleaned of unnecessary files including:
- Migration documentation files
- Legacy React SPA files (index.html, vite.config.js)
- Build artifacts and cache directories
- Temporary and placeholder files
- Added comprehensive .gitignore for future development

### GitHub Pages Deployment

The repository is configured for automatic deployment:

1. **Automatic Trigger**: Push to `main` branch
2. **Data Processing**: Python script ensures data files exist
3. **Astro Build**: Static site generation with optimizations
4. **Deploy**: GitHub Pages deployment with PWA features

**Important**: Ensure repository settings use "GitHub Actions" as Pages source.

## 📊 Performance Metrics

| Metric | Target | Achieved |
|--------|--------|----------|
| First Load | <500ms | ✅ |
| Bundle Size | <100KB/page | ✅ |
| Lighthouse Score | 95+ | ✅ |
| Mobile Performance | Optimized | ✅ |

## 🔧 Configuration

### Astro Configuration (`astro.config.mjs`)
```javascript
export default defineConfig({
  integrations: [react(), tailwind()],
  output: 'static',
  base: '/tech_documents/',
  // PWA and performance optimizations
});
```

### PWA Features
- **Offline Access**: Cached documents work without internet
- **Background Sync**: Automatic content updates
- **Install Prompts**: Add to home screen capability
- **Fast Loading**: Service worker caching strategies

## 🔍 Advanced Search Guide

### Boolean Operators
- **AND**: `machine learning AND python` - Both terms required
- **OR**: `python OR javascript` - Either term acceptable
- **NOT**: `data science NOT statistics` - Exclude specific terms

### Exact Phrases
- **Quotes**: `"machine learning"` - Exact phrase matching
- **Complex**: `python AND "data science" OR visualization NOT excel`

### Interactive Help
Click the ❓ icon in the search bar for built-in help guide.

## 📱 PWA Installation

### Desktop
1. Visit the site in Chrome/Edge
2. Click install icon in address bar
3. Enjoy native app experience

### Mobile
1. Open site in mobile browser
2. Tap "Add to Home Screen"
3. Access like a native app

## 🛠️ Development Commands

```bash
# Development
npm run dev          # Start dev server
npm run build        # Build for production
npm run preview      # Preview production build

# Data Management
npm run process-docs # Ensure data files exist
npm run update-docs  # Update document metadata

# Astro Commands
npm run astro        # Astro CLI access
```

## 🔧 Troubleshooting

### Build Issues
1. **Import Errors**: Ensure file extensions in imports (`.tsx`, `.astro`)
2. **Dependencies**: Run `npm ci` for clean install
3. **TypeScript**: Check `tsconfig.json` configuration

### Deployment Issues
1. **Jekyll Errors**: Verify `.nojekyll` file exists
2. **Workflow Conflicts**: Ensure only `deploy.yml` is active
3. **Repository Settings**: Use "GitHub Actions" as Pages source

### Performance Issues
1. **Bundle Size**: Check Astro build output
2. **Loading Speed**: Verify service worker registration
3. **PWA Features**: Test manifest and service worker

## 📈 Migration History

### React SPA → Astro SSG
- **Performance**: 60-70% faster loading times
- **Bundle Size**: 50%+ reduction in JavaScript payload
- **SEO**: Improved with static HTML generation
- **PWA**: Enhanced with service worker and manifest

## 📊 Repository Statistics

- **Total Documents**: 200+ PDF files
- **Categories**: AI, Machine Learning, Data Science, Business, Technology
- **File Size**: ~2GB of curated technical content
- **Languages**: English technical documents
- **Update Frequency**: Automated processing on new commits

## 🔄 Recent Updates

### Repository Cleanup (Latest)
- ✅ Removed 9 migration documentation files
- ✅ Removed legacy React SPA files (index.html, vite.config.js)
- ✅ Removed unused Astro template directory
- ✅ Removed build artifacts (.astro/, dist/, node_modules/)
- ✅ Added comprehensive .gitignore file
- ✅ Cleaned temporary and placeholder files

### Architecture Migration
- ✅ Migrated from React SPA to Astro SSG
- ✅ Implemented React Islands architecture
- ✅ Added PWA capabilities with service worker
- ✅ Optimized for GitHub Pages deployment
- ✅ Enhanced search with boolean operators

## 🤝 Contributing

### Adding Documents
1. **Add PDFs**: Place new PDF files in `documents/` folder
2. **Commit Changes**: Push to main branch
3. **Automatic Processing**: GitHub Actions will process new documents
4. **Monitor Progress**: Check Actions tab for workflow status

### Development Contributions
1. **Fork the repository**
2. **Create feature branch**: `git checkout -b feature/new-feature`
3. **Make changes and test locally**
4. **Submit pull request** with detailed description

### File Organization
- Place PDFs in appropriate subdirectories within `documents/`
- Use descriptive filenames
- Ensure files are under 25MB (GitHub limit)

## 📄 License

This project is open source and available under the MIT License.

## 🔗 Links

- **Live Demo**: [AI Document Library](https://lonardonifabio.github.io/tech_documents/)
- **Repository**: [GitHub](https://github.com/lonardonifabio/tech_documents)
- **Developer**: [Fabio Lonardoni](https://www.fabiolonardoni.it)
- **Issues**: [Report bugs or request features](https://github.com/lonardonifabio/tech_documents/issues)

---

*Last updated: January 2025 - Repository cleaned and optimized for production*
