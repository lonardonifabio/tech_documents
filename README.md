# AI & Data Science Document Library

An automated, AI-powered document library for AI/ML and Data Science resources with intelligent categorization, social media sharing optimization, and interactive knowledge visualization.

## 🚀 Features

### Core Functionality
- **Automated Document Processing**: AI-powered categorization and metadata extraction using Ollama
- **Interactive Knowledge Graph**: Visual representation of document relationships with D3.js
- **Advanced Search & Filtering**: Multi-criteria search with real-time filtering
- **PDF Preview Generation**: Automated preview image generation for social sharing
- **Document Modal Viewer**: In-browser document viewing with enhanced sharing options
- **Responsive Design**: Optimized for desktop, tablet, and mobile devices

### Social Media Integration
- **Enhanced LinkedIn Sharing**: Custom preview generation with document-specific content
- **Dynamic Meta Tags**: Context-aware Open Graph tags for rich social media previews
- **Twitter Card Support**: Optimized sharing for Twitter platform
- **Mobile Native Sharing**: Uses native sharing APIs on mobile devices
- **SEO Optimization**: Structured data and canonical URLs for better search visibility

### Technical Features
- **Progressive Web App (PWA)**: Installable with offline capabilities
- **Service Worker**: Caching and performance optimization
- **Google Analytics**: Integrated tracking and analytics
- **TypeScript Support**: Type-safe development environment
- **Canvas-based Preview Generation**: Dynamic document preview images

## 🛠️ Technology Stack

- **Framework**: [Astro](https://astro.build/) - Static site generator with component islands
- **Frontend**: React + TypeScript for interactive components
- **Styling**: Tailwind CSS for responsive design
- **Build Tool**: Vite for fast development and building
- **AI Processing**: Ollama for document analysis and categorization
- **Visualization**: D3.js for knowledge graph rendering
- **Image Generation**: HTML5 Canvas for dynamic preview creation
- **Deployment**: GitHub Pages with automated CI/CD

## 📁 Project Structure

```
tech_documents/
├── .github/workflows/           # GitHub Actions CI/CD
│   └── deploy.yml              # Automated deployment pipeline
├── src/
│   ├── components/             # React components
│   │   ├── DocumentCard.tsx    # Individual document display
│   │   ├── DocumentLibrary.tsx # Main library interface
│   │   ├── DocumentLibraryWithGraph.tsx # Library with graph integration
│   │   ├── ErrorBoundary.tsx   # Error handling wrapper
│   │   ├── ErrorMessage.tsx    # Error display component
│   │   ├── KnowledgeGraph.tsx  # Interactive D3.js visualization
│   │   ├── LinkedInPreviewDemo.tsx # Preview generation demo
│   │   ├── LoadingSpinner.tsx  # Loading state component
│   │   ├── PDFModal.tsx        # Document viewer modal
│   │   └── SearchFilters.tsx   # Search and filter controls
│   ├── config/                 # Configuration files
│   ├── js/                     # JavaScript utilities
│   │   ├── app.js             # Main application logic
│   │   └── translations.js    # Internationalization
│   ├── layouts/
│   │   └── Layout.astro       # Main layout with enhanced meta tags
│   ├── pages/
│   │   ├── index.astro        # Main library page
│   │   ├── knowledge-graph.astro # Knowledge graph page
│   │   ├── linkedin-sharing-test.astro # LinkedIn sharing test
│   │   ├── test-preview.astro  # Preview generation test
│   │   ├── test-sharing.astro  # Social sharing test
│   │   ├── document/
│   │   │   └── [id].astro     # Dynamic document pages
│   │   ├── preview/
│   │   │   └── [id].jpg.ts    # Dynamic preview image generation
│   │   └── share/
│   │       └── [id].astro     # Social sharing pages
│   ├── services/              # Business logic services
│   │   ├── embedding-service.ts # Document embedding generation
│   │   ├── linkedin-sharing-service.ts # Enhanced LinkedIn sharing
│   │   └── preview-generator.ts # Canvas-based preview generation
│   ├── types/                 # TypeScript definitions
│   │   ├── document-library.d.ts # Document type definitions
│   │   └── knowledge-graph.ts  # Graph type definitions
│   ├── env.d.ts              # Environment type definitions
│   ├── index.html            # HTML template
│   ├── io_ds.png            # Application icon
│   └── readme.me            # Source readme
├── data/
│   ├── documents.json        # Document metadata and AI analysis
│   ├── processed_files.json  # Processing status tracking
│   ├── Official/            # Official document sources
│   └── test/               # Test data
├── documents/              # PDF document collection (1100+ files)
├── public/                # Static assets
│   ├── .nojekyll          # GitHub Pages configuration
│   ├── favicon.svg        # Site favicon
│   ├── manifest.json      # PWA manifest
│   ├── og-image.jpg       # Default Open Graph image
│   ├── og-image.svg       # SVG version of OG image
│   ├── sw.js             # Service worker
│   └── test-og.html      # Open Graph testing page
├── scripts/               # Python automation scripts
│   ├── ensure_data.py     # Data validation and setup
│   ├── fixed_ollama_processor.py # Stable Ollama processing
│   ├── generate_knowledge_graph.py # Graph data generation
│   ├── generate_previews_simple.py # Simple preview generation
│   ├── generate_previews.py # Advanced preview generation
│   ├── incremental_ollama_processor.py # Incremental processing
│   ├── ollama_port_manager.py # Port management utility
│   ├── pdf_preview_generator.py # PDF preview extraction
│   ├── requirements.txt   # Python dependencies
│   ├── start_ollama_service.py # Cross-platform Ollama startup
│   └── start_ollama_service.sh # Bash Ollama startup script
├── astro.config.mjs       # Astro configuration
├── package.json          # Node.js dependencies and scripts
├── package-lock.json     # Dependency lock file
├── tailwind.config.mjs   # Tailwind CSS configuration
├── tsconfig.json         # TypeScript configuration
├── .gitignore           # Git ignore rules
└── README.md            # This file
```

## 🔧 Installation & Setup

### Prerequisites
- Node.js (v18 or higher)
- Python 3.8+ (for AI processing)
- Ollama (for document analysis)
- npm or yarn package manager

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/lonardonifabio/tech_documents.git
   cd tech_documents
   ```

2. **Install Node.js dependencies**
   ```bash
   npm install
   ```

3. **Install Python dependencies**
   ```bash
   pip install -r scripts/requirements.txt
   ```

4. **Start Ollama service**
   ```bash
   # Using the provided script (recommended)
   python scripts/start_ollama_service.py
   # Or manually
   ollama serve &
   ```

5. **Start development server**
   ```bash
   npm run dev
   ```

6. **Open in browser**
   ```
   http://localhost:4321
   ```

### Build for Production

```bash
# Build static site
npm run build

# Preview production build
npm run preview
```

## 🤖 AI Document Processing

### Ollama Integration

The library uses Ollama for intelligent document analysis:

- **Automated Categorization**: AI-powered classification of documents
- **Metadata Extraction**: Automatic extraction of key information
- **Summary Generation**: AI-generated document summaries
- **Keyword Identification**: Intelligent keyword extraction
- **Relationship Mapping**: Document similarity and relationship analysis

### Processing Scripts

- **`fixed_ollama_processor.py`**: Stable processing with error handling
- **`incremental_ollama_processor.py`**: Process only new/updated documents
- **`ollama_port_manager.py`**: Manages Ollama service port conflicts

### Troubleshooting Ollama Service

If you encounter "address already in use" errors:

```bash
# Use the automated fix script
python scripts/start_ollama_service.py

# Or manual fix
pkill -f "ollama serve"
lsof -ti:11434 | xargs kill -9
ollama serve &
```

## 📱 Enhanced Social Media Sharing

### LinkedIn Optimization

The application includes comprehensive LinkedIn sharing with:

- **Custom Preview Generation**: Document-specific preview images using Canvas
- **Rich Content Creation**: Enhanced post content with key insights
- **Mobile Native Sharing**: Uses native sharing APIs on mobile devices
- **Multiple Sharing Options**: Preview sharing and document attachment sharing

### Preview Generation Features

- **Category-Based Styling**: Different visual themes for each document category
- **Dynamic Content**: Includes title, category, difficulty, and keywords
- **LinkedIn-Optimized**: 1200x630px images for optimal display
- **Caching System**: Efficient preview generation and storage

### Open Graph Meta Tags

Complete Open Graph implementation for rich social media previews:

```html
<!-- Enhanced Open Graph for LinkedIn sharing -->
<meta property="og:title" content="Document Title">
<meta property="og:description" content="Document description">
<meta property="og:type" content="website">
<meta property="og:url" content="https://lonardonifabio.github.io/tech_documents/document/123">
<meta property="og:image" content="https://example.com/preview.jpg">
<meta property="og:image:secure_url" content="https://example.com/preview.jpg">
<meta property="og:image:type" content="image/jpeg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:site_name" content="AI & Data Science Document Library">
```

### Testing Social Sharing

Use the built-in test pages:
- `/test-sharing` - General social sharing test
- `/linkedin-sharing-test` - LinkedIn-specific testing
- `/test-preview` - Preview generation testing

## 🔍 Key Components

### DocumentLibrary.tsx
Main component handling document display, search, and filtering functionality with real-time updates.

### KnowledgeGraph.tsx
Interactive visualization of document relationships using D3.js with:
- Force-directed layout
- Category-based clustering
- Interactive node exploration
- Zoom and pan capabilities

### PDFModal.tsx
Enhanced document viewer with:
- PDF preview display
- Multiple LinkedIn sharing options
- Document download functionality
- Mobile-optimized interface

### Preview Generation Services

#### preview-generator.ts
Canvas-based preview image generation with:
- Category-specific styling
- Dynamic text rendering
- Gradient backgrounds
- Icon integration

#### linkedin-sharing-service.ts
Enhanced LinkedIn sharing with:
- Multiple sharing modes
- Mobile optimization
- Native sharing API integration
- Fallback strategies

## 📊 Analytics & Performance

### Tracking
- **Google Analytics 4**: Comprehensive user behavior tracking
- **Performance Monitoring**: Core Web Vitals and loading metrics
- **Social Sharing Analytics**: Track sharing performance and engagement

### Performance Optimizations
- **Static Site Generation**: Pre-built pages for fast loading
- **Image Optimization**: Responsive images with proper sizing
- **Code Splitting**: Component-level code splitting with Astro islands
- **Service Worker**: Offline support and caching strategy
- **CDN Delivery**: GitHub Pages CDN for global distribution

## 🌐 Deployment

### Automated Deployment

The application uses GitHub Actions for automated deployment:

```yaml
# .github/workflows/deploy.yml highlights
- Install system dependencies (ImageMagick, LibreOffice)
- Configure ImageMagick policies for PDF processing
- Install Python and Node.js dependencies
- Start Ollama service with port management
- Generate document previews
- Build Astro static site
- Deploy to GitHub Pages
```

### Production URLs
- **Main Site**: https://lonardonifabio.github.io/tech_documents/
- **Knowledge Graph**: https://lonardonifabio.github.io/tech_documents/knowledge-graph
- **Sharing Test**: https://lonardonifabio.github.io/tech_documents/test-sharing

## 🔒 Security & Privacy

- **HTTPS Only**: All resources served over secure connections
- **Content Security Policy**: XSS protection implementation
- **Privacy Compliant**: GDPR-compliant analytics
- **Secure Image Processing**: Safe PDF processing with ImageMagick policies

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines

- Follow TypeScript best practices
- Use Tailwind CSS for styling
- Implement proper error handling
- Add tests for new features
- Update documentation as needed

## 🐛 Troubleshooting

### Common Issues

#### Ollama Service Issues
```bash
# Port already in use
python scripts/start_ollama_service.py

# Service not responding
curl -s http://127.0.0.1:11434/api/tags
```

#### Build Issues
```bash
# Clear cache and rebuild
rm -rf node_modules/.astro
npm run build
```

#### Preview Generation Issues
```bash
# Test preview generation
python scripts/generate_previews.py
```

### Debug Tools

- **LinkedIn Post Inspector**: Test LinkedIn sharing
- **Facebook Debugger**: Validate Open Graph tags
- **Twitter Card Validator**: Test Twitter sharing
- **Built-in Test Pages**: Use `/test-sharing` and related pages

## 📈 Performance Metrics

### Current Statistics
- **1100+ Documents**: Comprehensive AI/ML resource collection
- **Automated Processing**: AI-powered categorization and analysis
- **Social Optimization**: Enhanced sharing across all major platforms
- **Mobile-First**: Responsive design with native sharing support

### Loading Performance
- **First Contentful Paint**: < 1.5s
- **Largest Contentful Paint**: < 2.5s
- **Cumulative Layout Shift**: < 0.1
- **Time to Interactive**: < 3s

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Fabio Lonardoni**
- Website: [Fabio Lonardoni](https://www.fabiolonardoni.it)
- LinkedIn: [Fabio Lonardoni](https://www.linkedin.com/in/fabio-lonardoni-innovation-manager/)

## 🙏 Acknowledgments

- AI/ML community for providing valuable resources
- Ollama team for the excellent local AI processing capabilities
- Open source libraries and frameworks used in this project
- Contributors and users providing feedback and suggestions

## 📞 Support

For support, questions, or feature requests:
- Open an issue on GitHub
- Contact via LinkedIn
- Check the documentation and test pages
- Use the built-in debugging tools

---

**Note**: This library is continuously updated with new AI/ML documents and features. The AI processing pipeline automatically categorizes and analyzes new documents, while the enhanced social sharing ensures optimal presentation across all platforms. Star the repository to stay updated with the latest additions!
