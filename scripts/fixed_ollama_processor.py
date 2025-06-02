#!/usr/bin/env python3
"""
Fixed Ollama document processor optimized for Mistral model
Handles JSON parsing issues and provides robust document analysis
"""

import os
import json
import hashlib
import logging
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
import ollama
import PyPDF2

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class FixedOllamaDocumentProcessor:
    def __init__(self, model_name: str = "mistral:7b"):
        """Initialize the processor with Ollama and Mistral model"""
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
        """Ensure the Mistral model is available in Ollama"""
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
    
    def parse_ollama_response(self, response_text: str) -> Optional[Dict]:
        """Parse Ollama response with robust error handling"""
        if not response_text:
            return None
        
        logger.info(f"Raw response: {response_text[:200]}...")
        
        # Method 1: Direct JSON parsing
        try:
            return json.loads(response_text.strip())
        except json.JSONDecodeError:
            pass
        
        # Method 2: Extract JSON between braces
        first_brace = response_text.find('{')
        last_brace = response_text.rfind('}')
        
        if first_brace != -1 and last_brace != -1 and last_brace > first_brace:
            potential_json = response_text[first_brace:last_brace + 1]
            try:
                return json.loads(potential_json)
            except json.JSONDecodeError:
                pass
        
        # Method 3: Regex field extraction
        logger.info("Attempting to extract fields using regex patterns")
        
        extracted_data = {}
        
        # Extract title
        title_patterns = [
            r'"title"\s*:\s*"([^"]*)"',
            r'title\s*:\s*"([^"]*)"',
            r'Title\s*:\s*([^\n,}]*)'
        ]
        for pattern in title_patterns:
            title_match = re.search(pattern, response_text, re.IGNORECASE)
            if title_match:
                extracted_data["title"] = title_match.group(1).strip()
                break
        
        # Extract summary
        summary_patterns = [
            r'"summary"\s*:\s*"([^"]*)"',
            r'summary\s*:\s*"([^"]*)"',
            r'Summary\s*:\s*([^\n,}]*)'
        ]
        for pattern in summary_patterns:
            summary_match = re.search(pattern, response_text, re.IGNORECASE)
            if summary_match:
                extracted_data["summary"] = summary_match.group(1).strip()
                break
        
        # Extract category
        category_patterns = [
            r'"category"\s*:\s*"([^"]*)"',
            r'category\s*:\s*"([^"]*)"',
            r'Category\s*:\s*([^\n,}]*)'
        ]
        for pattern in category_patterns:
            category_match = re.search(pattern, response_text, re.IGNORECASE)
            if category_match:
                extracted_data["category"] = category_match.group(1).strip()
                break
        
        # Extract difficulty
        difficulty_patterns = [
            r'"difficulty"\s*:\s*"([^"]*)"',
            r'difficulty\s*:\s*"([^"]*)"',
            r'Difficulty\s*:\s*([^\n,}]*)'
        ]
        for pattern in difficulty_patterns:
            difficulty_match = re.search(pattern, response_text, re.IGNORECASE)
            if difficulty_match:
                extracted_data["difficulty"] = difficulty_match.group(1).strip()
                break
        
        # Extract keywords array
        keywords_patterns = [
            r'"keywords"\s*:\s*\[(.*?)\]',
            r'keywords\s*:\s*\[(.*?)\]'
        ]
        for pattern in keywords_patterns:
            keywords_match = re.search(pattern, response_text, re.DOTALL | re.IGNORECASE)
            if keywords_match:
                keywords_str = keywords_match.group(1)
                keywords = []
                for keyword_match in re.finditer(r'"([^"]*)"', keywords_str):
                    keywords.append(keyword_match.group(1))
                extracted_data["keywords"] = keywords[:5]  # Limit to 5
                break
        
        # Extract authors array
        authors_patterns = [
            r'"authors"\s*:\s*\[(.*?)\]',
            r'authors\s*:\s*\[(.*?)\]'
        ]
        for pattern in authors_patterns:
            authors_match = re.search(pattern, response_text, re.DOTALL | re.IGNORECASE)
            if authors_match:
                authors_str = authors_match.group(1)
                authors = []
                for author_match in re.finditer(r'"([^"]*)"', authors_str):
                    authors.append(author_match.group(1))
                extracted_data["authors"] = authors
                break
        
        # Extract content_preview
        preview_patterns = [
            r'"content_preview"\s*:\s*"([^"]*)"',
            r'content_preview\s*:\s*"([^"]*)"'
        ]
        for pattern in preview_patterns:
            preview_match = re.search(pattern, response_text, re.IGNORECASE)
            if preview_match:
                extracted_data["content_preview"] = preview_match.group(1).strip()
                break
        
        if extracted_data:
            logger.info("Successfully extracted data using regex patterns")
            return extracted_data
        
        return None
    
    def analyze_document_with_ollama(self, text: str, filename: str) -> Dict:
        """Use Ollama with Mistral to analyze document content"""
        if not text.strip():
            return self._get_fallback_analysis(filename)
        
        # Truncate text if too long to avoid token limits
        max_chars = 1500
        if len(text) > max_chars:
            text = text[:max_chars] + "..."
        
        # Simple, clear prompt for Mistral
        prompt = f"""Analyze this document and respond with ONLY a JSON object in this exact format:

{{"title": "document title", "summary": "brief summary with around 500 characters", "keywords": ["keyword1", "keyword2", "keyword3"], "category": "one of: AI, Machine Learning, Data Science, Analytics, Business, Technology, Research", "difficulty": "one of: Beginner, Intermediate, Advanced", "authors": [], "content_preview": "first 80 characters of content"}}

Document: {filename}
Content: {text}

JSON response:"""

        try:
            response = ollama.generate(
                model=self.model_name,
                prompt=prompt,
                options={
                    "temperature": 0.1,
                    "top_p": 0.9,
                    "num_predict": 500
                }
            )
            
            response_text = response.get('response', '').strip()
            logger.info(f"Ollama response for {filename}: {response_text[:150]}...")
            
            # Parse response with robust error handling
            analysis = self.parse_ollama_response(response_text)
            
            if analysis:
                analysis = self._validate_analysis(analysis, filename)
                logger.info(f"Successfully analyzed {filename} with Ollama")
                return analysis
            else:
                logger.warning(f"Failed to parse Ollama response for {filename}, using fallback")
                return self._get_fallback_analysis(filename)
                
        except Exception as e:
            logger.error(f"Ollama analysis failed for {filename}: {e}")
            return self._get_fallback_analysis(filename)
    
    def _validate_analysis(self, analysis: Dict, filename: str) -> Dict:
        """Validate and clean analysis data"""
        # Ensure required fields exist
        required_fields = ["title", "summary", "keywords", "category", "difficulty", "authors", "content_preview"]
        for field in required_fields:
            if field not in analysis:
                analysis[field] = ""
        
        # Clean and validate title
        if not analysis["title"] or len(analysis["title"].strip()) < 3:
            analysis["title"] = filename.replace('.pdf', '').replace('_', ' ').replace('-', ' ')
        
        # Validate category
        valid_categories = ["AI", "Machine Learning", "Data Science", "Analytics", "Business", "Technology", "Research"]
        if analysis["category"] not in valid_categories:
            # Try to infer from filename
            filename_lower = filename.lower()
            if any(word in filename_lower for word in ['ai', 'artificial']):
                analysis["category"] = "AI"
            elif any(word in filename_lower for word in ['machine', 'learning', 'ml']):
                analysis["category"] = "Machine Learning"
            elif any(word in filename_lower for word in ['data', 'analytics']):
                analysis["category"] = "Data Science"
            elif any(word in filename_lower for word in ['business']):
                analysis["category"] = "Business"
            else:
                analysis["category"] = "Technology"
        
        # Validate difficulty
        valid_difficulties = ["Beginner", "Intermediate", "Advanced"]
        if analysis["difficulty"] not in valid_difficulties:
            analysis["difficulty"] = "Intermediate"
        
        # Ensure keywords is a list with max 5 items
        if not isinstance(analysis["keywords"], list):
            analysis["keywords"] = []
        analysis["keywords"] = analysis["keywords"][:5]
        if not analysis["keywords"]:
            analysis["keywords"] = ["Technology"]
        
        # Ensure authors is a list
        if not isinstance(analysis["authors"], list):
            analysis["authors"] = []
        
        # Ensure summary is reasonable length
        if len(analysis["summary"]) > 350:
            analysis["summary"] = analysis["summary"][:347] + "..."
        elif len(analysis["summary"]) < 50:
            analysis["summary"] = f"This document covers {analysis['title'].lower()} providing comprehensive information and insights on the subject matter."
        
        # Ensure content_preview exists
        if not analysis["content_preview"]:
            analysis["content_preview"] = f"Document: {analysis['title']}"
        
        return analysis
    
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
            keywords = ['Technology', 'Research', 'Documentation']
        
        return {
            "title": clean_title,
            "summary": f"This comprehensive document provides detailed coverage of {clean_title.lower()} concepts, methodologies, and practical applications. It offers valuable insights into theoretical foundations and real-world applications relevant to the field.",
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
            "keywords": analysis.get("keywords", ["Technology"]),
            "category": analysis.get("category", "Technology"),
            "difficulty": analysis.get("difficulty", "Intermediate"),
            "content_preview": analysis.get("content_preview", f"PDF document: {filepath.name}")
        }
        
        return doc_info
    
    def scan_and_process(self, force_reprocess: bool = False) -> bool:
        """Scan for new or changed documents and process them"""
        if not self.documents_dir.exists():
            logger.error(f"Documents directory does not exist: {self.documents_dir}")
            return False
        
        # Ensure Ollama model is available
        if not self.ensure_model_available():
            logger.error("Failed to ensure Ollama model availability")
            return False
        
        processed_files = self.load_processed_files()
        existing_documents = self.load_existing_documents() if not force_reprocess else []
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
            
            # Check if file is new, changed, or force reprocessing
            if force_reprocess or file_path_str not in processed_files or processed_files[file_path_str] != current_hash:
                logger.info(f"Processing {'new' if file_path_str not in processed_files else 'updated'} file: {filepath.name}")
                
                doc_info = self.process_document(filepath)
                
                # Remove old entry if it exists
                existing_documents = [doc for doc in existing_documents if doc['filename'] != filepath.name]
                
                # Add new entry
                new_documents.append(doc_info)
                processed_files[file_path_str] = current_hash
                updated = True
        
        if updated or force_reprocess:
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
    model_name = os.getenv('OLLAMA_MODEL', 'mistral:7b')
    if len(sys.argv) > 1 and not sys.argv[1].startswith('--'):
        model_name = sys.argv[1]
    
    # Check for force reprocess flag
    force_reprocess = '--force' in sys.argv or '-f' in sys.argv
    
    processor = FixedOllamaDocumentProcessor(model_name)
    
    logger.info("Starting document processing with fixed Ollama processor...")
    if force_reprocess:
        logger.info("Force reprocessing all documents...")
    
    success = processor.scan_and_process(force_reprocess=force_reprocess)
    
    if success:
        logger.info("Document processing completed successfully")
    else:
        logger.info("No documents were processed")

if __name__ == "__main__":
    main()
