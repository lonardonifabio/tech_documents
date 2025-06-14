# AI & Data Science Document Library

An automated, AI-powered document library for AI/ML and Data Science resources with intelligent categorization and social media sharing optimization.

## 🚀 Features

### Core Functionality
- **Automated Document Processing**: AI-powered categorization and metadata extraction
- **Interactive Knowledge Graph**: Visual representation of document relationships
- **Advanced Search & Filtering**: Multi-criteria search with real-time filtering
- **PDF Preview**: In-browser document viewing with modal interface
- **Responsive Design**: Optimized for desktop, tablet, and mobile devices

### Social Media Integration
- **LinkedIn Sharing Optimization**: Enhanced Open Graph meta tags for rich previews
- **Twitter Card Support**: Optimized sharing for Twitter platform
- **Dynamic Meta Tags**: Context-aware social media previews for individual documents
- **SEO Optimization**: Structured data and canonical URLs for better search visibility

### Technical Features
- **Progressive Web App (PWA)**: Installable with offline capabilities
- **Service Worker**: Caching and performance optimization
- **Google Analytics**: Integrated tracking and analytics
- **TypeScript Support**: Type-safe development environment

## 🛠️ Technology Stack

- **Framework**: [Astro](https://astro.build/) - Static site generator with component islands
- **Frontend**: React + TypeScript for interactive components
- **Styling**: Tailwind CSS for responsive design
- **Build Tool**: Vite for fast development and building
- **Deployment**: GitHub Pages with automated CI/CD

## 📁 Project Structure

```
tech_documents/
├── src/
│   ├── components/          # React components
│   │   ├── DocumentCard.tsx
│   │   ├── DocumentLibrary.tsx
│   │   ├── KnowledgeGraph.tsx
│   │   └── ...
│   ├── layouts/
│   │   └── Layout.astro     # Main layout with meta tags
│   ├── pages/
│   │   ├── index.astro      # Main library page
│   │   ├── knowledge-graph.astro
│   │   ├── test-sharing.astro
│   │   └── document/
│   │       └── [id].astro   # Dynamic document pages
│   ├── services/
│   │   └── embedding-service.ts
│   └── types/               # TypeScript definitions
├── data/
│   └── documents.json       # Document metadata
├── documents/               # PDF files
├── public/                  # Static assets
└── scripts/                 # Build and utility scripts
```

## 🔧 Installation & Setup

### Prerequisites
- Node.js (v18 or higher)
- npm or yarn package manager

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/lonardonifabio/tech_documents.git
   cd tech_documents
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Start development server**
   ```bash
   npm run dev
   ```

4. **Open in browser**
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

## 📱 Social Media Sharing

### LinkedIn Optimization

The application includes comprehensive LinkedIn sharing optimization:

- **Open Graph Meta Tags**: Complete og: properties for rich previews
- **Image Optimization**: Properly sized cover images (1200x630px)
- **Dynamic URLs**: Context-aware canonical URLs for each page
- **Author Attribution**: LinkedIn-specific author meta tags

### Testing Social Sharing

Use the built-in test page to verify social media sharing:
```
https://lonardonifabio.github.io/tech_documents/test-sharing
```

### Debugging Tools

- **Facebook Debugger**: https://developers.facebook.com/tools/debug/
- **LinkedIn Post Inspector**: Available in LinkedIn's publishing tools
- **Twitter Card Validator**: https://cards-dev.twitter.com/validator

## 🔍 Key Components

### DocumentLibrary.tsx
Main component handling document display, search, and filtering functionality.

### KnowledgeGraph.tsx
Interactive visualization of document relationships using D3.js.

### Layout.astro
Base layout with comprehensive meta tags for social media optimization.

### Document Pages ([id].astro)
Dynamic pages for individual documents with SEO and social sharing optimization.

## 📊 Analytics & Tracking

- **Google Analytics 4**: Integrated tracking (ID: G-4EXW1VQ31D)
- **Performance Monitoring**: Core Web Vitals tracking
- **User Interaction**: Document views and search analytics

## 🌐 Deployment

The application is automatically deployed to GitHub Pages using GitHub Actions:

- **Production URL**: https://lonardonifabio.github.io/tech_documents/
- **Automatic Deployment**: On push to main branch
- **Build Process**: Astro static site generation with asset optimization

## 🔒 Security & Privacy

- **HTTPS Only**: All resources served over secure connections
- **Content Security Policy**: Implemented for XSS protection
- **Privacy Compliant**: GDPR-compliant analytics implementation

## 📈 Performance Optimization

- **Static Site Generation**: Pre-built pages for fast loading
- **Image Optimization**: Responsive images with proper sizing
- **Code Splitting**: Component-level code splitting with Astro islands
- **Caching Strategy**: Service worker implementation for offline support
- **CDN Delivery**: GitHub Pages CDN for global distribution

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Fabio Lonardoni**
- GitHub: [@lonardonifabio](https://github.com/lonardonifabio)
- Twitter: [@fabiolonardoni](https://twitter.com/fabiolonardoni)
- LinkedIn: [Fabio Lonardoni](https://linkedin.com/in/fabiolonardoni)

## 🙏 Acknowledgments

- AI/ML community for providing valuable resources
- Open source libraries and frameworks used in this project
- Contributors and users providing feedback and suggestions

## 📞 Support

For support, questions, or feature requests:
- Open an issue on GitHub
- Contact via LinkedIn or Twitter
- Check the documentation and test pages

---

**Note**: This library is continuously updated with new AI/ML documents and features. Star the repository to stay updated with the latest additions!
