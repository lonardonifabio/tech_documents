import React, { useState, useEffect } from 'react';
import DocumentChat from './DocumentChat';
import ErrorBoundary from './ErrorBoundary';

interface Document {
  id: string;
  filename: string;
  title?: string;
  summary: string;
  authors?: string[];
  keywords: string[];
  key_concepts?: string[];
  category: string;
  difficulty: string;
  filepath: string;
  file_size: number;
  upload_date: string;
}

interface PDFModalProps {
  doc: Document;
  isOpen: boolean;
  onClose: () => void;
}

const PDFModal: React.FC<PDFModalProps> = ({ doc, isOpen, onClose }) => {
  const [previewError, setPreviewError] = useState(false);
  const [expandedSummary, setExpandedSummary] = useState(false);
  
  const getPDFPreviewUrl = (doc: Document): string => {
    // Use raw.githubusercontent.com for better CORS compatibility
    const rawGithubUrl = `https://raw.githubusercontent.com/lonardonifabio/tech_documents/main/${doc.filepath}`;
    return `https://mozilla.github.io/pdf.js/web/viewer.html?file=${encodeURIComponent(rawGithubUrl)}`;
  };
  
  const handleOverlayClick = (e: React.MouseEvent<HTMLDivElement>) => {
    if (e.target === e.currentTarget) {
      onClose();
    }
  };
  
  const handleKeyDown = (e: KeyboardEvent) => {
    if (e.key === 'Escape') {
      onClose();
    }
  };

  const truncateText = (text: string, maxLength: number = 200): string => {
    if (!text || text.length <= maxLength) return text || '';
    return text.substring(0, maxLength) + '...';
  };

  const formatFileSize = (bytes: number): string => {
    const mb = (bytes / (1024 * 1024)).toFixed(1);
    return `${mb} MB`;
  };

  const formatDate = (dateString: string): string => {
    try {
      const date = new Date(dateString);
      return date.toLocaleDateString('en-US', { 
        year: 'numeric', 
        month: 'short', 
        day: 'numeric' 
      });
    } catch {
      return 'Unknown date';
    }
  };
  
  useEffect(() => {
    if (isOpen) {
      document.addEventListener('keydown', handleKeyDown);
      document.body.style.overflow = 'hidden';
      
      return () => {
        document.removeEventListener('keydown', handleKeyDown);
        document.body.style.overflow = 'unset';
      };
    }
  }, [isOpen]);
  
  if (!isOpen) return null;
  
  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center p-4">
      <div className="bg-white rounded-lg shadow-xl w-full max-w-7xl h-full max-h-[90vh] flex flex-col">
        {/* Header */}
        <div className="flex items-center justify-between p-4 border-b">
          <h2 className="text-xl font-semibold text-gray-800 truncate pr-4">
            {doc.title || doc.filename}
          </h2>
          <button
            onClick={onClose}
            className="text-gray-500 hover:text-gray-700 text-2xl font-bold w-8 h-8 flex items-center justify-center rounded-full hover:bg-gray-100"
            title="Close preview (ESC)"
          >
            ×
          </button>
        </div>
        
        {/* Main Content */}
        <div className="flex-1 flex overflow-hidden">
          {/* Left Sidebar - Document Information */}
          <div className="w-80 bg-gray-50 border-r overflow-y-auto p-4 space-y-4">
            {/* Title */}
            <div>
              <h3 className="text-sm font-semibold text-gray-700 mb-2">📄 Title</h3>
              <p className="text-sm text-gray-900 leading-relaxed">
                {doc.title || doc.filename || 'No title available'}
              </p>
            </div>

            {/* Authors */}
            <div>
              <h3 className="text-sm font-semibold text-gray-700 mb-2">👥 Authors</h3>
              {doc.authors && doc.authors.length > 0 ? (
                <div className="space-y-1">
                  {doc.authors.map((author, index) => (
                    <p key={index} className="text-sm text-gray-900">
                      {author}
                    </p>
                  ))}
                </div>
              ) : (
                <p className="text-sm text-gray-500 italic">No author information available</p>
              )}
            </div>

            {/* Summary */}
            <div>
              <h3 className="text-sm font-semibold text-gray-700 mb-2">📝 Summary</h3>
              {doc.summary ? (
                <div>
                  <p className="text-sm text-gray-900 leading-relaxed">
                    {expandedSummary ? doc.summary : truncateText(doc.summary, 200)}
                  </p>
                  {doc.summary.length > 200 && (
                    <button
                      onClick={() => setExpandedSummary(!expandedSummary)}
                      className="text-blue-600 hover:text-blue-800 text-sm mt-2 font-medium"
                    >
                      {expandedSummary ? 'Show less' : 'Read more'}
                    </button>
                  )}
                </div>
              ) : (
                <p className="text-sm text-gray-500 italic">No summary available</p>
              )}
            </div>

            {/* Key Concepts */}
            <div>
              <h3 className="text-sm font-semibold text-gray-700 mb-2">💡 Key Concepts</h3>
              {doc.key_concepts && doc.key_concepts.length > 0 ? (
                <div className="space-y-2">
                  {doc.key_concepts.map((concept, index) => (
                    <div key={index} className="bg-white p-2 rounded border-l-2 border-blue-500">
                      <p className="text-sm text-gray-900 leading-relaxed">
                        {concept}
                      </p>
                    </div>
                  ))}
                </div>
              ) : (
                <p className="text-sm text-gray-500 italic">No key concepts available</p>
              )}
            </div>

            {/* Keywords */}
            <div>
              <h3 className="text-sm font-semibold text-gray-700 mb-2">🏷️ Keywords</h3>
              {doc.keywords && doc.keywords.length > 0 ? (
                <div className="flex flex-wrap gap-1">
                  {doc.keywords.map((keyword, index) => (
                    <span
                      key={index}
                      className="bg-blue-100 text-blue-800 px-2 py-1 rounded-full text-xs font-medium"
                    >
                      {keyword}
                    </span>
                  ))}
                </div>
              ) : (
                <p className="text-sm text-gray-500 italic">No keywords available</p>
              )}
            </div>

            {/* Document Metadata */}
            <div className="pt-4 border-t">
              <h3 className="text-sm font-semibold text-gray-700 mb-2">📊 Document Info</h3>
              <div className="space-y-2 text-sm">
                <div className="flex justify-between">
                  <span className="text-gray-600">Category:</span>
                  <span className="bg-green-100 text-green-800 px-2 py-1 rounded text-xs">
                    {doc.category || 'Unknown'}
                  </span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">Difficulty:</span>
                  <span className="bg-orange-100 text-orange-800 px-2 py-1 rounded text-xs">
                    {doc.difficulty || 'Unknown'}
                  </span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">File Size:</span>
                  <span className="text-gray-900">{formatFileSize(doc.file_size)}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">Upload Date:</span>
                  <span className="text-gray-900">{formatDate(doc.upload_date)}</span>
                </div>
              </div>
            </div>

            {/* Action Buttons */}
            <div className="pt-4 border-t">
              <a
                href={`https://raw.githubusercontent.com/lonardonifabio/tech_documents/main/${doc.filepath}`}
                target="_blank"
                rel="noopener noreferrer"
                className="w-full bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors duration-200 text-center block text-sm font-medium"
              >
                📥 Download PDF
              </a>
            </div>
          </div>

          {/* Center - PDF Preview */}
          <div className="flex-1 bg-white">
            {previewError ? (
              <div className="flex items-center justify-center h-full bg-gray-50">
                <div className="text-center">
                  <div className="text-6xl mb-4">⚠️</div>
                  <h3 className="text-xl font-semibold text-gray-700 mb-2">
                    Unable to load PDF
                  </h3>
                  <p className="text-gray-500 mb-4">
                    The PDF could not be displayed in the viewer.
                  </p>
                  <a
                    href={`https://raw.githubusercontent.com/lonardonifabio/tech_documents/main/${doc.filepath}`}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition-colors duration-200"
                  >
                    Download PDF
                  </a>
                </div>
              </div>
            ) : (
              <iframe
                src={getPDFPreviewUrl(doc)}
                className="w-full h-full border-0"
                onError={() => setPreviewError(true)}
                title={`Preview of ${doc.title || doc.filename}`}
              />
            )}
          </div>

          {/* Right Sidebar - Chat Interface */}
          <div className="w-80 border-l">
            <ErrorBoundary
              fallback={
                <div className="p-4 bg-red-50 border border-red-200 rounded-lg m-4">
                  <div className="flex items-center gap-2 text-red-800 mb-2">
                    <span className="text-lg">⚠️</span>
                    <h3 className="font-semibold">Chat Error</h3>
                  </div>
                  <p className="text-red-700 text-sm mb-3">
                    The document chat feature encountered an error. This might be due to:
                  </p>
                  <ul className="text-red-700 text-xs mb-3 list-disc list-inside">
                    <li>Ollama not running locally</li>
                    <li>CORS configuration issues</li>
                    <li>Network connectivity problems</li>
                  </ul>
                  <button
                    onClick={() => window.location.reload()}
                    className="px-3 py-1 bg-red-600 text-white text-sm rounded hover:bg-red-700 transition-colors"
                  >
                    Reload Page
                  </button>
                </div>
              }
            >
              <DocumentChat document={doc} />
            </ErrorBoundary>
          </div>
        </div>
      </div>
    </div>
  );
};

export default PDFModal;
