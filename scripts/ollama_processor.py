#!/usr/bin/env python3
"""
Optimized document processor using Ollama with DeepSeek model
Designed for GitHub Actions automation
"""

import os
import json
import hashlib
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
import ollama
import PyPDF2

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class OllamaDocumentProcessor:
    def __init__(self, model_name: str = "deepseek-r1:1.8b"):
        """Initialize the processor with Ollama and DeepSeek model"""
        self.model_name = model_name
        self.base_dir = Path.cwd()
        self.documents_dir = self.base_dir / 'documents'
        self.data_dir = self.base_dir / 'data'
        self.dist_data_dir = self.base_dir / 'dist' / 'data'
        self.processed_files_path = self.data_dir / 'processed_files.json'
        
        logger.info(f"Initialized processor with model: {model_name}")
        logger.info(f"Documents directory: {self.documents_dir}")
        logger.info(f"Data directory: {self.data_dir}")
    
    def ensure_model_available(self) -> bool:
        """Ensure the DeepSeek model is available in Ollama"""
        try:
            models = ollama.list()
            available_models = [model['name'] for model in models.get('models', [])]
            
            if self.model_name not in available_models:
                logger.info(f"Model {self.model_name} not found. Attempting to pull...")
                ollama.pull(self.model_name)
                logger.info(f"Successfully pulled {self.model_name}")
            
            return True
        except Exception as e:
            logger.error(f"Failed to ensure model availability: {e}")
            return False
    
    def extract_pdf_text(self, filepath: Path, max_pages: int = 3) -> str:
        """Extract text from PDF file (first few pages for analysis)"""
        try:
            with open(filepath, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                
                # Extract text from first few pages only for efficiency
                pages_to_read = min(len(pdf_reader.pages), max_pages)
                for page_num in range(pages_to_read):
                    page = pdf_reader.pages[page_num]
                    text += page.extract_text() + "\n"
                
                return text.strip()
        except Exception as e:
            logger.warning(f"Failed to extract text from {filepath}: {e}")
            return ""
    
    def analyze_document_with_ollama(self, text: str, filename: str) -> Dict:
        """Use Ollama with DeepSeek to analyze document content"""
        if not text.strip():
            return self._get_fallback_analysis(filename)
        
        # Truncate text if too long to avoid token limits
        max_chars = 2000
        if len(text) > max_chars:
            text = text[:max_chars] + "..."
        
        prompt = f"""Analyze this document and provide a JSON response with the following structure:
{{
    "title": "Clean, readable title",
    "summary": "summary of the document content with max 400 characters",
    "keywords": ["keyword1", "keyword2", "keyword3", "keyword4", "keyword5"],
    "category": "just one of: AI, Machine Learning, Data Science, Analytics, Business, Technology, Research",
    "difficulty": "just one of: Beginner, Intermediate, Advanced",
    "authors": ["author1", "author2"] or [] if not found,
    "content_preview": "First 100 characters of meaningful content"
}}

Document filename: {filename}
Document content:
{text}

Respond only with valid JSON, no additional text."""

        try:
            response = ollama.generate(
                model=self.model_name,
                prompt=prompt,
                options={
                    "temperature": 0.1,  # Low temperature for consistent results
                    "top_p": 0.9,
                    "num_predict": 500   # Limit response length
                }
            )
            
            response_text = response.get('response', '').strip()
            
            # Try to parse JSON response
            try:
                analysis = json.loads(response_text)
                logger.info(f"Successfully analyzed {filename} with Ollama")
                return analysis
            except json.JSONDecodeError:
                logger.warning(f"Invalid JSON response from Ollama for {filename}")
                return self._get_fallback_analysis(filename)
                
        except Exception as e:
            logger.error(f"Ollama analysis failed for {filename}: {e}")
            return self._get_fallback_analysis(filename)
    
    def _get_fallback_analysis(self, filename: str) -> Dict:
        """Provide fallback analysis when Ollama fails"""
        clean_title = filename.replace('.pdf', '').replace('_', ' ').replace('-', ' ')
        
        # Simple keyword extraction from filename
        keywords = []
        filename_lower = filename.lower()
        keyword_map = {
            'ai': 'AI', 'machine': 'Machine Learning', 'data': 'Data Science',
            'learning': 'Machine Learning', 'neural': 'Neural Networks',
            'deep': 'Deep Learning', 'analytics': 'Analytics',
            'business': 'Business', 'python': 'Python', 'statistics': 'Statistics'
        }
        
        for key, value in keyword_map.items():
            if key in filename_lower and value not in keywords:
                keywords.append(value)
        
        if not keywords:
            keywords = ['AI', 'Data Science', 'Technology']
        
        return {
            "title": clean_title,
            "summary": f"Technical document covering {clean_title.lower()} concepts and methodologies.",
            "keywords": keywords[:5],
            "category": "Technology",
            "difficulty": "Intermediate",
            "authors": [],
            "content_preview": f"Document: {clean_title}"
        }
    
    def get_file_hash(self, filepath: Path) -> str:
        """Generate MD5 hash of file content"""
        with open(filepath, 'rb') as f:
            return hashlib.md5(f.read()).hexdigest()
    
    def load_processed_files(self) -> Dict:
        """Load the list of already processed files with their hashes"""
        if self.processed_files_path.exists():
            with open(self.processed_files_path, 'r') as f:
                return json.load(f)
        return {}
    
    def save_processed_files(self, processed_files: Dict):
        """Save the list of processed files"""
        self.data_dir.mkdir(exist_ok=True)
        with open(self.processed_files_path, 'w') as f:
            json.dump(processed_files, f, indent=2)
    
    def load_existing_documents(self) -> List[Dict]:
        """Load existing documents from database"""
        db_path = self.data_dir / 'documents.json'
        if db_path.exists():
            with open(db_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []
    
    def save_documents(self, documents: List[Dict]):
        """Save documents to both data and dist/data directories"""
        # Save to data directory
        self.data_dir.mkdir(exist_ok=True)
        data_output = self.data_dir / 'documents.json'
        with open(data_output, 'w', encoding='utf-8') as f:
            json.dump(documents, f, indent=2, ensure_ascii=False)
        
        # Save to dist/data directory
        self.dist_data_dir.mkdir(parents=True, exist_ok=True)
        dist_output = self.dist_data_dir / 'documents.json'
        with open(dist_output, 'w', encoding='utf-8') as f:
            json.dump(documents, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Updated documents.json with {len(documents)} documents")
    
    def process_document(self, filepath: Path) -> Dict:
        """Process a single document with Ollama analysis"""
        logger.info(f"Processing document: {filepath.name}")
        
        # Extract text content
        text_content = self.extract_pdf_text(filepath)
        
        # Analyze with Ollama
        analysis = self.analyze_document_with_ollama(text_content, filepath.name)
        
        # Get file stats
        stat = filepath.stat()
        
        # Create document entry
        doc_info = {
            "id": hashlib.md5(str(filepath).encode()).hexdigest(),
            "filename": filepath.name,
            "title": analysis.get("title", filepath.stem.replace('_', ' ')),
            "authors": analysis.get("authors", []),
            "filepath": f"documents/{filepath.name}",
            "upload_date": datetime.fromtimestamp(stat.st_mtime).isoformat(),
            "file_size": stat.st_size,
            "summary": analysis.get("summary", f"Document: {filepath.stem}"),
            "keywords": analysis.get("keywords", ["AI", "Technology"]),
            "category": analysis.get("category", "Technology"),
            "difficulty": analysis.get("difficulty", "Intermediate"),
            "content_preview": analysis.get("content_preview", f"PDF document: {filepath.name}")
        }
        
        return doc_info
    
    def scan_and_process(self) -> bool:
        """Scan for new or changed documents and process them"""
        if not self.documents_dir.exists():
            logger.error(f"Documents directory does not exist: {self.documents_dir}")
            return False
        
        # Ensure Ollama model is available
        if not self.ensure_model_available():
            logger.error("Failed to ensure Ollama model availability")
            return False
        
        processed_files = self.load_processed_files()
        existing_documents = self.load_existing_documents()
        new_documents = []
        updated = False
        
        # Get all PDF files
        pdf_files = list(self.documents_dir.glob('*.pdf'))
        logger.info(f"Found {len(pdf_files)} PDF files")
        
        for filepath in pdf_files:
            if not filepath.is_file():
                continue
            
            file_path_str = str(filepath)
            current_hash = self.get_file_hash(filepath)
            
            # Check if file is new or changed
            if file_path_str not in processed_files or processed_files[file_path_str] != current_hash:
                logger.info(f"Processing {'new' if file_path_str not in processed_files else 'updated'} file: {filepath.name}")
                
                doc_info = self.process_document(filepath)
                
                # Remove old entry if it exists
                existing_documents = [doc for doc in existing_documents if doc['filename'] != filepath.name]
                
                # Add new entry
                new_documents.append(doc_info)
                processed_files[file_path_str] = current_hash
                updated = True
        
        # Check for deleted files
        files_to_remove = []
        for file_path_str in processed_files.keys():
            if not Path(file_path_str).exists():
                filename = Path(file_path_str).name
                logger.info(f"Removing deleted file: {filename}")
                existing_documents = [doc for doc in existing_documents if doc['filename'] != filename]
                files_to_remove.append(file_path_str)
                updated = True
        
        # Remove deleted files from processed_files
        for file_path_str in files_to_remove:
            del processed_files[file_path_str]
        
        if updated:
            # Combine existing and new documents
            all_documents = existing_documents + new_documents
            
            # Sort by filename for consistency
            all_documents.sort(key=lambda x: x['filename'])
            
            self.save_documents(all_documents)
            self.save_processed_files(processed_files)
            logger.info("Documents database updated successfully")
            return True
        
        logger.info("No changes detected")
        return False

def main():
    """Main entry point"""
    import sys
    
    # Allow custom model name via environment variable or argument
    model_name = os.getenv('OLLAMA_MODEL', 'deepseek-r1:1.5b')
    if len(sys.argv) > 1:
        model_name = sys.argv[1]
    
    processor = OllamaDocumentProcessor(model_name)
    
    logger.info("Starting document processing with Ollama...")
    success = processor.scan_and_process()
    
    if success:
        logger.info("Document processing completed successfully")
    else:
        logger.info("No documents were processed")

if __name__ == "__main__":
    main()
