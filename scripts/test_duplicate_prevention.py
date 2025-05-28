#!/usr/bin/env python3
"""
Test script to verify that the document processing system correctly prevents re-processing of already processed documents.
"""

import os
import sys
import json
from pathlib import Path

# Add the current directory to the path so we can import the DocumentProcessor
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from process_documents import DocumentProcessor

def test_duplicate_prevention():
    """Test that already processed documents are skipped"""
    print("=== Test: Duplicate Prevention ===")
    
    # Initialize the processor
    processor = DocumentProcessor()
    
    # Check if processed files exist
    processed_files_path = 'dist/data/processed_files.json'
    if os.path.exists(processed_files_path):
        with open(processed_files_path, 'r') as f:
            processed_files = json.load(f)
        print(f"✓ Found {len(processed_files)} already processed files:")
        for filepath in processed_files.keys():
            print(f"  - {filepath}")
    else:
        print("✗ No processed files found")
        return
    
    # Check documents directory
    documents_dir = Path('documents')
    if not documents_dir.exists():
        print("✗ Documents directory not found")
        return
    
    # Count documents in directory
    doc_files = list(documents_dir.rglob('*.pdf')) + list(documents_dir.rglob('*.docx')) + list(documents_dir.rglob('*.doc'))
    print(f"✓ Found {len(doc_files)} document files in directory:")
    for doc_file in doc_files:
        print(f"  - {doc_file}")
    
    # Test the is_already_processed method for each document
    print("\n=== Testing duplicate detection ===")
    for doc_file in doc_files:
        is_processed = processor.is_already_processed(doc_file)
        status = "✓ SKIP (already processed)" if is_processed else "→ PROCESS (new/changed)"
        print(f"{status}: {doc_file.name}")
    
    # Load existing documents database
    db_path = 'dist/data/documents.json'
    if os.path.exists(db_path):
        with open(db_path, 'r', encoding='utf-8') as f:
            existing_docs = json.load(f)
        print(f"\n✓ Documents database contains {len(existing_docs)} entries")
    else:
        print("\n✗ Documents database not found")
    
    print("\n=== Test completed ===")
    print("If all documents show 'SKIP (already processed)', the duplicate prevention is working correctly!")

if __name__ == "__main__":
    test_duplicate_prevention()
