#!/usr/bin/env python3
"""
Ultimate Ollama document processor with robust DeepSeek handling
Handles all known DeepSeek response formats and parsing issues
"""

import os
import json
import hashlib
import logging
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
import ollama
import PyPDF2

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class UltimateOllamaDocumentProcessor:
    def __init__(self, model_name: str = "deepseek-r1:1.5b"):
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
            # Test connection first
            response = ollama.list()
            available_models = [model['name'] for model in response.get('models', [])]
            
            if self.model_name not in available_models:
                logger.info(f"Model {self.model_name} not found. Attempting to pull...")
                ollama.pull(self.model_name)
                logger.info(f"Successfully pulled {self.model_name}")
            
            # Test the model with a simple query
            test_response = ollama.generate(
                model=self.model_name,
                prompt="Hello",
                options={"num_predict": 10}
            )
            logger.info("Model test successful")
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
    
    def extract_json_from_response(self, response_text: str) -> Optional[str]:
        """Extract JSON from various response formats"""
        if not response_text:
            return None
        
        # Clean the response
        response_text = response_text.strip()
        
        # Method 1: Handle DeepSeek thinking format
        if '<think>' in response_text:
            # Find the end of thinking section
            think_end = response_text.find('</think>')
            if think_end != -1:
                response_text = response_text[think_end + 8:].strip()
            else:
                # If no closing tag, try to find JSON after thinking content
                json_start = response_text.find('{')
                if json_start != -1:
                    response_text = response_text[json_start:]
        
        # Method 2: Remove any XML-like tags
        response_text = re.sub(r'<[^>]+>', '', response_text).strip()
        
        # Method 3: Try to find complete JSON blocks
        json_patterns = [
            # Complete JSON object with nested structures
            r'\{(?:[^{}]|{[^{}]*})*\}',
            # Simple JSON object
            r'\{[^{}]*\}',
            # JSON with arrays
            r'\{[^{}]*\[[^\]]*\][^{}]*\}',
        ]
        
        for pattern in json_patterns:
            matches = re.findall(pattern, response_text, re.DOTALL)
            for match in matches:
                try:
                    # Test if this is valid JSON
                    parsed = json.loads(match)
                    if isinstance(parsed, dict) and len(parsed) > 2:  # Must have multiple fields
                        return match
                except json.JSONDecodeError:
                    continue
        
        # Method 4: Extract between first { and last }
        first_brace = response_text.find('{')
        last_brace = response_text.rfind('}')
        
        if first_brace != -1 and last_brace != -1 and last_brace > first_brace:
            potential_json = response_text[first_brace:last_brace + 1]
            try:
                parsed = json.loads(potential_json)
                if isinstance(parsed, dict):
                    return potential_json
            except json.JSONDecodeError:
                pass
        
        return None
    
    def extract_fields_with_regex(self, response_text: str) -> Dict[str, Any]:
        """Extract individual fields using regex patterns"""
        extracted_data = {}
        
        # Title patterns
        title_patterns = [
            r'"title"\s*:\s*"([^"]*)"',
            r'title\s*:\s*"([^"]*)"',
            r'Title\s*:\s*([^\n,}]*)',
            r'title\s*=\s*"([^"]*)"'
        ]
        for pattern in title_patterns:
            match = re.search(pattern, response_text, re.IGNORECASE)
            if match:
                extracted_data["title"] = match.group(1).strip()
                break
        
        # Summary patterns
        summary_patterns = [
            r'"summary"\s*:\s*"([^"]*)"',
            r'summary\s*:\s*"([^"]*)"',
            r'Summary\s*:\s*([^\n,}]*)',
            r'summary\s*=\s*"([^"]*)"'
        ]
        for pattern in summary_patterns:
            match = re.search(pattern, response_text, re.IGNORECASE)
            if match:
                extracted_data["summary"] = match.group(1).strip()
                break
        
        # Category patterns
        category_patterns = [
            r'"category"\s*:\s*"([^"]*)"',
            r'category\s*:\s*"([^"]*)"',
            r'Category\s*:\s*([^\n,}]*)',
            r'category\s*=\s*"([^"]*)"'
        ]
        for pattern in category_patterns:
            match = re.search(pattern, response_text, re.IGNORECASE)
            if match:
                extracted_data["category"] = match.group(1).strip()
                break
        
        # Difficulty patterns
        difficulty_patterns = [
            r'"difficulty"\s*:\s*"([^"]*)"',
            r'difficulty\s*:\s*"([^"]*)"',
            r'Difficulty\s*:\s*([^\n,}]*)',
            r'difficulty\s*=\s*"([^"]*)"'
        ]
        for pattern in difficulty_patterns:
            match = re.search(pattern, response_text, re.IGNORECASE)
            if match:
                extracted_data["difficulty"] = match.group(1).strip()
                break
        
        # Keywords patterns (array)
        keywords_patterns = [
            r'"keywords"\s*:\s*\[(.*?)\]',
            r'keywords\s*:\s*\[(.*?)\]',
            r'Keywords\s*:\s*\[(.*?)\]'
        ]
        for pattern in keywords_patterns:
            match = re.search(pattern, response_text, re.DOTALL | re.IGNORECASE)
            if match:
                keywords_str = match.group(1)
                keywords = []
                # Extract quoted strings
                for keyword_match in re.finditer(r'"([^"]*)"', keywords_str):
                    keywords.append(keyword_match.group(1))
                # If no quoted strings, try comma-separated
                if not keywords:
                    keywords = [k.strip() for k in keywords_str.split(',') if k.strip()]
                extracted_data["keywords"] = keywords[:5]  # Limit to 5
                break
        
        # Authors patterns (array)
        authors_patterns = [
            r'"authors"\s*:\s*\[(.*?)\]',
            r'authors\s*:\s*\[(.*?)\]',
            r'Authors\s*:\s*\[(.*?)\]'
        ]
        for pattern in authors_patterns:
            match = re.search(pattern, response_text, re.DOTALL | re.IGNORECASE)
            if match:
                authors_str = match.group(1)
                authors = []
                # Extract quoted strings
                for author_match in re.finditer(r'"([^"]*)"', authors_str):
                    authors.append(author_match.group(1))
                # If no quoted strings, try comma-separated
                if not authors:
                    authors = [a.strip() for a in authors_str.split(',') if a.strip()]
                extracted_data["authors"] = authors
                break
        
        # Content preview patterns
        preview_patterns = [
            r'"content_preview"\s*:\s*"([^"]*)"',
            r'content_preview\s*:\s*"([^"]*)"',
            r'Content Preview\s*:\s*([^\n,}]*)',
            r'content_preview\s*=\s*"([^"]*)"'
        ]
        for pattern in preview_patterns:
            match = re.search(pattern, response_text, re.IGNORECASE)
            if match:
                extracted_data["content_preview"] = match.group(1).strip()
                break
        
        return extracted_data
    
    def parse_ollama_response(self, response_text: str) -> Optional[Dict]:
        """Parse Ollama response with multiple fallback methods"""
        if not response_text:
            return None
        
        logger.debug(f"Raw response: {response_text[:300]}...")
        
        # Method 1: Direct JSON parsing
        try:
            parsed = json.loads(response_text.strip())
            if isinstance(parsed, dict) and len(parsed) > 2:
                logger.info("Successfully parsed JSON directly")
                return parsed
        except json.JSONDecodeError:
            pass
        
        # Method 2: Extract and parse JSON
        json_str = self.extract_json_from_response(response_text)
        if json_str:
            try:
                parsed = json.loads(json_str)
                logger.info("Successfully parsed extracted JSON")
                return parsed
            except json.JSONDecodeError as e:
                logger.debug(f"Failed to parse extracted JSON: {e}")
        
        # Method 3: Regex field extraction
        extracted_data = self.extract_fields_with_regex(response_text)
        if extracted_data and len(extracted_data) >= 3:  # Must have at least 3 fields
            logger.info("Successfully extracted data using regex patterns")
            return extracted_data
        
        # Method 4: Try to fix common JSON issues
        if '{' in response_text and '}' in response_text:
            # Try to fix common issues like missing quotes, trailing commas
            json_attempt = response_text[response_text.find('{'):response_text.rfind('}')+1]
            
            # Fix common issues
            fixes = [
                (r'(\w+):', r'"\1":'),  # Add quotes to keys
                (r':\s*([^",\[\]{}]+)(?=\s*[,}])', r': "\1"'),  # Add quotes to values
                (r',\s*}', '}'),  # Remove trailing commas
                (r',\s*]', ']'),  # Remove trailing commas in arrays
            ]
            
            for pattern, replacement in fixes:
                json_attempt = re.sub(pattern, replacement, json_attempt)
            
            try:
                parsed = json.loads(json_attempt)
                logger.info("Successfully parsed JSON after fixes")
                return parsed
            except json.JSONDecodeError:
                pass
        
        logger.warning("All parsing methods failed")
        return None
    
    def analyze_document_with_ollama(self, text: str, filename: str) -> Dict:
        """Use Ollama with DeepSeek to analyze document content"""
        if not text.strip():
            return self._get_fallback_analysis(filename)
        
        # Truncate text if too long
        max_chars = 1500  # Reduced to avoid token limits
        if len(text) > max_chars:
            text = text[:max_chars] + "..."
        
        # Ultra-specific prompt to avoid thinking tags
        prompt = f"""RESPOND WITH ONLY JSON. NO THINKING. NO EXPLANATIONS.

{{
    "title": "document title here",
    "summary": "brief summary under 300 characters",
    "keywords": ["keyword1", "keyword2", "keyword3"],
    "category": "one of: AI, Machine Learning, Data Science, Analytics, Business, Technology, Research",
    "difficulty": "one of: Beginner, Intermediate, Advanced",
    "authors": ["author1"] or [],
    "content_preview": "first 80 characters of content"
}}

Document: {filename}
Text: {text}

JSON ONLY:"""

        try:
            response = ollama.generate(
                model=self.model_name,
                prompt=prompt,
                options={
                    "temperature": 0.0,  # Deterministic
                    "top_p": 0.8,
                    "num_predict": 500,  # Limit response length
                    "stop": ["\n\n", "```", "<think>", "Note:", "Explanation:"]
                }
            )
            
            response_text = response.get('response', '').strip()
            logger.info(f"Raw Ollama response for {filename}: {response_text[:150]}...")
            
            # Parse with robust error handling
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
            if isinstance(analysis["keywords"], str):
                analysis["keywords"] = [analysis["keywords"]]
            else:
                analysis["keywords"] = []
        analysis["keywords"] = analysis["keywords"][:5]
        if not analysis["keywords"]:
            # Generate keywords from filename and category
            keywords = [analysis["category"]]
            filename_words = filename.replace('.pdf', '').replace('_', ' ').replace('-', ' ').split()
            for word in filename_words[:3]:
                if len(word) > 3 and word.lower() not in ['the', 'and', 'for', 'with']:
                    keywords.append(word.title())
            analysis["keywords"] = keywords[:5]
        
        # Ensure authors is a list
        if not isinstance(analysis["authors"], list):
            if isinstance(analysis["authors"], str) and analysis["authors"]:
                analysis["authors"] = [analysis["authors"]]
            else:
                analysis["authors"] = []
        
        # Validate summary length
        if len(analysis["summary"]) > 350:
            analysis["summary"] = analysis["summary"][:347] + "..."
        elif len(analysis["summary"]) < 50:
            analysis["summary"] = f"This document covers {analysis['title'].lower()} providing comprehensive information and insights on the subject matter for readers interested in {analysis['category'].lower()}."
        
        # Ensure content_preview exists
        if not analysis["content_preview"]:
            analysis["content_preview"] = f"Document: {analysis['title']}"
        elif len(analysis["content_preview"]) > 100:
            analysis["content_preview"] = analysis["content_preview"][:97] + "..."
        
        return analysis
    
    def _get_fallback_analysis(self, filename: str) -> Dict:
        """Provide fallback analysis when Ollama fails"""
        clean_title = filename.replace('.pdf', '').replace('_', ' ').replace('-', ' ')
        
        # Smart keyword extraction from filename
        keywords = []
        filename_lower = filename.lower()
        keyword_map = {
            'ai': 'AI', 'artificial': 'AI', 'machine': 'Machine Learning', 
            'data': 'Data Science', 'learning': 'Machine Learning', 
            'neural': 'Neural Networks', 'deep': 'Deep Learning', 
            'analytics': 'Analytics', 'business': 'Business', 
            'python': 'Python', 'statistics': 'Statistics',
            'science': 'Science', 'research': 'Research'
        }
        
        for key, value in keyword_map.items():
            if key in filename_lower and value not in keywords:
                keywords.append(value)
        
        if not keywords:
            keywords = ['Technology', 'Research', 'Documentation']
        
        # Smart category detection
        category = "Technology"
        if any(word in filename_lower for word in ['ai', 'artificial']):
            category = "AI"
        elif any(word in filename_lower for word in ['machine', 'learning', 'ml']):
            category = "Machine Learning"
        elif any(word in filename_lower for word in ['data', 'analytics', 'science']):
            category = "Data Science"
        elif any(word in filename_lower for word in ['business']):
            category = "Business"
        
        return {
            "title": clean_title,
            "summary": f"This comprehensive document provides detailed coverage of {clean_title.lower()} concepts and methodologies. It offers valuable insights into theoretical foundations and practical applications relevant to {category.lower()}, serving as an essential resource for professionals and researchers.",
            "keywords": keywords[:5],
            "category": category,
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
    model_name = os.getenv('OLLAMA_MODEL', 'deepseek-r1:1.5b')
    if len(sys.argv) > 1 and not sys.argv[1].startswith('--'):
        model_name = sys.argv[1]
    
    # Check for force reprocess flag
    force_reprocess = '--force' in sys.argv or '-f' in sys.argv
    
    processor = UltimateOllamaDocumentProcessor(model_name)
    
    logger.info("Starting document processing with ultimate Ollama processor...")
    if force_reprocess:
        logger.info("Force reprocessing all documents...")
    
    success = processor.scan_and_process(force_reprocess=force_reprocess)
    
    if success:
        logger.info("Document processing completed successfully")
    else:
        logger.info("No documents were processed")

if __name__ == "__main__":
    main()
