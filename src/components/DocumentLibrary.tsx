import React, { useState, useEffect } from 'react';
import DocumentCard from './DocumentCard';
import SearchFilters from './SearchFilters';
import LoadingSpinner from './LoadingSpinner';
import ErrorMessage from './ErrorMessage';

interface Document {
  id: string;
  filename: string;
  title?: string;
  summary: string;
  authors?: string[];
  keywords: string[];
  category: string;
  difficulty: string;
  filepath: string;
  file_size: number;
  upload_date: string;
}

const DocumentLibrary: React.FC = () => {
  const [documents, setDocuments] = useState<Document[]>([]);
  const [filteredDocs, setFilteredDocs] = useState<Document[]>([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('');
  const [selectedDifficulty, setSelectedDifficulty] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const loadDocuments = async () => {
      // Try multiple possible paths for the documents.json file
      const possiblePaths = [
        '/tech_documents/data/documents.json',
        './data/documents.json',
        'data/documents.json',
        '/data/documents.json'
      ];

      for (const path of possiblePaths) {
        try {
          console.log(`Trying to fetch from: ${path}`);
          const response = await fetch(path);
          if (response.ok) {
            const data = await response.json();
            console.log('Successfully loaded documents:', data);
            setDocuments(data);
            setFilteredDocs(data);
            setLoading(false);
            return;
          }
        } catch (err) {
          console.log(`Failed to fetch from ${path}:`, err);
        }
      }
      
      // If all paths fail, set error
      setError('Unable to load documents from any path');
      setLoading(false);
    };

    loadDocuments();
  }, []);

  // Enhanced Boolean Search Function
  const performBooleanSearch = (documents: Document[], searchTerm: string): Document[] => {
    if (!searchTerm.trim()) return documents;

    // Parse search term for boolean operators
    const parseSearchTerm = (term: string) => {
      // Split by AND, OR, NOT (case insensitive)
      const tokens = term.split(/\s+(AND|OR|NOT)\s+/i);
      const parsed = [];
      
      for (let i = 0; i < tokens.length; i++) {
        const token = tokens[i].trim();
        if (token && !['AND', 'OR', 'NOT'].includes(token.toUpperCase())) {
          // Handle quoted phrases
          const isQuoted = token.startsWith('"') && token.endsWith('"');
          const cleanToken = isQuoted ? token.slice(1, -1) : token;
          
          parsed.push({
            term: cleanToken.toLowerCase(),
            operator: i > 0 ? tokens[i-1].toUpperCase() : 'AND',
            isQuoted: isQuoted,
            isNegated: i > 0 && tokens[i-1].toUpperCase() === 'NOT'
          });
        }
      }
      
      return parsed.length > 0 ? parsed : [{ term: term.toLowerCase(), operator: 'AND', isQuoted: false, isNegated: false }];
    };

    // Check if document matches a search term
    const documentMatches = (doc: Document, searchToken: any) => {
      const { term, isQuoted } = searchToken;
      
      const searchFields = [
        doc.filename || '',
        doc.title || '',
        doc.summary || '',
        (doc.authors || []).join(' '),
        (doc.keywords || []).join(' ')
      ].map(field => field.toLowerCase());

      if (isQuoted) {
        // Exact phrase search
        return searchFields.some(field => field.includes(term));
      } else {
        // Individual word search
        const words = term.split(/\s+/);
        return words.every((word: string) => 
          searchFields.some(field => field.includes(word))
        );
      }
    };

    // Apply boolean logic
    const searchTokens = parseSearchTerm(searchTerm);
    
    return documents.filter(doc => {
      let result = true;
      let hasPositiveMatch = false;

      for (const token of searchTokens) {
        const matches = documentMatches(doc, token);
        
        if (token.isNegated) {
          if (matches) {
            result = false;
            break;
          }
        } else {
          hasPositiveMatch = hasPositiveMatch || matches;
          
          if (token.operator === 'AND') {
            result = result && matches;
          } else if (token.operator === 'OR') {
            result = result || matches;
          }
        }
      }

      // If we only have negative terms, we need at least one positive match
      const hasOnlyNegativeTerms = searchTokens.every(token => token.isNegated);
      if (hasOnlyNegativeTerms) {
        return result;
      }

      return result && hasPositiveMatch;
    });
  };

  useEffect(() => {
    let filtered = documents;

    // Apply boolean search
    if (searchTerm) {
      filtered = performBooleanSearch(filtered, searchTerm);
    }

    // Apply category filter
    if (selectedCategory) {
      filtered = filtered.filter(doc => doc.category === selectedCategory);
    }

    // Apply difficulty filter
    if (selectedDifficulty) {
      filtered = filtered.filter(doc => doc.difficulty === selectedDifficulty);
    }

    setFilteredDocs(filtered);
  }, [searchTerm, selectedCategory, selectedDifficulty, documents]);

  const categories = [...new Set(documents.map(doc => doc.category))];
  const difficulties = [...new Set(documents.map(doc => doc.difficulty))];

  if (loading) {
    return <LoadingSpinner />;
  }

  if (error) {
    return <ErrorMessage error={error} onRetry={() => window.location.reload()} />;
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 py-8">
        <header className="text-center mb-12">
          <h1 className="text-4xl font-bold text-gray-800 mb-4">
            🤖 AI & Data Science Library
          </h1>
          <p className="text-xl text-gray-600 mb-2">
            Automated collection of Artificial Intelligence and Data Science documents
          </p>
          <p className="text-sm text-gray-500">
            {documents.length} documents • Click any document to preview
          </p>
          <p className="text-sm text-gray-500">
            Developed by <a href="https://www.fabiolonardoni.it" className="text-blue-500 hover:underline">Fabio Lonardoni</a>
          </p>
        </header>

        <SearchFilters
          searchTerm={searchTerm}
          setSearchTerm={setSearchTerm}
          selectedCategory={selectedCategory}
          setSelectedCategory={setSelectedCategory}
          selectedDifficulty={selectedDifficulty}
          setSelectedDifficulty={setSelectedDifficulty}
          categories={categories}
          difficulties={difficulties}
        />

        {filteredDocs.length > 0 ? (
          <>
            <div className="mb-6 text-sm text-gray-600 bg-white px-4 py-2 rounded-lg inline-block">
              📊 Showing {filteredDocs.length} of {documents.length} documents
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
              {filteredDocs.map(doc => (
                <DocumentCard key={doc.id} doc={doc} />
              ))}
            </div>
          </>
        ) : (
          <div className="text-center py-16 bg-white rounded-lg">
            <div className="text-6xl mb-4">📭</div>
            <h3 className="text-xl font-semibold text-gray-700 mb-2">
              No documents found
            </h3>
            <p className="text-gray-500">
              Try modifying your search criteria
            </p>
          </div>
        )}
      </div>
    </div>
  );
};

export default DocumentLibrary;
