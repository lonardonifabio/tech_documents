import React, { useState, useEffect } from 'react';

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

interface PDFModalProps {
  doc: Document;
  isOpen: boolean;
  onClose: () => void;
}

const PDFModal: React.FC<PDFModalProps> = ({ doc, isOpen, onClose }) => {
  const [previewError, setPreviewError] = useState(false);
  
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
    <div className="modal-overlay" onClick={handleOverlayClick}>
      <div className="modal-content">
        <button
          onClick={onClose}
          className="close-button"
          title="Close preview (ESC)"
        >
          ×
        </button>
        
        <div className="modal-header">
          <h3 className="text-lg font-semibold text-gray-800 truncate pr-12">
            {doc.title || doc.filename}
          </h3>
        </div>
        
        <div className="modal-body">
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
              className="modal-iframe"
              onError={() => setPreviewError(true)}
              title={`Preview of ${doc.title || doc.filename}`}
            />
          )}
        </div>
      </div>
    </div>
  );
};

export default PDFModal;
