# Interactive Knowledge Graph Component

This document describes the interactive knowledge graph component that visualizes document relationships using AI-generated embeddings and D3.js.

## Overview

The knowledge graph component provides an interactive visualization of document relationships based on semantic similarity. It uses Mistral AI (via Ollama) to generate embeddings locally and creates a network graph where:

- **Nodes** represent documents (size = file size, color = AI-detected topic)
- **Links** connect semantically similar documents
- **Clusters** group documents by AI-detected topics

## Features

### ✨ Core Features
- **Interactive D3.js visualization** with zoom, pan, and drag functionality
- **AI-powered embeddings** using Mistral via Ollama (with fallback)
- **Topic detection and clustering** with color-coded nodes
- **Semantic similarity connections** between related documents
- **Hover previews** showing document summaries
- **Click-to-open** documents in PDF viewer
- **Topic filtering** to focus on specific areas
- **Offline support** via service worker caching
- **Bundle size optimized** (<50KB additional)

### 🎯 Interactive Elements
- **Hover**: Shows document preview tooltip
- **Click**: Opens document in PDF viewer
- **Drag**: Repositions nodes in the graph
- **Zoom/Pan**: Navigate the graph space
- **Topic Filters**: Show/hide documents by topic

## Architecture

### Components Structure
```
src/
├── components/
│   ├── KnowledgeGraph.tsx          # Main D3.js visualization component
│   └── DocumentLibraryWithGraph.tsx # Wrapper with view toggle
├── services/
│   └── embedding-service.ts        # AI embedding generation service
├── types/
│   └── knowledge-graph.ts          # TypeScript type definitions
└── pages/
    ├── index.astro                 # Main page with library view
    └── knowledge-graph.astro       # Direct knowledge graph page
```

### Service Worker
```
public/
└── sw.js                          # Offline caching and PWA support
```

## AI Integration

### Ollama Integration
The component integrates with Ollama running locally on `http://localhost:11434`:

```typescript
// Check Ollama connection
const connected = await embeddingService.checkOllamaConnection();

// Generate embeddings
const embedding = await embeddingService.generateEmbedding(text);

// Detect topics
const topic = await embeddingService.detectTopic(document);
```

### Fallback System
When Ollama is not available, the system uses:
- **Hash-based embeddings** for similarity calculations
- **Keyword-based topic detection** using predefined categories
- **Local caching** to avoid recomputation

### Topic Categories
The AI detects documents into these categories:
- Machine Learning
- Deep Learning
- Data Science
- AI Ethics
- Business Intelligence
- Natural Language Processing
- Computer Vision
- Reinforcement Learning
- Statistics
- Programming
- Business Strategy
- Other

## Usage

### Basic Implementation
```tsx
import KnowledgeGraph from './components/KnowledgeGraph';

<KnowledgeGraph
  documents={documents}
  width={800}
  height={600}
  onNodeClick={(node) => openDocument(node)}
  onNodeHover={(node) => showPreview(node)}
/>
```

### With Document Library Toggle
```tsx
import DocumentLibraryWithGraph from './components/DocumentLibraryWithGraph';

<DocumentLibraryWithGraph initialView="graph" />
```

## Configuration

### Embedding Service Configuration
```typescript
// In embedding-service.ts
private ollamaUrl = 'http://localhost:11434';
private model = 'mistral';
```

### Graph Visualization Settings
```typescript
// In KnowledgeGraph.tsx
const similarityThreshold = 0.3;  // Minimum similarity for connections
const nodeRadius = Math.sqrt(fileSize / 100000) + 8;  // Node size calculation
```

### Force Simulation Parameters
```typescript
.force('charge', d3.forceManyBody().strength(-300))
.force('center', d3.forceCenter(width / 2, height / 2))
.force('collision', d3.forceCollide().radius(25))
```

## Performance Optimizations

### Bundle Size Optimization
- **Tree-shaking**: Only imports used D3 modules
- **Code splitting**: Lazy loading of components
- **Compression**: Gzip compression for assets
- **Caching**: Service worker caches resources

### Runtime Performance
- **Embedding caching**: Stores generated embeddings in localStorage
- **Similarity calculation**: Optimized cosine similarity computation
- **Force simulation**: Efficient D3.js physics simulation
- **Debounced interactions**: Prevents excessive re-renders

### Memory Management
- **Cleanup**: Proper D3 selection cleanup on unmount
- **Event listeners**: Removed on component destruction
- **Simulation**: Stopped when component unmounts

## Offline Support

### Service Worker Features
- **Static asset caching**: CSS, JS, fonts, images
- **Dynamic content caching**: Documents and embeddings
- **Cache strategies**: 
  - Cache-first for static assets
  - Network-first for data
  - Stale-while-revalidate for pages

### PWA Capabilities
- **Installable**: Can be installed as a PWA
- **Offline functionality**: Works without internet connection
- **Background sync**: Processes embeddings when online

## Development

### Prerequisites
```bash
# Install dependencies
npm install d3 @types/d3

# Ensure Ollama is running (optional)
ollama serve
ollama pull mistral
```

### Local Development
```bash
# Start development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

### Testing Ollama Integration
1. Install Ollama: https://ollama.ai/
2. Pull Mistral model: `ollama pull mistral`
3. Start Ollama: `ollama serve`
4. Component will automatically detect and use Ollama

## Deployment

### Astro SSG Compatibility
The component is fully compatible with Astro's static site generation:

```astro
---
import DocumentLibraryWithGraph from '../components/DocumentLibraryWithGraph';
---

<Layout title="Knowledge Graph">
  <DocumentLibraryWithGraph client:load />
</Layout>
```

### GitHub Pages Deployment
Configured for GitHub Pages with proper base paths:
- Service worker: `/tech_documents/sw.js`
- Data files: `/tech_documents/data/documents.json`
- Assets: `/tech_documents/assets/`

## API Reference

### KnowledgeGraph Props
```typescript
interface KnowledgeGraphProps {
  documents: DocumentNode[];
  width?: number;
  height?: number;
  onNodeClick?: (node: DocumentNode) => void;
  onNodeHover?: (node: DocumentNode | null) => void;
}
```

### EmbeddingService Methods
```typescript
class EmbeddingService {
  checkOllamaConnection(): Promise<boolean>
  generateEmbedding(text: string): Promise<number[]>
  detectTopic(document: DocumentNode): Promise<string>
  calculateSimilarity(emb1: number[], emb2: number[]): number
  processDocuments(docs: DocumentNode[]): Promise<EmbeddingData>
  saveEmbeddings(embeddings: EmbeddingData): Promise<void>
  loadCachedEmbeddings(): EmbeddingData | null
}
```

## Troubleshooting

### Common Issues

1. **Ollama Connection Failed**
   - Ensure Ollama is running: `ollama serve`
   - Check port 11434 is available
   - Component will use fallback embeddings

2. **Large Bundle Size**
   - Check D3 imports are tree-shaken
   - Verify only necessary modules are imported
   - Use production build for accurate size

3. **Performance Issues**
   - Reduce similarity threshold for fewer connections
   - Limit number of documents processed
   - Clear embedding cache if corrupted

4. **Service Worker Issues**
   - Check browser console for SW errors
   - Verify correct paths for GitHub Pages
   - Clear browser cache and re-register

### Debug Mode
Enable debug logging:
```typescript
// In embedding-service.ts
console.log('Ollama connected:', connected);
console.log('Generated embedding:', embedding.length);
console.log('Detected topic:', topic);
```

## Future Enhancements

### Planned Features
- **3D visualization** using Three.js
- **Advanced clustering** algorithms (t-SNE, UMAP)
- **Real-time collaboration** features
- **Export capabilities** (PNG, SVG, JSON)
- **Advanced filtering** by multiple criteria
- **Search within graph** functionality

### Performance Improvements
- **WebGL rendering** for large datasets
- **Virtual scrolling** for node lists
- **Web Workers** for embedding computation
- **IndexedDB** for large-scale caching

## License

This component is part of the AI Document Library project and follows the same license terms.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Implement changes with tests
4. Submit a pull request

For questions or issues, please open a GitHub issue.
