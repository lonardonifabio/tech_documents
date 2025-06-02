import React, { useState, useEffect } from 'react';

const DocumentLibrary = () => {
  const [documents, setDocuments] = useState([]);
  const [filteredDocs, setFilteredDocs] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('');
  const [selectedDifficulty, setSelectedDifficulty] = useState('');
  const [expandedDocs, setExpandedDocs] = useState(new Set());
  const [expandedAuthors, setExpandedAuthors] = useState(new Set());

  useEffect(() => {
    // Load documents from GitHub Pages
    fetch('/dist/data/documents.json')
      .then(response => response.json())
      .then(data => {
        setDocuments(data);
        setFilteredDocs(data);
      })
      .catch(error => console.error('Error loading documents:', error));
  }, []);

  useEffect(() => {
    let filtered = documents;

    if (searchTerm) {
      filtered = filtered.filter(doc =>
        doc.filename.toLowerCase().includes(searchTerm.toLowerCase()) ||
        doc.summary.toLowerCase().includes(searchTerm.toLowerCase()) ||
        doc.keywords.some(keyword =>
          keyword.toLowerCase().includes(searchTerm.toLowerCase())
        ) ||
        (doc.authors && doc.authors.some(author =>
          author.toLowerCase().includes(searchTerm.toLowerCase())
        ))
      );
    }

    if (selectedCategory) {
      filtered = filtered.filter(doc => doc.category === selectedCategory);
    }

    if (selectedDifficulty) {
      filtered = filtered.filter(doc => doc.difficulty === selectedDifficulty);
    }

    setFilteredDocs(filtered);
  }, [searchTerm, selectedCategory, selectedDifficulty, documents]);

  const categories = [...new Set(documents.map(doc => doc.category))];
  const difficulties = [...new Set(documents.map(doc => doc.difficulty))];

  const toggleExpanded = (docId) => {
    const newExpanded = new Set(expandedDocs);
    if (newExpanded.has(docId)) {
      newExpanded.delete(docId);
    } else {
      newExpanded.add(docId);
    }
    setExpandedDocs(newExpanded);
  };

  const toggleExpandedAuthors = (docId) => {
    const newExpanded = new Set(expandedAuthors);
    if (newExpanded.has(docId)) {
      newExpanded.delete(docId);
    } else {
      newExpanded.add(docId);
    }
    setExpandedAuthors(newExpanded);
  };

  const truncateText = (text, maxLength = 150) => {
    if (text.length <= maxLength) return text;
    return text.substring(0, maxLength) + '...';
  };

  const renderAuthors = (doc) => {
    if (!doc.authors || doc.authors.length === 0) {
      return <span className="text-gray-400 text-xs">No author information</span>;
    }

    const isExpanded = expandedAuthors.has(doc.id);
    const maxAuthorsToShow = 2;
    const shouldTruncate = doc.authors.length > maxAuthorsToShow;

    if (!shouldTruncate) {
      // If 2 or fewer authors, show all without truncation
      return (
        <div className="text-xs text-gray-600">
          <span className="font-medium">Authors: </span>
          <span>{doc.authors.join(', ')}</span>
        </div>
      );
    }

    // More than 2 authors - implement truncation
    const authorsToShow = isExpanded ? doc.authors : doc.authors.slice(0, maxAuthorsToShow);
    const authorsText = authorsToShow.join(', ');

    return (
      <div className="text-xs text-gray-600">
        <span className="font-medium">Authors: </span>
        <span>{authorsText}</span>
        {!isExpanded && <span> and {doc.authors.length - maxAuthorsToShow} more</span>}
        <button
          onClick={() => toggleExpandedAuthors(doc.id)}
          className="text-blue-600 hover:text-blue-800 ml-1 font-medium"
        >
          {isExpanded ? 'Show less' : 'Show more'}
        </button>
      </div>
    );
  };

  const getDocumentPreviewUrl = (filepath) => {
    const githubRawUrl = `https://raw.githubusercontent.com/lonardonifabio/tech_documents/main/${filepath}`;
    return `https://mozilla.github.io/pdf.js/web/viewer.html?file=${encodeURIComponent(githubRawUrl)}`;
  };

  const getGitHubPreviewUrl = (filepath) => {
    return `https://github.com/lonardonifabio/tech_documents/blob/main/${filepath}`;
  };

  return (
    <div className="max-w-6xl mx-auto p-6">
      <h1 className="text-3xl font-bold mb-8">AI & Data Science Document Library</h1>

      {/* Search filters */}
      <div className="mb-8 space-y-4">
        <input
          type="text"
          placeholder="Search documents, keywords, authors..."
          className="w-full p-3 border rounded-lg"
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
        />

        <div className="flex space-x-4">
          <select
            className="p-2 border rounded"
            value={selectedCategory}
            onChange={(e) => setSelectedCategory(e.target.value)}
          >
            <option value="">All categories</option>
            {categories.map(cat => (
              <option key={cat} value={cat}>{cat}</option>
            ))}
          </select>

          <select
            className="p-2 border rounded"
            value={selectedDifficulty}
            onChange={(e) => setSelectedDifficulty(e.target.value)}
          >
            <option value="">All levels</option>
            {difficulties.map(diff => (
              <option key={diff} value={diff}>{diff}</option>
            ))}
          </select>
        </div>
      </div>

      {/* Document grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {filteredDocs.map(doc => {
          const isExpanded = expandedDocs.has(doc.id);
          const shouldTruncate = doc.summary.length > 150;
          
          return (
            <div key={doc.id} className="border rounded-lg overflow-hidden hover:shadow-lg transition-shadow">
              {/* Document Preview - GitHub Compatible */}
              <div className="relative h-48 bg-gray-100 flex items-center justify-center">
                {/* Document icon and info */}
                <div className="flex flex-col items-center justify-center text-gray-600 p-4">
                  <svg className="w-16 h-16 mb-3 text-red-500" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M4 4a2 2 0 012-2h4.586A2 2 0 0112 2.586L15.414 6A2 2 0 0116 7.414V16a2 2 0 01-2 2H6a2 2 0 01-2-2V4zm2 6a1 1 0 011-1h6a1 1 0 110 2H7a1 1 0 01-1-1zm1 3a1 1 0 100 2h6a1 1 0 100-2H7z" clipRule="evenodd" />
                  </svg>
                  <span className="text-sm font-medium text-center px-2 line-clamp-2">{doc.title || doc.filename}</span>
                  <span className="text-xs text-gray-500 mt-1">{(doc.file_size / 1024 / 1024).toFixed(1)} MB</span>
                </div>
                
                {/* Preview overlay with GitHub-compatible actions */}
                <div className="absolute inset-0 bg-black bg-opacity-0 hover:bg-opacity-20 transition-all duration-200 flex items-center justify-center">
                  <div className="opacity-0 hover:opacity-100 flex space-x-2 transition-opacity">
                    <a
                      href={getDocumentPreviewUrl(doc.filepath)}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="bg-blue-600 text-white px-3 py-1 rounded text-sm font-medium hover:bg-blue-700"
                    >
                      View PDF
                    </a>
                    <a
                      href={getGitHubPreviewUrl(doc.filepath)}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="bg-gray-800 text-white px-3 py-1 rounded text-sm font-medium hover:bg-gray-900"
                    >
                      GitHub
                    </a>
                  </div>
                </div>
              </div>

              <div className="p-4">
                <h3 className="font-semibold text-lg mb-2 line-clamp-2">{doc.title || doc.filename}</h3>
                
                {/* Authors */}
                <div className="mb-2">
                  {renderAuthors(doc)}
                </div>
                
                {/* Summary */}
                <div className="text-gray-600 text-sm mb-3">
                  <p>
                    {isExpanded ? doc.summary : truncateText(doc.summary)}
                  </p>
                  {shouldTruncate && (
                    <button
                      onClick={() => toggleExpanded(doc.id)}
                      className="text-blue-600 hover:text-blue-800 text-xs mt-1 font-medium"
                    >
                      {isExpanded ? 'Show less' : 'Show more'}
                    </button>
                  )}
                </div>

                {/* Keywords */}
                <div className="flex flex-wrap gap-1 mb-3">
                  {doc.keywords.slice(0, 3).map(keyword => (
                    <span key={keyword} className="bg-blue-100 text-blue-800 px-2 py-1 rounded text-xs">
                      {keyword}
                    </span>
                  ))}
                  {doc.keywords.length > 3 && (
                    <span className="text-gray-500 text-xs px-2 py-1">
                      +{doc.keywords.length - 3} more
                    </span>
                  )}
                </div>

                {/* Category and Difficulty */}
                <div className="flex justify-between items-center text-sm text-gray-500 mb-3">
                  <span className="bg-green-100 text-green-800 px-2 py-1 rounded">
                    {doc.category}
                  </span>
                  <span className="bg-orange-100 text-orange-800 px-2 py-1 rounded">
                    {doc.difficulty}
                  </span>
                </div>

                {/* Actions */}
                <div className="flex space-x-2">
                  <a
                    href={getDocumentPreviewUrl(doc.filepath)}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="flex-1 text-center bg-blue-600 text-white px-3 py-2 rounded text-sm hover:bg-blue-700 transition-colors"
                  >
                    View PDF
                  </a>
                  <a
                    href={getGitHubPreviewUrl(doc.filepath)}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="flex-1 text-center border border-gray-300 text-gray-700 px-3 py-2 rounded text-sm hover:bg-gray-50 transition-colors"
                  >
                    GitHub
                  </a>
                </div>
              </div>
            </div>
          );
        })}
      </div>

      {filteredDocs.length === 0 && (
        <div className="text-center py-8 text-gray-500">
          No documents found with the current search criteria.
        </div>
      )}
    </div>
  );
};

export default DocumentLibrary;
