import os
import json
import hashlib
from datetime import datetime
from pathlib import Path

def get_file_info(filepath):
    """Get basic file information"""
    stat = filepath.stat()
    return {
        "id": hashlib.md5(str(filepath).encode()).hexdigest(),
        "filename": filepath.name,
        "title": filepath.stem.replace('_', ' ').replace('-', ' '),
        "authors": [],
        "filepath": str(filepath).replace('\\', '/').replace('../documents/', 'documents/'),
        "upload_date": datetime.fromtimestamp(stat.st_mtime).isoformat(),
        "file_size": stat.st_size,
        "summary": f"Document: {filepath.stem.replace('_', ' ')}",
        "keywords": ["AI", "Data Science", "Machine Learning"],
        "category": "General",
        "difficulty": "Intermediate",
        "content_preview": f"PDF document: {filepath.name}"
    }

def process_documents():
    """Process all PDF documents in the documents directory"""
    documents_dir = Path('../documents')
    documents = []
    
    print(f"Looking for documents in: {documents_dir.absolute()}")
    
    if not documents_dir.exists():
        print(f"Documents directory does not exist: {documents_dir}")
        return
    
    pdf_files = list(documents_dir.glob('*.pdf'))
    print(f"Found {len(pdf_files)} PDF files")
    
    for filepath in pdf_files:
        if filepath.is_file():
            print(f"Processing: {filepath.name}")
            doc_info = get_file_info(filepath)
            documents.append(doc_info)
    
    # Create data directory if it doesn't exist
    data_dir = Path('../data')
    data_dir.mkdir(exist_ok=True)
    
    # Save documents.json
    output_file = data_dir / 'documents.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(documents, f, indent=2, ensure_ascii=False)
    
    print(f"Created {output_file} with {len(documents)} documents")
    
    # Also create in dist/data for the website
    dist_data_dir = Path('../dist/data')
    dist_data_dir.mkdir(parents=True, exist_ok=True)
    
    dist_output_file = dist_data_dir / 'documents.json'
    with open(dist_output_file, 'w', encoding='utf-8') as f:
        json.dump(documents, f, indent=2, ensure_ascii=False)
    
    print(f"Also created {dist_output_file}")

if __name__ == "__main__":
    process_documents()
