import os
import json
import hashlib
from datetime import datetime
from pathlib import Path
import ollama
import re

# Try to import langchain components with fallback
try:
    from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader
    print("✓ Imported from langchain_community")
except ImportError:
    try:
        from langchain.document_loaders import PyPDFLoader, Docx2txtLoader
        print("✓ Imported from langchain.document_loaders")
    except ImportError:
        try:
            # Try alternative imports
            from langchain_community.document_loaders.pdf import PyPDFLoader
            from langchain_community.document_loaders.word_document import Docx2txtLoader
            print("✓ Imported from langchain_community specific modules")
        except ImportError:
            # Fallback to basic PDF processing
            PyPDFLoader = None
            Docx2txtLoader = None
            print("⚠ PyPDFLoader and Docx2txtLoader not available")

try:
    from langchain.text_splitter import RecursiveCharacterTextSplitter
except ImportError:
    try:
        from langchain_text_splitters import RecursiveCharacterTextSplitter
    except ImportError:
        RecursiveCharacterTextSplitter = None

try:
    from langchain.schema import Document
except ImportError:
    try:
        from langchain_core.documents import Document
    except ImportError:
        # Create a simple Document class if langchain is not available
        class Document:
            def __init__(self, page_content, metadata=None):
                self.page_content = page_content
                self.metadata = metadata or {}

class DocumentProcessor:
    def __init__(self):
        self.processed_files = self.load_processed_files()
        self.documents_db = []

    def load_processed_files(self):
        """Load the list of already processed files"""
        if os.path.exists('dist/data/processed_files.json'):
            with open('dist/data/processed_files.json', 'r') as f:
                return json.load(f)
        return {}

    def save_processed_files(self):
        """Save the list of processed files"""
        os.makedirs('dist/data', exist_ok=True)
        with open('dist/data/processed_files.json', 'w') as f:
            json.dump(self.processed_files, f)

    def get_file_hash(self, filepath):
        """Generate MD5 hash of file content"""
        with open(filepath, 'rb') as f:
            return hashlib.md5(f.read()).hexdigest()

    def load_document(self, filepath):
        """Load document based on file extension"""
        file_ext = Path(filepath).suffix.lower()
    
        if file_ext == '.pdf':
            if PyPDFLoader is None:
                print(f"Warning: PyPDFLoader not available, skipping {filepath}")
                return None
            loader = PyPDFLoader(str(filepath))  # Convert to string
        elif file_ext in ['.docx', '.doc']:
            if Docx2txtLoader is None:
                print(f"Warning: Docx2txtLoader not available, skipping {filepath}")
                return None
            loader = Docx2txtLoader(str(filepath))  # Convert to string
        else:
            return None
    
        try:
            return loader.load()
        except Exception as e:
            print(f"Error loading document {filepath}: {e}")
            return None

    def extract_title_and_authors(self, text):
        """Extract title and authors from document text using regex and AI"""
        # Take only the first 2000 characters for title/author analysis
        text_start = text[:2000]
        
        # Common patterns for titles (often in uppercase or with special formatting)
        title_patterns = [
            r'^([A-Z][A-Z\s\-:,]{10,100})\n',  # Title in uppercase at the beginning
            r'Title:\s*(.+?)(?:\n|Author)',     # "Title:" followed by title
            r'^(.{10,100})\n\n',                # First line followed by empty line
        ]
        
        # Patterns for authors
        author_patterns = [
            r'Author[s]?:\s*(.+?)(?:\n\n|\n[A-Z])',
            r'By:\s*(.+?)(?:\n\n|\n[A-Z])',
            r'([A-Z][a-z]+\s+[A-Z][a-z]+(?:\s*,\s*[A-Z][a-z]+\s+[A-Z][a-z]+)*)',
        ]
        
        title = None
        authors = []
        
        # Search for title
        for pattern in title_patterns:
            match = re.search(pattern, text_start, re.MULTILINE | re.IGNORECASE)
            if match:
                title = match.group(1).strip()
                break
        
        # Search for authors
        for pattern in author_patterns:
            matches = re.findall(pattern, text_start, re.MULTILINE)
            if matches:
                if isinstance(matches[0], str):
                    # Split by commas and clean
                    authors = [author.strip() for author in matches[0].split(',')]
                    authors = [author for author in authors if len(author) > 2]
                break
        
        return title, authors

    def check_ollama_availability(self):
        """Check if Ollama is available and the model exists"""
        try:
            # Try to list available models
            models = ollama.list()
            if not models or 'models' not in models:
                print("Warning: No models found in Ollama response")
                return False
                
            available_models = [model['name'] for model in models.get('models', [])]
            print(f"Available Ollama models: {available_models}")
            
            # Check if llama2:7b is available, or try alternative models
            preferred_models = ['deepseek-r1:7b', 'mistral', 'llama3', 'llama2:7b', 'llama2', 'llama3:8b', 'codellama']
            
            for model in preferred_models:
                if model in available_models:
                    print(f"Using model: {model}")
                    return model
            
            print("Warning: No compatible models found. Available models:", available_models)
            return False
            
        except Exception as e:
            print(f"Warning: Ollama not available: {e}")
            print("Make sure Ollama is running with: ollama serve")
            return False

    def generate_basic_metadata(self, text, title=None, authors=None):
        """Generate basic metadata without AI when Ollama is not available"""
        # Extract keywords from text using simple frequency analysis
        words = re.findall(r'\b[a-zA-Z]{4,}\b', text.lower())
        word_freq = {}
        for word in words:
            if word not in ['this', 'that', 'with', 'from', 'they', 'have', 'been', 'will', 'were', 'said', 'each', 'which', 'their', 'time', 'would', 'there', 'could', 'other']:
                word_freq[word] = word_freq.get(word, 0) + 1
        
        # Get top 5 most frequent words as keywords
        keywords = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:5]
        keywords = [word[0] for word in keywords]
        
        # Determine category based on keywords
        category = "General"
        ai_terms = ['artificial', 'intelligence', 'machine', 'learning', 'neural', 'deep', 'algorithm', 'model', 'data']
        governance_terms = ['policy', 'governance', 'regulation', 'ethics', 'law', 'legal']
        
        text_lower = text.lower()
        if any(term in text_lower for term in ai_terms):
            if any(term in text_lower for term in governance_terms):
                category = "AI Governance"
            else:
                category = "Machine Learning"
        elif any(term in text_lower for term in governance_terms):
            category = "AI Ethics"
        
        return {
            "summary": f"Document discussing {category.lower()} topics with focus on {', '.join(keywords[:3])}.",
            "keywords": keywords,
            "category": category,
            "difficulty": "Intermediate",
            "title": title or "Untitled document",
            "authors": authors or []
        }

    def summarize_with_llama(self, text, title=None, authors=None):
        """Generate document metadata using Llama AI model"""
        # Check if Ollama is available first
        model_name = self.check_ollama_availability()
        if not model_name:
            print("Ollama not available, using basic metadata generation.")
            return self.generate_basic_metadata(text, title, authors)
        
        prompt = f"""
        Analyze this academic document and provide:
        1. A 2-3 sentence summary
        2. 5 main keywords
        3. Category (e.g: Machine Learning, Deep Learning, NLP, Computer Vision, Data Science, AI Governance, AI Ethics)
        4. Difficulty level (Beginner/Intermediate/Advanced)
        5. If no title was provided, extract the document title
        6. If no authors were provided, extract the document authors

        {f"Title already identified: {title}" if title else ""}
        {f"Authors already identified: {', '.join(authors)}" if authors else ""}

        Document:
        {text[:4000]}

        Respond in JSON format:
        {{
            "summary": "...",
            "keywords": ["keyword1", "keyword2", ...],
            "category": "...",
            "difficulty": "...",
            "title": "...",
            "authors": ["author1", "author2", ...]
        }}
        """

        try:
            response = ollama.generate(model=model_name, prompt=prompt)
            
            # Check if response is valid
            if not response or 'response' not in response:
                print(f"Error: Empty or invalid response from Ollama")
                raise ValueError("Empty response from Ollama")
            
            response_text = response['response']
            if not response_text or response_text.strip() == "":
                print(f"Error: Empty response text from Ollama")
                raise ValueError("Empty response text")
            
            # Extract JSON from response
            json_start = response_text.find('{')
            json_end = response_text.rfind('}') + 1
            
            if json_start == -1 or json_end == 0:
                print(f"Error: No JSON found in response: {response_text[:200]}...")
                raise ValueError("No JSON found in response")
            
            json_str = response_text[json_start:json_end]
            
            if not json_str or json_str.strip() == "":
                print(f"Error: Empty JSON string extracted")
                raise ValueError("Empty JSON string")
            
            # Add debug output
            print(f"Debug: Attempting to parse JSON: {json_str[:100]}...")
            
            result = json.loads(json_str)
            
            # Use manually extracted values if available
            if title:
                result["title"] = title
            if authors:
                result["authors"] = authors
                
            return result
            
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON from Ollama response: {e}")
            print(f"Raw response: {response_text[:500] if 'response_text' in locals() else 'No response text'}")
            return self.generate_basic_metadata(text, title, authors)
        except Exception as e:
            print(f"Error processing with Ollama: {e}. Using basic metadata generation.")
            return self.generate_basic_metadata(text, title, authors)

    def is_already_processed(self, filepath):
        """Check if file has already been processed and hasn't changed"""
        file_hash = self.get_file_hash(filepath)
        filepath_str = str(filepath).replace('\\', '/')  # Normalize path separators
        
        # Check both the normalized path and any stored paths
        for stored_path in self.processed_files.keys():
            normalized_stored_path = stored_path.replace('\\', '/')
            if filepath_str == normalized_stored_path:
                if self.processed_files[stored_path] == file_hash:
                    print(f"Skipping already processed file: {filepath}")
                    return True
        
        return False

    def load_existing_documents(self):
        """Load existing documents from database"""
        db_path = 'dist/data/documents.json'
        if os.path.exists(db_path):
            with open(db_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []

    def process_documents(self):
        """Process all documents in the documents directory"""
        documents_dir = Path('documents')
        new_documents = []
        existing_documents = self.load_existing_documents()

        for filepath in documents_dir.rglob('*'):
            if not filepath.is_file():
                continue

            if filepath.suffix.lower() not in ['.pdf', '.docx', '.doc']:
                continue

            # Check if file has already been processed
            if self.is_already_processed(filepath):
                continue

            print(f"Processing: {filepath}")

            # Load document
            docs = self.load_document(filepath)
            if not docs:
                continue

            # Combine all text
            full_text = " ".join([doc.page_content for doc in docs])

            # Extract title and authors
            title, authors = self.extract_title_and_authors(full_text)

            # Generate metadata with Llama
            metadata = self.summarize_with_llama(full_text, title, authors)

            # Create database entry
            doc_entry = {
                "id": hashlib.md5(str(filepath).encode()).hexdigest(),
                "filename": filepath.name,
                "title": metadata.get("title", filepath.name),
                "authors": metadata.get("authors", []),
                "filepath": str(filepath),
                "upload_date": datetime.now().isoformat(),
                "file_size": filepath.stat().st_size,
                "summary": metadata["summary"],
                "keywords": metadata["keywords"],
                "category": metadata["category"],
                "difficulty": metadata["difficulty"],
                "content_preview": full_text[:500] + "..." if len(full_text) > 500 else full_text
            }

            new_documents.append(doc_entry)
            
            # Update hash of processed file
            file_hash = self.get_file_hash(filepath)
            self.processed_files[str(filepath)] = file_hash

        if new_documents:
            # Combine existing documents with new ones
            all_documents = existing_documents + new_documents
            self.update_database(all_documents)
            self.save_processed_files()
            print(f"Processed {len(new_documents)} new documents")
        else:
            print("No new documents to process")

    def update_database(self, documents):
        """Save updated database"""
        os.makedirs('dist/data', exist_ok=True)
        with open('dist/data/documents.json', 'w', encoding='utf-8') as f:
            json.dump(documents, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    processor = DocumentProcessor()
    processor.process_documents()
