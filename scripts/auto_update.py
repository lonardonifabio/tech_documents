<<<<<<< HEAD
import os
import json
import hashlib
import time
from datetime import datetime
from pathlib import Path
import shutil

class DocumentWatcher:
    def __init__(self):
        # Handle both local development and GitHub Actions
        base_dir = Path.cwd()
        if base_dir.name == 'scripts':
            # Running from scripts directory
            self.documents_dir = base_dir.parent / 'documents'
            self.data_dir = base_dir.parent / 'data'
            self.dist_data_dir = base_dir.parent / 'dist' / 'data'
        else:
            # Running from project root (GitHub Actions)
            self.documents_dir = base_dir / 'documents'
            self.data_dir = base_dir / 'data'
            self.dist_data_dir = base_dir / 'dist' / 'data'
        
        self.processed_files_path = self.data_dir / 'processed_files.json'
        
        # Debug output
        print(f"Working directory: {base_dir}")
        print(f"Documents directory: {self.documents_dir}")
        print(f"Data directory: {self.data_dir}")
        print(f"Dist data directory: {self.dist_data_dir}")
        
    def load_processed_files(self):
        """Load the list of already processed files with their hashes"""
        if self.processed_files_path.exists():
            with open(self.processed_files_path, 'r') as f:
                return json.load(f)
        return {}
    
    def save_processed_files(self, processed_files):
        """Save the list of processed files"""
        self.data_dir.mkdir(exist_ok=True)
        with open(self.processed_files_path, 'w') as f:
            json.dump(processed_files, f, indent=2)
    
    def get_file_hash(self, filepath):
        """Generate MD5 hash of file content"""
        with open(filepath, 'rb') as f:
            return hashlib.md5(f.read()).hexdigest()
    
    def get_file_info(self, filepath):
        """Get basic file information"""
        stat = filepath.stat()
        return {
            "id": hashlib.md5(str(filepath).encode()).hexdigest(),
            "filename": filepath.name,
            "title": filepath.stem.replace('_', ' ').replace('-', ' '),
            "authors": [],
            "filepath": f"documents/{filepath.name}",
            "upload_date": datetime.fromtimestamp(stat.st_mtime).isoformat(),
            "file_size": stat.st_size,
            "summary": f"Document: {filepath.stem.replace('_', ' ')}",
            "keywords": ["AI", "Data Science", "Machine Learning"],
            "category": "General",
            "difficulty": "Intermediate",
            "content_preview": f"PDF document: {filepath.name}"
        }
    
    def load_existing_documents(self):
        """Load existing documents from database"""
        db_path = self.data_dir / 'documents.json'
        if db_path.exists():
            with open(db_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []
    
    def save_documents(self, documents):
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
        
        print(f"Updated documents.json in both data/ and dist/data/ with {len(documents)} documents")
    
    def scan_for_changes(self):
        """Scan for new or changed documents"""
        if not self.documents_dir.exists():
            print(f"Documents directory does not exist: {self.documents_dir}")
            return False
        
        processed_files = self.load_processed_files()
        existing_documents = self.load_existing_documents()
        new_documents = []
        updated = False
        
        # Get all PDF files
        pdf_files = list(self.documents_dir.glob('*.pdf'))
        print(f"Found {len(pdf_files)} PDF files in {self.documents_dir}")
        
        for filepath in pdf_files:
            if not filepath.is_file():
                continue
            
            file_path_str = str(filepath)
            current_hash = self.get_file_hash(filepath)
            
            # Check if file is new or changed
            if file_path_str not in processed_files or processed_files[file_path_str] != current_hash:
                print(f"Processing {'new' if file_path_str not in processed_files else 'updated'} file: {filepath.name}")
                doc_info = self.get_file_info(filepath)
                
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
                print(f"Removing deleted file: {filename}")
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
            return True
        
        return False
    
    def watch_continuously(self, interval=10):
        """Watch for changes continuously"""
        print(f"Starting document watcher... checking every {interval} seconds")
        print("Press Ctrl+C to stop")
        
        try:
            while True:
                if self.scan_for_changes():
                    print(f"Documents updated at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                time.sleep(interval)
        except KeyboardInterrupt:
            print("\nDocument watcher stopped")

def main():
    import sys
    
    watcher = DocumentWatcher()
    
    if len(sys.argv) > 1 and sys.argv[1] == '--watch':
        # Continuous watching mode
        interval = int(sys.argv[2]) if len(sys.argv) > 2 else 10
        watcher.watch_continuously(interval)
    else:
        # Single scan mode
        print("Scanning for document changes...")
        if watcher.scan_for_changes():
            print("Documents database updated!")
        else:
            print("No changes detected.")

if __name__ == "__main__":
    main()
=======
import os
import json
import hashlib
import time
from datetime import datetime
from pathlib import Path
import shutil

class DocumentWatcher:
    def __init__(self):
        # Handle both local development and GitHub Actions
        base_dir = Path.cwd()
        if base_dir.name == 'scripts':
            # Running from scripts directory
            self.documents_dir = base_dir.parent / 'documents'
            self.data_dir = base_dir.parent / 'data'
            self.dist_data_dir = base_dir.parent / 'dist' / 'data'
        else:
            # Running from project root (GitHub Actions)
            self.documents_dir = base_dir / 'documents'
            self.data_dir = base_dir / 'data'
            self.dist_data_dir = base_dir / 'dist' / 'data'
        
        self.processed_files_path = self.data_dir / 'processed_files.json'
        
        # Debug output
        print(f"Working directory: {base_dir}")
        print(f"Documents directory: {self.documents_dir}")
        print(f"Data directory: {self.data_dir}")
        print(f"Dist data directory: {self.dist_data_dir}")
        
    def load_processed_files(self):
        """Load the list of already processed files with their hashes"""
        if self.processed_files_path.exists():
            with open(self.processed_files_path, 'r') as f:
                return json.load(f)
        return {}
    
    def save_processed_files(self, processed_files):
        """Save the list of processed files"""
        self.data_dir.mkdir(exist_ok=True)
        with open(self.processed_files_path, 'w') as f:
            json.dump(processed_files, f, indent=2)
    
    def get_file_hash(self, filepath):
        """Generate MD5 hash of file content"""
        with open(filepath, 'rb') as f:
            return hashlib.md5(f.read()).hexdigest()
    
    def get_file_info(self, filepath):
        """Get basic file information"""
        stat = filepath.stat()
        return {
            "id": hashlib.md5(str(filepath).encode()).hexdigest(),
            "filename": filepath.name,
            "title": filepath.stem.replace('_', ' ').replace('-', ' '),
            "authors": [],
            "filepath": f"documents/{filepath.name}",
            "upload_date": datetime.fromtimestamp(stat.st_mtime).isoformat(),
            "file_size": stat.st_size,
            "summary": f"Document: {filepath.stem.replace('_', ' ')}",
            "keywords": ["AI", "Data Science", "Machine Learning"],
            "category": "General",
            "difficulty": "Intermediate",
            "content_preview": f"PDF document: {filepath.name}"
        }
    
    def load_existing_documents(self):
        """Load existing documents from database"""
        db_path = self.data_dir / 'documents.json'
        if db_path.exists():
            with open(db_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []
    
    def save_documents(self, documents):
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
        
        print(f"Updated documents.json in both data/ and dist/data/ with {len(documents)} documents")
    
    def scan_for_changes(self):
        """Scan for new or changed documents"""
        if not self.documents_dir.exists():
            print(f"Documents directory does not exist: {self.documents_dir}")
            return False
        
        processed_files = self.load_processed_files()
        existing_documents = self.load_existing_documents()
        new_documents = []
        updated = False
        
        # Get all PDF files
        pdf_files = list(self.documents_dir.glob('*.pdf'))
        print(f"Found {len(pdf_files)} PDF files in {self.documents_dir}")
        
        for filepath in pdf_files:
            if not filepath.is_file():
                continue
            
            file_path_str = str(filepath)
            current_hash = self.get_file_hash(filepath)
            
            # Check if file is new or changed
            if file_path_str not in processed_files or processed_files[file_path_str] != current_hash:
                print(f"Processing {'new' if file_path_str not in processed_files else 'updated'} file: {filepath.name}")
                doc_info = self.get_file_info(filepath)
                
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
                print(f"Removing deleted file: {filename}")
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
            return True
        
        return False
    
    def watch_continuously(self, interval=10):
        """Watch for changes continuously"""
        print(f"Starting document watcher... checking every {interval} seconds")
        print("Press Ctrl+C to stop")
        
        try:
            while True:
                if self.scan_for_changes():
                    print(f"Documents updated at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                time.sleep(interval)
        except KeyboardInterrupt:
            print("\nDocument watcher stopped")

def main():
    import sys
    
    watcher = DocumentWatcher()
    
    if len(sys.argv) > 1 and sys.argv[1] == '--watch':
        # Continuous watching mode
        interval = int(sys.argv[2]) if len(sys.argv) > 2 else 10
        watcher.watch_continuously(interval)
    else:
        # Single scan mode
        print("Scanning for document changes...")
        if watcher.scan_for_changes():
            print("Documents database updated!")
        else:
            print("No changes detected.")

if __name__ == "__main__":
    main()
>>>>>>> d383fcdd2b2676b9a4a41783f227ffcc5b7a941b
