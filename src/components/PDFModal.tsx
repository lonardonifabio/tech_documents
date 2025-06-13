import React, { useState, useEffect } from 'react';

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
  content_preview?: string;
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

  // Generate LinkedIn post content
  //#const generateLinkedInPost = (doc: Document): string => {
  //#  const title = doc.title || doc.filename;
  //#  const summary = doc.summary;
  //#  const contentPreview = doc.content_preview;
  //#  const keyConcepts = doc.key_concepts || [];
  //#  const keywords = doc.keywords.slice(0, 5); // Take first 5 keywords
  //#  const category = doc.category;
  //#  const difficulty = doc.difficulty;
  //#  
  //#  // Use the GitHub Pages URL for the application
  //#  const githubPagesUrl = `https://lonardonifabio.github.io/tech_documents/?doc=${doc.id}`;
  //#
  //#  let post = `🚀 Just shared an insightful resource with my LinkedIn network!\n\n`;
  //#  post += `📄 **${title}**\n\n`;
  //#  
  //#  // Add summary
  //#  if (summary) {
  //#    const truncatedSummary = summary.length > 300 ? summary.substring(0, 300) + '...' : summary;
  //#    post += `📝 **Summary:**\n${truncatedSummary}\n\n`;
  //#  }
  //#  
  //#  // Add content preview if available
  //#  if (contentPreview && contentPreview !== summary) {
  //#    const truncatedPreview = contentPreview.length > 200 ? contentPreview.substring(0, 200) + '...' : contentPreview;
  //#    post += `🔍 **Key Insights:**\n${truncatedPreview}\n\n`;
  //#  }
  //#  
  //#  // Add key concepts if available
  //#  if (keyConcepts.length > 0) {
  //#    post += `💡 **Key Concepts:**\n`;
  //#    keyConcepts.slice(0, 3).forEach(concept => {
  //#      post += `• ${concept}\n`;
  //#    });
  //#    post += `\n`;
  //#  }
  //#  
  //#  // Add category and difficulty
  //#  post += `📊 **Category:** ${category} | **Level:** ${difficulty}\n\n`;
  //#  
  //#  // Add call to action
  //#  post += `🤖 Explore this document with AI-powered assistance:\n${githubPagesUrl}\n\n`;
  //#  post += `📚 **Discover 1100+ AI & Data Science Documents:**\n`;
  //#  post += `🌐 https://lonardonifabio.github.io/tech_documents/\n\n`;
  //#  
  //#  // Add hashtags
  //#  post += `#ArtificialIntelligence #DataScience #MachineLearning #AI #TechResources `;
  //#  keywords.forEach(keyword => {
  //#    const cleanKeyword = keyword.replace(/[^a-zA-Z0-9]/g, '');
  //#    if (cleanKeyword.length > 2) {
  //#      post += `#${cleanKeyword} `;
  //#    }
  //#  });
  //#  
  //#  return post;
  //#};

  // Generate LinkedIn post content
  const generateLinkedInPost = (doc: Document): string => {
    const title = doc.title || doc.filename;
    //const summary = doc.summary;
    const contentPreview = doc.content_preview;
    //const keyConcepts = doc.key_concepts || [];
    const keywords = doc.keywords.slice(0, 5); // Take first 5 keywords
    //const category = doc.category;
    //const difficulty = doc.difficulty;
    
    // Use the GitHub Pages URL for the application
    const githubPagesUrl = `https://lonardonifabio.github.io/tech_documents/?doc=${doc.id}`;

    let post = `🚀 Just shared an insightful resource with my LinkedIn network!\n`;
    post += `📄 **${title}**\n`;
    post += `🤖 Explore it with AI-powered assistance: ${githubPagesUrl}\n\n`;
    // Add content preview if available
    if (contentPreview) {
      post += `🔍 **Content Preview:**\n${contentPreview}\n`;
    }
    post += `📊 **Explore 1100+ AI & Data Science Documents:**\n`;
    post += `🌐 Visit: https://lonardonifabio.github.io/tech_documents/\n`;
    post += `\n`;
    // Add hashtags
    keywords.forEach(keyword => {
      post += `#${keyword.replace(/\s+/g, '')} `;
    });
    return post;
  };

  // Share on LinkedIn with mobile-optimized approach
  const shareOnLinkedIn = () => {
    if (typeof window === 'undefined') return; // Guard against SSR
    
    const title = doc.title || doc.filename;
    // Use the dedicated document URL with proper Open Graph meta tags
    const documentUrl = `https://lonardonifabio.github.io/tech_documents/document/${doc.id}`;
    
    // Detect if user is on mobile
    const isMobile = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
    
    if (isMobile) {
      // For mobile devices, use the dedicated URL with proper meta tags
      // This will allow LinkedIn's crawler to extract proper Open Graph data
      
      // Try to use the native sharing API if available
      if (navigator.share) {
        const postContent = generateLinkedInPost(doc);
        navigator.share({
          title: `AI Document: ${title}`,
          text: postContent,
          url: documentUrl
        }).catch(err => {
          console.log('Native sharing failed, falling back to LinkedIn URL');
          // Fallback to LinkedIn URL with dedicated document URL
          const linkedInUrl = `https://www.linkedin.com/sharing/share-offsite/?url=${encodeURIComponent(documentUrl)}`;
          window.open(linkedInUrl, '_blank');
        });
      } else {
        // For mobile without native sharing, use the dedicated URL
        // LinkedIn's mobile crawler will extract meta tags from the dedicated page
        const linkedInUrl = `https://www.linkedin.com/sharing/share-offsite/?url=${encodeURIComponent(documentUrl)}`;
        window.open(linkedInUrl, '_blank');
      }
    } else {
      // For desktop, use the full post content with dedicated URL
      const postContent = generateLinkedInPost(doc);
      const encodedContent = encodeURIComponent(postContent);
      const linkedInUrl = `https://www.linkedin.com/sharing/share-offsite/?url=${encodeURIComponent(documentUrl)}&text=${encodedContent}`;
      window.open(linkedInUrl, '_blank', 'width=600,height=600');
    }
  };
  
  useEffect(() => {
    if (isOpen && typeof document !== 'undefined') {
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
      <div className="bg-white rounded-lg shadow-xl w-full max-w-6xl h-full max-h-[90vh] flex flex-col">
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
          <div className="w-80 bg-gray-50 border-r flex flex-col">
            <div className="flex-1 overflow-y-auto p-4 space-y-4">
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
            <div className="pt-4 border-t space-y-3">
              <button
                onClick={shareOnLinkedIn}
                className="w-full bg-linkedin text-white px-4 py-2 rounded-lg hover:bg-linkedin-dark transition-colors duration-200 text-center text-sm font-medium flex items-center justify-center gap-2"
                title="Share on LinkedIn"
              >
                <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/>
                </svg>
                📤 Share on LinkedIn
              </button>
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
        </div>
      </div>
    </div>
  );
};

export default PDFModal;
