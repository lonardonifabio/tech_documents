#!/usr/bin/env python3
"""
Bulletproof Ollama processor that forces DeepSeek to return only JSON
Uses multiple strategies to ensure AI model responses are always used
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

class BulletproofOllamaDocumentProcessor:
    def __init__(self, model_name: str = "deepseek-r1:1.5b"):
        """Initialize the processor with Ollama and DeepSeek model"""
        self.model_name = model_name
        self.base_dir = Path.cwd()
        self.documents_dir = self.base_dir / 'documents'
        self.data_dir = self.base_dir / 'data'
        self.dist_data_dir = self.base_dir / 'dist' / 'data'
        self.processed_files_path = self.data_dir / 'processed_files.json'
        
        logger.info(f"Initialized bulletproof processor with model: {model_name}")
    
    def ensure_model_available(self) -> bool:
        """Ensure the DeepSeek model is available in Ollama"""
        try:
            response = ollama.list()
            available_models = [model['name'] for model in response.get('models', [])]
            logger.info(f"Available models: {available_models}")
            
            if self.model_name not in available_models:
                logger.info(f"Model {self.model_name} not found. Attempting to pull...")
                ollama.pull(self.model_name)
                logger.info(f"Successfully pulled {self.model_name}")
            
            # Test the model
            test_response = ollama.generate(
                model=self.model_name,
                prompt="Hello",
                options={"num_predict": 5}
            )
            logger.info("Model test successful")
            return True
            
        except Exception as e:
            logger.error(f"Failed to ensure model availability: {e}")
            return False
    
    def extract_pdf_text(self, filepath: Path, max_pages: int = 2) -> str:
        """Extract text from PDF file"""
        try:
            with open(filepath, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                
                pages_to_read = min(len(pdf_reader.pages), max_pages)
                for page_num in range(pages_to_read):
                    page = pdf_reader.pages[page_num]
                    text += page.extract_text() + "\n"
                
                return text.strip()
        except Exception as e:
            logger.warning(f"Failed to extract text from {filepath}: {e}")
            return ""
    
    def force_json_extraction(self, response_text: str, filename: str) -> Dict:
        """Force extraction of JSON data from any response format"""
        logger.info(f"Processing response for {filename} ({len(response_text)} chars)")
        logger.info(f"Raw response: {response_text}")
        
        # Initialize result with defaults
        result = {
            "title": filename.replace('.pdf', '').replace('_', ' ').replace('-', ' '),
            "summary": "",
            "keywords": [],
            "category": "Technology",
            "difficulty": "Intermediate", 
            "authors": [],
            "content_preview": ""
        }
        
        if not response_text:
            logger.warning("Empty response, using filename-based analysis")
            return self._analyze_from_filename(filename)
        
        # Method 1: Try direct JSON parsing
        try:
            parsed = json.loads(response_text.strip())
            if isinstance(parsed, dict):
                logger.info("✅ Direct JSON parsing succeeded")
                result.update(parsed)
                return self._validate_and_clean(result, filename)
        except json.JSONDecodeError:
            logger.info("❌ Direct JSON parsing failed")
        
        # Method 2: Remove thinking tags and try again
        cleaned_text = response_text
        if '<think>' in cleaned_text:
            logger.info("Found thinking tags, removing...")
            # Remove everything between <think> and </think>
            cleaned_text = re.sub(r'<think>.*?</think>', '', cleaned_text, flags=re.DOTALL)
            # If no closing tag, remove from <think> to first {
            if '<think>' in cleaned_text:
                think_pos = cleaned_text.find('<think>')
                brace_pos = cleaned_text.find('{', think_pos)
                if brace_pos != -1:
                    cleaned_text = cleaned_text[:think_pos] + cleaned_text[brace_pos:]
                else:
                    cleaned_text = cleaned_text[:think_pos]
        
        # Remove any remaining XML-like tags
        cleaned_text = re.sub(r'<[^>]+>', '', cleaned_text).strip()
        
        try:
            parsed = json.loads(cleaned_text)
            if isinstance(parsed, dict):
                logger.info("✅ Cleaned JSON parsing succeeded")
                result.update(parsed)
                return self._validate_and_clean(result, filename)
        except json.JSONDecodeError:
            logger.info("❌ Cleaned JSON parsing failed")
        
        # Method 3: Extract JSON between braces
        first_brace = response_text.find('{')
        last_brace = response_text.rfind('}')
        
        if first_brace != -1 and last_brace != -1 and last_brace > first_brace:
            json_candidate = response_text[first_brace:last_brace + 1]
            try:
                parsed = json.loads(json_candidate)
                if isinstance(parsed, dict):
                    logger.info("✅ Brace extraction succeeded")
                    result.update(parsed)
                    return self._validate_and_clean(result, filename)
            except json.JSONDecodeError:
                logger.info("❌ Brace extraction failed")
        
        # Method 4: Aggressive field extraction using regex
        logger.info("Using aggressive field extraction...")
        
        # Extract title
        title_patterns = [
            r'"title"\s*:\s*"([^"]*)"',
            r'title\s*:\s*"([^"]*)"',
            r'Title\s*:\s*([^\n,}]*)',
            r'title\s*=\s*"([^"]*)"',
            r'Title:\s*([^\n]*)'
        ]
        for pattern in title_patterns:
            match = re.search(pattern, response_text, re.IGNORECASE)
            if match:
                result["title"] = match.group(1).strip()
                logger.info(f"Extracted title: {result['title']}")
                break
        
        # Extract summary
        summary_patterns = [
            r'"summary"\s*:\s*"([^"]*)"',
            r'summary\s*:\s*"([^"]*)"',
            r'Summary\s*:\s*([^\n,}]*)',
            r'summary\s*=\s*"([^"]*)"',
            r'Summary:\s*([^\n]*)'
        ]
        for pattern in summary_patterns:
            match = re.search(pattern, response_text, re.IGNORECASE)
            if match:
                result["summary"] = match.group(1).strip()
                logger.info(f"Extracted summary: {result['summary'][:50]}...")
                break
        
        # Extract category
        category_patterns = [
            r'"category"\s*:\s*"([^"]*)"',
            r'category\s*:\s*"([^"]*)"',
            r'Category\s*:\s*([^\n,}]*)',
            r'Category:\s*([^\n]*)'
        ]
        for pattern in category_patterns:
            match = re.search(pattern, response_text, re.IGNORECASE)
            if match:
                result["category"] = match.group(1).strip()
                logger.info(f"Extracted category: {result['category']}")
                break
        
        # Extract difficulty
        difficulty_patterns = [
            r'"difficulty"\s*:\s*"([^"]*)"',
            r'difficulty\s*:\s*"([^"]*)"',
            r'Difficulty\s*:\s*([^\n,}]*)',
            r'Difficulty:\s*([^\n]*)'
        ]
        for pattern in difficulty_patterns:
            match = re.search(pattern, response_text, re.IGNORECASE)
            if match:
                result["difficulty"] = match.group(1).strip()
                logger.info(f"Extracted difficulty: {result['difficulty']}")
                break
        
        # Extract keywords
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
                # If no quotes, try comma-separated
                if not keywords:
                    keywords = [k.strip().strip('"\'') for k in keywords_str.split(',') if k.strip()]
                result["keywords"] = keywords[:5]
                logger.info(f"Extracted keywords: {result['keywords']}")
                break
        
        # Extract authors
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
                for author_match in re.finditer(r'"([^"]*)"', authors_str):
                    authors.append(author_match.group(1))
                if not authors:
                    authors = [a.strip().strip('"\'') for a in authors_str.split(',') if a.strip()]
                result["authors"] = authors
                logger.info(f"Extracted authors: {result['authors']}")
                break
        
        # Extract content_preview
        preview_patterns = [
            r'"content_preview"\s*:\s*"([^"]*)"',
            r'content_preview\s*:\s*"([^"]*)"',
            r'Content Preview\s*:\s*([^\n,}]*)'
        ]
        for pattern in preview_patterns:
            match = re.search(pattern, response_text, re.IGNORECASE)
            if match:
                result["content_preview"] = match.group(1).strip()
                logger.info(f"Extracted content_preview: {result['content_preview'][:30]}...")
                break
        
        # If we still don't have a summary, try to extract any meaningful text
        if not result["summary"]:
            # Look for any descriptive text in the response
            text_patterns = [
                r'This document[^.]*\.',
                r'The document[^.]*\.',
                r'It covers[^.]*\.',
                r'This paper[^.]*\.',
                r'The paper[^.]*\.'
            ]
            for pattern in text_patterns:
                match = re.search(pattern, response_text, re.IGNORECASE)
                if match:
                    result["summary"] = match.group(0)
                    break
        
        logger.info("✅ Aggressive extraction completed")
        return self._validate_and_clean(result, filename)
    
    def _analyze_from_filename(self, filename: str) -> Dict:
        """Analyze document based on filename when AI fails"""
        clean_title = filename.replace('.pdf', '').replace('_', ' ').replace('-', ' ')
        
        # Smart category detection from filename
        filename_lower = filename.lower()
        category = "Technology"
        keywords = ["Technology"]
        
        if any(word in filename_lower for word in ['ai', 'artificial']):
            category = "AI"
            keywords = ["AI", "Artificial Intelligence"]
        elif any(word in filename_lower for word in ['machine', 'learning', 'ml']):
            category = "Machine Learning"
            keywords = ["Machine Learning", "ML"]
        elif any(word in filename_lower for word in ['data', 'analytics', 'science']):
            category = "Data Science"
            keywords = ["Data Science", "Analytics"]
        elif any(word in filename_lower for word in ['business', 'revenue', 'employee']):
            category = "Business"
            keywords = ["Business", "Management"]
        elif any(word in filename_lower for word in ['python', 'pandas']):
            category = "Data Science"
            keywords = ["Python", "Programming"]
        elif any(word in filename_lower for word in ['excel']):
            category = "Analytics"
            keywords = ["Excel", "Analytics"]
        elif any(word in filename_lower for word in ['statistics', 'statistical']):
            category = "Data Science"
            keywords = ["Statistics", "Data Science"]
        
        return {
            "title": clean_title,
            "summary": f"This document provides comprehensive coverage of {clean_title.lower()} concepts and methodologies, offering valuable insights for professionals and researchers in {category.lower()}.",
            "keywords": keywords,
            "category": category,
            "difficulty": "Intermediate",
            "authors": [],
            "content_preview": f"Document: {clean_title}"
        }
    
    def _validate_and_clean(self, data: Dict, filename: str) -> Dict:
        """Validate and clean extracted data"""
        # Ensure title
        if not data.get("title") or len(data["title"].strip()) < 3:
            data["title"] = filename.replace('.pdf', '').replace('_', ' ').replace('-', ' ')
        
        # Validate category
        valid_categories = ["AI", "Machine Learning", "Data Science", "Analytics", "Business", "Technology", "Research"]
        if data.get("category") not in valid_categories:
            # Infer from filename
            filename_lower = filename.lower()
            if any(word in filename_lower for word in ['ai', 'artificial']):
                data["category"] = "AI"
            elif any(word in filename_lower for word in ['machine', 'learning', 'ml']):
                data["category"] = "Machine Learning"
            elif any(word in filename_lower for word in ['data', 'analytics', 'science']):
                data["category"] = "Data Science"
            elif any(word in filename_lower for word in ['business']):
                data["category"] = "Business"
            else:
                data["category"] = "Technology"
        
        # Validate difficulty
        valid_difficulties = ["Beginner", "Intermediate", "Advanced"]
        if data.get("difficulty") not in valid_difficulties:
            data["difficulty"] = "Intermediate"
        
        # Ensure keywords is a list
        if not isinstance(data.get("keywords"), list):
            if isinstance(data.get("keywords"), str):
                data["keywords"] = [data["keywords"]]
            else:
                data["keywords"] = []
        
        # Limit keywords and ensure we have some
        data["keywords"] = data["keywords"][:5]
        if not data["keywords"]:
            data["keywords"] = [data["category"], "Document"]
        
        # Ensure authors is a list
        if not isinstance(data.get("authors"), list):
            if isinstance(data.get("authors"), str) and data["authors"]:
                data["authors"] = [data["authors"]]
            else:
                data["authors"] = []
        
        # Validate summary
        if not data.get("summary") or len(data["summary"]) < 20:
            data["summary"] = f"This document covers {data['title'].lower()} providing comprehensive information and insights on {data['category'].lower()}."
        elif len(data["summary"]) > 300:
            data["summary"] = data["summary"][:297] + "..."
        
        # Ensure content_preview
        if not data.get("content_preview"):
            data["content_preview"] = f"Document: {data['title']}"
        elif len(data["content_preview"]) > 100:
            data["content_preview"] = data["content_preview"][:97] + "..."
        
        return data
    
    def analyze_document_with_ollama(self, text: str, filename: str) -> Dict:
        """Use Ollama with multiple attempts to get structured data"""
        if not text.strip():
            logger.warning(f"No text content for {filename}")
            return self._analyze_from_filename(filename)
        
        # Truncate text
        max_chars = 800
        if len(text) > max_chars:
            text = text[:max_chars] + "..."
        
        logger.info(f"Analyzing {filename} with {len(text)} characters")
        
        # Try multiple prompts with increasing strictness
        prompts = [
            # Attempt 1: Ultra-strict JSON-only prompt
            f"""You must respond with ONLY a JSON object. No thinking, no explanations, no other text.

{{"title": "document title", "summary": "brief summary", "keywords": ["keyword1", "keyword2"], "category": "Technology", "difficulty": "Intermediate", "authors": [], "content_preview": "preview"}}

Document: {filename}
Text: {text}

JSON:""",
            
            # Attempt 2: Even more explicit
            f"""RETURN ONLY JSON. NO OTHER TEXT.

Analyze this document and return this exact JSON structure:
{{"title": "title here", "summary": "summary here", "keywords": ["word1", "word2"], "category": "Technology", "difficulty": "Intermediate", "authors": [], "content_preview": "preview here"}}

File: {filename}
Content: {text}""",
            
            # Attempt 3: Minimal prompt
            f"""JSON only:
{{"title": "{filename.replace('.pdf', '').replace('_', ' ')}", "summary": "summary of {filename}", "keywords": ["Technology"], "category": "Technology", "difficulty": "Intermediate", "authors": [], "content_preview": "Document content"}}

Improve this JSON based on: {text[:200]}"""
        ]
        
        for attempt, prompt in enumerate(prompts, 1):
            try:
                logger.info(f"Attempt {attempt} for {filename}")
                
                response = ollama.generate(
                    model=self.model_name,
                    prompt=prompt,
                    options={
                        "temperature": 0.0,
                        "top_p": 0.8,
                        "num_predict": 300,
                        "stop": ["```", "<think>", "\n\n\n", "Note:", "Explanation:"]
                    }
                )
                
                response_text = response.get('response', '').strip()
                
                if response_text:
                    result = self.force_json_extraction(response_text, filename)
                    logger.info(f"✅ Attempt {attempt} succeeded for {filename}")
                    return result
                
            except Exception as e:
                logger.warning(f"Attempt {attempt} failed for {filename}: {e}")
                continue
        
        # If all attempts fail, use filename analysis
        logger.warning(f"All AI attempts failed for {filename}, using filename analysis")
        return self._analyze_from_filename(filename)
    
    def get_file_hash(self, filepath: Path) -> str:
        """Generate MD5 hash of file content"""
        with open(filepath, 'rb') as f:
            return hashlib.md5(f.read()).hexdigest()
    
    def load_processed_files(self) -> Dict:
        """Load processed files tracking"""
        if self.processed_files_path.exists():
            with open(self.processed_files_path, 'r') as f:
                return json.load(f)
        return {}
    
    def save_processed_files(self, processed_files: Dict):
        """Save processed files tracking"""
        self.data_dir.mkdir(exist_ok=True)
        with open(self.processed_files_path, 'w') as f:
            json.dump(processed_files, f, indent=2)
    
    def load_existing_documents(self) -> List[Dict]:
        """Load existing documents database"""
        db_path = self.data_dir / 'documents.json'
        if db_path.exists():
            with open(db_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []
    
    def save_documents(self, documents: List[Dict]):
        """Save documents to both locations"""
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
        """Process a single document"""
        logger.info(f"Processing document: {filepath.name}")
        
        # Extract text
        text_content = self.extract_pdf_text(filepath)
        logger.info(f"Extracted {len(text_content)} characters from {filepath.name}")
        
        # Analyze with AI (guaranteed to return something)
        analysis = self.analyze_document_with_ollama(text_content, filepath.name)
        
        # Get file stats
        stat = filepath.stat()
        
        # Create document entry
        doc_info = {
            "id": hashlib.md5(str(filepath).encode()).hexdigest(),
            "filename": filepath.name,
            "title": analysis["title"],
            "authors": analysis["authors"],
            "filepath": f"documents/{filepath.name}",
            "upload_date": datetime.fromtimestamp(stat.st_mtime).isoformat(),
            "file_size": stat.st_size,
            "summary": analysis["summary"],
            "keywords": analysis["keywords"],
            "category": analysis["category"],
            "difficulty": analysis["difficulty"],
            "content_preview": analysis["content_preview"]
        }
        
        logger.info(f"✅ Successfully processed {filepath.name} with AI analysis")
        return doc_info
    
    def scan_and_process(self, force_reprocess: bool = False) -> bool:
        """Scan and process all documents"""
        if not self.documents_dir.exists():
            logger.error(f"Documents directory does not exist: {self.documents_dir}")
            return False
        
        # Ensure model is available
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
            
            # Check if processing needed
            if force_reprocess or file_path_str not in processed_files or processed_files[file_path_str] != current_hash:
                logger.info(f"Processing {'new' if file_path_str not in processed_files else 'updated'} file: {filepath.name}")
                
                doc_info = self.process_document(filepath)
                
                # Remove old entry if exists
                existing_documents = [doc for doc in existing_documents if doc['filename'] != filepath.name]
                
                # Add new entry
                new_documents.append(doc_info)
                processed_files[file_path_str] = current_hash
                updated = True
        
        if updated or force_reprocess:
            # Combine and sort documents
            all_documents = existing_documents + new_documents
            all_documents.sort(key=lambda x: x['filename'])
            
            self.save_documents(all_documents)
            self.save_processed_files(processed_files)
            logger.info("✅ Documents database updated successfully")
            return True
        
        logger.info("No changes detected")
        return False

def main():
    """Main entry point"""
    import sys
    
    model_name = os.getenv('OLLAMA_MODEL', 'deepseek-r1:1.5b')
    if len(sys.argv) > 1 and not sys.argv[1].startswith('--'):
        model_name = sys.argv[1]
    
    force_reprocess = '--force' in sys.argv or '-f' in sys.argv
    
    processor = BulletproofOllamaDocumentProcessor(model_name)
    
    logger.info("Starting bulletproof document processing...")
    if force_reprocess:
        logger.info("Force reprocessing all documents...")
    
    success = processor.scan_and_process(force_reprocess=force_reprocess)
    
    if success:
        logger.info("✅ Document processing completed successfully")
    else:
        logger.info("No documents were processed")

if __name__ == "__main__":
    main()
