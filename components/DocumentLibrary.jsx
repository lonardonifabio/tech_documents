import React, { useState, useEffect } from 'react';

const DocumentLibrary = () => {
  const [documents, setDocuments] = useState([]);
  const [filteredDocs, setFilteredDocs] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('');
  const [selectedDifficulty, setSelectedDifficulty] = useState('');
  const [expandedDocs, setExpandedDocs] = useState(new Set());

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
        )
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

  const truncateText = (text, maxLength = 100) => {
    if (text.length <= maxLength) return text;
    return text.substring(0, maxLength) + '...';
  };

  return (
    <div className="max-w-6xl mx-auto p-6">
      <h1 className="text-3xl font-bold mb-8">AI & Data Science Document Library</h1>

      {/* Search filters */}
      <div className="mb-8 space-y-4">
        <input
          type="text"
          placeholder="Search documents, keywords..."
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
          const shouldTruncate = doc.summary.length > 100;
          
          return (
            <div key={doc.id} className="border rounded-lg p-4 hover:shadow-lg transition-shadow">
              <h3 className="font-semibold text-lg mb-2">{doc.filename}</h3>
              
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

              <div className="flex flex-wrap gap-1 mb-3">
                {doc.keywords.map(keyword => (
                  <span key={keyword} className="bg-blue-100 text-blue-800 px-2 py-1 rounded text-xs">
                    {keyword}
                  </span>
                ))}
              </div>

              <div className="flex justify-between items-center text-sm text-gray-500">
                <span className="bg-green-100 text-green-800 px-2 py-1 rounded">
                  {doc.category}
                </span>
                <span className="bg-orange-100 text-orange-800 px-2 py-1 rounded">
                  {doc.difficulty}
                </span>
              </div>

              <div className="mt-3">
                <a
                  href={`https://github.com/lonardonifabio/tech_documents/blob/main/${doc.filepath}`}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-blue-600 hover:underline text-sm"
                >
                  View document →
                </a>
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
