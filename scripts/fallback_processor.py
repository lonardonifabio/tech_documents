#!/usr/bin/env python3
"""
Fallback document processor for GitHub Actions
Creates document metadata without requiring Ollama
"""

import os
import json
import hashlib
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
import PyPDF2

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class FallbackDocumentProcessor:
    def __init__(self):
        """Initialize the fallback processor"""
        self.base_dir = Path.cwd()
        self.documents_dir = self.base_dir / 'documents'
        self.data_dir = self.base_dir / 'data'
        self.dist_data_dir = self.base_dir / 'dist' / 'data'
        self.processed_files_path = self.data_dir / 'processed_files.json'
        
        logger.info("Initialized fallback processor")
        logger.info(f"Documents directory: {self.documents_dir}")
        logger.info(f"Data directory: {self.data_dir}")
    
    def extract_pdf_text(self, filepath: Path, max_pages: int = 2) -> str:
        """Extract text from PDF file (first few pages for analysis)"""
        try:
            with open(filepath, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                
                # Extract text from first few pages only
                pages_to_read = min(len(pdf_reader.pages), max_pages)
                for page_num in range(pages_to_read):
                    page = pdf_reader.pages[page_num]
                    text += page.extract_text() + "\n"
                
                return text.strip()
        except Exception as e:
            logger.warning(f"Failed to extract text from {filepath}: {e}")
            return ""
    
    def analyze_document_fallback(self, text: str, filename: str) -> Dict:
        """Analyze document using simple heuristics"""
        clean_title = filename.replace('.pdf', '').replace('_', ' ').replace('-', ' ')
        
        # Extract keywords from filename and text
        keywords = []
        filename_lower = filename.lower()
        text_lower = text.lower() if text else ""
        
        # Keyword mapping based on common terms
        keyword_map = {
            'ai': 'Artificial Intelligence',
            'artificial': 'Artificial Intelligence',
            'intelligence': 'Artificial Intelligence',
            'machine': 'Machine Learning',
            'learning': 'Machine Learning',
            'data': 'Data Science',
            'science': 'Data Science',
            'neural': 'Neural Networks',
            'network': 'Neural Networks',
            'deep': 'Deep Learning',
            'analytics': 'Analytics',
            'analysis': 'Analytics',
            'business': 'Business',
            'python': 'Python',
            'statistics': 'Statistics',
            'statistical': 'Statistics',
            'algorithm': 'Algorithms',
            'model': 'Machine Learning',
            'prediction': 'Predictive Analytics',
            'classification': 'Classification',
            'regression': 'Regression',
            'clustering': 'Clustering',
            'optimization': 'Optimization',
            'visualization': 'Data Visualization',
            'database': 'Database',
            'sql': 'SQL',
            'programming': 'Programming',
            'software': 'Software Engineering',
            'engineering': 'Engineering',
            'research': 'Research',
            'guide': 'Tutorial',
            'introduction': 'Tutorial',
            'beginner': 'Tutorial',
            'blockchain': 'Blockchain',
            'accessibility': 'Accessibility',
            'excel': 'Excel',
            'pandas': 'Pandas',
            'outlier': 'Data Analysis',
            'detection': 'Data Analysis',
            'goal': 'Business Strategy',
            'setting': 'Business Strategy',
            'motivation': 'Management',
            'employees': 'Management',
            'revenue': 'Business',
            'leaders': 'Leadership',
            'strategic': 'Strategy',
            'foresight': 'Strategy',
            'executive': 'Executive',
            'ethical': 'Ethics',
            'swot': 'Business Analysis',
            'decision': 'Decision Making',
            'trees': 'Decision Trees',
            'activation': 'Neural Networks',
            'functions': 'Neural Networks'
        }
        
        # Check filename and text for keywords
        for key, value in keyword_map.items():
            if (key in filename_lower or key in text_lower) and value not in keywords:
                keywords.append(value)
        
        # Ensure we have at least some keywords
        if not keywords:
            keywords = ['Technology', 'Research', 'Documentation']
        
        # Limit to 5 keywords
        keywords = keywords[:5]
        
        # Determine category based on keywords
        category = "Technology"  # default
        if any(kw in ['Artificial Intelligence', 'Machine Learning', 'Deep Learning', 'Neural Networks'] for kw in keywords):
            category = "AI"
        elif any(kw in ['Data Science', 'Analytics', 'Statistics', 'Data Analysis'] for kw in keywords):
            category = "Data Science"
        elif any(kw in ['Business', 'Management', 'Leadership', 'Strategy', 'Business Strategy', 'Business Analysis'] for kw in keywords):
            category = "Business"
        elif any(kw in ['Programming', 'Software Engineering', 'Python'] for kw in keywords):
            category = "Programming"
        elif any(kw in ['Research'] for kw in keywords):
            category = "Research"
        
        # Determine difficulty based on filename patterns
        difficulty = "Intermediate"  # default
        if any(term in filename_lower for term in ['beginner', 'introduction', 'basic', 'guide', 'tutorial', 'minutes']):
            difficulty = "Beginner"
        elif any(term in filename_lower for term in ['advanced', 'expert', 'deep', 'comprehensive']):
            difficulty = "Advanced"
        
        # Generate summary based on content and filename
        summary = f"Technical document covering {clean_title.lower()} concepts and methodologies."
        
        # Try to create more specific summaries based on keywords
        if 'Machine Learning' in keywords:
            summary = f"Machine learning resource focusing on {clean_title.lower()} techniques and applications."
        elif 'Data Science' in keywords:
            summary = f"Data science guide covering {clean_title.lower()} methods and best practices."
        elif 'Business' in keywords:
            summary = f"Business document providing insights on {clean_title.lower()} strategies and approaches."
        elif 'Programming' in keywords or 'Python' in keywords:
            summary = f"Programming guide covering {clean_title.lower()} concepts and implementation."
        elif 'Tutorial' in keywords:
            summary = f"Educational tutorial on {clean_title.lower()} for practical learning."
        
        # Try to extract a meaningful sentence from the text if available
        if text and len(text) > 100:
            sentences = text.split('.')
            for sentence in sentences[:5]:
                sentence = sentence.strip()
                if 20 < len(sentence) < 200 and not sentence.isupper():
                    summary = sentence + "."
                    break
        
        return {
            "title": clean_title,
            "summary": summary,
            "keywords": keywords,
            "category": category,
            "difficulty": difficulty,
            "authors": [],
            "content_preview": text[:100] if text else f"Document: {clean_title}"
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
            try:
                with open(db_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    # Remove any Git merge conflict markers
                    if '<<<<<<< HEAD' in content:
                        logger.warning("Found Git merge conflict markers in documents.json, cleaning...")
                        lines = content.split('\n')
                        clean_lines = []
                        skip_until_end = False
                        
                        for line in lines:
                            if line.startswith('<<<<<<< HEAD'):
                                skip_until_end = True
                                continue
                            elif line.startswith('======='):
                                continue
                            elif line.startswith('>>>>>>> '):
                                skip_until_end = False
                                continue
                            elif not skip_until_end:
                                clean_lines.append(line)
                        
                        content = '\n'.join(clean_lines)
                    
                    return json.loads(content)
            except (json.JSONDecodeError, Exception) as e:
                logger.warning(f"Failed to load existing documents: {e}")
                return []
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
        """Process a single document with fallback analysis"""
        logger.info(f"Processing document: {filepath.name}")
        
        # Extract text content
        text_content = self.extract_pdf_text(filepath)
        
        # Analyze with fallback method
        analysis = self.analyze_document_fallback(text_content, filepath.name)
        
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
            "keywords": analysis.get("keywords", ["Technology"]),
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
        
        if updated or not existing_documents:
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
    processor = FallbackDocumentProcessor()
    
    logger.info("Starting document processing with fallback method...")
    success = processor.scan_and_process()
    
    if success:
        logger.info("Document processing completed successfully")
    else:
        logger.info("No documents were processed")

if __name__ == "__main__":
    main()
