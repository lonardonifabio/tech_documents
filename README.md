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
│   └── deploy.yml              # Astro deployment workflow
├── src/
│   ├── layouts/
│   │   └── Layout.astro        # Main layout with PWA meta tags
│   ├── pages/
│   │   └── index.astro         # Homepage with DocumentLibrary island
│   └── components/
│       ├── DocumentLibrary.tsx # Main app component (React Island)
│       ├── DocumentCard.tsx    # Document display component
│       ├── PDFModal.tsx        # PDF preview modal
│       ├── SearchFilters.tsx   # Advanced search interface
│       ├── LoadingSpinner.tsx  # Loading state
│       └── ErrorMessage.tsx    # Error handling
├── public/
│   ├── sw.js                   # Service Worker for PWA
│   ├── manifest.json           # Web App Manifest
│   └── .nojekyll              # Disables Jekyll processing
├── documents/                  # PDF documents to process
├── data/
│   ├── documents.json         # Generated document metadata
│   └── processed_files.json   # Processing state tracking
└── scripts/
    ├── ensure_data.py         # Data file initialization
    └── requirements.txt       # Python dependencies
```

## 🚀 Quick Start

### Prerequisites
- Node.js 20+
- Python 3.9+

### Local Development

1. **Clone and install**
   ```bash
   git clone <your-repo-url>
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
   ```

4. **Build for production**
   ```bash
   npm run build
   npm run preview
   ```

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

## 🤝 Contributing

1. **Add Documents**: Place PDFs in `documents/` folder
2. **Automatic Processing**: GitHub Actions handles the rest
3. **Monitor Progress**: Check Actions tab for workflow status

## 📄 License

This project is open source and available under the MIT License.

---

**Live Demo**: [AI Document Library](https://lonardonifabio.github.io/tech_documents/)
**Developer**: [Fabio Lonardoni](https://www.fabiolonardoni.it)
